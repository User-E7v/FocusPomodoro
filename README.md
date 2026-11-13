# FocusPomodoro

**FocusPomodoro** is a comprehensive, command-line interface (CLI) time-management and productivity application written in Python. It implements the **Pomodoro Technique**, a structured time-management method developed by Francesco Cirillo, designed to enhance focus, minimize mental fatigue, and track long-term productivity metrics directly from your terminal.

---

## Table of Contents

1. [Overview and Core Concepts](#overview-and-core-concepts)
2. [Key Features](#key-features)
3. [Timer Modes](#timer-modes)
4. [System Requirements](#system-requirements)
5. [Installation and Execution](#installation-and-execution)
6. [User Guide and Workflow](#user-guide-and-workflow)
7. [Data Persistence and Statistics Schema](#data-persistence-and-statistics-schema)
8. [Technical Architecture](#technical-architecture)

---

## Overview and Core Concepts

The Pomodoro Technique breaks work down into focused intervals, traditionally 25 minutes in length, separated by short breaks. **FocusPomodoro** automates this cycle within a clean, distraction-free terminal environment. Users can run multiple consecutive sessions (cycles), customize work-to-rest ratios, receive visual and auditory cues, and review historical performance data stored locally.

---

## Key Features

* **Multiple Pre-configured and Custom Timer Modes:** Offers seven distinct operational modes tailored to different cognitive workloads, from quick sprints to extended deep-work sessions.
* **Dynamic Terminal UI:** Features a real-time ASCII progress bar, screen clearing for a clutter-free view, and ANSI color-coded countdown timers that shift colors based on urgency:
  * **Green:** More than 60 seconds remaining.
  * **Yellow:** Between 31 and 60 seconds remaining.
  * **Magenta:** Between 11 and 30 seconds remaining.
  * **Red:** 10 seconds or less remaining, accompanied by an urgent warning prompt.
* **Cross-Platform Audio Notifications:** Utilizes Windows native `winsound.Beep` frequencies on Windows systems and standard terminal bell alerts (`\a`) on Unix-like systems (Linux/macOS) to signal the end of work and break intervals.
* **Automated Statistics Tracking:** Automatically logs every completed or interrupted session to a local JSON file (`pomodoro_stats.json`), calculating total completed sessions, cumulative focus time, and average session duration.
* **Graceful Interrupt Handling:** Supports `KeyboardInterrupt` (`Ctrl + C`) to safely abort an active timer while still recording partial session data to your history.
* **Motivational Feedback System:** Displays milestone-based motivational quotes upon completing individual intervals and full multi-pomodoro sets.

---

## Timer Modes

When starting a session, you can select from the following seven configurations:

| Option | Mode Name | Work Duration | Break Duration | Best Used For |
| :--- | :--- | :--- | :--- | :--- |
| **[1]** | **Classic Pomodoro** | 25 minutes | 5 minutes | Standard tasks, general productivity, and routine work. |
| **[2]** | **Long Pomodoro** | 50 minutes | 10 minutes | Complex problem-solving and extended coding or writing blocks. |
| **[3]** | **Custom** | User-defined | User-defined | Tailoring intervals to specific personal workflows or deadlines. |
| **[4]** | **Study Mode** | 45 minutes | 15 minutes | Academic reading, lecture review, and intensive learning. |
| **[5]** | **Quick Session** | 15 minutes | 3 minutes | Overcoming procrastination, small administrative tasks, or warm-ups. |
| **[6]** | **Deep Work** | 90 minutes | 20 minutes | High-focus creative output and uninterrupted cognitive work. |
| **[7]** | **Timer Only** | User-defined | None (0 min) | Simple countdowns without automated break transitions. |

---

## System Requirements

* **Python Version:** Python 3.6 or higher.
* **External Dependencies:** None. The application relies entirely on the Python Standard Library (`time`, `os`, `json`, `datetime`, `threading`, `collections`, and `winsound` for Windows).
* **Terminal Compatibility:** Any terminal emulator supporting ANSI escape sequences (Windows Terminal, PowerShell, Command Prompt, macOS Terminal, GNOME Terminal, etc.).

---

## Installation and Execution

1. **Download the Source Code:** Ensure `FocusPomodoro.py` is saved in your desired working directory.
2. **Open a Terminal:** Navigate to the directory containing the script:
   ```bash
   cd path/to/directory
   ```
3. **Run the Application:** Execute the script using the Python interpreter:
   ```bash
   python FocusPomodoro.py
   ```
   *(Note: On some macOS or Linux systems, you may need to use `python3 FocusPomodoro.py`.)*

---

## User Guide and Workflow

Upon launching the application, you will be presented with the **Main Menu**:

1. **[1] Start Pomodoro:**
   * Choose one of the 7 timer modes.
   * Specify the target number of Pomodoro cycles (between `1` and `10`).
   * The work countdown begins immediately.
   * Once a work interval finishes, an audio alert sounds, and you will be prompted to press `Enter` to begin your break (if applicable).
   * After completing all scheduled cycles, a final summary screen displays your total focus time.
2. **[2] View Statistics:**
   * Displays cumulative metrics including total completed Pomodoros, total time invested (in hours and minutes), average session length, and a log of the 10 most recent sessions with their completion status (`COMPLETE` or `STOPPED`).
3. **[3] How to Use:**
   * Provides a built-in reference guide explaining the methodology behind the Pomodoro Technique and a summary of available modes.
4. **[4] Settings:**
   * Lists active system capabilities and best practices for maintaining focus during work intervals.
5. **[5] Exit:**
   * Cleanly terminates the program.

---

## Data Persistence and Statistics Schema

All session metrics are stored locally in the same directory as the script inside a file named `pomodoro_stats.json`. If the file does not exist, it is automatically generated upon the completion or interruption of your first session.

### JSON Structure Example

```json
{
    "sessions": [
        {
            "mode": "Classic Pomodoro",
            "duration": 1500,
            "completed": true,
            "pomodoro_num": 1,
            "timestamp": "2026-11-13T16:00:00.123456"
        }
    ],
    "total_pomodoros": 1,
    "total_time": 1500
}
```

* **`mode`**: The name of the timer preset used.
* **`duration`**: Actual elapsed time in seconds.
* **`completed`**: Boolean indicating whether the session finished (`true`) or was manually interrupted (`false`).
* **`pomodoro_num`**: The sequence index of the session within its batch.
* **`timestamp`**: ISO 8601 formatted date and time of when the session ended.

---

## Technical Architecture

The codebase is modularized into distinct functional components:

* **UI Rendering (`clear_screen`, `print_header`, `print_ascii_timer`, `draw_progress_bar`):** Handles cross-platform screen clearing (`cls` vs `clear`) and dynamically calculates completion ratios to render a 40-character ASCII progress bar every second.
* **Input Validation (`get_timer_mode`, `get_pomodoro_count`):** Wraps user inputs in `while` loops with `try-except ValueError` blocks to prevent crashes from non-numeric or out-of-range entries.
* **Core Engine (`run_pomodoro`):** Manages the 1-second tick loop using `time.sleep(1)`, tracks actual wall-clock duration via `time.time()`, triggers audio alerts, and catches `KeyboardInterrupt` exceptions to handle early termination gracefully.
* **Data Layer (`save_stats`, `view_stats`):** Manages reading from and writing to `pomodoro_stats.json` with safe fallback initialization if the file is missing or corrupted.