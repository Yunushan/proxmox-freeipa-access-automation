from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
REQUIRED_COMMANDS = ("ansible-lint", "yamllint", "ansible-playbook")
PLAYBOOKS = (
    "playbooks/freeipa.yml",
    "playbooks/proxmox.yml",
    "playbooks/linux-clients.yml",
    "playbooks/site.yml",
    "playbooks/validate.yml",
)


def require_command(command: str) -> None:
    if shutil.which(command) is None:
        raise RuntimeError(f"{command} was not found in PATH.")


def run_command(command: list[str], env: dict[str, str]) -> None:
    print(f"Running: {' '.join(command)}")
    subprocess.run(command, check=True, cwd=ROOT_DIR, env=env)


def main() -> int:
    for command in REQUIRED_COMMANDS:
        require_command(command)

    ansible_dir = ROOT_DIR / ".ansible"
    ansible_dir.mkdir(exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="lint-inventory-", dir=ansible_dir) as temp_dir:
        lint_inventory_root = Path(temp_dir)
        lint_group_vars_dir = lint_inventory_root / "group_vars" / "all"
        lint_group_vars_dir.mkdir(parents=True, exist_ok=True)

        shutil.copy2(ROOT_DIR / "inventories" / "production" / "hosts.yml.example", lint_inventory_root / "hosts.yml")
        shutil.copy2(
            ROOT_DIR / "inventories" / "production" / "group_vars" / "all" / "main.yml",
            lint_group_vars_dir / "main.yml",
        )
        shutil.copy2(
            ROOT_DIR / "inventories" / "production" / "group_vars" / "all" / "vault.yml.example",
            lint_group_vars_dir / "vault.yml",
        )

        env = os.environ.copy()
        env["ANSIBLE_INVENTORY"] = str(lint_inventory_root / "hosts.yml")

        run_command(["ansible-lint"], env)
        run_command(["yamllint", "."], env)

        for playbook in PLAYBOOKS:
            run_command(["ansible-playbook", "--syntax-check", "-i", str(lint_inventory_root / "hosts.yml"), playbook], env)

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        raise SystemExit(exc.returncode) from exc
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1) from exc
