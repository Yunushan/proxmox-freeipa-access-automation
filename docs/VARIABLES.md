# Variables

This repository splits environment variables by domain under `inventories/<env>/group_vars/all/`.

## File layout

- `10-features.yml`: top-level feature toggles
- `15-rollout.yml`: rollout serial and failure-budget settings
- `20-freeipa.yml`: FreeIPA admin/API values, groups, hostgroups, HBAC, and sudo rules
- `30-linux-clients.yml`: Linux enrollment, manual client definitions, and Proxmox discovery
- `35-windows-clients.yml`: Windows domain-membership settings and limited FreeIPA-aware helper settings
- `40-proxmox-ldap.yml`: Proxmox LDAP realm configuration
- `50-proxmox-sync.yml`: recurring Proxmox realm-sync timer settings
- `60-proxmox-rbac.yml`: Proxmox custom roles and ACL bindings
- `vault-freeipa.yml`: encrypted FreeIPA admin secret
- `vault-proxmox.yml`: encrypted Proxmox LDAP bind secret and optional sudo password
- `vault-windows.yml`: encrypted Windows WinRM and domain-join secrets

`main.yml` remains as a directory index only.

## Rollout controls

The repository exposes play-level rollout controls through `15-rollout.yml`.

- `freeipa_access_serial`
- `freeipa_access_max_fail_percentage`
- `proxmox_rollout_serial`
- `proxmox_rollout_max_fail_percentage`
- `linux_freeipa_enroll_serial`
- `linux_freeipa_enroll_max_fail_percentage`
- `windows_management_serial`
- `windows_management_max_fail_percentage`

Those values drive the FreeIPA access play, the Proxmox play, Linux hostname resolution, Linux validation, and Linux enrollment.

## Source and runtime groups

- `linux_ipa_clients`: declarative source inventory group
- `linux_ipa_clients_runtime`: generated runtime group used by Linux preparation, validation, and enrollment playbooks
- `windows_qemu_guest_agent_clients`: optional inventory group used only for QEMU Guest Agent installation on reachable Windows guests
- `windows_management_clients`: optional inventory group used by the separate Windows domain-membership workflow
- `windows_freeipa_helper_clients`: optional inventory group used by the limited FreeIPA-aware Windows helper workflow

Use `linux_ipa_clients_runtime` when a FreeIPA hostgroup should include the full prepared Linux guest set.

## Windows management

- `windows_domain_membership_enabled`: when `true`, the separate Windows workflow manages hosts in `windows_management_clients`
- `windows_domain_membership_state`: `domain` joins the Windows host to Active Directory, while `workgroup` removes it from the domain and places it into `windows_domain_membership_workgroup_name`
- `windows_domain_membership_dns_domain_name`: AD DNS domain that the Windows host should join
- `windows_domain_membership_domain_admin_user`: AD account used for the join or unjoin operation
- `windows_domain_membership_domain_admin_password`: vaulted password for that AD account; defaults to `vault_windows_domain_admin_password`
- `windows_domain_membership_domain_ou_path`: optional OU path used when creating the computer object during a join
- `windows_domain_membership_domain_server`: optional domain controller to target explicitly during the join
- `windows_domain_membership_hostname`: optional Windows hostname to apply during the membership change
- `windows_domain_membership_workgroup_name`: workgroup name used when `windows_domain_membership_state: workgroup`; defaults to `WORKGROUP`
- `windows_domain_membership_reboot`: when `true`, the membership module reboots the Windows host automatically if required; defaults to `true`
- `windows_domain_membership_reboot_timeout`: maximum seconds the workflow waits for the Windows host to come back after an automatic reboot; defaults to `900`
- `vault_windows_admin_password`: optional vaulted WinRM password used by the example Windows inventory entries
- `vault_windows_domain_admin_password`: vaulted AD domain-join password used by the Windows membership workflow
- in FreeIPA-centered environments, Windows logon should still flow through Active Directory or a FreeIPA-AD trust; Windows hosts do not join FreeIPA directly
- a FreeIPA-only environment without Active Directory or a FreeIPA-AD trust cannot use the Windows domain-membership workflow for real Windows logon

## Windows FreeIPA helpers

