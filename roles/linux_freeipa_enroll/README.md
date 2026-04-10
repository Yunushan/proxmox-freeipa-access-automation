# linux_freeipa_enroll

Enrolls Linux guests into FreeIPA by calling the upstream `freeipa.ansible_freeipa.ipaclient` role with repository defaults.

## Responsibilities

- validate Linux enrollment inputs
- join the target host to FreeIPA

## Key Variables

- `linux_freeipa_enroll_enabled`
- `linux_freeipa_enroll_serial`
- `linux_freeipa_enroll_success_group`
- `linux_freeipa_enroll_timeout_group`
- `linux_freeipa_enroll_join_attempts`
- `linux_freeipa_enroll_join_retry_delay`
- `linux_freeipa_enroll_continue_on_join_timeout`
- `linux_freeipa_enroll_collect_join_timeout_diagnostics`
- `linux_freeipa_enroll_refresh_apt_cache`
- `linux_freeipa_enroll_wait_for_cloud_init`
- `linux_freeipa_enroll_cloud_init_timeout`
- `linux_freeipa_enroll_wait_for_apt_background_services`
- `linux_freeipa_enroll_apt_background_services_timeout`
- `linux_freeipa_enroll_apt_lock_timeout`
- `linux_freeipa_enroll_https_port`
- `linux_freeipa_enroll_bootstrap_ipa_server_hosts_from_inventory`
- `linux_freeipa_enroll_networkmanager_dns_refresh_strategy`
- `linux_freeipa_enroll_merge_inventory_ipa_servers`
- `linux_freeipa_enroll_force_no_dns_lookup_with_explicit_servers`
- `linux_freeipa_enroll_clear_proxy_environment`
- `linux_freeipa_enroll_preflight_json_probe_enabled`
- `linux_freeipa_enroll_preflight_json_probe_timeout`
- `linux_freeipa_enroll_manage_authoritative_dns`
- `linux_freeipa_enroll_authoritative_dns_delegate_host`
- `linux_freeipa_enroll_authoritative_dns_query_server`
- `linux_freeipa_enroll_authoritative_dns_remove_link_local_aaaa`
- `linux_freeipa_enroll_pin_local_hostname_in_etc_hosts`
- `linux_ipa_servers`
- `linux_ipaadmin_principal`
- `linux_ipaadmin_password`
- `linux_ipaclient_kinit_attempts`
- `linux_ipaclient_mkhomedir`
- `linux_ipaclient_force_join`
- `linux_ipasssd_permit`
- `linux_ipa_manage_etc_hosts`
- `linux_ipa_etc_hosts_entries`

## Notes

