from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
REQUIRED_COMMANDS = ("ansible-lint", "yamllint")
ANSIBLE_LINT_ENV_OVERRIDES = {
    "ANSIBLE_DEPRECATION_WARNINGS": "False",
}


def require_command(command: str) -> None:
    if shutil.which(command) is None:
        raise RuntimeError(f"{command} was not found in PATH.")


def run_command(
    command: list[str],
    env_overrides: dict[str, str] | None = None,
) -> None:
    print(f"Running: {' '.join(command)}")
    env = os.environ.copy()
    if env_overrides:
        env.update(env_overrides)

    python_warnings = env.get("PYTHONWARNINGS", "")
    deprecation_filter = "ignore::DeprecationWarning"
    env["PYTHONWARNINGS"] = (
        f"{deprecation_filter},{python_warnings}"
        if python_warnings
        else deprecation_filter
    )

    subprocess.run(command, check=True, cwd=ROOT_DIR, env=env)


def main() -> int:
    for command in REQUIRED_COMMANDS:
        require_command(command)

    run_command(["ansible-lint"], env_overrides=ANSIBLE_LINT_ENV_OVERRIDES)
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