- `windows_freeipa_helpers_enabled`: when `true`, the limited FreeIPA-aware Windows helper workflow manages hosts in `windows_freeipa_helper_clients`
- `windows_freeipa_helpers_emit_summary`: when `true`, the helper workflow prints the final `windows_freeipa_helpers_summary` host fact after successful execution; defaults to `true`
- `windows_freeipa_helpers_ipa_servers`: IPA server hostnames used for helper validation; defaults to `linux_ipa_servers`
- `windows_freeipa_helpers_https_port`: HTTPS port used for IPA reachability checks from Windows; defaults to `linux_freeipa_enroll_https_port` or `443`
- `windows_freeipa_helpers_trust_ipa_ca`: when `true`, the helper workflow imports the provided IPA CA certificate into the Windows certificate store
- `windows_freeipa_helpers_ipa_ca_auto_fetch`: when `true`, the helper workflow can bootstrap the IPA CA certificate directly from an IPA server when no explicit certificate file or inline content is provided
- `windows_freeipa_helpers_ipa_ca_auto_fetch_server`: optional IPA server used for CA auto-fetch; defaults to the first host in `windows_freeipa_helpers_ipa_servers`
- `windows_freeipa_helpers_ipa_ca_expected_thumbprint`: optional pinned certificate thumbprint checked against the staged IPA CA before import; useful when you want CA auto-fetch without blind trust-on-first-use
- `windows_freeipa_helpers_ipa_ca_certificate_src`: controller-side certificate file copied to Windows before the IPA CA import
- `windows_freeipa_helpers_ipa_ca_certificate_content`: inline certificate content used when no controller-side source file is provided
- `windows_freeipa_helpers_ipa_ca_store_location`: target Windows certificate-store location for the IPA CA import; defaults to `LocalMachine`
- `windows_freeipa_helpers_ipa_ca_store_name`: target Windows certificate-store name for the IPA CA import; defaults to `Root`
- `windows_freeipa_helpers_manage_hosts_entries`: when `true`, the helper workflow manages the Windows hosts file with `windows_freeipa_helpers_hosts_entries`
- `windows_freeipa_helpers_hosts_entries`: list of `{ ip, canonical_name, aliases }` mappings written to the Windows hosts file for IPA endpoints or other bootstrap names
- `windows_freeipa_helpers_manage_local_group_memberships`: when `true`, the helper workflow manages local Windows groups with `windows_freeipa_helpers_local_group_memberships`
- `windows_freeipa_helpers_local_group_memberships`: list of `{ name, members, state }` definitions applied through `win_group_membership`, useful for local groups such as `Administrators` or `Remote Desktop Users`
- `windows_freeipa_helpers_manage_openssh_server`: when `true`, the helper workflow manages OpenSSH Server on Windows
- `windows_freeipa_helpers_openssh_install`: when `true`, the helper workflow installs the OpenSSH Server capability before managing the service; defaults to `true`
- `windows_freeipa_helpers_openssh_service_name`: Windows service name used for OpenSSH Server management; defaults to `sshd`
- `windows_freeipa_helpers_openssh_start_mode`: Windows service start mode used for OpenSSH Server; defaults to `auto`
- `windows_freeipa_helpers_openssh_state`: desired Windows OpenSSH Server service state; defaults to `started`
- `windows_freeipa_helpers_openssh_port`: Windows OpenSSH Server TCP port used for firewall management; defaults to `22`
- `windows_freeipa_helpers_openssh_configure_firewall`: when `true`, the helper workflow ensures an inbound Windows firewall rule exists for the configured OpenSSH Server port
- `windows_freeipa_helpers_openssh_firewall_rule_name`: display name of that managed Windows firewall rule; defaults to `OpenSSH Server (Ansible Managed)`
- `windows_freeipa_helpers_validate_dns`: when `true`, the helper workflow validates DNS resolution for every server in `windows_freeipa_helpers_ipa_servers`
- `windows_freeipa_helpers_validate_tcp`: when `true`, the helper workflow validates TCP reachability for every server in `windows_freeipa_helpers_ipa_servers` across `windows_freeipa_helpers_tcp_ports`
- `windows_freeipa_helpers_tcp_ports`: TCP ports that the helper workflow checks against each IPA server; defaults to `[88, 389, 443]`
- `windows_freeipa_helpers_tcp_timeout_ms`: TCP connection timeout in milliseconds for each server-port validation; defaults to `3000`
- `windows_freeipa_helpers_validate_https`: when `true`, the helper workflow validates HTTPS reachability and TLS trust for every server in `windows_freeipa_helpers_ipa_servers`
- `windows_freeipa_helpers_https_timeout_ms`: HTTPS validation timeout in milliseconds for the Windows helper workflow; defaults to `15000`
- `windows_freeipa_helpers_validate_time_source`: when `true`, the helper workflow validates Windows time-source reachability with `w32tm`
- `windows_freeipa_helpers_time_source`: optional time source used for that `w32tm` validation; defaults to the first host in `windows_freeipa_helpers_ipa_servers`
- `windows_freeipa_helpers_summary`: host fact emitted by the helper workflow that summarizes CA trust, hosts bootstrap, local group management, OpenSSH management, and validation coverage for the current Windows host
- `playbooks/windows-freeipa-validate.yml`: validation-only entrypoint for `windows_freeipa_helper_clients`; it forces CA trust, hosts-file changes, local-group changes, and OpenSSH management off while keeping the helper validation and summary path
- this workflow is helper-only and does not provide Windows domain membership or native Windows logon against FreeIPA

