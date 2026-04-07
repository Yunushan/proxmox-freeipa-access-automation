# linux_sssd_refresh

Refreshes Linux SSSD caches so FreeIPA-side access changes become visible on enrolled clients without a manual cache clear.

## Responsibilities

- detect whether `sss_cache` is installed
- clear cached SSSD state when available
- restart the `sssd` service when present

## Key Variables

- `linux_sssd_refresh_enabled`

## Notes

- This role is intended for already managed Linux IPA clients.
- Hosts that are not enrolled yet simply skip the cache clear or service restart steps.
