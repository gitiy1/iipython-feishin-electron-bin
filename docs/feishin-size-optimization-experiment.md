# Feishin size-optimization experiment (patches + build steps)

## Goal

Apply three upstream changes:

- Disable production sourcemaps.
- Reduce `asarUnpack` scope.
- Enable aggressive renderer tree-shaking.

## Patches

- `patches/feishin-size-optimizations.patch` (adjusts `electron-builder.yml` asarUnpack scope).
- `patches/feishin-vite-sourcemap-treeshake.patch` (disables sourcemaps and enables renderer tree-shaking).

## Local build instructions

```bash
git clone https://github.com/iiPythonx/feishin
cd feishin

# apply patches

git apply /path/to/patches/feishin-size-optimizations.patch

git apply /path/to/patches/feishin-vite-sourcemap-treeshake.patch

# install + build

corepack enable
pnpm install
pnpm run build

# compare output size

du -sh out
```

## Notes

- Tree-shaking and reduced `asarUnpack` scope can break runtime behavior if native modules or asset paths are
  incorrectly packed. Verify app startup and core flows after building.
- Sourcemaps disabled will reduce output size but make post-release debugging harder.

## Status

Attempted to fetch the upstream source archive in this environment to run the build comparison, but the download was
blocked by policy. Use the steps above to run the experiment locally where network and build tooling are available.
