# proxmox_vm_event_onboarding

Deploys the optional Proxmox VM hook and controller-side webhook for event-driven Linux onboarding.

## Responsibilities

- deploy the controller-side webhook environment file and `systemd` service
- deploy the Proxmox-side hookscript and hook configuration
- attach the hookscript to local Proxmox VMs when requested

## Key Variables

- `proxmox_vm_event_onboarding_enabled`
- `proxmox_vm_event_webhook_token`
- `proxmox_vm_event_hook_webhook_url`
- `proxmox_vm_event_webhook_ansible_extra_args`
- `proxmox_vm_event_hookscript_attach_existing_vms`
- `proxmox_vm_event_hookscript_override_existing`

## Notes

- The controller-side webhook still needs non-interactive vault arguments or another unattended secret source if the event playbook depends on vaulted values.
- `proxmox_vm_event_hook_webhook_url` must use `http://` unless the controller webhook is also configured with both `proxmox_vm_event_webhook_tls_certfile` and `proxmox_vm_event_webhook_tls_keyfile`.
- Proxmox does not expose a standalone VM `create` hook phase; new VMs are handled on their first `post-start` event when the hookscript is already attached.
- Hookscript attachment is per VM. This role can reconcile current VMs on participating nodes, but future creation workflows should also preserve the hookscript on templates or through later reconciliation runs.
