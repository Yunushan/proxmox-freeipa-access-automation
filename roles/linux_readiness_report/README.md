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
