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
- `ipaclient_domain` must be the shared IPA DNS domain such as `example.com`, not an IPA server hostname such as `ipa01.example.com`.
- `linux_ipa_servers` should preferably be a YAML list of IPA server FQDNs. Comma-separated strings are normalized, but list syntax is the preferred form.
- The upstream collection must be installed from `requirements.yml` before execution.
