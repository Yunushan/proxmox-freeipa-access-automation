# proxmox_linux_vm_discovery

Discovers guest VMs from one or more Proxmox nodes and adds them to the Linux IPA runtime group.

## Responsibilities

- validate discovery settings
- read QEMU guests from the selected Proxmox nodes
- collect guest-agent network data
- choose a usable IP address
- add discovered guests to the runtime inventory

## Key Variables

- `linux_ipa_runtime_group`
- `linux_ipa_proxmox_discovery_enabled`
- `linux_ipa_proxmox_discovery_nodes`
- `linux_ipa_proxmox_discovery_vmids`
- `linux_ipa_proxmox_discovery_only_running`
- `linux_ipa_proxmox_discovery_skip_missing_ip`
- `linux_ipa_proxmox_discovery_ip_preference`
- `linux_ipa_proxmox_discovery_inventory_prefix`
- `linux_ipa_proxmox_discovery_use_vm_name_as_hint`
- `linux_ipa_proxmox_discovery_complete_short_vm_names_with_suffix`
- `linux_ipa_proxmox_discovery_allowlist_enabled`
- `linux_ipa_proxmox_discovery_allowlist_vmids`
- `linux_ipa_proxmox_discovery_allowlist_ips`
- `linux_ipa_proxmox_discovery_allowlist_names`
- `linux_ipa_proxmox_discovery_ansible_user`
- `linux_ipa_proxmox_discovery_ansible_password`
- `linux_ipa_proxmox_discovery_ansible_ssh_private_key_file`
- `linux_ipa_proxmox_discovery_ansible_become`
- `linux_ipa_proxmox_discovery_ansible_become_method`
- `linux_ipa_proxmox_discovery_ansible_become_password`

## Notes

- Discovery relies on the QEMU guest agent for IP visibility.
- Guest discovery only prepares inventory; hostname resolution and IPA enrollment happen in later steps.
- By default, `linux_ipa_proxmox_discovery_use_vm_name_as_hint` only trusts VM names that are already FQDNs. Set `linux_ipa_proxmox_discovery_complete_short_vm_names_with_suffix: true` together with `linux_ipa_identity_hostname_suffix` when you also want short Proxmox VM names such as `Teleport-Server-1` promoted automatically to `teleport-server-1.example.com`.
- When `linux_ipa_proxmox_discovery_allowlist_enabled` is `true`, only discovered guests that match at least one configured VMID, IP, or name are admitted to the runtime inventory. Name matching is exact and checks the generated runtime inventory name, the raw Proxmox VM name, and any FQDN hostname hint derived from that VM name.
- When QEMU Guest Agent is still missing inside a discovered guest, provide a valid first-touch SSH path with `linux_ipa_proxmox_discovery_ansible_user` plus a password or private key so later QGA installation and enrollment tasks can reach the guest.
- When discovered Linux guests use a non-root SSH account, also set `linux_ipa_proxmox_discovery_ansible_become`, `linux_ipa_proxmox_discovery_ansible_become_method`, and `linux_ipa_proxmox_discovery_ansible_become_password` unless that account already has passwordless sudo.
- `linux_ipa_proxmox_discovery_vmids` is optional and is mainly useful for event-driven runs that should scope discovery to one or more specific VMIDs.
