import os
import sys
import time
import json
import logging
from pynput import mouse
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from threading import Timer
from screeninfo import get_monitors
import math

def get_resource_path(relative_path):
    """ Get the absolute path to a resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class MouseTracker:
    def __init__(self, save_interval=60):
        self.cursor_positions = []
        self.mouse_track_dir = get_resource_path('app/tracking/mouse-tracking')
        self.listener = None
        self.save_interval = save_interval
        self.screen_info = self.get_screen_info()
        self.timer = None
        self.position_time = {}
        self.left_click_count = 0
        self.right_click_count = 0
        self.left_click_positions = []
        self.right_click_positions = []
        self.color_map = {10: 'blue', 20: 'yellow', 35: 'orange', 45: 'red'}
        self.arrow_frequency = 3  # Draw an arrow for every third segment
        self._create_directory()
        self._start_save_timer()

    def _create_directory(self):
        os.makedirs(self.mouse_track_dir, exist_ok=True)

    def get_screen_info(self):
        try:
            screens = get_monitors()
            return [{'id': i, 'x': screen.x, 'y': screen.y, 'width': screen.width, 'height': screen.height}
                    for i, screen in enumerate(screens)]
        except Exception as e:
            logging.error(f"Error getting screen info: {e}")
            return [{'id': 0, 'x': 0, 'y': 0, 'width': 1920, 'height': 1080}]

    def start_tracking(self):
        self.listener = mouse.Listener(on_move=self.on_mouse_move, on_click=self.on_mouse_click)
        self.listener.start()
        logging.info("Mouse tracking started.")

    def stop_tracking(self):
        if self.listener:
            self.listener.stop()
            logging.info("Mouse tracking stopped.")
        self.stop_timer()

    def on_mouse_move(self, x, y):
        screen_id = self.get_screen_id(x, y)
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor_positions.append((x, y, screen_id))

    def on_mouse_click(self, x, y, button, pressed):
        if pressed:
            screen_id = self.get_screen_id(x, y)
            click_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if button == mouse.Button.left:
                self.left_click_count += 1
                self.left_click_positions.append((x, y, screen_id, click_time))
            elif button == mouse.Button.right:
                self.right_click_count += 1
                self.right_click_positions.append((x, y, screen_id, click_time))

    def get_screen_id(self, x, y):
        for screen in self.screen_info:
            if screen['x'] <= x < screen['x'] + screen['width'] and screen['y'] <= y < screen['y'] + screen['height']:
                return screen['id']
        return 0

    def save_cursor_track(self):
        timestamp = int(time.time())
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        json_data = {
            'timestamp': current_time,
            'positions': self.cursor_positions,
            'left_clicks': self.left_click_positions,
            'right_clicks': self.right_click_positions
        }
        json_path = os.path.join(self.mouse_track_dir, f'cursor_track_{timestamp}.json')
        with open(json_path, 'w') as f:
            json.dump(json_data, f)
        logging.info(f"Saved cursor track data: {json_path}")
        self.cursor_positions = []  # Reset cursor positions

    def _start_save_timer(self):
        self.timer = Timer(self.save_interval, self.save_cursor_track)
        self.timer.start()

    def stop_timer(self):
        if self.timer:
            self.timer.cancel()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    tracker = MouseTracker(save_interval=60)
    tracker.start_tracking()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        tracker.stop_tracking()
