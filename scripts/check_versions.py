from __future__ import annotations

import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

VERSION_FILE = ROOT / "src" / "user_registration" / "_version.py"

PACKAGE_FILES = [
    ROOT / "pyproject.toml",
    ROOT / "adapters" / "fastapi" / "pyproject.toml",
    ROOT / "adapters" / "sqlalchemy" / "pyproject.toml",
]


VERSION_PATTERN = re.compile(
    r'^__version__\s*=\s*["\']([^"\']+)["\']',
    re.MULTILINE,
)


def get_source_version() -> str:
    content = VERSION_FILE.read_text(encoding="utf-8")

    match = VERSION_PATTERN.search(content)

    if match is None:
        raise RuntimeError(f"Could not find __version__ in {VERSION_FILE}")

    return match.group(1)


def get_project_metadata(
    path: Path,
) -> tuple[str, str | None, bool]:
    with path.open("rb") as file:
        data = tomllib.load(file)

    project = data["project"]

    name = project["name"]

    dynamic = project.get("dynamic", [])

    if "version" in dynamic:
        return name, None, True

    version = project.get("version")

    if version is None:
        raise RuntimeError(f"{path}: project version is neither static nor dynamic")

    return name, version, False


def main() -> None:
    source_version = get_source_version()

    print(f"Source version: {source_version}")
    print()

    for package_file in PACKAGE_FILES:
        name, version, is_dynamic = get_project_metadata(package_file)

        if is_dynamic:
            print(f"{name}: dynamic ({source_version})")
            continue

        print(f"{name}: {version}")

        if version != source_version:
            raise SystemExit(
                f"Version mismatch: {name} has {version}, "
                f"but source version is {source_version}"
            )

    print()
    print("All package versions are synchronized.")


if __name__ == "__main__":
    main()
