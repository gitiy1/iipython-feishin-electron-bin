#!/usr/bin/env python3
"""Apply size-optimization edits to the Feishin upstream source tree.

Usage:
  python tools/feishin_optimize.py /path/to/feishin
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REACT_ICON_IMPORT_RE = re.compile(
    r"^import\s*{\s*(?P<names>[^}]+)\s*}\s*from\s*['\"](?P<module>react-icons/(?P<pack>[^'\"]+))['\"];?\s*$",
    re.MULTILINE,
)


def update_electron_builder(path: Path) -> bool:
    content = path.read_text(encoding="utf-8")
    original = content
    content = content.replace(
        "asarUnpack:\n    - resources/**\n",
        "asarUnpack:\n    - resources/**/*.node\n    - resources/**/*.dll\n    - resources/**/*.so\n    - resources/**/*.dylib\n",
    )
    if "# consider dropping AppImage" not in content:
        content = content.replace(
            "- tar.xz\n",
            "- tar.xz\n    # consider dropping AppImage when size is a priority\n",
        )
    if content != original:
        path.write_text(content, encoding="utf-8")
        return True
    return False


def update_electron_vite(path: Path) -> bool:
    content = path.read_text(encoding="utf-8")
    original = content
    content = re.sub(r"sourcemap: true", "sourcemap: false", content)
    if "rollupOptions:" not in content:
        content = content.replace(
            "minify: 'esbuild',\n",
            "minify: 'esbuild',\n            rollupOptions: {\n                treeshake: true,\n            },\n",
        )
    if content != original:
        path.write_text(content, encoding="utf-8")
        return True
    return False


def update_remote_vite(path: Path) -> bool:
    content = path.read_text(encoding="utf-8")
    original = content
    content = re.sub(r"sourcemap: true", "sourcemap: false", content)
    if content != original:
        path.write_text(content, encoding="utf-8")
        return True
    return False


def _resolve_react_icons_version(data: dict) -> str | None:
    for section in ("dependencies", "devDependencies"):
        deps = data.get(section, {})
        if "react-icons" in deps:
            return deps["react-icons"]
    return None


def update_package_json(path: Path) -> bool:
    data = json.loads(path.read_text(encoding="utf-8"))
    deps = data.get("dependencies", {})
    if "@react-icons/all-files" not in deps:
        react_icons_version = _resolve_react_icons_version(data)
        if react_icons_version:
            deps["@react-icons/all-files"] = react_icons_version
            data["dependencies"] = deps
            path.write_text(json.dumps(data, indent=4, sort_keys=True) + "\n", encoding="utf-8")
            return True
    return False


def update_react_icon_imports(root: Path) -> int:
    count = 0
    for path in root.rglob("*.ts"):
        count += _update_react_icon_file(path)
    for path in root.rglob("*.tsx"):
        count += _update_react_icon_file(path)
    return count


def _rewrite_react_icon_imports(content: str) -> str:
    def replacer(match: re.Match[str]) -> str:
        pack = match.group("pack")
        names = match.group("names")
        imports = []
        for entry in names.split(","):
            entry = entry.strip()
            if not entry:
                continue
            if " as " in entry:
                original, alias = [part.strip() for part in entry.split(" as ", 1)]
                local = alias
            else:
                original = entry
                local = entry
            imports.append(
                f"import {local} from \"@react-icons/all-files/{pack}/{original}\";"
            )
        return "\n".join(imports)

    updated = REACT_ICON_IMPORT_RE.sub(replacer, content)
    return updated


def _update_react_icon_file(path: Path) -> int:
    content = path.read_text(encoding="utf-8")
    updated = _rewrite_react_icon_imports(content)
    if updated != content:
        path.write_text(content, encoding="utf-8")
        return 1
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, help="Path to the Feishin source root")
    args = parser.parse_args()

    root = args.source
    builder_changed = update_electron_builder(root / "electron-builder.yml")
    vite_changed = update_electron_vite(root / "electron.vite.config.ts")
    remote_changed = update_remote_vite(root / "remote.vite.config.ts")
    pkg_changed = update_package_json(root / "package.json")
    icon_files_changed = update_react_icon_imports(root)

    print("electron-builder.yml updated:", builder_changed)
    print("electron.vite.config.ts updated:", vite_changed)
    print("remote.vite.config.ts updated:", remote_changed)
    print("package.json updated:", pkg_changed)
    print("react-icons files updated:", icon_files_changed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
