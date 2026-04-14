# windows_freeipa_helpers

Applies limited FreeIPA-aware helper tasks to Windows hosts without attempting Windows domain join.
Use `playbooks/windows-freeipa-helpers.yml` for the mutating helper path and
`playbooks/windows-freeipa-validate.yml` for validation-only runs.

## Responsibilities

- build a per-host helper summary that reports CA trust, hosts bootstrap, local group, OpenSSH, DNS, TCP, HTTPS, and time-source status
- optionally import the FreeIPA CA certificate into the Windows trust store
- optionally auto-fetch the IPA CA certificate from an IPA server before import
- optionally enforce a pinned IPA CA certificate thumbprint before import
- optionally manage Windows hosts-file bootstrap entries for IPA endpoints
- optionally manage local Windows group memberships
- optionally install and configure Windows OpenSSH Server
- validate DNS resolution for IPA servers from Windows
- validate TCP reachability for key IPA service ports from Windows
- validate HTTPS reachability and certificate trust for IPA servers from Windows
- validate Windows time-source reachability against an IPA-related time source

## Key Variables

- `windows_freeipa_helpers_enabled`
- `windows_freeipa_helpers_emit_summary`
- `windows_freeipa_helpers_ipa_servers`
- `windows_freeipa_helpers_https_port`
- `windows_freeipa_helpers_trust_ipa_ca`
- `windows_freeipa_helpers_ipa_ca_auto_fetch`
- `windows_freeipa_helpers_ipa_ca_auto_fetch_server`
- `windows_freeipa_helpers_ipa_ca_expected_thumbprint`
- `windows_freeipa_helpers_ipa_ca_certificate_src`
- `windows_freeipa_helpers_ipa_ca_certificate_content`
- `windows_freeipa_helpers_manage_hosts_entries`
- `windows_freeipa_helpers_hosts_entries`
- `windows_freeipa_helpers_manage_local_group_memberships`
- `windows_freeipa_helpers_local_group_memberships`
- `windows_freeipa_helpers_manage_openssh_server`
- `windows_freeipa_helpers_openssh_install`
- `windows_freeipa_helpers_openssh_port`
- `windows_freeipa_helpers_validate_dns`
- `windows_freeipa_helpers_validate_tcp`
- `windows_freeipa_helpers_tcp_ports`
- `windows_freeipa_helpers_tcp_timeout_ms`
- `windows_freeipa_helpers_validate_https`
- `windows_freeipa_helpers_https_timeout_ms`
- `windows_freeipa_helpers_validate_time_source`
- `windows_freeipa_helpers_time_source`

## Notes

- This role is for Windows 10/11 and Windows Server guests reached through WinRM or PSRP.
- This role does not domain-join Windows and does not provide native Windows logon against FreeIPA.
- Use the separate Active Directory workflow when you need real Windows domain membership.
- IPA CA auto-fetch is a helper bootstrap path and should be treated as trust-on-first-use unless you already control the network path to the IPA server or pin the expected certificate thumbprint.
- The role exposes the final `windows_freeipa_helpers_summary` host fact and prints it by default when `windows_freeipa_helpers_emit_summary` is enabled.
