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
- `linux_freeipa_enroll_recover_stuck_apt_daily`
- `linux_freeipa_enroll_apt_lock_recovery_timeout`
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
- `linux_freeipa_enroll_split_dns_enabled`
- `linux_freeipa_enroll_split_dns_public_dns_servers`
- `linux_freeipa_enroll_manage_local_group_sudoers`
- `linux_freeipa_enroll_local_sudo_groups`
- `linux_freeipa_enroll_local_sudo_group_domain_variants`
- `linux_freeipa_enroll_local_sudo_sync_ipa_group_members`
- `linux_freeipa_enroll_local_sudo_nopasswd`
- `linux_freeipa_enroll_sssd_access_update_mode`
- `linux_freeipa_enroll_sssd_fast_memcache_timeout`
- `linux_freeipa_enroll_sssd_fast_entry_cache_timeout`
- `linux_freeipa_enroll_sssd_fast_negative_cache_timeout`
- `linux_freeipa_enroll_sssd_fast_refresh_expired_interval`
- `linux_freeipa_enroll_manage_local_sshd_allow_users`
- `linux_freeipa_enroll_local_sshd_allow_users_extra`
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
- `linux_freeipa_enroll_recover_stuck_apt_daily` defaults to `true`, so when the Debian APT lock wait times out and `apt-daily.service` is still active, the role stops the related APT timers and services, terminates the stale background update job, and retries the lock check instead of failing immediately.
- `linux_freeipa_enroll_apt_lock_recovery_timeout` defaults to `15`, which bounds the short post-recovery lock check after a stale `apt-daily.service` termination.
- `linux_freeipa_enroll_preflight_json_probe_enabled` defaults to `true`, so the role probes `https://<ipa-server>:<linux_freeipa_enroll_https_port>/ipa/json` with a short timeout before the upstream join and fails fast on a slow or hung IPA web/API endpoint.
- When some IPA servers answer that preflight promptly and others do not, the role automatically drops the unhealthy candidates from the upstream join retry plan instead of wasting retries on them.
- When every configured IPA server fails that preflight and `linux_freeipa_enroll_continue_on_join_timeout` is enabled, the role skips the upstream join retry loop and marks the host timed out immediately with the preflight summary.
- `linux_freeipa_enroll_collect_join_timeout_diagnostics` defaults to `true`, so a final JSON-RPC timeout also writes a bounded `ipa-join -d` replay log on the guest and includes a short diagnostics summary in the final failure or timeout note.
- `linux_freeipa_enroll_split_dns_enabled` defaults to `true`, so `systemd-resolved` guests automatically keep public DNS as the global/default resolver path and route only the IPA DNS domain such as `example.com` to the IPA DNS servers after a successful enrollment.
- The same split-DNS reconciliation also runs on later playbook executions for guests that are already IPA-enrolled, so stale resolver state from an older run can be repaired without forcing a fresh re-enrollment.
- `linux_freeipa_enroll_split_dns_public_dns_servers` defaults to an empty list, so the role auto-detects the current active-link DNS servers when that link is not already carrying the route-only IPA domain and falls back to the current global DNS servers otherwise. Set it explicitly if you want fixed public resolver IPs instead of automatic detection.
- The repository-owned split-DNS path is independent of `linux_ipaclient_configure_dns_resolver`, so the default repository workflow can keep the upstream flat resolver management disabled and still apply split DNS automatically on supported `systemd-resolved` guests after enrollment.
- `linux_freeipa_enroll_manage_local_group_sudoers` defaults to `true`, so successful Linux enrollments also install a local sudoers drop-in for the configured IPA-backed admin groups. This makes group members such as `linux-ssh-admins` able to run `sudo` through normal NSS/SSSD group resolution even when the guest-side IPA sudo-rule responder path is inconsistent.
- `linux_freeipa_enroll_local_sudo_groups` defaults to `['linux-ssh-admins']`.
- `linux_freeipa_enroll_local_sudo_group_domain_variants` defaults to `true`, so that local sudoers drop-in also writes IPA-qualified variants such as `linux-ssh-admins@example.com` and `linux-ssh-admins@EXAMPLE.COM` for guests where SSSD exposes group names in qualified form.
- `linux_freeipa_enroll_local_sudo_sync_ipa_group_members` defaults to `true`, so the guest also queries FreeIPA for the direct members of those configured admin groups and writes explicit sudoers user entries for them. This makes `sudo` work even on guests where local group-name matching still differs from the IPA-side group naming.
- `linux_freeipa_enroll_local_sudo_nopasswd` defaults to `false`, so group members still authenticate with their own password for commands such as `sudo su` unless you explicitly opt into passwordless sudo.
- `linux_freeipa_enroll_sssd_access_update_mode` defaults to `stable`, which leaves SSSD cache timings at the upstream client defaults for the most conservative behavior. Set it to `fast` if you want the role to install an SSSD drop-in that reduces identity and group-membership cache delays for IPA GUI access changes.
- `linux_freeipa_enroll_sssd_fast_memcache_timeout` defaults to `30`, `linux_freeipa_enroll_sssd_fast_entry_cache_timeout` defaults to `30`, `linux_freeipa_enroll_sssd_fast_negative_cache_timeout` defaults to `15`, and `linux_freeipa_enroll_sssd_fast_refresh_expired_interval` defaults to `15`. Those values are only applied when the access-update mode is `fast`.
- `linux_freeipa_enroll_manage_local_sshd_allow_users` defaults to `true`, so successful Linux enrollments also enforce an `sshd` `AllowGroups` rule derived from those same Linux admin groups. This keeps SSH access tied to current IPA-backed group membership instead of the last playbook-rendered user snapshot.
- `linux_freeipa_enroll_local_sshd_allow_users_extra` defaults to `['root']`, and the role also preserves the current Ansible connection user automatically by adding their primary groups to the generated `AllowGroups` rule so repository automation does not lock itself out.
- `ipaclient_domain` must be the shared IPA DNS domain such as `example.com`, not an IPA server hostname such as `ipa01.example.com`.
- `linux_ipa_servers` should preferably be a YAML list of IPA server FQDNs. Comma-separated strings are normalized, but list syntax is the preferred form.
- When DNS is not ready yet, the role can manage a dedicated `/etc/hosts` block from `linux_ipa_etc_hosts_entries` before IPA connectivity checks run.
- `linux_freeipa_enroll_manage_authoritative_dns` can also repair the specific host A, PTR, and link-local AAAA records in FreeIPA DNS before enrollment. It is disabled by default because it mutates authoritative DNS data.
- When the relevant reverse zone is not hosted in FreeIPA DNS, the role now keeps the forward A and AAAA repair path but skips PTR repair instead of failing the enrollment.
- `linux_freeipa_enroll_pin_local_hostname_in_etc_hosts` defaults to `true`, so the role also pins the guest enrollment FQDN to the guest primary IPv4 in `/etc/hosts` before hostname verification and join attempts.
- The guest FQDN used for enrollment must not resolve to loopback or link-local addresses such as `127.0.0.1`, `::1`, `169.254.0.0/16`, or `fe80::/10`.
- The guest primary IPv4 address should also reverse-resolve back to that same FQDN before enrollment. When authoritative PTR repair is unavailable in the current FreeIPA DNS workflow, the role warns and continues instead of failing on the PTR mismatch alone.
- The upstream collection must be installed from `requirements.yml` before execution.
