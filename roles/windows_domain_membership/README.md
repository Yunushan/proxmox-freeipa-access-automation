# windows_domain_membership

Manages Windows host membership in Active Directory or a workgroup through the separate Windows workflow.

## Responsibilities

- validate the Windows membership input variables
- join Windows hosts to Active Directory
- optionally rename the Windows host during the membership change
- optionally move Windows hosts back to a workgroup
- reboot automatically when the membership change requires it

## Key Variables

- `windows_domain_membership_enabled`
- `windows_domain_membership_state`
- `windows_domain_membership_dns_domain_name`
- `windows_domain_membership_domain_admin_user`
- `windows_domain_membership_domain_admin_password`
- `windows_domain_membership_domain_ou_path`
- `windows_domain_membership_domain_server`
- `windows_domain_membership_hostname`
- `windows_domain_membership_workgroup_name`
- `windows_domain_membership_reboot`
- `windows_domain_membership_reboot_timeout`

## Notes

- This role is intended for Windows 10/11 and Windows Server guests reached through WinRM or PSRP.
- In FreeIPA-centered environments, actual Windows logon should still be handled through Active Directory or a FreeIPA-AD trust model. Windows hosts join the AD side, not FreeIPA directly.
- FreeIPA-only Windows domain join is not supported by this role.
