# linux_ipa_inventory_prepare

Builds the generated Linux runtime inventory used by the Linux enrollment and hostname-resolution flows.

## Responsibilities

- collect hosts from declared source inventory groups
- validate manual `linux_ipa_client_hosts` entries
- add both sources into the runtime group

## Key Variables

- `linux_ipa_runtime_group`
- `linux_ipa_inventory_source_groups`
- `linux_ipa_client_hosts`

## Notes

- This role does not discover Proxmox VMs by itself; that is handled by `proxmox_linux_vm_discovery`.
- The default runtime group is `linux_ipa_clients_runtime`.
