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

REACT_ICON_MAP = {
    "react-icons/ri": "@react-icons/all-files/ri",
    "react-icons/ci": "@react-icons/all-files/ci",
    "react-icons/fa": "@react-icons/all-files/fa",
    "react-icons/lu": "@react-icons/all-files/lu",
    "react-icons/md": "@react-icons/all-files/md",
    "react-icons/pi": "@react-icons/all-files/pi",
    "react-icons/si": "@react-icons/all-files/si",
    "react-icons/cg": "@react-icons/all-files/cg",
}

REACT_ICON_FILES = [
    "src/renderer/features/sidebar/components/sidebar-icon.tsx",
    "src/renderer/features/window-controls/components/window-controls.tsx",
    "src/renderer/layouts/window-bar.tsx",
    "src/remote/components/remote-container.tsx",
    "src/remote/components/buttons/image-button.tsx",
    "src/remote/components/buttons/reconnect-button.tsx",
    "src/shared/components/icon/icon.tsx",
    "src/shared/components/spinner/spinner.tsx",
]


def update_electron_builder(path: Path) -> bool:
    content = path.read_text(encoding="utf-8")
    original = content
    content = content.replace("asarUnpack:\n    - resources/**\n", "asarUnpack:\n    - resources/**/*.node\n    - resources/**/*.dll\n    - resources/**/*.so\n    - resources/**/*.dylib\n")
    if "# consider dropping AppImage" not in content:
        content = content.replace("- tar.xz\n", "- tar.xz\n    # consider dropping AppImage when size is a priority\n")
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
            "minify: 'esbuild',\n", "minify: 'esbuild',\n            rollupOptions: {\n                treeshake: true,\n            },\n"
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


def update_package_json(path: Path) -> bool:
    data = json.loads(path.read_text(encoding="utf-8"))
    deps = data.get("dependencies", {})
    if "@react-icons/all-files" not in deps:
        deps["@react-icons/all-files"] = "^4.1.0"
        data["dependencies"] = deps
        path.write_text(json.dumps(data, indent=4, sort_keys=True) + "\n", encoding="utf-8")
        return True
    return False


def update_react_icon_imports(root: Path) -> bool:
    changed = False
    for relpath in REACT_ICON_FILES:
        file_path = root / relpath
        if not file_path.exists():
            continue
        content = file_path.read_text(encoding="utf-8")
        original = content
        for old, new in REACT_ICON_MAP.items():
            content = content.replace(old, new)
        if content != original:
            file_path.write_text(content, encoding="utf-8")
            changed = True
    return changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, help="Path to the Feishin source root")
    args = parser.parse_args()

    root = args.source
    builder_changed = update_electron_builder(root / "electron-builder.yml")
    vite_changed = update_electron_vite(root / "electron.vite.config.ts")
    remote_changed = update_remote_vite(root / "remote.vite.config.ts")
    pkg_changed = update_package_json(root / "package.json")
    icons_changed = update_react_icon_imports(root)

    print("electron-builder.yml updated:", builder_changed)
    print("electron.vite.config.ts updated:", vite_changed)
    print("remote.vite.config.ts updated:", remote_changed)
    print("package.json updated:", pkg_changed)
    print("react-icons imports updated:", icons_changed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
