# Architecture

## Identity flow

```text
FreeIPA users/groups
        |
        +--> Proxmox LDAP realm --> synced PVE users/groups --> PVE ACLs/roles
        |
        +--> Linux IPA clients --> SSSD/PAM/NSS --> HBAC decides login access
        |
        +--> FreeRADIUS (separate concern, same directory backend)
```

## Why FreeIPA and not FreeRADIUS as the source

FreeRADIUS is excellent for AAA workflows such as Wi-Fi, NAC, VPN, and 802.1X.
It is not the best place to become your canonical identity store for virtualization and guest operating systems.

For virtualization and Linux guest access, FreeIPA gives you:

- centralized users and groups,
- host-based access control,
- consistent SSSD integration,
- easier join/offboarding lifecycle.

## Why direct LDAP for Proxmox

Proxmox can authenticate against LDAP-based realms and sync users/groups into PVE.
That makes Proxmox a consumer of directory state instead of another manual identity island.

## Proxmox compatibility envelope

The Proxmox automation in this repository is built around the `pveum` and `pvesh` interfaces used for:

- authentication realm definition,
- directory sync,
- role management,
- ACL binding.

The project is intended to support Proxmox VE major versions `6`, `7`, `8`, `9`, and `10` as the tested baseline.
That support is enforced by validation using `pveversion`, and the tested set is configurable through `proxmox_supported_major_versions`.
By default, `proxmox_allow_future_major_versions` is enabled, so majors newer than the highest tested entry also pass the compatibility gate.
That future-major pass-through is not a claim that the full workflow has already been validated against those released Proxmox series.
Legacy majors `1` through `5` can be allowed locally by changing that variable, but that should be treated as an environment-specific override rather than a tested public support claim.

This does not mean every Proxmox release behaves identically.
Small CLI or API output differences can still exist across minor releases, so changes should still be tested in a lab before production rollout.

## Why scheduled sync on a single node

Only one Proxmox node should own the recurring sync job in a cluster to avoid duplicated work and accidental overlap.
This project uses the `proxmox_primary` inventory group for that purpose.

## Linux guest model

Linux guests are joined to FreeIPA using the upstream `ipaclient` role.
This repository can source those guests from static inventory entries,
manual host definitions, or Proxmox VM discovery.
The source inventory group is `linux_ipa_clients`, and the generated runtime
group is `linux_ipa_clients_runtime`.
When the connection target is only an IP or a synthetic alias, the combined
`site` and `linux-clients` flows resolve the guest's effective FQDN before
FreeIPA hostgroup membership is built.

This is better than creating local guest users via automation because:

- onboarding becomes group membership,
- offboarding becomes group removal or account disable,
- authorization stays centralized,
- auditability improves.

## Windows note

This project leaves Windows out on purpose.
For proper Windows domain logon, use Active Directory or an AD trust model where appropriate.
