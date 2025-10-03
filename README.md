# Session Tracker v1.2.0

A professional PyQt6 desktop application for tracking work sessions with advanced features including timer countdowns, statistics, charts, and reporting.

![Version](https://img.shields.io/badge/version-1.2.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![PyQt6](https://img.shields.io/badge/PyQt6-6.0+-orange)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

## Features

### Core Functionality
- **Session Tracking**: Start, pause, resume, and stop work sessions
- **Activity Logging**: Track activity names and detailed notes for each session
- **Real-time Timer**: Live session duration display with millisecond precision
- **System Tray Integration**: Minimize to tray with quick access controls

### Timer System
- **Customizable Countdown Timer**: Set session duration (hours, minutes, seconds)
- **Millisecond Precision**: Accurate countdown display (HH:MM:SS.mmm)
- **Visual Alerts**: On-screen notifications when timer expires
- **Sound Alerts**: Audio notification on countdown completion
- **Auto-stop**: Automatically stops session when timer reaches zero

### Data Management
- **Persistent Storage**: JSON-based data storage in user home directory
- **Session History**: View all past sessions in searchable table
- **Multi-line Notes**: Support for detailed session notes with custom delegate
- **CSV Import/Export**: Easy data portability
- **Backup System**: Automatic backup before data operations

### Analytics & Reporting
- **Statistics Dashboard**: Total sessions, active time, average duration
- **Calendar View**: Color-coded calendar showing session days
- **Interactive Charts**: Pie charts and bar charts for visual analysis (requires PyQt6-Charts)
- **PDF Reports**: Generate weekly and monthly session reports
- **Search & Filter**: Quick search across session IDs, activities, and notes

### User Interface
- **Tabbed Interface**: Organized views for Sessions, Statistics, Calendar, and Charts
- **Keyboard Shortcuts**:
  - `Ctrl+Shift+S`: Start session
  - `Ctrl+Shift+T`: Stop session
  - `Ctrl+Shift+P`: Pause/Resume
  - `Ctrl+Shift+E`: Export data
- **Session Management**: Edit and delete session entries
- **Responsive Design**: Clean, professional interface

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Required Dependencies
Install all dependencies using:
```bash
pip install -r requirements.txt
```

**Core Requirements:**
- PyQt6
- PyQt6-Charts (optional, for charts functionality)
- PyQt6-Multimedia (for sound alerts)
- reportlab (for PDF generation)

### Manual Installation
```bash
# Install PyQt6
pip install PyQt6

# Install PyQt6-Charts (optional)
pip install PyQt6-Charts

# Install PyQt6-Multimedia
pip install PyQt6-Multimedia

# Install ReportLab
pip install reportlab
```

## Usage

### Running the Application
```bash
python session_tracker.py
```

Or make it executable:
```bash
chmod +x session_tracker.py
./session_tracker.py
```

### Quick Start Guide

1. **Start a Session**:
   - Enter an activity name (e.g., "Development", "Meeting")
   - Optionally add notes
   - Click "Start Session" or press `Ctrl+Shift+S`

2. **Use Timer (Optional)**:
   - Check "Session Timer (Optional)" box
   - Set desired duration (hours, minutes, seconds)
   - Timer will countdown and alert when finished

3. **Pause/Resume**:
   - Click "Pause" or press `Ctrl+Shift+P` during active session
   - Click "Resume" to continue

4. **Stop Session**:
   - Click "Stop Session" or press `Ctrl+Shift+T`
   - Session is saved automatically

5. **View History**:
   - Browse all sessions in the Sessions tab
   - Search by ID, activity, or notes
   - Edit or delete entries as needed

6. **Generate Reports**:
   - Go to File → Generate Report
   - Choose Weekly or Monthly report
   - PDF will be generated with session summary

## Data Storage

Session data is stored in JSON format at:
```
~/.session_tracker/sessions.json
```

Backups are automatically created before import operations:
```
~/.session_tracker/sessions.json.backup
```

## Sound Files

The application uses system sound files for timer alerts. Default path:
```
/usr/share/sounds/sound-icons/percussion-10.wav
```

Falls back to system beep if sound file is not available.

## File Structure

```
session-tracker/
├── session_tracker.py       # Main application file
├── icons/                    # Application icons
│   ├── bar-chart.svg
│   ├── chevron-down.svg
│   ├── chevron-right.svg
│   ├── list.svg
│   ├── pie-chart.svg
│   ├── play-circle.svg
│   ├── stop-circle.svg
│   └── trash.svg
├── README.md                 # This file
└── requirements.txt          # Python dependencies
```

## Changelog

### Version 1.2.0 (Current)
- Added customizable countdown timer with millisecond precision
- Implemented sound alerts on timer expiration
- Added seconds precision to timer configuration
- Enhanced countdown display with centered, styled presentation
- Improved timer control logic and session integration
- System tray notifications for timer events
- Auto-stop session on timer expiration

### Version 1.1.0
- Added calendar view with color-coded sessions
- Implemented PDF report generation (weekly/monthly)
- Added keyboard shortcuts for common actions
- System tray integration with quick controls
- Enhanced statistics dashboard
- Improved session management and editing

### Version 1.0.0
- Initial release
- Basic session tracking
- CSV import/export
- Charts and statistics
- Multi-line notes support

## Known Issues

- PyQt6-Charts is optional; charts tab will not appear if not installed
- Sound alerts require compatible system sound files
- PDF generation uses default letter page size

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## Author

**David Foucher**

## License

This project is licensed under the MIT License.

## Support

For issues, questions, or feature requests, please open an issue on GitHub.

---

**Session Tracker v1.2.0** - Professional Desktop Session Tracking Made Simple
