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
- `linux_ipa_proxmox_discovery_only_running`
- `linux_ipa_proxmox_discovery_skip_missing_ip`
- `linux_ipa_proxmox_discovery_ip_preference`
- `linux_ipa_proxmox_discovery_inventory_prefix`
- `linux_ipa_proxmox_discovery_use_vm_name_as_hint`

## Notes

- Discovery relies on the QEMU guest agent for IP visibility.
- Guest discovery only prepares inventory; hostname resolution and IPA enrollment happen in later steps.
