# iipython-feishin-electron-bin

An AUR-style packaging repository for the **iiPythonx** Feishin builds, using the system-wide Electron runtime.

## Local build

```bash
git clone <this-repo-url>
cd iipython-feishin-electron-bin
makepkg -si
```

## Updating

A GitHub Actions workflow is included to keep `PKGBUILD` and `.SRCINFO` in sync with the latest release from
`iiPythonx/feishin`.

- The scheduled cron trigger runs weekly (see `.github/workflows/update-aur.yml`).
- If there is no new upstream release, the workflow exits quickly without rebuilding or creating releases.
- If the package is not yet present on AUR, the workflow will still push the current build there for publishing.
- The package installs `app.asar` and assets only to avoid bundling the upstream Electron runtime.

If you prefer to update locally, edit `PKGBUILD` and regenerate `.SRCINFO` (or run the update script manually).

```bash
python .github/scripts/update_pkgbuild.py
```
