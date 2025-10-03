# Session Tracker v1.2.0 - Release Notes

**Release Date**: October 3, 2025
**Version**: 1.2.0
**Author**: David Foucher

---

## What's New in v1.2.0

### 🎯 Major Features

#### Countdown Timer System
The headline feature of this release is a fully-featured countdown timer system:

- **Customizable Duration**: Set session timers with hours, minutes, and seconds precision
- **Millisecond Accuracy**: Live countdown display showing HH:MM:SS.mmm format
- **Visual Display**: Centered countdown with clean black background and white text
- **Smooth Updates**: 50ms refresh rate for seamless countdown experience

#### Enhanced Alerts
- **Sound Notifications**: WAV audio playback when timer expires
- **Visual Alerts**: Pop-up dialog on countdown completion
- **System Tray Notifications**: Unobtrusive notifications in system tray
- **Fallback Support**: System beep if sound files unavailable

#### Smart Session Management
- **Auto-Stop**: Sessions automatically end when timer reaches zero
- **Pause Integration**: Timer properly pauses when session is paused
- **Accuracy**: Microsecond-level time calculations for precise tracking

### 🔧 Improvements

- Timer configuration disables during active sessions to prevent changes
- Enhanced timer state validation and error handling
- Improved countdown visibility management
- Better integration with existing session tracking features

### 📦 Package Contents

This release package includes:

```
release-v1.2.0/
├── session_tracker.py       # Main application (v1.2.0)
├── icons/                    # All required SVG icons
│   ├── bar-chart.svg
│   ├── chevron-down.svg
│   ├── chevron-right.svg
│   ├── list.svg
│   ├── pie-chart.svg
│   ├── play-circle.svg
│   ├── stop-circle.svg
│   └── trash.svg
├── README.md                 # Complete documentation
├── INSTALL.md                # Detailed installation guide
├── CHANGELOG.md              # Full version history
├── LICENSE                   # MIT License
├── requirements.txt          # Python dependencies
└── RELEASE_NOTES.md          # This file
```

---

## Installation Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Install & Run
```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python session_tracker.py
```

For detailed installation instructions, see [INSTALL.md](INSTALL.md).

---

## Quick Feature Guide

### Using the Countdown Timer

1. **Enable Timer**:
   - Check "Session Timer (Optional)" checkbox
   - Set hours, minutes, and seconds

2. **Start Session**:
   - Fill in activity name
   - Click "Start Session"
   - Countdown begins automatically

3. **Monitor Progress**:
   - Large countdown display shows remaining time
   - Header shows negative countdown format
   - Updates in real-time with milliseconds

4. **Timer Expiration**:
   - Sound alert plays (3 times)
   - Visual dialog appears
   - System tray notification shown
   - Session automatically stops

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Shift+S` | Start Session |
| `Ctrl+Shift+T` | Stop Session |
| `Ctrl+Shift+P` | Pause/Resume |
| `Ctrl+Shift+E` | Export Data |

---

## System Requirements

### Minimum
- Python 3.8+
- 256 MB RAM
- 50 MB disk space
- 1024x768 display

### Recommended
- Python 3.10+
- 512 MB RAM
- 100 MB disk space
- 1920x1080 display

### Dependencies
- **PyQt6** (required) - GUI framework
- **PyQt6-Multimedia** (required) - Sound support
- **reportlab** (required) - PDF generation
- **PyQt6-Charts** (optional) - Charts functionality

---

## Upgrade Notes

### From v1.1.0

This is a feature update - no breaking changes. Your existing session data will continue to work.

**New Features Available**:
- Countdown timer with millisecond precision
- Sound alerts on timer expiration
- Auto-stop session capability

**Data Compatibility**: 100% backward compatible

### From v1.0.0

All v1.1.0 features remain available:
- Calendar view
- PDF reports
- Keyboard shortcuts
- System tray integration

Plus new v1.2.0 timer features.

---

## Known Issues & Limitations

### Known Issues
- None at this time

### Limitations
- Sound alerts require system sound files (WAV format)
- Charts require PyQt6-Charts package (optional dependency)
- PDF reports use letter page size only
- Maximum timer duration: 23 hours, 59 minutes, 59 seconds

### Platform-Specific Notes

**Linux**:
- Sound files typically in `/usr/share/sounds/`
- May need `sound-theme-freedesktop` package

**Windows**:
- Falls back to system beep if WAV not found
- All features fully supported

**macOS**:
- Full feature support
- Sound alerts work with system sounds

---

## Testing Checklist

Verify these features after installation:

- [ ] Application launches without errors
- [ ] Can start/stop/pause sessions
- [ ] Timer countdown displays correctly
- [ ] Sound alert plays on timer expiration
- [ ] Session auto-stops when timer expires
- [ ] Calendar view loads
- [ ] PDF reports generate
- [ ] Charts display (if PyQt6-Charts installed)
- [ ] CSV export/import works
- [ ] System tray icon appears

---

## Documentation

- **README.md** - Complete feature documentation
- **INSTALL.md** - Platform-specific installation guides
- **CHANGELOG.md** - Detailed version history
- **LICENSE** - MIT License terms

---

## Support & Feedback

### Getting Help
1. Read the [README.md](README.md) for feature documentation
2. Check [INSTALL.md](INSTALL.md) for installation issues
3. Review [CHANGELOG.md](CHANGELOG.md) for version history

### Reporting Issues
When reporting bugs, please include:
- Operating system and version
- Python version (`python --version`)
- Complete error message
- Steps to reproduce

### Contributing
Contributions welcome! Feel free to:
- Submit bug reports
- Suggest new features
- Submit pull requests
- Improve documentation

---

## Credits

**Developer**: David Foucher
**Framework**: PyQt6
**License**: MIT

---

## What's Next?

Future versions may include:
- Custom sound file selection
- Multiple timer presets
- Timer history and analytics
- Export timer statistics
- Custom alert messages
- Dark theme support

---

**Thank you for using Session Tracker!**

For the complete changelog, see [CHANGELOG.md](CHANGELOG.md)

---

Session Tracker v1.2.0 - Professional Session Tracking with Advanced Timer Features
