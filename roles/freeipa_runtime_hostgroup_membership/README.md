# freeipa_runtime_hostgroup_membership

Adds event-target Linux guests to the FreeIPA hostgroups that are backed by the Linux runtime inventory group.

## Responsibilities

- collect the resolved FQDNs of the current runtime Linux targets
- find FreeIPA hostgroups that reference the runtime inventory group
- add the current runtime Linux targets to those FreeIPA hostgroups without rewriting the full membership set

## Key Variables

- `freeipa_runtime_hostgroup_membership_enabled`
- `freeipa_runtime_hostgroup_membership_inventory_group`
- `freeipa_runtime_hostgroup_membership_hostgroup_inventory_groups`
- `freeipa_hostgroups`

## Notes

- This role is intended for event-driven or scoped Linux runs where rewriting the entire hostgroup membership would be too broad.
- It assumes the base FreeIPA access model already exists and only adds the current runtime Linux targets as members.
- `freeipa_runtime_hostgroup_membership_inventory_group` controls which runtime hosts are added.
- `freeipa_runtime_hostgroup_membership_hostgroup_inventory_groups` controls which declarative FreeIPA hostgroups are updated. This lets `site.yml` and `proxmox-vm-event.yml` add only successfully enrolled hosts while still targeting hostgroups defined against `linux_ipa_clients_runtime`.
