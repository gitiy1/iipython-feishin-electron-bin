# Feishin size optimization notes (exploration)

This document captures potential size-reduction approaches for the upstream `iiPythonx/feishin` project. The goal is to
identify changes that reduce the final packaged size without breaking functionality.

## Observations from upstream configs

- `electron-builder.yml` currently packages `out/**/*` and `package.json`, adds `assets/**` as extra resources, and
  unpacks `resources/**` from the asar bundle. This implies many assets and unpacked resources are shipped verbatim,
  which can dominate size. It also sets `npmRebuild: false`, so native modules are not rebuilt during packaging.
- `electron.vite.config.ts` enables sourcemaps for main/preload/renderer, which adds build artifacts even in release
  builds.
- The build targets include AppImage, deb, and tar.xz. Switching to deb can reduce download size but does not reduce
  the actual app payload if the same build outputs are packaged.

## Potential size-reduction strategies

### 1) Disable production sourcemaps

**Why**: sourcemaps can be large and are typically not required for production builds.

**Potential change**:
- Disable `sourcemap` for `main`, `preload`, and `renderer` in `electron.vite.config.ts` for release builds.

**Trade-off**: debugging production issues becomes harder.

### 2) Reduce `asarUnpack` scope

**Why**: `asarUnpack: ["resources/**"]` forces a large unpacked directory that expands install size.

**Potential change**:
- Limit `asarUnpack` to only what must be unpacked at runtime (e.g., native modules, binaries, or specific assets).
- Audit which files actually require unpacking; keep the rest inside `app.asar`.

**Trade-off**: any runtime code that expects direct filesystem access to unpacked files might break if the files are
moved back into the asar.

### 3) Audit and trim `extraResources`

**Why**: `extraResources: ["assets/**"]` ships all assets without filtering.

**Potential change**:
- Split assets into required runtime assets vs. build-time resources.
- Only ship runtime assets in `extraResources` (remove unused assets from packaging or move build-only assets out of
  the packaged path).

### 4) Aggressive tree-shaking in renderer build

**Why**: the renderer bundle size can be reduced if unused code is removed and dependencies are optimized.

**Potential change**:
- Enable stricter `build.rollupOptions.treeshake` and verify sideEffects flags in dependencies.
- Use dynamic imports to split large feature modules so they are not bundled in the initial chunk.
- Verify that UI libraries (e.g., Mantine, Radix) are imported per-component rather than via large barrel exports.

**Trade-off**: build complexity increases; dynamic imports may affect UX if not preloaded.

### 5) Evaluate optional/unused dependencies

**Why**: shipping libraries that are not used in production inflates bundle size.

**Potential change**:
- Audit dependencies for dev-only usage and move them to `devDependencies`.
- Replace heavy dependencies with lighter equivalents when possible.

### 6) Consider a “lite” build target

**Why**: allow users who want a smaller build to opt into a feature-reduced version.

**Potential change**:
- Introduce a build flag (e.g., `FEISHIN_LITE=1`) that disables optional features or heavy plugins at build time.

## Packaging-level notes for the AUR wrapper

- Our system-electron package already avoids bundling the upstream runtime. The remaining size is mostly from
  `app.asar` and assets, so upstream build optimizations are the most effective way forward.
- Changing from AppImage to deb mainly affects download and extraction format; the payload size is similar if the
  same build artifacts are packaged.

## Next steps if you want to proceed

1) Decide on a minimal, low-risk set of upstream changes (e.g., disabling sourcemaps + reducing asarUnpack scope).
2) Build and compare the output size vs. current release.
3) Validate runtime behavior and update packaging once upstream changes are published.
