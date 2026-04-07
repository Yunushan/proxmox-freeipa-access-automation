# linux_ipa_ssh_bootstrap

Bootstraps controller SSH key access on Linux guests so first-touch password access can promote itself into reusable key-based access.

## Responsibilities

- validate the controller keypair paths used for bootstrap
- install the controller public key into the effective SSH user's `authorized_keys`
- prefer the matching controller private key for later Linux guest plays in the same run

## Key Variables

- `linux_ipa_ssh_bootstrap_enabled`
- `linux_ipa_ssh_bootstrap_password`
- `linux_ipa_ssh_bootstrap_public_key_file`
- `linux_ipa_ssh_bootstrap_private_key_file`

## Notes

- This role uses the current SSH connection user, which matches normal `ssh-copy-id` behavior.
- It still requires first-contact reachability, typically via `ansible_password` or a shared bootstrap password.
- Host key verification remains controlled separately by `linux_ipa_ssh_host_key_policy`.
