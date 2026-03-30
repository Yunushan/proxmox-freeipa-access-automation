# freeipa_access_model

Manages the declarative FreeIPA access model used by this repository.

## Responsibilities

- validate FreeIPA access-model inputs
- ensure user groups exist
- resolve hostgroup members to final hostnames
- ensure hostgroups exist
- ensure HBAC rules exist and are enabled or disabled as requested

## Key Variables

- `freeipa_access_model_enabled`
- `freeipa_admin_principal`
- `freeipa_admin_password`
- `freeipa_user_groups`
- `freeipa_hostgroups`
- `freeipa_hbac_rules`

## Notes

- Hostgroup members should resolve to final FQDNs before this role runs.
- Combined playbooks can derive those hostnames from Linux guest preparation and identity resolution.