- This role expects the target hosts to be reachable and to resolve to their final IPA hostname.
- Successful enrollments are added to `linux_freeipa_enroll_success_group` so later plays can target only the guests that actually completed IPA enrollment.
- When `linux_freeipa_enroll_continue_on_join_timeout` is enabled, guests that still hit a final FreeIPA join timeout are added to `linux_freeipa_enroll_timeout_group` instead of failing the whole workflow.
- The repository retries the upstream client join when FreeIPA returns a JSON-RPC timeout. Use `linux_freeipa_enroll_join_attempts`, `linux_freeipa_enroll_join_retry_delay`, and `linux_ipaclient_kinit_attempts` to tune slow or busy IPA environments.
- `linux_freeipa_enroll_merge_inventory_ipa_servers` defaults to `true`, so Linux enrollment automatically appends the `ipa_servers` inventory hostnames to `linux_ipa_servers` before joining.
- When more than one IPA server is available, each retry pass walks those server candidates one at a time instead of repeating the same join target blindly.
- When explicit IPA servers are configured, `linux_freeipa_enroll_force_no_dns_lookup_with_explicit_servers` defaults to `true`, so the role forces `ipaclient_no_dns_lookup` and avoids extra discovery behavior during the upstream join.
- `linux_freeipa_enroll_clear_proxy_environment` defaults to `true`, so the upstream join injects a focused `NO_PROXY` list for the IPA servers and domain instead of relying on whatever global proxy environment the guest happens to have.
- `linux_freeipa_enroll_https_port` defaults to `443` and controls the HTTPS port used by the guest-side IPA web/API reachability checks and JSON probes.
- `linux_freeipa_enroll_bootstrap_ipa_server_hosts_from_inventory` defaults to `true`, so the role can seed guest `/etc/hosts` entries for IPA server FQDNs from the `ipa_servers` inventory before DNS-dependent preflight checks run.
- `linux_freeipa_enroll_networkmanager_dns_refresh_strategy` uses `apply` by default, so `NetworkManager`-managed guests use a targeted active-device refresh after a successful IPA join instead of restarting the whole daemon. Set it to `restart` if you need the heavier legacy refresh behavior or `none` if you prefer to let the new DNS settings take effect on a later reconnect or reboot.
- The older `linux_freeipa_enroll_restart_networkmanager_after_dns_config` boolean is still accepted as a compatibility alias when the new strategy variable is left unset.
- `linux_freeipa_enroll_refresh_apt_cache` defaults to `true`, so Debian-family guests refresh APT metadata before the upstream role installs `freeipa-client` packages. This avoids stale mirror indexes that otherwise surface as `404 Not Found` package fetch failures during enrollment.
- `linux_freeipa_enroll_wait_for_cloud_init` defaults to `true`, so Debian-family guests first wait for `/var/lib/cloud/instance/boot-finished` when cloud-init is present. This avoids racing Ubuntu first-boot package operations during enrollment.
- `linux_freeipa_enroll_cloud_init_timeout` defaults to `60`, which bounds that cloud-init completion wait before the role continues to the generic APT lock wait and diagnostics path.
- `linux_freeipa_enroll_wait_for_apt_background_services` defaults to `false`, because the following APT lock-holder wait is the more reliable signal for real package-manager contention. Enable it only if you explicitly want to pre-wait on `apt-daily` and `apt-daily-upgrade` systemd activity.
- `linux_freeipa_enroll_apt_background_services_timeout` defaults to `60` when that optional systemd service wait is enabled.
- `linux_freeipa_enroll_apt_lock_timeout` defaults to `60`, so Debian-family guests fail faster when active `apt` or `dpkg` lock holders do not clear promptly.
- `linux_freeipa_enroll_preflight_json_probe_enabled` defaults to `true`, so the role probes `https://<ipa-server>:<linux_freeipa_enroll_https_port>/ipa/json` with a short timeout before the upstream join and fails fast on a slow or hung IPA web/API endpoint.
- When some IPA servers answer that preflight promptly and others do not, the role automatically drops the unhealthy candidates from the upstream join retry plan instead of wasting retries on them.
- When every configured IPA server fails that preflight and `linux_freeipa_enroll_continue_on_join_timeout` is enabled, the role skips the upstream join retry loop and marks the host timed out immediately with the preflight summary.
- `linux_freeipa_enroll_collect_join_timeout_diagnostics` defaults to `true`, so a final JSON-RPC timeout also writes a bounded `ipa-join -d` replay log on the guest and includes a short diagnostics summary in the final failure or timeout note.
- `ipaclient_domain` must be the shared IPA DNS domain such as `example.com`, not an IPA server hostname such as `ipa01.example.com`.
- `linux_ipa_servers` should preferably be a YAML list of IPA server FQDNs. Comma-separated strings are normalized, but list syntax is the preferred form.
- When DNS is not ready yet, the role can manage a dedicated `/etc/hosts` block from `linux_ipa_etc_hosts_entries` before IPA connectivity checks run.
- `linux_freeipa_enroll_manage_authoritative_dns` can also repair the specific host A, PTR, and link-local AAAA records in FreeIPA DNS before enrollment. It is disabled by default because it mutates authoritative DNS data.
- When the relevant reverse zone is not hosted in FreeIPA DNS, the role now keeps the forward A and AAAA repair path but skips PTR repair instead of failing the enrollment.
- `linux_freeipa_enroll_pin_local_hostname_in_etc_hosts` defaults to `true`, so the role also pins the guest enrollment FQDN to the guest primary IPv4 in `/etc/hosts` before hostname verification and join attempts.
- The guest FQDN used for enrollment must not resolve to loopback or link-local addresses such as `127.0.0.1`, `::1`, `169.254.0.0/16`, or `fe80::/10`.
- The guest primary IPv4 address should also reverse-resolve back to that same FQDN before enrollment. When authoritative PTR repair is unavailable in the current FreeIPA DNS workflow, the role warns and continues instead of failing on the PTR mismatch alone.
- The upstream collection must be installed from `requirements.yml` before execution.
