#!/usr/bin/env python3
"""
Session Tracker Application
A PyQt6 application with QtCharts for tracking desktop sessions

Version: 1.1.0
Author: David Foucher
"""

import sys
import json
import datetime
from pathlib import Path
from typing import List, Dict, Any
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import Qt, QTimer, QDateTime, pyqtSignal, QSettings
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QPushButton, QLabel, QTableWidget,
    QTableWidgetItem, QHeaderView, QTabWidget,
    QMessageBox, QSystemTrayIcon, QMenu, QFileDialog,
    QCheckBox
)
from PyQt6.QtGui import QAction, QIcon, QPixmap

# Import QtCharts - this is the critical import
try:
    from PyQt6.QtCharts import (
        QChart, QChartView, QPieSeries, QBarSeries, 
        QBarSet, QValueAxis, QBarCategoryAxis
    )
    CHARTS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: QtCharts not available: {e}")
    CHARTS_AVAILABLE = False
    # Create dummy classes to prevent errors
    class QChart:
        pass
    class QChartView:
        def __init__(self, *args, **kwargs):
            super().__init__()


class SessionData:
    """Manages session tracking data"""
    
    def __init__(self):
        self.data_file = Path.home() / ".session_tracker" / "sessions.json"
        self.data_file.parent.mkdir(exist_ok=True)
        self.sessions = self.load_sessions()
        self.current_session = None
        self.session_start = None
    
    def load_sessions(self) -> List[Dict[str, Any]]:
        """Load sessions from file"""
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    # Ensure all entries have ID and comments for backward compatibility
                    for entry in data:
                        if "id" not in entry:
                            entry["id"] = len(data)  # Assign unique ID if missing
                        if "comments" not in entry:
                            entry["comments"] = ""
                    return data
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Failed to load sessions: {e}")
                return []
        return []
    
    def save_sessions(self):
        """Save sessions to file with backup"""
        try:
            backup_file = self.data_file.with_suffix('.backup')
            if self.data_file.exists():
                self.data_file.rename(backup_file)  # Create backup
            with open(self.data_file, 'w') as f:
                json.dump(self.sessions, f, indent=2)
            if backup_file.exists():
                backup_file.unlink()  # Remove backup on success
        except (IOError, OSError) as e:
            raise RuntimeError(f"Failed to save sessions: {e}")
    
    def start_session(self, activity: str = "Work"):
        """Start a new session"""
        self.session_start = datetime.datetime.now()
        self.current_session = {
            "activity": activity,
            "start": self.session_start.isoformat(),
            "duration": 0,
            "comments": ""  # Initialize comments
        }
    
    def end_session(self):
        """End current session"""
        if self.current_session and self.session_start:
            duration = (datetime.datetime.now() - self.session_start).seconds
            self.current_session["end"] = datetime.datetime.now().isoformat()
            self.current_session["duration"] = duration
            self.current_session["id"] = len(self.sessions) + 1  # Assign ID
            self.sessions.append(self.current_session)
            self.save_sessions()
            self.current_session = None
            self.session_start = None
    
    def delete_entries(self, entry_ids: List[int]):
        """Delete multiple session entries by IDs.
        
        Args:
            entry_ids (List[int]): List of unique IDs to delete.
        
        Raises:
            ValueError: If any entry is not found.
            RuntimeError: If a save error occurs.
        """
        deleted_count = 0
        for entry_id in entry_ids:
            entry_found = False
            for i, session in enumerate(self.sessions):
                if session.get("id") == entry_id:
                    del self.sessions[i]
                    entry_found = True
                    deleted_count += 1
                    break
            if not entry_found:
                raise ValueError(f"Entry with ID {entry_id} not found.")
        
        if deleted_count > 0:
            self.save_sessions()
        else:
            raise ValueError("No entries were deleted.")
    
    def edit_entry(self, entry_id: int, updates: Dict[str, Any]):
        """Edit an existing session entry.
        
        Args:
            entry_id (int): The ID of the entry to edit.
            updates (Dict[str, Any]): Key-value pairs to update (e.g., {'activity': 'New Activity', 'comments': 'Note'}).
        
        Raises:
            ValueError: If the entry is not found.
            RuntimeError: If a save error occurs.
        """
        entry_found = False
        for session in self.sessions:
            if session.get("id") == entry_id:
                for key, value in updates.items():
                    if key in session or key == "comments":  # Allow comments to be added
                        session[key] = value
                entry_found = True
                break
        
        if not entry_found:
            raise ValueError(f"Entry with ID {entry_id} not found.")
        
        self.save_sessions()
    
    def get_statistics(self) -> Dict[str, Any]:
        """Calculate statistics from sessions"""
        if not self.sessions:
            return {
                "total_sessions": 0,
                "total_time": 0,
                "average_duration": 0,
                "activities": {}
            }
        
        total_time = sum(s.get("duration", 0) for s in self.sessions)
        activities = {}
        
        for session in self.sessions:
            activity = session.get("activity", "Unknown")
            if activity not in activities:
                activities[activity] = {"count": 0, "time": 0}
            activities[activity]["count"] += 1
            activities[activity]["time"] += session.get("duration", 0)
        
        return {
            "total_sessions": len(self.sessions),
            "total_time": total_time,
            "average_duration": total_time // len(self.sessions) if self.sessions else 0,
            "activities": activities
        }