## Linux readiness reporting

- `linux_readiness_report_enabled`: when `true`, the readiness-report role runs and builds a structured Linux runtime-host audit; defaults to `true`
- `linux_readiness_report_emit_summary`: when `true`, the readiness-report playbook prints a one-line operator summary after building the report; defaults to `true`
- `linux_readiness_report_write_file`: when `true`, the readiness-report playbook writes a JSON document on the controller; defaults to `true`
- `linux_readiness_report_output_path`: optional controller-side JSON output path for the readiness report; defaults to `.ansible/linux-readiness-report.json` under the repository root when left empty
- `linux_readiness_report_runtime_group`: runtime inventory group that should be audited; defaults to `linux_ipa_clients_runtime`
- `linux_readiness_report_manageable_group`: runtime inventory group treated as SSH-ready by the report; defaults to `linux_ipa_clients_manageable_runtime`
- `linux_readiness_report_connection_unavailable_group`: runtime inventory group treated as not yet SSH-ready by the report; defaults to `linux_ipa_clients_connection_unavailable_runtime`
- `playbooks/linux-readiness-report.yml`: read-only audit entrypoint that prepares Linux runtime inventory, reuses the SSH connection probe path, probes QEMU Guest Agent status for Proxmox-discovered guests, and writes a controller-side report

## Hostname resolution rules

FreeIPA still needs each guest's final hostname.

The runtime flow resolves hostnames in this order:

1. `freeipa_hostgroup_hostname` when already set
2. `ipa_hostname` when explicitly declared
3. `ipa_hostname` or the guest short hostname with `linux_ipa_identity_hostname_suffix` when that suffix is set
4. the inventory hostname when it is already an FQDN
5. `hostname -f` on the guest during the combined `site` or `linux-clients` flows

For `freeipa.yml`, rely on declarative values such as FQDN inventory names or `ipa_hostname`.

Relevant Linux enrollment hostname controls:

