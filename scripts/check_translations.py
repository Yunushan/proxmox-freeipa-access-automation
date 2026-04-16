from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
CANONICAL_README = ROOT_DIR / "README.md"
I18N_DIR = ROOT_DIR / "docs" / "i18n"
TRANSLATION_GLOB = "README.*.md"
HEADING_PATTERN = re.compile(r"^(##|###)\s+.+$", re.MULTILINE)
DEFAULT_MIN_NONEMPTY_LINE_RATIO = 0.60


@dataclass
class TranslationIssue:
    path: Path
    message: str


def extract_headings(path: Path) -> list[str]:
    return HEADING_PATTERN.findall(path.read_text(encoding="utf-8"))


def extract_heading_lines(path: Path) -> list[str]:
    return [
        line.rstrip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if re.match(r"^(##|###)\s+.+$", line)
    ]


def count_nonempty_lines(path: Path) -> int:
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())


def validate_translation(
    path: Path,
    canonical_headings: list[str],
    canonical_heading_lines: list[str],
    canonical_nonempty_lines: int,
    min_nonempty_line_ratio: float,
) -> list[TranslationIssue]:
    issues: list[TranslationIssue] = []
    text = path.read_text(encoding="utf-8")
    heading_levels = extract_headings(path)
    heading_lines = extract_heading_lines(path)
    nonempty_lines = count_nonempty_lines(path)
    nonempty_line_ratio = (
        nonempty_lines / canonical_nonempty_lines if canonical_nonempty_lines > 0 else 1.0
    )

    if "Translation scope: full" not in text:
        issues.append(
            TranslationIssue(path, "missing required metadata line: 'Translation scope: full'")
        )
    if "Canonical source: ../../README.md" not in text:
        issues.append(
            TranslationIssue(
                path,
                "missing required metadata line: 'Canonical source: ../../README.md'",
            )
        )
    if not re.search(r"^Last synced:\s+\d{4}-\d{2}-\d{2}$", text, re.MULTILINE):
        issues.append(
            TranslationIssue(path, "missing or malformed 'Last synced: YYYY-MM-DD' metadata")
        )

    if len(heading_levels) != len(canonical_headings):
        issues.append(
            TranslationIssue(
                path,
                f"heading count mismatch: {len(heading_levels)} found, expected {len(canonical_headings)}",
            )
        )

    if heading_levels != canonical_headings:
        issues.append(
            TranslationIssue(
                path,
                "heading level sequence does not match the canonical README",
            )
        )

    if nonempty_line_ratio < min_nonempty_line_ratio:
        issues.append(
            TranslationIssue(
                path,
                (
                    "content coverage appears too short: "
                    f"{nonempty_lines} non-empty lines vs {canonical_nonempty_lines} "
                    f"in canonical README ({nonempty_line_ratio:.0%}, minimum {min_nonempty_line_ratio:.0%})"
                ),
            )
        )

    if len(heading_lines) != len(canonical_heading_lines):
        return issues

    for index, (current, expected) in enumerate(zip(heading_lines, canonical_heading_lines), start=1):
        if current[:3] != expected[:3]:
            issues.append(
                TranslationIssue(
                    path,
                    f"heading {index} level mismatch: found '{current}', expected a heading matching '{expected}'",
                )
            )
            break

    return issues


def iter_translation_files() -> list[Path]:
    return sorted(
        path
        for path in I18N_DIR.glob(TRANSLATION_GLOB)
        if path.name != "README.template.md"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check translated README files for structural parity with the canonical English README."
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="exit with status 1 when any translation parity issue is found",
    )
    parser.add_argument(
        "--min-nonempty-line-ratio",
        type=float,
        default=DEFAULT_MIN_NONEMPTY_LINE_RATIO,
        help=(
            "minimum non-empty line ratio required compared with the canonical README "
            f"(default: {DEFAULT_MIN_NONEMPTY_LINE_RATIO:.2f})"
        ),
    )
    args = parser.parse_args()

    canonical_headings = extract_headings(CANONICAL_README)
    canonical_heading_lines = extract_heading_lines(CANONICAL_README)
    canonical_nonempty_lines = count_nonempty_lines(CANONICAL_README)
    issues: list[TranslationIssue] = []

    for path in iter_translation_files():
        file_issues = validate_translation(
            path,
            canonical_headings,
            canonical_heading_lines,
            canonical_nonempty_lines,
            args.min_nonempty_line_ratio,
        )
        if not file_issues:
            print(f"OK  {path.relative_to(ROOT_DIR)}")
            continue

        print(f"FAIL {path.relative_to(ROOT_DIR)}")
        for issue in file_issues:
            print(f"  - {issue.message}")
        issues.extend(file_issues)

    if issues and args.strict:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
