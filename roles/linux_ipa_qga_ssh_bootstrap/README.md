# linux_ipa_qga_ssh_bootstrap

Bootstraps Linux guest SSH access through the Proxmox QEMU Guest Agent so already running VMs can become reachable without a reboot or a temporary SSH password.

## Responsibilities

- validate the controller SSH keypair used for bootstrap
- verify the Proxmox guest agent responds for runtime Linux guests
- create a dedicated Linux automation user inside the guest
- install the controller SSH public key for that user
- ensure the bootstrap user has passwordless sudo for subsequent Ansible runs
- switch the runtime host to that bootstrap user and private key for later plays

## Key Variables

- `linux_ipa_qga_ssh_bootstrap_enabled`
- `linux_ipa_qga_ssh_bootstrap_user`
- `linux_ipa_qga_ssh_bootstrap_shell`
- `linux_ipa_qga_ssh_bootstrap_public_key_file`
- `linux_ipa_qga_ssh_bootstrap_private_key_file`
- `linux_ipa_qga_ssh_bootstrap_install_sudo`
- `linux_ipa_qga_ssh_bootstrap_timeout`
- `linux_ipa_qga_ssh_bootstrap_qm_path`
- `linux_ipa_qga_ssh_bootstrap_delegate_python_interpreter`

## Notes

- This role only applies to runtime Linux hosts that carry both `linux_ipa_proxmox_node_inventory_host` and `linux_ipa_proxmox_vmid`.
- It relies on the QEMU Guest Agent already being active in the guest.
- The bootstrap user is persistent by default so later site/linux runs can keep using the same automation account.
- `linux_ipa_qga_ssh_bootstrap_qm_path` defaults to `/usr/sbin/qm` so delegated Proxmox tasks do not depend on an interactive PATH.
