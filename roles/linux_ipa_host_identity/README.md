# linux_ipa_host_identity

Resolves the effective FreeIPA hostname for a Linux guest and publishes it for later hostgroup use.

## Responsibilities

- read the guest FQDN and short hostname
- prefer an explicit `ipa_hostname` when provided
- optionally append a configured suffix to short hostnames
- optionally complete a short hostname with the IPA domain
- assert that the final value is a usable FQDN

## Key Variables

- `ipa_hostname`
- `ipaclient_domain`
- `linux_ipa_identity_hostname_suffix`
- `linux_ipa_identity_allow_domain_completion`

## Notes

- This role is used when the source inventory does not already use final FQDNs.
- The resolved value is published as `freeipa_resolved_hostname`.
