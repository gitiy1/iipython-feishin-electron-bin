# Build artifact size analysis guide

This guide shows how to analyze build outputs (e.g., AppImage/DEB/TAR) to find the largest files/directories after
unpacking. It is intended for local use on your build machine.

## 1) Unpack artifacts

### AppImage

```bash
./Feishin-linux-x86_64.AppImage --appimage-extract
mv squashfs-root appimage-root
```

### DEB

```bash
mkdir -p deb-root
ar x Feishin-linux-amd64.deb
bsdtar -xf data.tar.xz -C deb-root
```

### tar.xz

```bash
mkdir -p tar-root
bsdtar -xf Feishin-linux-x64.tar.xz -C tar-root
```

## 2) Find top-level size offenders

```bash
# top-level sizes
sudo du -h --max-depth=2 appimage-root | sort -h | tail -n 20
sudo du -h --max-depth=2 deb-root | sort -h | tail -n 20
sudo du -h --max-depth=2 tar-root | sort -h | tail -n 20
```

## 3) Drill into app.asar (optional)

```bash
# unpack and inspect app.asar
npx asar extract appimage-root/resources/app.asar app.asar.unpacked
sudo du -h --max-depth=2 app.asar.unpacked | sort -h | tail -n 30

# find top 50 largest files
find app.asar.unpacked -type f -printf '%s\t%p\n' | sort -n | tail -n 50 | numfmt --to=iec --field=1
```

## 4) Compare outputs between builds

```bash
# record size snapshots
sudo du -h --max-depth=2 appimage-root | sort -h > appimage-sizes.txt
sudo du -h --max-depth=2 deb-root | sort -h > deb-sizes.txt

# diff snapshots
diff -u appimage-sizes.txt deb-sizes.txt | less
```

## Notes

- Use the same extraction steps for each build to compare apples to apples.
- If `app.asar.unpacked/node_modules` dominates size, focus on dependency trimming or renderer bundle optimization.
- If `resources/assets` dominates size, consider asset reduction or selective packaging.
