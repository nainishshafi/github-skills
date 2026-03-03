#!/usr/bin/env python3
"""
find-readmes.py

Locates all README files and SKILL.md files in the current repository and
prepares a timestamped output file path for the scan-repo-readme skill.

Output (stdout):
  Line 1:  Output file path  (e.g. .scan-readme-results/readme-scan-20240315-143022.md)
  Line 2+: Absolute path of each README or SKILL.md file found, one per line

Usage:
  .venv/Scripts/python .github/skills/scan-repo-readme/scripts/find-readmes.py   # Windows
  .venv/bin/python     .github/skills/scan-repo-readme/scripts/find-readmes.py   # Unix
  python3              .github/skills/scan-repo-readme/scripts/find-readmes.py   # fallback
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# README filenames to match (case-sensitive check first, then case-insensitive fallback)
README_NAMES = {
    "readme.md",
    "readme.rst",
    "readme.txt",
    "readme.adoc",
    "readme.org",
    "readme",
}

# Directories to skip entirely
SKIP_DIRS = {
    ".git",
    ".github",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    ".env",
    "dist",
    "build",
    ".next",
    ".nuxt",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    "coverage",
    ".coverage",
}

OUTPUT_DIR = ".scan-readme-results"


def resolve_python() -> str:
    """Return the best available Python interpreter path."""
    candidates = [
        Path(".venv") / "Scripts" / "python",  # Windows venv
        Path(".venv") / "bin" / "python",  # Unix venv
    ]
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)
    return "python3"


def find_readmes(root: Path, root_only: bool = False) -> list[Path]:
    """Return README files.

    If `root_only` is True, include only the repository root README and
    README files located directly under immediate child directories.
    Otherwise walk the repo recursively (skipping SKIP_DIRS).
    """
    found: list[Path] = []
    if root_only:
        # repo root
        for name in README_NAMES:
            p = root / name
            if p.exists():
                found.append(p)
                break
        # immediate children (one level deep)
        for child in root.iterdir():
            if not child.is_dir():
                continue
            if child.name.startswith('.') or child.name in SKIP_DIRS:
                continue
            for name in README_NAMES:
                p = child / name
                if p.exists():
                    found.append(p)
                    break
        return sorted(found)

    for dirpath, dirnames, filenames in os.walk(root):
        # Prune directories in-place to skip noise
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fname in filenames:
            if fname.lower() in README_NAMES:
                found.append(Path(dirpath) / fname)
    return sorted(found)


def find_skills(root: Path) -> list[Path]:
    """Find all SKILL.md files under .github/skills/."""
    skills_dir = root / ".github" / "skills"
    if not skills_dir.is_dir():
        return []
    # Recurse to find SKILL.md in nested skill folders
    return sorted(skills_dir.rglob("SKILL.md"))


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Find README and SKILL.md files for scan-repo-readme skill")
    parser.add_argument("--root-only", action="store_true", help="Limit results to repo root + immediate child directories")
    parser.add_argument("--include-skills", action="store_true", help="Also print .github/skills SKILL.md files (off by default)")
    args = parser.parse_args()

    root = Path.cwd()

    # Create output directory and build timestamped output path
    output_dir = root / OUTPUT_DIR
    output_dir.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_path = output_dir / f"readme-scan-{ts}.md"

    # Print output path as line 1
    print(output_path)

    # Find and print README file paths
    readmes = find_readmes(root, root_only=args.root_only)
    for readme in readmes:
        print(readme)

    # Optionally print SKILL.md file paths (recursive under .github/skills)
    skills: list[Path] = []
    if args.include_skills:
        skills = find_skills(root)
        for skill in skills:
            print(skill)

    if not readmes and not skills:
        # Print a warning to stderr so it doesn't pollute the stdout protocol
        print("Warning: No README or SKILL.md files found in the repository.", file=sys.stderr)


if __name__ == "__main__":
    main()
