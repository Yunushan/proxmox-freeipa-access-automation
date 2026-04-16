# Translation Terminology Guide

## Purpose

This file keeps the translated README files consistent when they describe the same operational concepts.
Use it together with [TRANSLATION_GUIDE.md](TRANSLATION_GUIDE.md) and the canonical English [README.md](../../README.md).

## Core rules

- Translate explanatory prose and section headings when the target language has a natural, concise equivalent.
- Keep product names, protocols, file paths, inventory groups, playbook names, variable names, commands, flags, and code blocks unchanged.
- Keep recurring technical nouns stable inside a single translated README. Do not switch back and forth between a translated word and its English form unless the English form is a literal identifier.
- If a target language commonly keeps an operator term in English, that is acceptable. Consistency matters more than forcing a literal translation.
- When in doubt, preserve the exact technical noun and translate the surrounding explanation.

## Shared preferred terms

| Term | Guidance |
| --- | --- |
| `FreeIPA`, `Proxmox`, `Windows`, `Linux` | Never translate product names. |
| `SSH`, `LDAP`, `LDAPS`, `DNS`, `HBAC`, `SSSD`, `Kerberos` | Keep protocol and subsystem names unchanged. |
| `QEMU Guest Agent` | Keep the product/component name unchanged. |
| `inventory` | Keep `inventory` when referring to Ansible inventory structure, files, or groups. |
| `vault` | Keep `vault` when referring to Ansible vault files or commands. |
| `workflow` | Translate only if the target language has a short, natural operator term. Otherwise keep `workflow`. |
| `rollout` | Translate only if it reads naturally in that language. Otherwise keep `rollout`. |
| `validation` | Translate when natural; otherwise keep `validation`. |
| `preview`, `apply` | Translate in prose when natural, but never change CLI flags or commands. |
| `Controller`, `Targets` | Localize if the language has a clear technical equivalent; otherwise keep the English labels consistently. |
| `collection` | Keep `collection` when referring to an Ansible collection. |
| `hostgroup`, `playbook`, `role` | Keep exact technical nouns unless the translation already has an established and consistently used local equivalent. |

## Section-heading guidance

A translated README can follow either of these styles:

- localized general headings with preserved technical nouns
- mixed headings that keep short operator terms in English

Both are acceptable, but each file should pick one style and stay with it.

Examples of acceptable patterns:

- `Windows Workflow`, `Controller`, `Targets`
- localized equivalents for those same headings in the target language

Examples to avoid:

- translating `Controller` in one heading and keeping `Targets` in English without a clear style reason
- using both a translated word and `workflow` for the same recurring concept in different sections
- translating a variable name, inventory group name, or playbook name in prose so that it no longer matches the actual repository

## Practical review checklist

Before you merge a translated README:

- confirm that recurring technical nouns are used the same way throughout the file
- confirm that command blocks, file paths, playbook names, inventory groups, and variables still match the English source exactly
- confirm that headings sound intentional instead of randomly switching between localized and English operator words
- run `python scripts/check_translations.py --strict`
- do one human read-through after the checker passes, because the checker does not evaluate translation quality