- `linux_ipa_identity_hostname_suffix`: optional suffix used to turn short hostnames such as `app-server-01` into FQDNs such as `app-server-01.example.net`
- `linux_freeipa_enroll_manage_hostname`: when `true`, the Linux enrollment role updates the guest system hostname to the resolved FQDN before IPA enrollment
- `linux_freeipa_enroll_join_attempts`: number of times the repository retries the upstream FreeIPA client join when it fails with a JSON-RPC timeout; defaults to `3`
- `linux_freeipa_enroll_join_retry_delay`: seconds to wait between join retries after a JSON-RPC timeout; defaults to `15`
- `linux_freeipa_enroll_success_group`: runtime inventory group that collects only the Linux guests that completed FreeIPA enrollment successfully; defaults to `linux_ipa_clients_enrolled_runtime`
- `linux_freeipa_enroll_timeout_group`: runtime inventory group that collects Linux guests that exhausted all join retries and were allowed to continue in timed-out state; defaults to `linux_ipa_clients_enroll_timeout_runtime`
- `linux_freeipa_enroll_continue_on_join_timeout`: when `true`, Linux enrollment warns and continues after the final JSON-RPC join timeout instead of failing the workflow; timed-out guests are excluded from the success group and added to `linux_freeipa_enroll_timeout_group`; defaults to `false`
- `linux_freeipa_enroll_collect_join_timeout_diagnostics`: when `true`, Linux enrollment captures bounded guest-side timeout diagnostics, including a short `ipa-join -d` replay log, after the final JSON-RPC join timeout; defaults to `true`
- `linux_freeipa_enroll_refresh_apt_cache`: when `true`, Debian-family Linux enrollment targets refresh APT metadata before the upstream role installs `freeipa-client` packages, which avoids stale package indexes that can otherwise cause mirror `404` failures; defaults to `true`
- `linux_freeipa_enroll_wait_for_cloud_init`: when `true`, Debian-family Linux enrollment waits for `/var/lib/cloud/instance/boot-finished` on guests that use cloud-init before trying to refresh APT metadata; defaults to `true`
- `linux_freeipa_enroll_cloud_init_timeout`: seconds Debian-family Linux enrollment waits for cloud-init completion before continuing to the generic APT lock wait path; defaults to `60`
- `linux_freeipa_enroll_wait_for_apt_background_services`: when `true`, Debian-family Linux enrollment waits for `apt-daily.service` and `apt-daily-upgrade.service` to become inactive on systemd guests before refreshing APT metadata; it defaults to `false` because the following APT lock wait already catches real package-manager contention more reliably
- `linux_freeipa_enroll_apt_background_services_timeout`: seconds Debian-family Linux enrollment waits for those optional background package services before continuing to the generic APT lock wait path; defaults to `60`
- `linux_freeipa_enroll_apt_lock_timeout`: seconds Debian-family Linux enrollment waits for active `apt` or `dpkg` lock holders before failing the package-metadata refresh; useful when cloud-init or unattended upgrades are still finishing on a fresh guest; defaults to `60`
- `linux_freeipa_enroll_recover_stuck_apt_daily`: when `true`, Debian-family Linux enrollment stops the related APT timers and services, terminates a stale `apt-daily.service` update job after the APT lock wait times out, then retries the lock check instead of failing immediately; defaults to `true`
- `linux_freeipa_enroll_apt_lock_recovery_timeout`: seconds Debian-family Linux enrollment waits for locks to clear after terminating a stale `apt-daily.service`; defaults to `15`
- `linux_freeipa_enroll_https_port`: HTTPS port used for Linux guest IPA web/API reachability checks and JSON probes; defaults to `443`
- `linux_freeipa_enroll_bootstrap_ipa_server_hosts_from_inventory`: when `true`, Linux enrollment automatically seeds guest `/etc/hosts` entries for IPA server FQDNs using the `ipa_servers` inventory hostnames and their `ansible_host` IPs before DNS-dependent preflight checks; defaults to `true`
- `linux_freeipa_enroll_networkmanager_dns_refresh_strategy`: controls how Linux enrollment activates a successful upstream DNS resolver change on `NetworkManager`-managed guests; `apply` is the effective default and uses a targeted `nmcli device reapply` with a connection-reactivation fallback, `restart` uses a full `NetworkManager` restart, and `none` leaves the change to take effect on a later reconnect or reboot
- `linux_freeipa_enroll_restart_networkmanager_after_dns_config`: deprecated compatibility alias for the older boolean behavior; when explicitly set and `linux_freeipa_enroll_networkmanager_dns_refresh_strategy` is unset, `true` maps to `restart` and `false` maps to `none`
- `linux_freeipa_enroll_join_timeout_diagnostic_http_timeout`: HTTP timeout in seconds for the guest-side `https://<ipa-server>:<linux_freeipa_enroll_https_port>/ipa/json` timeout diagnostics probe; defaults to `10`
- `linux_freeipa_enroll_join_timeout_diagnostic_ipa_join_timeout`: maximum seconds allowed for the bounded `ipa-join -d` replay that is captured after the final JSON-RPC timeout; defaults to `30`
- `linux_freeipa_enroll_join_timeout_diagnostic_log_dir`: directory on the Linux guest where the bounded `ipa-join -d` timeout log is written; defaults to `/var/tmp`
- `linux_freeipa_enroll_merge_inventory_ipa_servers`: when `true`, Linux enrollment appends the `ipa_servers` inventory hostnames to `linux_ipa_servers` before resolution, reachability checks, and the upstream client join; defaults to `true`
- `linux_freeipa_enroll_force_no_dns_lookup_with_explicit_servers`: when `true`, Linux enrollment forces `ipaclient_no_dns_lookup` whenever explicit IPA server candidates are available, even if `linux_ipaclient_no_dns_lookup` was set to `false`; defaults to `true`
- `linux_freeipa_enroll_clear_proxy_environment`: when `true`, Linux enrollment injects a focused `NO_PROXY` list for the upstream FreeIPA client role so IPA server traffic bypasses any broad guest proxy configuration; defaults to `true`
- `linux_freeipa_enroll_preflight_json_probe_enabled`: when `true`, Linux enrollment probes `https://<ipa-server>:<linux_freeipa_enroll_https_port>/ipa/json` with a short timeout before running the upstream join so slow or hung IPA web/API endpoints fail fast; defaults to `true`
- `linux_freeipa_enroll_preflight_json_probe_timeout`: timeout in seconds for the fast `https://<ipa-server>:<linux_freeipa_enroll_https_port>/ipa/json` preflight probe; defaults to `15`
- when some IPA servers fail that preflight while others respond, Linux enrollment automatically drops the unhealthy candidates from the upstream join retry loop
- when every configured IPA server fails that preflight and `linux_freeipa_enroll_continue_on_join_timeout` is enabled, Linux enrollment skips the upstream join retry loop and marks the host timed out immediately with the preflight summary
- `linux_freeipa_enroll_manage_authoritative_dns`: when `true`, Linux enrollment repairs the specific guest A record, resets a mismatched PTR when the reverse zone is hosted in FreeIPA DNS, and removes link-local AAAA records before hostname validation and join attempts; defaults to `false`
- `linux_freeipa_enroll_authoritative_dns_delegate_host`: optional inventory host used to execute authoritative FreeIPA DNS repair tasks; defaults to the first host in `ipa_servers`
- `linux_freeipa_enroll_authoritative_dns_query_server`: DNS server IP used by the authoritative DNS repair logic when it queries FreeIPA DNS directly; defaults to `127.0.0.1` on the delegated IPA host
- `linux_freeipa_enroll_authoritative_dns_remove_link_local_aaaa`: when `true`, authoritative DNS repair removes `fe80::/10` AAAA records for Linux enrollment hosts; defaults to `true`
- `linux_freeipa_enroll_pin_local_hostname_in_etc_hosts`: when `true`, Linux enrollment pins the guest enrollment FQDN to the guest primary IPv4 in `/etc/hosts` before hostname validation and join attempts; defaults to `true`
- `linux_freeipa_enroll_split_dns_enabled`: when `true`, Linux enrollment automatically configures `systemd-resolved` split DNS after a successful IPA join so the IPA DNS domain is routed to the IPA servers while all other lookups keep using the preserved public/default DNS servers; defaults to `true`
- `linux_freeipa_enroll_split_dns_public_dns_mode`: selects how the split-DNS automation decides the guest's global/public resolver path. `explicit` is the default and prefers `linux_freeipa_enroll_split_dns_public_dns_servers` when you want deterministic public DNS on every guest. If that list is left empty, explicit mode falls back to the guest's currently detected non-IPA public/default resolvers when they are still present. `preserve` tells the role to preserve each guest's current public/default DNS when possible and to fall back to recovered link or netplan DNS when live resolver state is already contaminated
- `linux_freeipa_enroll_split_dns_public_dns_servers`: optional explicit public/default DNS server list used by the split-DNS automation. In the default `explicit` mode, set this to the public resolver IPs you want the guest to keep globally. If you leave it empty, the role now tries to recover the guest's non-IPA public/default resolvers from current runtime state, reverted link state, netplan, and guest facts before failing. In `preserve` mode, leaving it empty keeps the fully automatic preserve-and-recover behavior; defaults to `[]`
- `linux_freeipa_enroll_manage_local_group_sudoers`: when `true`, Linux enrollment installs a local sudoers drop-in after a successful join so configured IPA-backed admin groups can use `sudo` through normal NSS/SSSD group resolution even if the guest-side IPA sudo-rule path is unreliable; defaults to `true`
- `linux_freeipa_enroll_local_sudo_groups`: Linux groups written to that local sudoers drop-in; defaults to `['linux-ssh-admins']`
- `linux_freeipa_enroll_local_sudo_group_domain_variants`: when `true`, Linux enrollment also writes IPA-qualified variants of those groups such as `linux-ssh-admins@example.com` and `linux-ssh-admins@EXAMPLE.COM` to the local sudoers drop-in for guests that expose SSSD groups in qualified form; defaults to `true`
- `linux_freeipa_enroll_local_sudo_sync_ipa_group_members`: when `true`, Linux enrollment also queries FreeIPA for the direct members of those configured admin groups after a successful join and writes explicit sudoers user entries for them, which avoids guest-side group-name matching inconsistencies; defaults to `true`
- `linux_freeipa_enroll_local_sudo_nopasswd`: when `true`, the local sudoers drop-in grants `NOPASSWD:ALL` instead of password-authenticated sudo; defaults to `false`
- `linux_freeipa_enroll_sssd_access_update_mode`: selects the guest-side SSSD access propagation profile after a successful IPA join; `stable` leaves the upstream client defaults untouched, while `fast` installs a repository-managed SSSD drop-in to shorten cache delays for IPA GUI access changes; defaults to `stable`
- `linux_freeipa_enroll_sssd_fast_memcache_timeout`: `nss` memcache timeout written by the optional fast SSSD propagation profile; defaults to `30`
- `linux_freeipa_enroll_sssd_fast_entry_cache_timeout`: domain `entry_cache_*_timeout` value written by the optional fast SSSD propagation profile; defaults to `30`
- `linux_freeipa_enroll_sssd_fast_negative_cache_timeout`: domain `entry_negative_timeout` value written by the optional fast SSSD propagation profile; defaults to `15`
- `linux_freeipa_enroll_sssd_fast_refresh_expired_interval`: domain `refresh_expired_interval` value written by the optional fast SSSD propagation profile; defaults to `15`
- `linux_freeipa_enroll_manage_local_sshd_allow_users`: when `true`, Linux enrollment also writes an `AllowGroups` rule into `sshd_config` based on the same IPA-backed Linux admin groups so users removed from the FreeIPA SSH admin group lose new SSH login access even when a local account path would otherwise bypass HBAC; defaults to `true`
- `linux_freeipa_enroll_local_sshd_allow_users_extra`: additional usernames whose primary groups are kept in that `sshd` allowlist alongside the IPA-derived Linux admin groups; defaults to `['root']`, and the role also preserves the active Ansible connection user automatically
- the repository-owned split-DNS automation is separate from `linux_ipaclient_configure_dns_resolver`, so the upstream flat resolver management can remain disabled while supported `systemd-resolved` guests still receive automatic split DNS after enrollment
- when authoritative PTR repair is unavailable, Linux enrollment warns on reverse-DNS mismatch and continues with the upstream IPA client join instead of failing at the repository preflight step
- `linux_ipa_manage_etc_hosts`: when `true`, the Linux enrollment role manages a bootstrap block in `/etc/hosts` before IPA connectivity and hostname verification
- `linux_ipa_etc_hosts_entries`: list of `{ ip, names }` mappings for `/etc/hosts`, useful when IPA DNS is not reachable yet or when a guest FQDN must be pinned locally during bootstrap
- `guest_qemu_agent_install_manage_proxmox_vm_agent`: when `true`, Linux workflows also enable Proxmox-side guest-agent communication for Proxmox-backed Linux guests with `qm set <vmid> --agent 1`; defaults to `true`
- `guest_qemu_agent_install_reboot_after_proxmox_vm_agent_enable`: when `true`, Linux workflows reboot running Proxmox-backed VMs after enabling the Proxmox guest-agent option; leave it `false` if you want warn-only behavior instead; defaults to `false`
- `guest_qemu_agent_install_enabled`: when `true`, reachable Linux enrollment targets and optional `windows_qemu_guest_agent_clients` hosts install and start QEMU Guest Agent; Linux workflows retry that installation after bootstrap and again after Linux enrollment so guests that become reachable later in the same run are still covered, but the repository still needs a valid first-touch SSH or WinRM path into guests where the agent is missing
- `guest_qemu_agent_install_windows_package_path`: MSI path or URL used for Windows QEMU Guest Agent installation; defaults to the Fedora virtio-win direct-download `latest-qemu-ga` MSI path for `x86_64`
- `linux_ipa_ssh_host_key_policy`: SSH host key behavior for Linux guest connections; `accept_new` is the repository default for Linux runtime targets, while `strict` requires pre-populated `known_hosts` entries and `disabled` turns host key checking off for those Linux guest connections
- `linux_ipa_qga_ssh_bootstrap_enabled`: when `true`, Proxmox-backed Linux runtime guests use the QEMU Guest Agent to create a dedicated key-only automation user before SSH-based hostname resolution or enrollment, or to inject the controller key directly into `root` when `linux_ipa_qga_ssh_bootstrap_user: root`
- `linux_ipa_qga_ssh_bootstrap_user`: username created inside Proxmox-backed Linux guests for QGA-based SSH bootstrap; set this to `root` when you want direct root-key installation instead of a separate bootstrap user
- `linux_ipa_qga_ssh_bootstrap_shell`: login shell assigned to the QGA bootstrap user
- `linux_ipa_qga_ssh_bootstrap_public_key_file`: controller SSH public key installed through the QEMU Guest Agent bootstrap path
- `linux_ipa_qga_ssh_bootstrap_private_key_file`: controller SSH private key paired with the QGA bootstrap public key and used for later SSH connections
- `linux_ipa_qga_ssh_bootstrap_install_sudo`: when `true`, the QGA bootstrap path installs `sudo` if missing before creating the bootstrap sudoers entry for non-root bootstrap users; this is skipped when `linux_ipa_qga_ssh_bootstrap_user: root`
- `linux_ipa_qga_ssh_bootstrap_timeout`: timeout passed to `qm guest exec` during the QGA bootstrap path
- `linux_ipa_qga_ssh_bootstrap_fail_on_guest_exec_blocked`: when `true`, the QGA bootstrap path hard-fails if a guest agent allows `guest-ping` but rejects `guest-exec`; defaults to `false`
- `linux_ipa_qga_ssh_bootstrap_qm_path`: Proxmox CLI command or absolute path used for Proxmox-side `qm guest ...` calls; defaults to `qm`
- `linux_ipa_qga_ssh_bootstrap_qm_fallback_paths`: common absolute `qm` locations probed on the Proxmox node before failing; defaults to `/usr/sbin/qm`, `/usr/bin/qm`, and `/sbin/qm`
- `linux_ipa_qga_ssh_bootstrap_delegate_python_interpreter`: Python interpreter forced for delegated Proxmox-side `qm guest ...` tasks; defaults to `/usr/bin/python3`
- `linux_ipa_ssh_bootstrap_enabled`: when `true`, the Linux workflows install the controller SSH public key onto the Linux guest account used for Ansible connections before hostname resolution and enrollment
- `linux_ipa_ssh_bootstrap_password`: optional shared first-touch password used as a fallback `ansible_password` for runtime Linux guests, including runs where SSH key bootstrap is disabled; keep this in vaulted variables when used
- `linux_ipa_ssh_bootstrap_public_key_file`: controller SSH public key path installed onto Linux guests during SSH bootstrap
- `linux_ipa_ssh_bootstrap_private_key_file`: controller SSH private key path preferred for subsequent Linux guest plays after SSH bootstrap
- `linux_ipaclient_kinit_attempts`: value passed to the upstream `ipaclient_kinit_attempts` setting so host Kerberos ticket acquisition is retried more aggressively during Linux IPA enrollment; defaults to `10`
- `linux_sssd_refresh_enabled`: when `true`, the `freeipa.yml` and `site.yml` workflows clear SSSD caches and restart `sssd` on managed Linux clients after FreeIPA access-model changes so new sudo and HBAC policy is visible immediately
- `linux_ipa_proxmox_discovery_vmids`: optional VMID filter list for Proxmox discovery, mainly useful for event-driven runs such as the Proxmox hook/webhook workflow
- `linux_ipa_proxmox_discovery_allowlist_enabled`: when `true`, Proxmox-discovered Linux guests are admitted to the runtime inventory only when they match at least one configured allowlist value; defaults to `false`
- `linux_ipa_proxmox_discovery_allowlist_vmids`: optional exact VMID allowlist for Proxmox-discovered Linux guests; useful when you want event-driven or targeted runs to touch only a small approved VM set
- `linux_ipa_proxmox_discovery_allowlist_ips`: optional exact IP allowlist for Proxmox-discovered Linux guests; useful when the approved guest set is tracked by management IP rather than VMID or hostname
- `linux_ipa_proxmox_discovery_allowlist_names`: optional exact-name allowlist for Proxmox-discovered Linux guests; the discovery role matches these values against the generated runtime inventory name, the raw Proxmox VM name, and any FQDN hostname hint derived from that VM name
- `linux_ipa_proxmox_discovery_blacklist_vmids`: optional exact VMID blacklist for Proxmox-discovered Linux guests; matching VMs are always excluded from the runtime inventory even when broad node discovery is enabled
- `linux_ipa_proxmox_discovery_blacklist_ips`: optional exact IP blacklist for Proxmox-discovered Linux guests; useful when infrastructure VMs should never receive Linux IPA automation even if they move between VMIDs or names
- `linux_ipa_proxmox_discovery_blacklist_names`: optional exact-name blacklist for Proxmox-discovered Linux guests; the discovery role matches these values against the generated runtime inventory name, the raw Proxmox VM name, and any FQDN hostname hint derived from that VM name
- `linux_ipa_proxmox_discovery_ansible_user`: optional SSH username assigned to Proxmox-discovered Linux guests before later runtime plays run; use this when discovered guests do not accept the inventory-wide default login user such as `root`
- `linux_ipa_proxmox_discovery_ansible_port`: optional SSH port assigned to Proxmox-discovered Linux guests; leave it empty to keep the normal SSH default of `22`
- `linux_ipa_proxmox_discovery_ansible_password`: optional SSH password assigned to Proxmox-discovered Linux guests; when left empty, discovery falls back to `linux_ipa_ssh_bootstrap_password` if that shared first-touch password is set
- `linux_ipa_proxmox_discovery_ansible_ssh_private_key_file`: optional controller private key file assigned to Proxmox-discovered Linux guests for first-touch SSH access before QEMU Guest Agent or IPA enrollment automation can take over
- `linux_ipa_proxmox_discovery_ansible_become`: optional privilege-escalation flag assigned to Proxmox-discovered Linux guests; set it when the discovery login user is not `root` and later Linux tasks must run with `become`
- `linux_ipa_proxmox_discovery_ansible_become_method`: optional privilege-escalation method for Proxmox-discovered Linux guests, commonly `sudo`
- `linux_ipa_proxmox_discovery_ansible_become_password`: optional privilege-escalation password for Proxmox-discovered Linux guests; set it when the discovery login user needs a sudo password and does not have passwordless sudo
- `linux_ipa_proxmox_discovery_complete_short_vm_names_with_suffix`: when `true`, Proxmox discovery can turn a safe short VM name such as `Teleport-Server-1` into a hostname hint such as `teleport-server-1.example.com` by completing it with `linux_ipa_identity_hostname_suffix`; defaults to `false`
- `freeipa_runtime_hostgroup_membership_inventory_group`: runtime inventory group that supplies the current Linux hosts to add into FreeIPA hostgroups; defaults to `linux_ipa_clients_runtime`
- `freeipa_runtime_hostgroup_membership_hostgroup_inventory_groups`: declarative inventory-group names used to choose which `freeipa_hostgroups` should receive those runtime hosts; defaults to the value of `freeipa_runtime_hostgroup_membership_inventory_group`
- `proxmox_vm_event_onboarding_enabled`: when `true`, `site.yml` and `proxmox.yml` deploy the optional controller-side Proxmox VM event webhook and Proxmox-side hookscript/config so `post-start` and `post-migrate` events can trigger automatic Linux onboarding
- `proxmox_vm_event_webhook_token`: shared bearer token for the controller webhook listener and Proxmox hookscript; required when `proxmox_vm_event_onboarding_enabled` is `true`
- `proxmox_vm_event_hook_webhook_url`: full webhook URL reachable from Proxmox nodes, for example `https://automation.example.com:8085/hooks/proxmox-vm-event`; required when `proxmox_vm_event_onboarding_enabled` is `true`
- `proxmox_vm_event_webhook_ansible_extra_args`: optional non-interactive extra arguments passed to `ansible-playbook` by the controller webhook, commonly used for `--vault-id` file arguments in unattended event-driven runs
- `proxmox_vm_event_hookscript_attach_existing_vms`: when `true`, Proxmox rollout automatically attaches the repository hookscript to current QEMU VMs on participating discovery nodes; defaults to `true`
- `proxmox_vm_event_hookscript_override_existing`: when `true`, Proxmox rollout replaces conflicting per-VM hookscripts with the repository hookscript; defaults to `false`

