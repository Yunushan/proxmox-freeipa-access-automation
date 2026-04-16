# freeipa_access_model

Manages the declarative FreeIPA access model used by this repository.

## Responsibilities

- validate FreeIPA access-model inputs
- ensure user groups exist
- ensure the FreeIPA default login shell is set for Linux-oriented access
- optionally enforce a login shell for members of selected FreeIPA user groups
- resolve hostgroup members to final hostnames
- ensure hostgroups exist
- ensure HBAC rules exist and are enabled or disabled as requested
- ensure sudo rules exist and are enabled or disabled as requested

## Key Variables

- `freeipa_access_model_enabled`
- `freeipa_admin_principal`
- `freeipa_admin_password`
- `freeipa_access_model_manage_inventory_group_host_membership`
- `freeipa_user_groups`
- `freeipa_hostgroups`
- `freeipa_hbac_rules`
- `freeipa_sudo_rules`
- `freeipa_access_model_manage_default_login_shell`
- `freeipa_access_model_default_login_shell`
- `freeipa_access_model_manage_group_member_login_shell`
- `freeipa_access_model_login_shell_groups`

## Notes

- Hostgroup members should resolve to final FQDNs before this role runs.
- Combined playbooks can derive those hostnames from Linux guest preparation and identity resolution.
- Set `freeipa_access_model_manage_inventory_group_host_membership: false` when a workflow must create hostgroups before the inventory-backed Linux guests are enrolled into FreeIPA. The repository's combined `site` workflow then adds those hosts afterward through `freeipa_runtime_hostgroup_membership`.
- By default, the role sets the global FreeIPA default login shell to `/bin/bash` and also enforces `/bin/bash` for members of `linux-ssh-admins` so Linux admin users land in a normal Bash prompt on first SSH login.
- Group-member shell enforcement now normalizes both direct and indirect FreeIPA group-member output from `ipa group-show --raw`, which makes the reconciliation path more reliable across different FreeIPA membership layouts.
