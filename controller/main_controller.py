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

            # 🔧 콘솔 로그
            print(f"[센서 상태] 움직임: {'감지됨' if motion else '없음'}, 조도: {'어두움' if dark else '밝음'}")

            # 🔧 GUI 상태 표시 문자열 구성
            status = f"움직임: {'감지됨' if motion else '없음'} | 조도: {'어두움' if dark else '밝음'}"

            # 움직임 감지 로직
            if motion:
                self.motion_last_time = time.time()
                self.warning_issued = False
                self.timer.start()
            else:
                elapsed = time.time() - self.motion_last_time
                if elapsed > 10:
                    print("[경고] 1차 경고: 움직임 없음")
                    status += " | ⚠️ 1차 경고"
                    if elapsed > 15 and self.buzzer_enabled:
                        if not self.warning_issued:
                            print("[경고] 2차 경고: 부저 작동")
                            actuators.buzzer_on()
                            time.sleep(1)
                            actuators.buzzer_off()
                            self.warning_issued = True
                            status += " | 🔊 부저 울림"

        # 조도에 따라 LED 제어
        if dark:
            actuators.led_on()
            print("[출력] LED ON")
            status += " | LED: ON"
        else:
            actuators.led_off()
            print("[출력] LED OFF")
            status += " | LED: OFF"

        # 🔧 GUI 업데이트
        self.gui.update_status(status)

        time.sleep(1)

    def run(self):
        threading.Thread(target=self.monitor_loop, daemon=True).start()
        self.gui.run()
