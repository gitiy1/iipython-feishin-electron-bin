# pear-desktop-electron-bin (local build)

This folder contains a local PKGBUILD that repackages the Pear Desktop (YouTube Music) Linux build to run with
system-wide Electron. It is intended for **local builds only** (no AUR sync in this branch).

## Build

```bash
cd pear-desktop-electron
makepkg -si
```

## Notes

- The package uses the upstream `youtube-music_*.deb` release and repacks `app.asar` to point to `/usr/lib` so the
  system Electron runtime can load resources correctly.
- Electron major version is derived from the upstream binary (currently Electron 38).
