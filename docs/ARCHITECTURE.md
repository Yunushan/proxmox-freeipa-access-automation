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

## Why scheduled sync on a single node

Only one Proxmox node should own the recurring sync job in a cluster to avoid duplicated work and accidental overlap.
This project uses the `proxmox_primary` inventory group for that purpose.

## Linux guest model

Linux guests are joined to FreeIPA using the upstream `ipaclient` role.
This is better than creating local guest users via automation because:

- onboarding becomes group membership,
- offboarding becomes group removal or account disable,
- authorization stays centralized,
- auditability improves.

## Windows note

This project leaves Windows out on purpose.
For proper Windows domain logon, use Active Directory or an AD trust model where appropriate.
