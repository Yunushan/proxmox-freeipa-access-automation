# guest_qemu_agent_install

Installs and starts QEMU Guest Agent on guests that are already reachable over their normal management channel.

## Responsibilities

- install `qemu-guest-agent` on Linux guests reached over SSH
- install the QEMU Guest Agent MSI on Windows guests reached over WinRM or Windows SSH
- enable and start the guest agent service

## Key Variables

- `guest_qemu_agent_install_enabled`
- `guest_qemu_agent_install_linux_package_name`
- `guest_qemu_agent_install_linux_service_name`
- `guest_qemu_agent_install_windows_package_path`
- `guest_qemu_agent_install_windows_service_name`

## Notes

- This role is a fallback for guests that are already reachable, but do not yet have QEMU Guest Agent installed.
- It cannot help when a guest has neither SSH/WinRM access nor a working QEMU Guest Agent.
- On Proxmox, enabling guest-agent communication in the VM config still requires a fresh VM start before the host can use the agent channel.