Linux enrollment naming rules:

- `ipaclient_domain` is the shared IPA DNS domain, for example `example.com`
- `linux_ipa_servers` contains IPA server hostnames, for example `ipa01.example.com`
- do not set `ipaclient_domain` to one of the IPA server hostnames
- use YAML list syntax for `linux_ipa_servers` when possible, even though the role also normalizes comma-separated strings
- the guest FQDN used for Linux enrollment must resolve to a real guest address, not loopback or link-local values such as `127.0.0.1`, `::1`, `169.254.0.0/16`, or `fe80::/10`
- the guest primary IPv4 address should reverse-resolve back to that same FQDN before Linux enrollment starts

## FreeIPA access model

- `freeipa_access_model_manage_inventory_group_host_membership`: when `true`, `freeipa_access_model` adds members resolved from `freeipa_hostgroups[*].inventory_groups`; set it to `false` for pre-enrollment runs that should create hostgroups and rules first, then add enrolled runtime hosts later
- `freeipa_linux_admin_users`: IPA usernames added directly to the declarative `linux-ssh-admins` group so they receive the repository-managed Linux SSH and sudo access model; defaults to `[]`; when left empty, the repository now leaves existing FreeIPA group membership untouched instead of clearing it
- `freeipa_user_groups`: user groups created in FreeIPA
- `freeipa_hostgroups`: hostgroups built from declarative inventory groups or hostnames
- `freeipa_hbac_rules`: login and service-access rules such as SSH access
- `freeipa_sudo_rules`: sudo authorization rules evaluated by IPA-enrolled Linux clients
- `freeipa_access_model_manage_default_login_shell`: when `true`, `freeipa_access_model` ensures the global FreeIPA default shell matches `freeipa_access_model_default_login_shell`; defaults to `true`
- `freeipa_access_model_default_login_shell`: login shell enforced as the FreeIPA global default and, when group-member login-shell management is enabled, the shell applied to matching users; defaults to `/bin/bash`
- `freeipa_access_model_manage_group_member_login_shell`: when `true`, `freeipa_access_model` also updates the login shell of users who are members of `freeipa_access_model_login_shell_groups`; defaults to `true`
- `freeipa_access_model_login_shell_groups`: FreeIPA user groups whose direct members should be forced to `freeipa_access_model_default_login_shell`; defaults to `['linux-ssh-admins']` when that declarative group exists in `freeipa_user_groups`
