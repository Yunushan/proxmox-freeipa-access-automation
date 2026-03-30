# Tests

This repository currently keeps a lightweight smoke-test layer instead of a full integration harness.

## Current Coverage

- `scripts/lint.py` runs repository lint checks
- `scripts/smoke-test.py` prepares a temporary inventory from the public example files
- smoke checks validate example inventory loading with `ansible-inventory --list`
- smoke checks run `ansible-playbook --syntax-check` for every supported playbook

## Intent

The goal of this directory is to give the repository a dedicated verification surface that can grow into deeper fixture-based or Molecule-style scenarios later without overloading the main playbook and script directories.
