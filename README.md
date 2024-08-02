
Mouse Insight - Mouse Tracker
=============================

Description
-----------
Mouse Insight is a Python-based tool that tracks mouse movements and clicks to analyze user interaction with their computer. It captures detailed information about cursor positions, mouse click events, and periodically saves this data to JSON files for further analysis.

Features
--------
- Tracks mouse movements across multiple screens.
- Records left and right mouse clicks.
- Saves tracking data in JSON format.
- Generates a visual representation of mouse activity (optional feature not fully implemented in the script provided).

Requirements
------------
- Python 3.6 or higher
- pynput
- PIL (Pillow)
- screeninfo
- All dependencies can be installed via a requirements.txt file.

Installation
------------
1. Ensure Python 3.6+ is installed on your system.
2. Clone the repository or download the source code:
   [Insert your repository link or download link here]
3. Navigate to the project directory and install required Python packages:
   ```
   pip install -r requirements.txt
   ```

Usage
-----
To run the Mouse Tracker:
1. Navigate to the project directory in your terminal.
2. Run the script using Python:
   ```
   python mouse_tracker.py
   ```
3. The tracker will start immediately. Data is saved automatically at intervals specified in the script.

Configuration
-------------
- `save_interval`: Adjust the time interval (in seconds) between data recordings in the `mouse_tracker.py` script.
- Data is saved in the directory specified by `mouse_track_dir` within the script. Modify as necessary.

Output
------
- The program generates and saves data in the `app/tracking/mouse-tracking` directory by default.
- Outputs include:
  - `cursor_track_{timestamp}.json`: JSON file with detailed mouse tracking data.

Stopping the Tracker
--------------------
To stop the tracker, use `Ctrl+C` in your terminal. Ensure to stop gracefully to avoid any data loss.

Contributing
------------
Contributions are welcome! Please fork the repository, make your changes, and submit a pull request. If you find bugs or have suggestions, please open an issue in the repository.

License
-------
This project is licensed under the MIT License - see the LICENSE file for details.
