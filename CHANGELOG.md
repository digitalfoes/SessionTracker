# Changelog

All notable changes to Session Tracker will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2025-10-03

### Added
- **Countdown Timer System**
  - Customizable session timer with hours, minutes, and seconds configuration
  - Real-time millisecond precision countdown display (HH:MM:SS.mmm)
  - Centered, styled countdown display with black background and white text
  - Visual countdown updates every 50ms for smooth display

- **Timer Alerts**
  - Sound alerts on timer expiration (WAV file playback)
  - System beep fallback if sound file unavailable
  - Visual alert dialog on countdown completion
  - System tray notifications for timer events

- **Auto-stop Feature**
  - Sessions automatically stop when timer reaches zero
  - Prevents timer overflow and ensures accurate session tracking

- **UI Improvements**
  - Collapsible "Session Timer (Optional)" group box
  - Checkbox-based timer enable/disable
  - Seconds precision added to timer configuration
  - Enhanced timer label with countdown indicator

### Changed
- Timer display now shows negative countdown in small header timer
- Large countdown display shows remaining time with milliseconds
- Timer configuration is disabled during active session
- Improved timer state management and validation

### Fixed
- Timer accuracy improved with microsecond-level calculations
- Pause time correctly excluded from countdown calculations
- Timer expiration properly triggers session stop
- Countdown display visibility properly managed

## [1.1.0] - 2025-09-15

### Added
- **Calendar View**
  - Color-coded calendar showing session activity
  - Green dots for days with sessions
  - Date selection to view session details
  - Monthly overview of work patterns

- **PDF Report Generation**
  - Weekly session reports with statistics
  - Monthly session reports with summaries
  - Professional formatting with ReportLab
  - Automatic file save dialog

- **Keyboard Shortcuts**
  - `Ctrl+Shift+S`: Start session
  - `Ctrl+Shift+T`: Stop session
  - `Ctrl+Shift+P`: Pause/Resume session
  - `Ctrl+Shift+E`: Export data to CSV

- **System Tray Integration**
  - Minimize to system tray
  - Quick access menu with Start/Stop actions
  - Tray notifications for session events
  - Active/inactive status indicators

- **Enhanced Statistics**
  - Total sessions count
  - Total active time tracking
  - Average session duration
  - Today's session time display

### Changed
- Improved session table with better formatting
- Enhanced data persistence with error handling
- Better session ID generation (YYYYMMDD-NNN format)

### Fixed
- Multi-line notes properly saved and displayed
- CSV import/export handling of special characters
- Session pause time calculations

## [1.0.0] - 2025-08-01

### Added
- **Core Session Tracking**
  - Start, pause, resume, and stop sessions
  - Activity name and notes fields
  - Real-time session timer
  - Hybrid session ID format

- **Data Management**
  - JSON-based persistent storage
  - CSV import/export functionality
  - Session editing and deletion
  - Automatic data backup on import

- **User Interface**
  - Clean tabbed interface (Sessions, Statistics, Charts)
  - Session history table with sorting
  - Search and filter functionality
  - Multi-line notes with custom delegate

- **Charts and Statistics**
  - Pie charts for activity distribution
  - Bar charts for session duration comparison
  - Basic statistics dashboard
  - Visual data analysis

- **Session Management**
  - Pause/resume with time tracking
  - Active time calculation (excluding pauses)
  - Session duration tracking
  - Notes editing support

### Technical Details
- Built with PyQt6 framework
- QtCharts integration for visualizations
- ReportLab for PDF generation
- JSON data persistence
- System tray support

---

## Release Notes

### v1.2.0 Highlights
This release focuses on timer functionality and session automation. The new countdown timer allows users to set specific session durations with millisecond precision, complete with audio and visual alerts when time expires. Sessions now auto-stop when the timer reaches zero, ensuring accurate time tracking.

### v1.1.0 Highlights
Major update adding calendar view, PDF reporting, and keyboard shortcuts. System tray integration provides quick access to core functions. Calendar view helps visualize work patterns over time.

### v1.0.0 Highlights
Initial stable release with complete session tracking, data management, and visualization features. Supports pause/resume, CSV import/export, and interactive charts.

---

**For full documentation, see [README.md](README.md)**
