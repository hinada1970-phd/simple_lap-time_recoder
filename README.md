# Simple Lap-Time Recorder (PySide6)

A lightweight lap-timing desktop app built with **PySide6/Qt**. Start/stop with the spacebar, record laps with number keys (0–9), reset with Esc, and save results to CSV with S.

> Primary target: macOS (as noted in the source header), but it should also run on Windows/Linux wherever PySide6 is available.

---

## Features
- Clean, single‑window UI with large, readable timer
- **Space** to start/stop; **0–9** to log laps; **Esc** to reset; **S** to save
- Auto‑computed **per‑lap** and **total** elapsed times
- CSV export with session metadata and millisecond timestamps
- Always‑on display refresh (~100 ms)

---

## Requirements
- Python 3.8+
- PySide6

```bash
pip install PySide6
```

---

## Quick Start
1. Clone or download this repository.
2. Install dependencies (see above).
3. Run the app:

```bash
python3 symple_lap-time_recorder.py
```

> On first run, the window centers on your primary screen and shows a large **00:00.00** timer with a status hint.

---

## Usage
- **Start / Stop**: Press **Space**. The label color changes (blue while running, red when stopped).
- **Record Lap**: Press any number key **0–9** while running. Each press appends a new row to the lap log with:
  - the key you pressed (as **Lap Number**),
  - the **lap time** since the previous lap (or since start if it’s the first),
  - the **total elapsed** at the moment of logging,
  - a wall‑clock **timestamp**.
- **Reset**: Press **Esc**. Clears timer, lap list, and disables Save.
- **Save**: Press **S** or click **Save Results**. You’ll be prompted for a **Session Name**, then a save destination (defaults to `~/Desktop/<Session_YYYYMMDD_HHMMSS>.csv`).

### Keyboard Shortcuts
| Action | Key |
|---|---|
| Start / Stop | Space |
| Reset | Esc |
| Save | S |
| Record lap | 0–9 |

> Tip: You can use different digits to tag laps (e.g., **1** for warm‑up, **2** for sprint), since the “Lap Number” column stores the digit you pressed.

---

## CSV Export Format
When you save, the app writes a human‑readable CSV with session metadata and detailed lap rows.

### Header block
```
# Session Information
Session Name, <name you entered>
Save Date, <YYYY-MM-DD HH:MM:SS>
Total Laps, <count>
Total Time, <MM:SS.ss>
```

### Column headers
```
Lap Number, Lap Time (sec), Lap Time (display), Total Time (sec), Total Time (display), Timestamp
```

### Example row
```
1, 5.247, 00:05.25, 12.394, 00:12.39, 2025-09-03 14:22:10.317
```

Notes:
- `(sec)` columns are decimal seconds; `(display)` columns use `MM:SS.ss` formatting.
- `Timestamp` is local wall clock time down to milliseconds.

---

## Project Structure
```
.
├── symple_lap-time_recorder.py   # Main application (PySide6)
├── README.md                     # This file
└── LICENSE.md                    # Licence file
```

Key components inside the script:
- `LapTimerApp` (QMainWindow): UI setup, shortcuts, and state management
- `toggle_timer`, `reset_timer`, `record_lap`, `update_timer`: Core logic
- `save_results()`: CSV writer with session metadata and lap table
- `format_time()`: `MM:SS.ss` formatter

---

## Development
- Run locally with `python3 symple_lap-time_recorder.py`.
- Edit UI/logic in `LapTimerApp` methods.
- Consider adding unit tests for time formatting and CSV serialization if you evolve the code.

### Style / UI
- Uses Qt widgets with minimal stylesheets.
- `QTimer` ticks every 100 ms to refresh the display.

---

## Troubleshooting
- **PySide6 not found**: `pip install PySide6` (ensure the interpreter matches the one running the script).
- **No window / crashes on import**: Verify your Qt platform plugins are properly installed (common on fresh environments).
- **Shortcut doesn’t trigger**: Make sure the app window is focused. Some global shortcut managers/IMEs may intercept keys.
- **CSV won’t save**: Check file permissions and available disk space. Try saving to a user‑writable folder (e.g., Desktop/Documents).

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---

## Acknowledgments
- Built with **PySide6/Qt**.
- Thanks to the open‑source community for tooling and examples.

---

## Roadmap
- Split UI and logic layers
- Add split/sector deltas and best‑lap highlighting
- Import/export JSON session files
- Theming and high‑contrast mode
- Build standalone app bundles (macOS `.app`, Windows `.exe`) using PyInstaller

