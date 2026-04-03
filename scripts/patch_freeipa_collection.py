from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_COLLECTION_ROOT = (
    ROOT_DIR / "collections" / "ansible_collections" / "freeipa" / "ansible_freeipa"
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Patch the installed freeipa.ansible_freeipa collection to replace "
            "deprecated ansible-core imports removed in 2.24+."
        )
    )
    parser.add_argument(
        "--collection-root",
        type=Path,
        default=DEFAULT_COLLECTION_ROOT,
        help=(
            "Path to the installed freeipa.ansible_freeipa collection root. "
            f"Defaults to {DEFAULT_COLLECTION_ROOT}."
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    collection_root = args.collection_root.resolve()

    if not collection_root.is_dir():
        print(
            (
                "Collection root does not exist: "
                f"{collection_root}. Install the collection first."
            ),
            file=sys.stderr,
        )
        return 1

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
            "The collection still contains deprecated ansible-core imports after patching:",
            file=sys.stderr,
        )
        for item in remaining:
            print(f" - {item}", file=sys.stderr)
        return 1

    if changed_files:
        print(
            "Patched freeipa.ansible_freeipa for ansible-core 2.24+ compatibility:"
        )
        for item in changed_files:
            print(f" - {item}")
    else:
        print(
            "freeipa.ansible_freeipa is already patched for ansible-core 2.24+ compatibility."
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
