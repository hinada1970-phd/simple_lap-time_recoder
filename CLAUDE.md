# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Simple Lap-Time Recorder is a lightweight PySide6/Qt desktop application for lap timing. The entire application is contained in a single Python file (`symple_lap-time_recorder.py`) with a clean, keyboard-driven interface.

**Key Features**: Space bar start/stop, number keys (0-9) for lap recording, ESC reset, S for CSV export

## Development Commands

### Setup & Installation
```bash
# Install dependencies using pip
pip install PySide6

# Or using uv (package manager present in project)
uv sync
```

### Running the Application
```bash
# Run the main application
python3 symple_lap-time_recorder.py

# Alternative if using uv environment
uv run python symple_lap-time_recorder.py
```

### Testing the Application
```bash
# Test that the app imports correctly
python3 -c "import symple_lap-time_recorder; print('Import successful')"
```

## Code Architecture

### Single-File Design
The entire application is contained in `symple_lap-time_recorder.py` with these key components:

**`LapTimerApp` (QMainWindow)**: Main application class containing:
- UI setup and styling
- Keyboard shortcut management  
- Timer state management
- CSV export functionality

**Core Methods**:
- `toggle_timer()`: Start/stop timing with spacebar
- `record_lap(lap_number)`: Record lap when number key pressed
- `save_results()`: Export to CSV with session metadata
- `format_time()`: Convert seconds to MM:SS.ss format

**State Management**:
- `start_time`: Timer reference point
- `is_running`: Boolean timer state
- `elapsed_time`: Current elapsed time
- `lap_times`: List of lap data dictionaries

### Data Structure
Lap data stored as dictionaries with:
- `number`: Key pressed (0-9)
- `lap_time`: Time since previous lap
- `total_time`: Total elapsed time
- `timestamp`: Wall clock timestamp

## Key Implementation Details

### UI Framework
- **PySide6/Qt**: Single window with QVBoxLayout
- **Timer Updates**: 100ms refresh via QTimer
- **Keyboard Shortcuts**: QShortcut for Space, ESC, S, and 0-9
- **Styling**: Inline CSS with blue (running) and red (stopped) states

### File Operations
- **CSV Export**: Headers with session metadata, then lap data rows
- **Default Location**: ~/Desktop with auto-generated filename
- **Encoding**: UTF-8 with millisecond timestamps

### Dependencies
- **Core**: PySide6 (>=6.9.2)
- **Python**: 3.10+ (as specified in pyproject.toml)
- **Standard Library**: sys, time, csv, os, datetime, pathlib

## Development Notes

- No test framework present - consider pytest for future testing
- No linting configuration - consider adding ruff or flake8
- Single file design makes refactoring straightforward
- UI and logic are tightly coupled within LapTimerApp class
- Color changes and status updates are handled through inline CSS modification