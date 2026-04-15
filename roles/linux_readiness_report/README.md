# linux_readiness_report

Builds a read-only Linux readiness report from the prepared runtime inventory.

## Responsibilities

- summarize which Linux runtime hosts are reachable through the configured SSH management path
- distinguish promptless SSH paths from password-backed SSH paths
- probe QEMU Guest Agent status for Proxmox-discovered Linux guests
- write a controller-side JSON report for operator review

## Key Variables

- `linux_readiness_report_enabled`
- `linux_readiness_report_emit_summary`
- `linux_readiness_report_write_file`
- `linux_readiness_report_output_path`
- `linux_readiness_report_runtime_group`
- `linux_readiness_report_manageable_group`
- `linux_readiness_report_connection_unavailable_group`

## Notes

- Use `playbooks/linux-readiness-report.yml` when you want an operator report instead of a pass-or-fail validation run.
- SSH readiness reuses the existing `filter_linux_connection_ready_hosts` probe path.
- QGA status is only probed for hosts that came from Proxmox discovery and therefore have a node and VMID context.
- The role writes a JSON document with `summary` and `hosts` sections by default.

## Report Semantics

The report evaluates the SSH path that is already configured in inventory for each runtime host.
It does not try every possible Linux account or every possible authentication method.

Example host entry:

```json
{
  "inventory_name": "proxmox-node-a-vm101",
  "ansible_host": "192.0.2.101",
  "ansible_user": "root",
  "ssh": {
    "ready": true,
    "promptless": true,
    "auth_mode": "key_or_agent",
    "detail": "SSH connection probe succeeded"
  },
  "qga": {
    "applicable": true,
    "status": "available",
    "configured": true,
    "responsive": true,
    "detail": "QEMU Guest Agent responded to qm guest ping"
  },
  "ready_for_connection_dependent_automation": true
}
```

### SSH fields

- `ssh.ready: true` means the currently configured management connection worked from the controller.
- `ssh.promptless: true` means the probe succeeded without `ansible_password`, so the path is non-interactive from Ansible's perspective, typically key-based SSH or an SSH agent.
- `ssh.auth_mode: password_configured` means the host had `ansible_password` and the probe used `sshpass`.
- `ssh.auth_mode: key_or_agent` means the host had no `ansible_password` and the probe succeeded in `BatchMode`, so Ansible could connect without an interactive password prompt.
- `ssh.auth_mode: unknown` means the host was not SSH-ready, so the report could not classify it as a working password-backed or promptless path.
- `ready_for_connection_dependent_automation` currently mirrors `ssh.ready`.

### QGA fields

- `qga.status: available` means `qm guest ping <vmid>` succeeded on the owning Proxmox node.
- `qga.status: disabled` means the Proxmox VM config does not have the guest agent enabled.
- `qga.status: configured_unresponsive` means the Proxmox VM config enables the guest agent, but `qm guest ping` did not succeed.
- `qga.status: node_unreachable` means the controller could not reach the owning Proxmox node well enough to run the QGA probe.
- `qga.status: not_applicable` means the host was not created by Proxmox discovery, so the report has no node/VMID context for a QGA probe.

### Quick Inspection

```bash
jq '.summary' .ansible/linux-readiness-report.json
jq '.hosts[] | {inventory_name, ansible_user, ssh_auth_mode: .ssh.auth_mode, ssh_promptless: .ssh.promptless, qga_status: .qga.status}' .ansible/linux-readiness-report.json
```
