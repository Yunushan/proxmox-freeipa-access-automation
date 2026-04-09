# Translation Guide

## Scope

`README.md` in the repository root is the canonical documentation source.
Translated files in this directory should mirror the full README structure rather than only a short overview.

Each translated page should stay aligned on these points:

- project purpose
- core capabilities
- quick-start direction
- detailed operational notes
- security and verification guidance
- primary documentation links
- clear pointer back to the English canonical README

## File naming

Use this pattern:

- `README.<language-tag>.md`

Examples:

- `README.tr.md`
- `README.de.md`
- `README.zh-CN.md`

## Required metadata

Each translated page should include these metadata lines near the top:

```text
Translation scope: full
Canonical source: ../../README.md
Last synced: YYYY-MM-DD
```

## Maintenance rules

- update the translated README after major changes to quick start, architecture, supported features, rollout behavior, or security guidance
- keep command examples identical to the English source unless localization requires explanation
- keep product names, file paths, playbook names, and variable names untranslated
- prefer concise language over word-for-word translation
- if a translation becomes stale or incomplete, leave the English README as the reference and refresh the metadata date only after review

## Recommended structure

1. Title
2. Canonical-source note
3. Metadata block
4. Overview
5. Core capabilities
6. Full section coverage matching the English README
7. Common commands
8. Key documents

## Common command block

Use the same command examples across translations unless there is a strong reason to change them:

```bash
ansible-playbook playbooks/validate.yml --ask-vault-pass
ansible-playbook playbooks/site.yml --ask-vault-pass
```