class ChartWidget(QWidget):
    """Widget for displaying charts using QtCharts"""
    
    def __init__(self, session_data: SessionData):
        super().__init__()
        self.session_data = session_data
        self.init_ui()
    
    def init_ui(self):
        """Initialize the chart UI"""
        layout = QVBoxLayout()
        
        if CHARTS_AVAILABLE:
            # Create pie chart for activity distribution
            self.chart_view = self.create_pie_chart()
            layout.addWidget(self.chart_view)
            
            # Add refresh button
            refresh_btn = QPushButton("Refresh Charts")
            refresh_btn.clicked.connect(self.refresh_charts)
            layout.addWidget(refresh_btn)
        else:
            # Fallback when charts are not available
            label = QLabel("Charts not available - PyQt6.QtCharts not installed")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(label)
        
        self.setLayout(layout)
    
    def create_pie_chart(self):
        """Create a pie chart showing activity distribution"""
        stats = self.session_data.get_statistics()
        
        series = QPieSeries()
        for activity, data in stats["activities"].items():
            series.append(f"{activity} ({data['count']})", data["time"])
        
        # Customize slices
        for slice in series.slices():
            slice.setLabelVisible(True)
            slice.setLabel(f"{slice.label()}: {slice.percentage():.1f}%")
        
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Activity Distribution")
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        return chart_view
    
    def refresh_charts(self):
        """Refresh the charts with latest data"""
        if CHARTS_AVAILABLE and hasattr(self, 'chart_view'):
            # Update the chart with new data
            new_chart_view = self.create_pie_chart()
            layout = self.layout()
            layout.replaceWidget(self.chart_view, new_chart_view)
            self.chart_view.deleteLater()
            self.chart_view = new_chart_view


class SessionTrackerWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.session_data = SessionData()
        self.settings = QSettings("DavidFoucher", "SessionTracker")
        self.use_12hour_format = self.settings.value("use_12hour_format", True, type=bool)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Session Tracker v1.1.0")
        self.setGeometry(100, 100, 1100, 600)
        
        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Header with status
        header_layout = QHBoxLayout()
        self.status_label = QLabel("No active session")
        self.status_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.timer_label = QLabel("00:00:00")
        self.timer_label.setStyleSheet("font-size: 14px;")
        header_layout.addWidget(self.status_label)
        header_layout.addStretch()
        header_layout.addWidget(self.timer_label)
        main_layout.addLayout(header_layout)
        
        # Control buttons
        button_layout = QHBoxLayout()
        self.start_btn = QPushButton("Start Session")
        self.start_btn.clicked.connect(self.start_session)
        self.stop_btn = QPushButton("Stop Session")
        self.stop_btn.clicked.connect(self.stop_session)
        self.stop_btn.setEnabled(False)
        
        button_layout.addWidget(self.start_btn)
        button_layout.addWidget(self.stop_btn)
        button_layout.addStretch()
        
        # Add delete button
        self.delete_btn = QPushButton("Delete Selected")
        self.delete_btn.clicked.connect(self.delete_selected_entry)
        self.delete_btn.setStyleSheet("background-color: #d9534f; color: white;")
        button_layout.addWidget(self.delete_btn)
        
        main_layout.addLayout(button_layout)
        
        # Time format toggle
        time_format_layout = QHBoxLayout()
        self.time_format_checkbox = QCheckBox("Use 12-hour time format (AM/PM)")
        self.time_format_checkbox.setChecked(self.use_12hour_format)
        self.time_format_checkbox.stateChanged.connect(self.toggle_time_format)
        time_format_layout.addWidget(self.time_format_checkbox)
        time_format_layout.addStretch()
        main_layout.addLayout(time_format_layout)
        
        # Tab widget for different views
        self.tab_widget = QTabWidget()
        
        # Sessions tab
        self.sessions_table = self.create_sessions_table()
        self.tab_widget.addTab(self.sessions_table, "Sessions")
        
        # Statistics tab
        self.stats_widget = self.create_stats_widget()
        self.tab_widget.addTab(self.stats_widget, "Statistics")
        
        # Charts tab (if available)
        if CHARTS_AVAILABLE:
            self.chart_widget = ChartWidget(self.session_data)
            self.tab_widget.addTab(self.chart_widget, "Charts")
        
        main_layout.addWidget(self.tab_widget)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Load initial data
        self.refresh_sessions_table()
    
    def create_menu_bar(self):
        """Create the application menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        export_action = QAction("Export Data", self)
        export_action.triggered.connect(self.export_data)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        
        delete_action = QAction("Delete Selected Entry", self)
        delete_action.setShortcut("Delete")
        delete_action.triggered.connect(self.delete_selected_entry)
        edit_menu.addAction(delete_action)
        
        # About menu (top-level, not under Help)
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        menubar.addAction(about_action)
    
    def create_sessions_table(self) -> QTableWidget:
        """Create the sessions table widget"""
        table = QTableWidget()
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels(["ID", "Activity", "Start Time", "End Time", "Duration", "Comments"])
        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setEditTriggers(QTableWidget.EditTrigger.DoubleClicked | QTableWidget.EditTrigger.EditKeyPressed)
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.setSelectionMode(QTableWidget.SelectionMode.ExtendedSelection)
        
        # Connect cell changed signal to save edits
        table.cellChanged.connect(self.on_cell_changed)
        
        return table
    
    def create_stats_widget(self) -> QWidget:
        """Create the statistics widget"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        self.stats_label = QLabel()
        self.stats_label.setStyleSheet("font-size: 12px; padding: 10px;")
        self.update_statistics()
        
        layout.addWidget(self.stats_label)
        widget.setLayout(layout)
        return widget
    
    def format_datetime(self, iso_string: str) -> str:
        """Format datetime string based on user preference"""
        try:
            dt = datetime.datetime.fromisoformat(iso_string)
            if self.use_12hour_format:
                return dt.strftime("%Y-%m-%d %I:%M:%S %p")
            else:
                return dt.strftime("%Y-%m-%d %H:%M:%S")
        except (ValueError, AttributeError):
            return iso_string
    
    def toggle_time_format(self, state):
        """Toggle between 12-hour and 24-hour time format"""
        self.use_12hour_format = (state == Qt.CheckState.Checked.value)
        self.settings.setValue("use_12hour_format", self.use_12hour_format)
        self.refresh_sessions_table()
    
    def on_cell_changed(self, row: int, column: int):
        """Handle cell editing in the table"""
        # Temporarily disconnect to avoid recursive calls
        self.sessions_table.cellChanged.disconnect(self.on_cell_changed)
        
        try:
            # Get the entry ID from the first column
            id_item = self.sessions_table.item(row, 0)
            if id_item is None:
                return
            
            entry_id = int(id_item.text())
            
            # Determine what was edited and update accordingly
            updates = {}
            
            if column == 1:  # Activity
                item = self.sessions_table.item(row, column)
                if item:
                    updates["activity"] = item.text()
            elif column == 5:  # Comments
                item = self.sessions_table.item(row, column)
                if item:
                    updates["comments"] = item.text()
            
            # Save changes if any updates were made
            if updates:
                self.session_data.edit_entry(entry_id, updates)
                
        except (ValueError, RuntimeError) as e:
            QMessageBox.warning(self, "Edit Error", f"Failed to save changes: {e}")
        finally:
            # Reconnect the signal
            self.sessions_table.cellChanged.connect(self.on_cell_changed)
    
    def start_session(self):
        """Start a new tracking session"""
        self.session_data.start_session()
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.status_label.setText("Session Active")
        self.timer.start(1000)  # Update every second
    
    def stop_session(self):
        """Stop the current tracking session"""
        self.session_data.end_session()
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.status_label.setText("No active session")
        self.timer.stop()
        self.timer_label.setText("00:00:00")
        self.refresh_sessions_table()
        self.update_statistics()
        
        # Refresh charts if available
        if CHARTS_AVAILABLE and hasattr(self, 'chart_widget'):
            self.chart_widget.refresh_charts()
    
    def update_timer(self):
        """Update the timer display"""
        if self.session_data.session_start:
            elapsed = datetime.datetime.now() - self.session_data.session_start
            hours, remainder = divmod(elapsed.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.timer_label.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
    
    def refresh_sessions_table(self):
        """Refresh the sessions table with current data"""
        # Temporarily disconnect to avoid triggering cellChanged during refresh
        self.sessions_table.cellChanged.disconnect(self.on_cell_changed)
        
        sessions = self.session_data.sessions
        self.sessions_table.setRowCount(len(sessions))
        
        for row, session in enumerate(sessions):
            entry_id = session.get("id", row + 1)
            
            # ID column (not editable)
            id_item = QTableWidgetItem(str(entry_id))
            id_item.setFlags(id_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.sessions_table.setItem(row, 0, id_item)
            
            # Activity column (editable)
            self.sessions_table.setItem(row, 1, QTableWidgetItem(session.get("activity", "")))
            
            # Start time column (not editable)
            start_item = QTableWidgetItem(self.format_datetime(session.get("start", "")))
            start_item.setFlags(start_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.sessions_table.setItem(row, 2, start_item)
            
            # End time column (not editable)
            end_item = QTableWidgetItem(self.format_datetime(session.get("end", "")))
            end_item.setFlags(end_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.sessions_table.setItem(row, 3, end_item)
            
            # Duration column (not editable)
            duration = session.get("duration", 0)
            hours, remainder = divmod(duration, 3600)
            minutes, seconds = divmod(remainder, 60)
            duration_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            duration_item = QTableWidgetItem(duration_str)
            duration_item.setFlags(duration_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.sessions_table.setItem(row, 4, duration_item)
            
            # Comments column (editable)
            self.sessions_table.setItem(row, 5, QTableWidgetItem(session.get("comments", "")))
        
        # Reconnect the signal
        self.sessions_table.cellChanged.connect(self.on_cell_changed)
    
    def delete_selected_entry(self):
        """Delete selected entries from the table and database"""
        selected_rows = self.sessions_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "Please select one or more entries to delete.")
            return
        
        entry_ids = []
        for row in selected_rows:
            entry_id = int(self.sessions_table.item(row.row(), 0).text())
            entry_ids.append(entry_id)
        
        # Confirmation dialog
        if len(entry_ids) == 1:
            message = "Are you sure you want to delete this entry?"
        else:
            message = f"Are you sure you want to delete {len(entry_ids)} selected entries?"
        
        reply = QMessageBox.question(
            self, "Confirm Deletion", message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.session_data.delete_entries(entry_ids)
                self.refresh_sessions_table()
                self.update_statistics()
                if CHARTS_AVAILABLE and hasattr(self, 'chart_widget'):
                    self.chart_widget.refresh_charts()
                
                if len(entry_ids) == 1:
                    QMessageBox.information(self, "Success", "Entry deleted successfully.")
                else:
                    QMessageBox.information(self, "Success", f"{len(entry_ids)} entries deleted successfully.")
            except ValueError as e:
                QMessageBox.warning(self, "Error", str(e))
            except RuntimeError as e:
                QMessageBox.critical(self, "Database Error", str(e))
    
    def update_statistics(self):
        """Update the statistics display"""
        stats = self.session_data.get_statistics()
        
        total_hours = stats["total_time"] // 3600
        total_minutes = (stats["total_time"] % 3600) // 60
        avg_minutes = stats["average_duration"] // 60
        
        stats_text = f"""
        <h3>Session Statistics</h3>
        <p><b>Total Sessions:</b> {stats["total_sessions"]}</p>
        <p><b>Total Time:</b> {total_hours} hours, {total_minutes} minutes</p>
        <p><b>Average Duration:</b> {avg_minutes} minutes</p>
        <h4>Activities:</h4>
        """
        
        for activity, data in stats["activities"].items():
            hours = data["time"] // 3600
            minutes = (data["time"] % 3600) // 60
            stats_text += f"<p><b>{activity}:</b> {data['count']} sessions, {hours}h {minutes}m</p>"
        
        self.stats_label.setText(stats_text)
    
    def export_data(self):
        """Export session data to CSV"""
        import csv
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export Data", "", "CSV Files (*.csv)"
        )
        
        if filename:
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.DictWriter(
                    csvfile, 
                    fieldnames=["id", "activity", "start", "end", "duration", "comments"]
                )
                writer.writeheader()
                writer.writerows(self.session_data.sessions)
            
            QMessageBox.information(self, "Export Complete", f"Data exported to {filename}")
    
    def show_about(self):
        """Show about dialog"""
        about_text = """
        <h2>Session Tracker</h2>
        <p><b>Version:</b> 1.1.0</p>
        <p><b>Author:</b> David Foucher</p>
        <p><b>Copyright:</b> © 2025 David Foucher. All rights reserved.</p>
        <hr>
        <p>A PyQt6 application for tracking desktop sessions with support for:</p>
        <ul>
            <li>Session timing and activity tracking</li>
            <li>12/24-hour time format display</li>
            <li>Editable comments and activity names</li>
            <li>Statistical analysis and charts</li>
            <li>Data export to CSV</li>
        </ul>
        <p>Built with PyQt6 and QtCharts.</p>
        """
        QMessageBox.about(self, "About Session Tracker", about_text)
    
    def closeEvent(self, event):
        """Handle window close event"""
        if self.session_data.current_session:
            reply = QMessageBox.question(
                self, 
                "Active Session",
                "There is an active session. Do you want to stop it before closing?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.stop_session()
        
        event.accept()


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("Session Tracker")
    app.setOrganizationName("DavidFoucher")
    
    # Set application style
    app.setStyle("Fusion")
    
    # Create and show main window
    window = SessionTrackerWindow()
    window.show()
    
    # Check if QtCharts is available
    if not CHARTS_AVAILABLE:
        QMessageBox.warning(
            window,
            "QtCharts Not Available",
            "PyQt6.QtCharts is not installed. Charts functionality will be disabled.\n"
            "Install with: pip install PyQt6-Charts",
            QMessageBox.StandardButton.Ok
        )
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
