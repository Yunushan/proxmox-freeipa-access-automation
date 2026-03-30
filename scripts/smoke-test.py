from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
REQUIRED_COMMANDS = ("ansible-inventory", "ansible-playbook")
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


def prepare_example_inventory() -> tuple[Path, dict[str, str], tempfile.TemporaryDirectory]:
    ansible_dir = ROOT_DIR / ".ansible"
    ansible_dir.mkdir(exist_ok=True)

    temp_dir = tempfile.TemporaryDirectory(prefix="smoke-inventory-", dir=ansible_dir)
    smoke_inventory_root = Path(temp_dir.name)
    smoke_group_vars_dir = smoke_inventory_root / "group_vars" / "all"
    source_group_vars_dir = ROOT_DIR / "inventories" / "production" / "group_vars" / "all"

    shutil.copy2(
        ROOT_DIR / "inventories" / "production" / "hosts.yml.example",
        smoke_inventory_root / "hosts.yml",
    )
    shutil.copytree(source_group_vars_dir, smoke_group_vars_dir, dirs_exist_ok=True)
    for vault_example in smoke_group_vars_dir.glob("vault*.yml.example"):
        shutil.copy2(vault_example, vault_example.with_suffix(""))

    env = os.environ.copy()
    env["ANSIBLE_INVENTORY"] = str(smoke_inventory_root / "hosts.yml")
    return smoke_inventory_root / "hosts.yml", env, temp_dir


def main() -> int:
    for command in REQUIRED_COMMANDS:
        require_command(command)

    inventory_file, env, temp_dir = prepare_example_inventory()
    try:
        run_command(["ansible-inventory", "--list", "-i", str(inventory_file)], env)
        for playbook in PLAYBOOKS:
            run_command(
                ["ansible-playbook", "--syntax-check", "-i", str(inventory_file), playbook],
                env,
            )
    finally:
        temp_dir.cleanup()

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        raise SystemExit(exc.returncode) from exc
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1) from exc
