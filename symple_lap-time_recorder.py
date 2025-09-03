#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
macOS Lap Timer App (PySide6 version)
Space key: Start/Stop
Number keys: Record lap time
Escape key: Reset

Required library:
pip install PySide6
"""

import sys
import time
import csv
import os
from datetime import datetime
from pathlib import Path
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QLabel, QTextEdit, QFrame, QPushButton,
                               QFileDialog, QMessageBox, QInputDialog)
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QFont, QKeySequence, QShortcut, QPalette, QColor


class LapTimerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Lap-Time Recorder")
        self.setGeometry(100, 100, 400, 600) 
        self.center_on_screen()

        # Timer state
        self.start_time = None
        self.is_running = False
        self.elapsed_time = 0
        self.lap_times = []
        
        # Create UI elements
        self.setup_ui()
        
        # Set up key bindings
        self.setup_shortcuts()
        
        # Timer for updating display
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(100)  # Update every 100ms
    
    def center_on_screen(self):
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        main_window_geometry = self.frameGeometry()
        center_point = screen_geometry.center()
        main_window_geometry.moveCenter(center_point)
        self.move(main_window_geometry.topLeft())
        
    def setup_ui(self):
        """Create UI elements"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Timer display
        timer_frame = QFrame()
        timer_layout = QVBoxLayout(timer_frame)
        timer_layout.setAlignment(Qt.AlignCenter)
        
        self.time_label = QLabel("00:00.00")
        self.time_label.setFont(QFont("Arial", 42, QFont.Bold))
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("""
            QLabel {
                color: #333333;
                background-color: transparent;
                padding: 15px;
            }
        """)
        timer_layout.addWidget(self.time_label)
        
        # Status display
        self.status_label = QLabel("Press Space to Start")
        self.status_label.setFont(QFont("Arial", 18))
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                color: #666666;
                background-color: transparent;
                padding: 5px;
            }
        """)
        timer_layout.addWidget(self.status_label)
        
        main_layout.addWidget(timer_frame)
        
        # Instructions
        instructions_frame = QFrame()
        instructions_layout = QVBoxLayout(instructions_frame)
        instructions_layout.setAlignment(Qt.AlignCenter)
        
        instructions = [
            "Space: Start/Stop  |  Number keys (0-9): Record lap  |  Esc: Reset",
            "S: Save"
        ]
        
        for instruction in instructions:
            label = QLabel(instruction)
            label.setFont(QFont("Arial", 12))
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("""
                QLabel {
                    color:  #666666;
                    background-color: transparent;
                    padding: 2px;
                }
            """)
            instructions_layout.addWidget(label)
        
        main_layout.addWidget(instructions_frame)
        
        # Lap times display area
        lap_frame = QFrame()
        lap_layout = QVBoxLayout(lap_frame)
        
        lap_title = QLabel("Lap Times Record")
        lap_title.setFont(QFont("Arial", 14, QFont.Bold))
        lap_title.setStyleSheet("""
            QLabel {
                color: #333333;
                background-color: transparent;
                padding: 5px 0px;
            }
        """)
        lap_layout.addWidget(lap_title)
        
        self.lap_text = QTextEdit()
        self.lap_text.setReadOnly(True)
        self.lap_text.setFont(QFont("Monaco", 11))
        self.lap_text.setFixedHeight(200)
        self.lap_text.setStyleSheet("""
            QTextEdit {
                background-color: #ffffff;
                border: 1px solid #d0d0d0;
                border-radius: 8px;
                padding: 10px;
                color: #333333;
            }
        """)
        lap_layout.addWidget(self.lap_text)
        
        main_layout.addWidget(lap_frame)
        
        # Button area
        button_frame = QFrame()
        button_layout = QHBoxLayout(button_frame)
        button_layout.setContentsMargins(10, 10, 10, 10)
        
        # Save button
        self.save_button = QPushButton("Save Results")
        self.save_button.setFont(QFont("Arial", 14, QFont.Bold))
        self.save_button.setFixedSize(180, 50)
        self.save_button.clicked.connect(self.save_results)
        self.save_button.setEnabled(False)
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #007AFF;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056CC;
            }
            QPushButton:disabled {
                background-color: #CCCCCC;
                color: #888888;
            }
        """)
        
        button_layout.addWidget(self.save_button)
        
        main_layout.addWidget(button_frame)
    
    def setup_shortcuts(self):
        """Set up keyboard shortcuts"""
        # Space key
        space_shortcut = QShortcut(QKeySequence(Qt.Key_Space), self)
        space_shortcut.activated.connect(self.toggle_timer)
        
        # Escape key
        escape_shortcut = QShortcut(QKeySequence(Qt.Key_Escape), self)
        escape_shortcut.activated.connect(self.reset_timer)
        
        # S for save
        save_shortcut = QShortcut(QKeySequence(Qt.Key_S), self)
        save_shortcut.activated.connect(self.save_results)
        
        # Number keys (0-9)
        num_shortcut = {}
        for i in range(10):
            num_shortcut[f'var{i}'] = QShortcut(QKeySequence(str(i)), self)
            num_shortcut[f'var{i}'].activated.connect(lambda num=i: self.record_lap(num))
    
    def center_window(self):
        """Center window on screen"""
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        window_geometry = self.frameGeometry()
        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())
    
    def toggle_timer(self):
        """Toggle timer start/stop"""
        if not self.is_running:
            # Start
            self.start_time = time.time() - self.elapsed_time
            self.is_running = True
            self.status_label.setText("Running - Press Space to Stop")
            self.time_label.setStyleSheet("""
                QLabel {
                    color: #007AFF;
                    background-color: transparent;
                    padding: 15px;
                }
            """)
        else:
            # Stop
            self.is_running = False
            self.status_label.setText("Stopped - Press Space to Resume")
            self.time_label.setStyleSheet("""
                QLabel {
                    color: #FF6B6B;
                    background-color: transparent;
                    padding: 15px;
                }
            """)
    
    def reset_timer(self):
        """Reset timer"""
        self.is_running = False
        self.start_time = None
        self.elapsed_time = 0
        self.lap_times.clear()
        self.status_label.setText("Press Space to Start")
        self.time_label.setStyleSheet("""
            QLabel {
                color: #333333;
                background-color: transparent;
                padding: 15px;
            }
        """)
        
        # Clear lap times record
        self.lap_text.clear()
        
        # Disable save button
        self.save_button.setEnabled(False)
    
    def record_lap(self, lap_number):
        """Record lap time"""
        if self.is_running:
            current_time = self.elapsed_time
            
            # Calculate time difference from previous lap
            if self.lap_times:
                lap_time = current_time - self.lap_times[-1]['total_time']
            else:
                lap_time = current_time
            
            # Store lap data
            lap_data = {
                'number': lap_number,
                'lap_time': lap_time,
                'total_time': current_time,
                'timestamp': datetime.now()
            }
            self.lap_times.append(lap_data)
            
            # Add lap time to display
            self.add_lap_to_display(lap_data)
    
    def add_lap_to_display(self, lap_data):
        """Add lap time to display area"""
        lap_time_str = self.format_time(lap_data['lap_time'])
        total_time_str = self.format_time(lap_data['total_time'])
        timestamp_str = lap_data['timestamp'].strftime("%H:%M:%S")
        
        lap_info = f"[{lap_data['number']}] {lap_time_str} (Total: {total_time_str}) - {timestamp_str}"
        
        self.lap_text.append(lap_info)
        
        # Enable save button
        self.save_button.setEnabled(True)
        
        # Auto scroll
        from PySide6.QtGui import QTextCursor
        cursor = self.lap_text.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.lap_text.setTextCursor(cursor)
    
    def format_time(self, seconds):
        """Format seconds to MM:SS.ss format"""
        minutes = int(seconds // 60)
        remaining_seconds = seconds % 60
        return f"{minutes:02d}:{remaining_seconds:05.2f}"
    
    def save_results(self):
        """Save measurement results to CSV file"""
        if not self.lap_times:
            QMessageBox.information(self, "Information", "No lap times to save.")
            return
        
        # Input session name
        session_name, ok = QInputDialog.getText(
            self, "Session Name", "Enter a name for this session:",
            text=f"Session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        
        if not ok or not session_name.strip():
            return
        
        # Choose save location
        default_filename = f"{session_name.strip()}.csv"
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Results", 
            str(Path.home() / "Desktop" / default_filename),
            "CSV files (*.csv);;All files (*.*)"
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Header information
                writer.writerow(['# Session Information'])
                writer.writerow(['Session Name', session_name.strip()])
                writer.writerow(['Save Date', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
                writer.writerow(['Total Laps', len(self.lap_times)])
                writer.writerow(['Total Time', self.format_time(self.elapsed_time)])
                writer.writerow([])  # Empty row
                
                # Lap data header
                writer.writerow(['Lap Number', 'Lap Time (sec)', 'Lap Time (display)', 'Total Time (sec)', 'Total Time (display)', 'Timestamp'])
                
                # Lap data
                for lap_data in self.lap_times:
                    writer.writerow([
                        lap_data['number'],
                        f"{lap_data['lap_time']:.3f}",
                        self.format_time(lap_data['lap_time']),
                        f"{lap_data['total_time']:.3f}",
                        self.format_time(lap_data['total_time']),
                        lap_data['timestamp'].strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                    ])
            
            QMessageBox.information(self, "Save Complete", f"Results saved to:\n{file_path}")
            print("Save Complete! ", f"Results saved to:\n{file_path}")
            
        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"Error occurred while saving file:\n{str(e)}")
    
    def update_timer(self):
        """Update timer display"""
        if self.is_running and self.start_time:
            self.elapsed_time = time.time() - self.start_time
        
        # Update time display
        time_str = self.format_time(self.elapsed_time)
        self.time_label.setText(time_str)

def main():
    """Main function"""
    print("=== MAIN FUNCTION STARTED ===")
    
    app = QApplication(sys.argv)
    print("QApplication created")
    
    # Set default application font to avoid font warnings
    default_font = QFont("Arial")
    if not default_font.exactMatch():
        # Fallback to system default fonts
        default_font = QFont("Arial")
        if not default_font.exactMatch():
            default_font = QFont()  # Use system default
    
    app.setFont(default_font)
    print(f"Application font set to: {default_font.family()}")
    
    # Set application information
    app.setApplicationName("Lap Timer")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("LapTimer")
    print("Application information set")
    
    # Create main window
    print("Creating main window...")
    try:
        window = LapTimerApp()
        print("Main window created successfully")
    except Exception as e:
        print(f"ERROR creating main window: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("Showing window...")
    window.show()
    print("Window shown")
    
    # Bring window to front
    window.raise_()
    window.activateWindow()
    print("Window activated")
    
    print("Starting event loop...")
    sys.exit(app.exec())


if __name__ == "__main__":
    print("=== SCRIPT STARTED ===")
    print("Python version:", sys.version)
    try:
        print("PySide6 version:", QApplication.applicationVersion())
    except:
        print("Could not get PySide6 version")
    
    main()