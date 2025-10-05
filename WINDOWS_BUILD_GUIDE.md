# Windows Build Guide

This guide covers building the Windows `.exe` for Session Tracker.

## Quick Start (Windows Host)

1. Copy the `release-v1.2.0` folder to your Windows machine
2. Open Command Prompt or PowerShell
3. Navigate to the folder:
   ```cmd
   cd path\to\release-v1.2.0
   ```
4. Run the build script:
   ```cmd
   build_windows.bat
   ```
5. Find your executable:
   ```
   dist\session-tracker\session-tracker.exe
   ```

## Build Output

The build creates a one-folder distribution in `dist\session-tracker\`:
- `session-tracker.exe` - Main executable
- `icons\` - Application icons (SVG files)
- `_internal\` - Python runtime, Qt libraries, and dependencies

**Important**: Distribute the entire `dist\session-tracker\` folder, not just the `.exe` file.

## Testing on Linux with Wine

If you have Wine installed, you can test the Windows build on Linux:

```bash
# Test the executable
wine dist/session-tracker/session-tracker.exe

# Or with Qt platform override if needed
WINEDLLOVERRIDES="mscoree,mshtml=" wine dist/session-tracker/session-tracker.exe
```

## Cross-Building from Linux (Advanced)

While possible, cross-building Windows executables on Linux using Wine is complex and not recommended for production. The process requires:

1. **Install Wine and dependencies**:
   ```bash
   sudo dpkg --add-architecture i386
   sudo apt update
   sudo apt install wine wine32 wine64 winetricks
   ```

2. **Install Python for Windows in Wine**:
   ```bash
   # Download Python installer
   wget https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe
   
   # Install in Wine
   wine python-3.11.9-amd64.exe /quiet InstallAllUsers=1 PrependPath=1
   ```

3. **Build the executable**:
   ```bash
   # Install dependencies
   wine python -m pip install -r requirements.txt pyinstaller
   
   # Run PyInstaller
   wine pyinstaller pyinstaller.spec
   ```

4. **Test**:
   ```bash
   wine dist/session-tracker/session-tracker.exe
   ```

### Known Issues with Wine Builds

- Qt platform plugins may not work correctly
- System tray functionality may be limited
- File dialogs may behave differently
- Performance may be slower than native builds

**Recommendation**: Always use native Windows for production builds.

## Distribution Checklist

- [ ] Build on native Windows (or test Wine build thoroughly)
- [ ] Test the executable on a clean Windows machine
- [ ] Verify all icons load correctly
- [ ] Test system tray functionality
- [ ] Test PDF report generation
- [ ] Test data import/export
- [ ] Consider code signing for Windows SmartScreen
- [ ] Create installer (optional, using NSIS or Inno Setup)
- [ ] Test on Windows 10 and Windows 11

## Code Signing (Optional)

To avoid Windows SmartScreen warnings:

1. Obtain a code signing certificate
2. Sign the executable:
   ```cmd
   signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com dist\session-tracker\session-tracker.exe
   ```

## Creating an Installer (Optional)

You can create a proper Windows installer using:

- **NSIS** (Nullsoft Scriptable Install System)
- **Inno Setup**
- **WiX Toolset**

This provides:
- Start menu shortcuts
- Desktop shortcuts
- Uninstaller
- File associations
- Better user experience

## Troubleshooting

### "Python was not found" error
- Ensure Python 3.10+ is installed
- Verify Python is in your PATH
- Try running `py -3` instead of `python`

### PyInstaller fails
- Update pip: `python -m pip install --upgrade pip`
- Install build tools: `pip install --upgrade setuptools wheel`
- Clear build cache: `rmdir /s /q build dist`

### Missing DLLs
- Install Visual C++ Redistributable
- Ensure all dependencies in requirements.txt are installed

### Icons not showing
- Verify `icons/` folder is in `dist/session-tracker/`
- Check file paths are relative in the code
