# Feishin React Icons + Mantine size optimization notes

## React Icons (largest win)

The bundle includes many full icon packs. To reduce size, migrate to
`@react-icons/all-files` and import icons directly by path.

### Example replacements

```ts
// Before
import { RiCloseLine } from 'react-icons/ri';

// After
import { RiCloseLine } from '@react-icons/all-files/ri/RiCloseLine';
```

### Known import locations in `pizza` branch

- `src/renderer/features/sidebar/components/sidebar-icon.tsx` (react-icons/ri)
- `src/renderer/features/window-controls/components/window-controls.tsx` (react-icons/ri)
- `src/renderer/layouts/window-bar.tsx` (react-icons/ri)
- `src/remote/components/remote-container.tsx` (react-icons/ri)
- `src/remote/components/buttons/image-button.tsx` (react-icons/ci)
- `src/remote/components/buttons/reconnect-button.tsx` (react-icons/ri)
- `src/shared/components/icon/icon.tsx` (react-icons/fa, lu, md, pi, ri, si)
- `src/shared/components/spinner/spinner.tsx` (react-icons/cg)

### Suggested dependency change

```json
"dependencies": {
  "@react-icons/all-files": "^4.1.0"
}
```

Then remove `react-icons` or keep it temporarily during migration.

## Mantine (medium win)

Mantine is used broadly. The best improvements come from:

- Ensuring no wildcard imports (avoid `import * as Mantine ...`).
- Auditing usage of heavier components (modals, date pickers, notifications).
- Consider replacing a few heavy components with lighter equivalents if you can accept visual changes.

## Next steps

1. Convert React Icons imports to `@react-icons/all-files` in the files listed above.
2. Build and compare `app.asar` size and `node_modules/react-icons` footprint.
3. Evaluate Mantine components for replacement if further savings are needed.
