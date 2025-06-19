# 타이머, 센서 상태
import threading
import time
import tkinter as tk
from model import sensors, actuators, timer
from view.gui import ConcentrationGUI

class ConcentrationController:
    def __init__(self):
        self.timer = timer.StudyTimer()
        self.buzzer_enabled = True
        self.gui = ConcentrationGUI(tk.Tk(), self.toggle_buzzer)
        self.motion_last_time = time.time()
        self.warning_issued = False

    def toggle_buzzer(self):
        self.buzzer_enabled = not self.buzzer_enabled
        self.gui.update_status(f"부저 {'활성화' if self.buzzer_enabled else '비활성화'}")

    def monitor_loop(self):
        while True:
            motion = sensors.is_motion_detected()
            dark = sensors.is_dark()

            if motion:
                self.motion_last_time = time.time()
                self.warning_issued = False
                self.timer.start()
            else:
                if time.time() - self.motion_last_time > 10:
                    self.gui.update_status("⚠️ 1차 경고: 움직임 없음")
                    if time.time() - self.motion_last_time > 15 and self.buzzer_enabled:
                        if not self.warning_issued:
                            actuators.buzzer_on()
                            time.sleep(1)
                            actuators.buzzer_off()
                            self.warning_issued = True

            if dark:
                actuators.led_on()
            else:
                actuators.led_off()

            time.sleep(1)

    def run(self):
        threading.Thread(target=self.monitor_loop, daemon=True).start()
        self.gui.run()
