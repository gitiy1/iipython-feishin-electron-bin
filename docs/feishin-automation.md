# Feishin size optimization automation

This guide shows how to apply the size-optimization edits using a script instead of patch files.

## Script

`tools/feishin_optimize.py` updates the upstream source tree to:

- disable production sourcemaps
- disable remote build sourcemaps (remote.vite.config.ts)
- narrow `asarUnpack` patterns
- enable renderer tree-shaking
- add `@react-icons/all-files`
- rewrite known `react-icons/*` imports to `@react-icons/all-files/*`

## Usage

```bash
python /path/to/iipython-feishin-electron-bin/tools/feishin_optimize.py /path/to/feishin
```

## Follow-up

After running the script, rebuild as usual:

```bash
pnpm install
pnpm run build
```

Then compare output sizes to the baseline build.

## Notes

- The React Icons rewrite targets known import locations. If upstream adds new icon imports, re-run the script and
  extend `REACT_ICON_FILES`/`REACT_ICON_MAP` as needed.
