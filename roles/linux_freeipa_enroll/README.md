# linux_freeipa_enroll

Enrolls Linux guests into FreeIPA by calling the upstream `freeipa.ansible_freeipa.ipaclient` role with repository defaults.

## Responsibilities

- validate Linux enrollment inputs
- join the target host to FreeIPA

## Key Variables

- `linux_freeipa_enroll_enabled`
- `linux_freeipa_enroll_serial`
- `linux_ipa_servers`
- `linux_ipaadmin_principal`
- `linux_ipaadmin_password`
- `linux_ipaclient_mkhomedir`
- `linux_ipaclient_force_join`
- `linux_ipasssd_permit`

## Notes

- This role expects the target hosts to be reachable and to resolve to their final IPA hostname.
- The upstream collection must be installed from `requirements.yml` before execution.
