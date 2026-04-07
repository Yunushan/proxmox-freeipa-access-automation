# Event-Driven VM Onboarding

This repository includes an optional Proxmox hook and controller-side webhook so a VM `post-start` or `post-migrate` event can trigger Linux discovery, FreeIPA enrollment, targeted hostgroup membership updates, and an SSSD refresh without a manual playbook run.

## What It Includes

- `playbooks/proxmox-vm-event.yml`: the event-driven Ansible workflow
- `playbooks/includes/prepare_linux_event_inventory.yml`: event-scoped discovery preparation
- `roles/freeipa_runtime_hostgroup_membership/`: additive FreeIPA hostgroup membership updates for the event target
- `scripts/proxmox_event_webhook.py`: the controller-side webhook receiver
- `scripts/proxmox-event-webhook.service.example`: example `systemd` unit for the webhook receiver
- `scripts/proxmox-event-webhook.env.example`: example controller environment file
- `scripts/proxmox-vm-hook.pl`: the Proxmox VM hookscript
- `scripts/proxmox-vm-hook.conf.example`: example Proxmox hook configuration file

## Important Limits

- Run a normal `site.yml` or `freeipa.yml` rollout at least once first so the base FreeIPA access model already exists.
- Proxmox hookscript phases cover start, stop, and migrate events. There is no standalone VM `create` phase, so newly created VMs are handled on their first `post-start` event.
- Migration hooks run on both the source and target nodes. Store the hookscript on snippet storage that is available on every node that might execute it.
- Event-driven discovery still relies on the same prerequisites as normal discovery: the VM must be running, the QEMU guest agent must report a usable IP, and the guest must be reachable over SSH for enrollment.
- When `linux_ipa_qga_ssh_bootstrap_enabled` is true and the guest agent is already active, event-driven runs can create the automation SSH user and key access without a reboot or a temporary SSH password.
- If you enable `linux_ipa_ssh_bootstrap_enabled`, event-driven runs can also install the controller SSH public key automatically, but they still need an initial password-capable login path such as host `ansible_password` values or a shared vaulted `linux_ipa_ssh_bootstrap_password`.
- The event playbook filters discovery by VMID, not by node. That avoids missing the VM when Proxmox emits `post-migrate` hooks from both source and target nodes.

## Setup

1. Configure normal discovery and Linux enrollment in `inventories/production/group_vars/all/30-linux-clients.yml`.
2. Make sure `linux_ipa_proxmox_discovery_enabled: true` and `linux_ipa_proxmox_discovery_nodes` includes every node whose VMs should participate in automatic onboarding.
3. Create non-interactive vault password files or another non-interactive vault configuration for unattended `ansible-playbook` runs.
4. Copy `scripts/proxmox-event-webhook.env.example` to `/etc/default/proxmox-freeipa-event-webhook` on the Ansible controller and set the real token, inventory path, and vault arguments.
5. Copy `scripts/proxmox-event-webhook.service.example` to `/etc/systemd/system/proxmox-freeipa-event-webhook.service`, adjust the paths and service user if needed, then enable and start it with `systemctl enable --now proxmox-freeipa-event-webhook`.
6. Copy `scripts/proxmox-vm-hook.conf.example` to `/etc/default/proxmox-freeipa-hook` on each participating Proxmox node and set the real webhook URL and token.
7. Copy `scripts/proxmox-vm-hook.pl` to Proxmox snippet storage, for example `local:snippets/proxmox-vm-hook.pl` or shared snippet storage.
8. Attach the hookscript to each VM that should trigger automatic onboarding:

```bash
qm set 241 --hookscript local:snippets/proxmox-vm-hook.pl
```

To batch-attach the hookscript to existing VMs on a node:

```bash
for vmid in $(qm list | awk 'NR>1 {print $1}'); do
  qm set "$vmid" --hookscript local:snippets/proxmox-vm-hook.pl
done
```

## How The Event Flow Works

1. Proxmox executes the VM hookscript on `post-start` or `post-migrate`.
2. The hookscript sends the VMID and node metadata to the controller webhook.
3. The webhook batches near-simultaneous events, waits briefly for the guest to finish booting, and then runs `playbooks/proxmox-vm-event.yml`.
4. The event playbook discovers only the matching VMID across the configured Proxmox discovery nodes.
5. The event playbook resolves the guest hostname, enrolls the guest if needed, adds the guest to any FreeIPA hostgroup backed by `linux_ipa_clients_runtime`, and refreshes SSSD on that guest.

## Manual Test

After the webhook service is running, you can simulate an event from the controller itself:

```bash
curl -X POST \
  -H "Authorization: Bearer CHANGE_ME" \
  -H "Content-Type: application/json" \
  -d '{"vmid":"241","phase":"post-start","node":"pve6-ist","node_fqdn":"pve6-ist.karel.net.tr","source":"manual-test"}' \
  http://127.0.0.1:8085/hooks/proxmox-vm-event
```

To run the event playbook directly without the webhook:

```bash
ansible-playbook \
  -i inventories/production/hosts.yml \
  --vault-id freeipa@/etc/proxmox-freeipa-access-automation/freeipa.vault-pass \
  --vault-id proxmox@/etc/proxmox-freeipa-access-automation/proxmox.vault-pass \
  --extra-vars '{"linux_ipa_proxmox_discovery_vmids":["241"]}' \
  playbooks/proxmox-vm-event.yml
```

## References

- Proxmox hookscript phases for VMs: https://lists.proxmox.com/pipermail/pve-devel/2019-January/035483.html
- Proxmox migrate hook additions and documentation notes: https://lists.proxmox.com/pipermail/pve-devel/2022-October/054214.html
- Proxmox VM hook migration behavior and example updates: https://lists.proxmox.com/pipermail/pve-devel/2022-October/054216.html
