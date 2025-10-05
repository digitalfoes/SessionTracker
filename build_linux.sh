#!/usr/bin/env bash
set -euo pipefail

# Build standalone Linux bundle with PyInstaller (one-folder) and optionally AppImage
# Usage:
#   ./build_linux.sh            # build PyInstaller dist only
#   ./build_linux.sh appimage   # also build AppImage (requires appimagetool on PATH)

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

VENV_DIR=".venv-build"
PYTHON_BIN="python3"

# Create isolated venv for reproducible builds
if [ ! -d "$VENV_DIR" ]; then
  $PYTHON_BIN -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"
python -m pip install --upgrade pip wheel
python -m pip install -r requirements.txt pyinstaller

# Clean old builds
rm -rf build dist

# Build with spec (one-folder so relative icons/ paths work)
pyinstaller pyinstaller.spec

echo "PyInstaller build completed: dist/session-tracker/"

if [ "${1:-}" = "appimage" ]; then
  ./build_appimage.sh
fi
