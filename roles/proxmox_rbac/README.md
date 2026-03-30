# proxmox_rbac

Applies Proxmox custom roles and ACL bindings after directory sync has made the required groups visible.

## Responsibilities

- read current Proxmox roles, groups, and ACLs
- assert referenced synced groups already exist
- create custom roles when requested
- create ACL bindings when requested

## Key Variables

- `proxmox_rbac_enabled`
- `proxmox_custom_roles`
- `proxmox_acl_bindings`

## Notes

- Synced groups must already exist in Proxmox before ACL bindings are applied.
- This role manages additive configuration and assumes the desired bindings are defined declaratively.
