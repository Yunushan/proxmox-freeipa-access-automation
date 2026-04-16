# Translation Guide

## Scope

`README.md` in the repository root is the canonical documentation source.
Translated files in this directory should mirror the full README structure rather than only a short overview.
They should also follow the shared terminology policy in [TERMINOLOGY.md](TERMINOLOGY.md).

Each translated page should stay aligned on these points:

- project purpose
- core capabilities
- quick-start direction
- detailed operational notes
- security and verification guidance
- primary documentation links
- clear pointer back to the English canonical README
- consistent handling of recurring technical terms across translations

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
- follow the shared terminology glossary in [TERMINOLOGY.md](TERMINOLOGY.md)
- translate narrative prose and section titles when the target language has a natural equivalent, but keep recurring technical nouns consistent within the same file
- do not alternate between a translated term and its English form in the same README unless the English form is part of code or a literal identifier
- prefer concise language over word-for-word translation
- if a translation becomes stale or incomplete, leave the English README as the reference and refresh the metadata date only after review
- run `python scripts/check_translations.py --strict` before merging translation updates so heading structure drift is caught early
- translated README files are expected to stay broadly comparable in content coverage to the English README; they should not drop into a 200-400 line summary when the canonical file is substantially longer
- remember that the current checker validates metadata, heading structure, and coverage ratio, but it does not judge linguistic quality or terminology consistency on its own

## Terminology policy

Use these rules consistently:

- keep product names, protocols, inventory groups, playbook names, variable names, file paths, and code examples unchanged
- keep inline code and fenced code blocks identical to the English source unless there is a strong reason not to
- translate surrounding explanation freely, but keep the shared operator terms from [TERMINOLOGY.md](TERMINOLOGY.md) stable
- if the target language commonly borrows a term like `inventory`, `vault`, `workflow`, `rollout`, or `validation`, that is acceptable; just use the same form throughout the file
- if a section heading uses a localized form such as "Controller" translated into the target language, keep that same choice in the rest of the README
- if a translation is not actually localized yet, do not treat a structure-only pass as complete; either finish the language pass or leave the English README as the real reference

## Recommended structure

1. Title
2. Canonical-source note
3. Metadata block
4. Overview
5. Core capabilities
6. Full section coverage matching the English README
7. Common commands
8. Shared terminology aligned with [TERMINOLOGY.md](TERMINOLOGY.md)
9. Key documents

## Common command block

Use the same command examples across translations unless there is a strong reason to change them:

```bash
ansible-playbook playbooks/validate.yml --ask-vault-pass
ansible-playbook playbooks/site.yml --ask-vault-pass
```
