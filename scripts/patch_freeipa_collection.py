from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
COLLECTION_NAMESPACE_PARTS = ("ansible_collections", "freeipa", "ansible_freeipa")
DEFAULT_COLLECTION_BASES = (
    ROOT_DIR / "collections",
    Path.home() / ".ansible" / "collections",
    Path("/usr/share/ansible/collections"),
    Path("/usr/local/share/ansible/collections"),
)
ENV_COLLECTION_PATH_KEYS = (
    "ANSIBLE_COLLECTIONS_PATH",
    "ANSIBLE_COLLECTIONS_PATHS",
)
REPLACEMENTS = {
    "from ansible.module_utils._text import to_text\n":
        "from ansible.module_utils.common.text.converters import to_text\n",
    "from ansible.module_utils._text import to_native\n":
        "from ansible.module_utils.common.text.converters import to_native\n",
    "from ansible.module_utils._text import to_text, to_native\n":
        "from ansible.module_utils.common.text.converters import to_text, to_native\n",
    "from ansible.module_utils._text import to_native, to_text\n":
        "from ansible.module_utils.common.text.converters import to_native, to_text\n",
    "from ansible.module_utils.common._collections_compat import Mapping\n":
        "from collections.abc import Mapping\n",
}
DEPRECATED_IMPORT_SNIPPETS = (
    "from ansible.module_utils._text import",
    "from ansible.module_utils.common._collections_compat import",
)


def patch_file(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    updated = original
    for old, new in REPLACEMENTS.items():
        updated = updated.replace(old, new)

    if updated == original:
        return False

    path.write_text(updated, encoding="utf-8")
    return True


def collection_root_from_base(base_path: Path) -> Path:
    if base_path.name == "ansible_freeipa":
        return base_path
    return base_path.joinpath(*COLLECTION_NAMESPACE_PARTS)


def iter_python_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*.py")
        if ".git" not in path.parts and "__pycache__" not in path.parts
    )


def find_remaining_deprecated_imports(root: Path) -> list[str]:
    remaining: list[str] = []
    for path in iter_python_files(root):
        content = path.read_text(encoding="utf-8")
        for pattern in DEPRECATED_IMPORT_SNIPPETS:
            if pattern in content:
                remaining.append(f"{path.relative_to(root)}: {pattern}")
    return remaining


def split_collection_path_list(value: str) -> list[str]:
    if not value:
        return []

    parts = [part for part in value.split(os.pathsep) if part]
    if len(parts) > 1:
        return parts

    # Some users keep POSIX-style ':' separated values in repo config even when
    # running the helper from PowerShell on Windows.
    if os.pathsep != ":" and ":" in value:
        return [part for part in value.split(":") if part]

    return parts


def discover_collection_roots() -> list[Path]:
    candidate_roots: list[Path] = []

    for base_path in DEFAULT_COLLECTION_BASES:
        candidate_roots.append(collection_root_from_base(base_path.expanduser()))

    for env_key in ENV_COLLECTION_PATH_KEYS:
        for raw_path in split_collection_path_list(os.environ.get(env_key, "")):
            candidate_roots.append(collection_root_from_base(Path(raw_path).expanduser()))

    resolved_existing_roots: list[Path] = []
    seen: set[Path] = set()
    for candidate in candidate_roots:
        try:
            resolved = candidate.resolve()
        except OSError:
            continue

        if resolved in seen or not resolved.is_dir():
            continue

        seen.add(resolved)
        resolved_existing_roots.append(resolved)

    return resolved_existing_roots


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Patch installed freeipa.ansible_freeipa collections to replace "
            "deprecated ansible-core imports removed in 2.24+."
        )
    )
    parser.add_argument(
        "--collection-root",
        type=Path,
        action="append",
        default=[],
        help=(
            "Path to an installed freeipa.ansible_freeipa collection root or "
            "its parent collections directory. May be provided multiple times. "
            "If omitted, the script patches the repo-local and standard Ansible "
            "collection locations that exist on disk."
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.collection_root:
        collection_roots = [
            collection_root_from_base(path.expanduser()).resolve()
            for path in args.collection_root
        ]
    else:
        collection_roots = discover_collection_roots()

    if not collection_roots:
        print(
            (
                "No installed freeipa.ansible_freeipa collection was found in the "
                "repo-local, user, or system collection paths."
            ),
            file=sys.stderr,
        )
        return 1

    any_changes = False
    for collection_root in collection_roots:
        python_files = iter_python_files(collection_root)
        if not python_files:
            print(
                f"No Python files found under collection root: {collection_root}",
                file=sys.stderr,
            )
            return 1

        changed_files: list[str] = []
        for path in python_files:
            if patch_file(path):
                changed_files.append(str(path.relative_to(collection_root)))

        remaining = find_remaining_deprecated_imports(collection_root)
        if remaining:
            print(
                (
                    "The collection still contains deprecated ansible-core imports "
                    f"after patching: {collection_root}"
                ),
                file=sys.stderr,
            )
            for item in remaining:
                print(f" - {item}", file=sys.stderr)
            return 1

        if changed_files:
            any_changes = True
            print(
                "Patched freeipa.ansible_freeipa for ansible-core 2.24+ compatibility:"
            )
            print(f"Collection root: {collection_root}")
            for item in changed_files:
                print(f" - {item}")
        else:
            print(
                (
                    "freeipa.ansible_freeipa is already patched for ansible-core "
                    f"2.24+ compatibility: {collection_root}"
                )
            )

    if not any_changes:
        print("No patch changes were required.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
