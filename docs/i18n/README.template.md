# Project Title

This page must be a full translated README with the same section coverage as the English [README.md](../../README.md). The English file remains canonical.

Translation scope: full
Canonical source: ../../README.md
Last synced: YYYY-MM-DD

Follow [TERMINOLOGY.md](TERMINOLOGY.md) for shared technical terms and keep your terminology choices consistent across the whole file.

## Languages

State that the English README is canonical and link back to [docs/i18n/README.md](README.md).

## Why This Exists

Explain:

- the expected starting environment
- the operational problem the repository solves
- the design principle that FreeIPA is the source of truth for identity and access

## What You Get

Translate the complete feature list from the English README. Do not shorten this section.

## Scope

Recreate the same include/exclude table from the English README.

## Windows Workflow

Explain:

- that Windows support is a separate workflow
- the purpose of `windows_qemu_guest_agent_clients`
- the purpose of `windows_management_clients`
- the requirement for AD or FreeIPA-AD trust for real Windows logon
- the limited scope of `windows_freeipa_helper_clients`

## Architecture

Keep the architecture diagram and translate the supporting explanation.

## Requirements

### Controller

Translate the complete controller requirements list.

### Targets

Translate the complete target requirements list.

## Network Ports

Keep the full network-port table and the notes that follow it.

## Compatibility

Translate the full Proxmox compatibility explanation, including the version example override.

## Quick Start

Keep the shell and PowerShell examples and translate the surrounding explanation.

### 1. Copy the example inventory and vault templates

Translate the explanatory text and keep the command blocks intact.

### 2. Edit the environment-specific files

Translate the file list explanation, Linux source mode notes, and the non-root Proxmox SSH example.

### 3. Encrypt the vault files

Translate the vault guidance, helper wrapper explanation, and vault ID notes.

### 4. Install the required collection

Translate the bootstrap explanation and keep the commands intact.

### 5. Run validation first

Translate:

- the validation commands
- the Windows validation notes
- the Linux readiness report explanation
- the readiness field interpretation list
- the quick `jq` examples

### 6. Optional: preview planned changes

Translate the check-mode caveats and keep the note block structure.

### 7. Apply the full configuration

Translate the explanation for the final site run and the Windows vault-ID note.

## Rollout Order

Translate the rollout order explanation, the limited PowerShell example, and the default rollout controls.

## Tag Model

Translate the tag model and keep the example commands.

## Event-Driven VM Onboarding

Translate the full event-driven onboarding explanation.

## Inventory Model

Translate:

- the inventory-group explanation
- the important hostname note
- the template warning

### Linux Guest Source Modes

Translate the introductory explanation for the three Linux guest source modes.

#### 1. Static inventory hosts

Translate the explanation and keep the YAML example.

#### 2. Manual host definitions in variables

Translate the explanation, notes, and keep the YAML example.

#### 3. Proxmox VM auto-discovery

Translate:

- the YAML example
- the full discovery notes list
- all allowlist, blacklist, QGA, bootstrap, hostname, DNS, and retry explanations

## Configuration Surface

Translate the file list and the main variable-family table.

## Example Group Strategy

Translate the example group strategy and keep the suffix examples.

## Security

Translate the full security guidance and keep the shell/PowerShell examples.

## Idempotency and Caveats

Translate the full caveats list without shortening it.

## Verification

Translate the introduction and all three verification subsections.

### In FreeIPA

Translate the full checklist.

### In Proxmox

Translate the full checklist.

### On a Linux Guest

Translate the full checklist.

## Repository Layout

Keep the `<details>` block and the repository tree, translating only the surrounding helper text.

## Development

Translate the complete helper-file list and keep the command blocks.

## Next Extensions

Translate the full suggested extensions list.

## License

Point to the same MIT license file.
