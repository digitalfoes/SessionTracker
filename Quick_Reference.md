# Session Tracker v1.1.0 - Quick Reference Guide

## 🎯 What's New in v1.1.0

### 1. ❌ DELETE ENTRIES
**How to use:**
- Select one or more rows in the Sessions table
- Click the red "Delete Selected" button OR press the Delete key
- Confirm your choice in the dialog box
- Done! Your entries are removed

**Pro Tips:**
- Hold Ctrl and click to select multiple individual entries
- Hold Shift and click to select a range of entries
- Use Ctrl+A to select all entries

---

### 2. 🕐 12/24-HOUR TIME FORMAT
**How to use:**
- Look for the checkbox below the Start/Stop buttons
- ✅ Checked = 12-hour format (8:42 PM)
- ☐ Unchecked = 24-hour format (20:42)
- Your choice is saved automatically!

**Examples:**
```
12-hour: 2024-10-02 08:42:15 PM
24-hour: 2024-10-02 20:42:15
```

---

### 3. 📝 EDITABLE COMMENTS
**How to use:**
- Double-click any cell in the "Comments" column
- Type your note or comment
- Press Enter or click away - it saves automatically!

**You can also edit:**
- Activity names (column 2)

**Read-only columns:**
- ID, Start Time, End Time, Duration (system-managed)

---

### 4. ℹ️ ENHANCED ABOUT SECTION
**View it:**
- Click Help menu → About
- See version number (1.1.0)
- Author: David Foucher
- Copyright information
- Full feature list

---

## 🚀 Quick Start Guide

### First Time Using?
1. Click "Start Session" to begin tracking
2. Click "Stop Session" when done
3. View your sessions in the table
4. Add comments by double-clicking the Comments column
5. Check statistics in the Statistics tab
6. View visual charts in the Charts tab (if QtCharts installed)

### Daily Workflow
```
START SESSION → WORK → STOP SESSION → ADD COMMENTS → REPEAT
```

### Managing Your Data
- **Export:** File menu → Export Data (saves as CSV)
- **Delete:** Select entries → Click Delete button → Confirm
- **Edit:** Double-click Activity or Comments cells

---

## 🎨 Visual Guide

### Main Window Layout
```
┌─────────────────────────────────────────────────┐
│ Session Tracker v1.1.0                          │
├─────────────────────────────────────────────────┤
│ No active session              00:00:00         │
├─────────────────────────────────────────────────┤
│ [Start Session] [Stop Session]  [Delete Selected]│
│ ☑ Use 12-hour time format (AM/PM)              │
├─────────────────────────────────────────────────┤
│ ┌───────────────────────────────────────────┐  │
│ │ ID │ Activity │ Start │ End │ Dur │ Comments││
│ │  1 │   Work   │ ...   │ ... │ ... │   ...   ││
│ │  2 │  Study   │ ...   │ ... │ ... │   ...   ││
│ └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

### Menu Bar
```
File                Edit                 Help
├─ Export Data      ├─ Delete Selected   ├─ About
└─ Exit             └─ (Delete key)      
```

---

## 💾 Data Storage

**Location:** `~/.session_tracker/sessions.json`

**Backup:** Automatic backup created before each save

**Format:** JSON with these fields:
- id (unique identifier)
- activity (what you were doing)
- start (when you started)
- end (when you stopped)
- duration (in seconds)
- comments (your notes)

---

## ⚠️ Important Notes

### Data Safety
✅ Backup created automatically before saves
✅ Confirmation required for deletions
✅ Invalid entries handled gracefully
✅ Settings persist across restarts

### What Can't Be Changed
- Entry IDs (system-generated)
- Start/End times (recorded automatically)
- Duration (calculated from start/end)

### What Can Be Changed
- Activity names (double-click to edit)
- Comments (double-click to edit)
- Time display format (checkbox toggle)

---

## 🔧 Troubleshooting

### "Charts not available"
**Solution:** Install PyQt6-Charts
```bash
pip install PyQt6-Charts
```

### Can't edit a cell
**Check:** Are you double-clicking? Only Activity and Comments can be edited.

### Time format won't change
**Solution:** Check the checkbox below the buttons, then look at the table.

### Delete button grayed out
**Solution:** You need to select at least one row in the table first.

### Changes not saving
**Check:** Did you see an error message? Make sure the file isn't locked by another program.

---

## 📊 Statistics Tab

View comprehensive statistics:
- Total number of sessions
- Total time tracked
- Average session duration
- Breakdown by activity type
- Time spent per activity

---

## 📈 Charts Tab

Visual representation of your data:
- Pie chart showing activity distribution
- Color-coded slices
- Percentage labels
- Refresh button to update with latest data

---

## ⌨️ Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Delete selected entries | Delete key |
| Edit cell | F2 or double-click |
| Select all entries | Ctrl+A |
| Multi-select entries | Ctrl+Click |
| Range select | Shift+Click |

---

## 🎓 Best Practices

### Naming Activities
- Be consistent (always use "Work" not "work" or "WORK")
- Be specific ("Client Call" vs just "Call")
- Keep names short for better display

### Using Comments
- Add context: "Completed project X"
- Note interruptions: "Had to stop for meeting"
- Track sub-tasks: "Focused on bug fixes"
- Leave blank if not needed

### Time Format Choice
- **12-hour:** More familiar for most users
- **24-hour:** Better for international use, no AM/PM confusion

### Regular Maintenance
- Export your data weekly as backup
- Delete test entries you don't need
- Review statistics monthly
