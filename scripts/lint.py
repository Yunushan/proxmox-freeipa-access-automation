from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
REQUIRED_COMMANDS = ("ansible-lint", "yamllint")


def require_command(command: str) -> None:
    if shutil.which(command) is None:
        raise RuntimeError(f"{command} was not found in PATH.")


def run_command(command: list[str]) -> None:
    print(f"Running: {' '.join(command)}")
    subprocess.run(command, check=True, cwd=ROOT_DIR)


def main() -> int:
    for command in REQUIRED_COMMANDS:
        require_command(command)

    run_command(["ansible-lint"])
    run_command(["yamllint", "."])
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        raise SystemExit(exc.returncode) from exc
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1) from exc
