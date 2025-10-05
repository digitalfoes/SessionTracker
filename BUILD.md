# Session Tracker - Build Instructions

This guide explains how to produce standalone builds for Linux (.AppImage) and Windows (.exe) from `session_tracker.py`.

Key files:
- `pyinstaller.spec` – PyInstaller configuration (one-folder build) bundling `icons/` and PyQt6 modules.
- `build_linux.sh` – Builds the PyInstaller one-folder bundle on Linux; optionally triggers AppImage build.
- `build_appimage.sh` – Wraps the PyInstaller bundle into an AppImage (requires `appimagetool`).
- `build_windows.bat` – Builds the PyInstaller one-folder bundle on Windows.
- `packaging/appimage/AppRun` – AppImage launcher.
- `packaging/appimage/session-tracker.desktop` – Desktop file metadata for AppImage.

The application loads icons via relative paths like `icons/play-circle.svg`, so the build is configured as a one-folder distribution (not onefile) to preserve the directory layout.

## Prerequisites

- Python 3.10+ recommended.
- Build dependencies are listed in `requirements.txt`.
- PyInstaller is installed by the scripts automatically.
- For AppImage:
  - `appimagetool` must be available on your PATH. See https://github.com/AppImage/AppImageKit/releases
  - On some distros you may need `libfuse2` (or `fuse2`) to run AppImages.
- For Windows builds, use a Windows host with Python and the Visual C++ runtime installed.

## Linux: Build PyInstaller bundle

From `sessiontracker/release-v1.2.0/`:

```bash
chmod +x build_linux.sh build_appimage.sh packaging/appimage/AppRun
./build_linux.sh
```

Outputs:
- `dist/session-tracker/` directory containing:
  - `session-tracker` executable
  - `icons/` directory
  - required Qt plugins and libraries

Run it locally:

```bash
./dist/session-tracker/session-tracker
```

## Linux: Build AppImage

After the PyInstaller build completes, run:

```bash
./build_linux.sh appimage
# or, if already built:
./build_appimage.sh
```

Outputs:
- `session-tracker-1.2.0-x86_64.AppImage` at the release root.

Notes:
- The AppImage bundles the PyInstaller directory as-is. `AppRun` `cd`s into the bundled directory so relative `icons/` paths work.
- If system tray/icon issues occur on Wayland, try `QT_QPA_PLATFORM=xcb`.

## Windows: Build .exe

### Option 1: Native Windows Build (Recommended)

On Windows, from `sessiontracker/release-v1.2.0/` in a Developer Command Prompt or PowerShell:

```bat
build_windows.bat
```

Outputs:
- `dist\session-tracker\session-tracker.exe`

Run it:

```bat
start dist\session-tracker\session-tracker.exe
```

### Option 2: Cross-Build on Linux with Wine (Advanced)

Building Windows executables on Linux requires:
1. Wine 6.0+ installed
2. Python 3.10+ for Windows installed in Wine
3. Visual C++ runtime in Wine

Steps:
```bash
# Install Wine (if not already installed)
sudo dpkg --add-architecture i386
sudo apt update
sudo apt install wine wine32 wine64

# Download Python for Windows
wget https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe

# Install Python in Wine
wine python-3.11.9-amd64.exe /quiet InstallAllUsers=1 PrependPath=1

# Build (from release-v1.2.0/)
wine python -m pip install -r requirements.txt pyinstaller
wine pyinstaller pyinstaller.spec

# Test with Wine
wine dist/session-tracker/session-tracker.exe
```

**Note**: Wine builds may have compatibility issues. For production, use native Windows builds.

## Packaging and Distribution Tips

- Distribute the entire `dist/session-tracker/` folder on each platform, or the `.AppImage` for Linux.
- For Windows code-signing, sign `session-tracker.exe` and relevant DLLs after build.
- For Linux AppImage signing, see `appimagetool --sign`.
- PyQt6 Multimedia may rely on system GStreamer for advanced formats. This app uses a simple WAV beep; it falls back to `QApplication.beep()` if unavailable.

## Troubleshooting

- Missing Qt plugins (e.g. `xcb`): Ensure the PyInstaller bundle includes `qt6_plugins/platforms`. PyInstaller’s PyQt6 hooks usually handle this automatically. If needed, add explicit datas in `pyinstaller.spec`.
- Charts not showing: ensure `PyQt6-Charts` is installed; the app degrades gracefully without charts.
- Icons not found: verify the `icons/` directory is present next to the executable in the final bundle.

## Customizing

- Change AppImage metadata in `packaging/appimage/session-tracker.desktop` and icon in `icons/`.
- Update version string in `build_appimage.sh` (variable `VERSION`) to match your release.
