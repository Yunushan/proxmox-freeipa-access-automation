# proxmox_ldap_realm

Configures the Proxmox LDAP realm used to consume identities from FreeIPA.

## Responsibilities

- validate required LDAP and version inputs
- read current realm state from Proxmox
- compare desired configuration against current drift
- apply realm changes only when needed
- optionally run an initial realm sync

## Key Variables

- `proxmox_ldap_enabled`
- `proxmox_supported_major_versions`
- `proxmox_allow_future_major_versions`
- `proxmox_ldap_realm_id`
- `proxmox_ldap_server1`
- `proxmox_ldap_base_dn`
- `proxmox_ldap_group_dn`
- `proxmox_ldap_bind_dn`
- `proxmox_ldap_bind_password`
- `proxmox_ldap_sync_attributes`
- `proxmox_ldap_sync_defaults`

## Notes

- This role should run on the node designated in `proxmox_primary`.
- It expects `pveversion`, `pvesh`, and `pveum` to be available on the target host.
- Major versions newer than the highest tested entry in `proxmox_supported_major_versions` are accepted when `proxmox_allow_future_major_versions` is `true`.
