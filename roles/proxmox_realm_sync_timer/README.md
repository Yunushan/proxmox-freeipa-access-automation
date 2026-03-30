# proxmox_realm_sync_timer

Deploys the recurring Proxmox realm sync automation on the designated Proxmox node.

## Responsibilities

- deploy the realm sync helper script
- deploy the systemd service and timer units
- reload systemd when units change
- enable and start the timer

## Key Variables

- `proxmox_realm_sync_timer_enabled`
- `proxmox_realm_sync_service_name`
- `proxmox_realm_sync_on_calendar`
- `proxmox_realm_sync_persistent`
- `proxmox_realm_sync_scope`
- `proxmox_realm_sync_enable_new`
- `proxmox_realm_sync_remove_vanished`

## Notes

- This role is intended to run on the Proxmox node that owns realm configuration.
- The timer uses the local helper script templates shipped with this repository.
