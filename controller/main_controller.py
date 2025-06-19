# controller/main_controller.py
import threading
import time
import tkinter as tk
from model import sensors, actuators, timer
from view.gui import ConcentrationGUI
from config.pins import MOTION_WARNING_TIME, MOTION_BUZZER_TIME, SENSOR_CHECK_INTERVAL

class ConcentrationController:
    def __init__(self):
        self.timer = timer.StudyTimer()
        self.buzzer_enabled = True
        self.gui = ConcentrationGUI(tk.Tk(), self.toggle_buzzer)
        self.motion_last_time = time.time()
        self.warning_issued = False
        self.running = True

    def toggle_buzzer(self):
        """부저 토글 및 상태 업데이트"""
        self.buzzer_enabled = not self.buzzer_enabled
        status = f"부저 {'활성화' if self.buzzer_enabled else '비활성화'}"
        self.gui.update_status(status)
        print(f"[설정] {status}")

    def monitor_loop(self):
        """센서 모니터링 메인 루프"""
        while self.running:
            try:
                # 센서 값 읽기
                motion = sensors.is_motion_detected()
                dark = sensors.is_dark()
                light_value = sensors.get_light_value()

                # 콘솔 로그
                print(f"[센서] 움직임: {'감지' if motion else '없음'} | "
                      f"조도: {light_value:4d} ({'어두움' if dark else '밝음'})")

                # GUI 상태 문자열 구성
                status = f"움직임: {'감지됨' if motion else '없음'} | "
                status += f"조도: {light_value} ({'어두움' if dark else '밝음'})"

                # 움직임 감지 로직
                if motion:
                    self.motion_last_time = time.time()
                    self.warning_issued = False
                    self.timer.start()
                    print("[타이머] 공부 시간 측정 시작")
                else:
                    elapsed = time.time() - self.motion_last_time
                    
                    if elapsed > MOTION_WARNING_TIME:
                        print(f"[경고] 1차 경고: {elapsed:.1f}초간 움직임 없음")
                        status += " | ⚠️ 1차 경고"
                        
                        if elapsed > MOTION_BUZZER_TIME and self.buzzer_enabled:
                            if not self.warning_issued:
                                print("[경고] 2차 경고: 부저 작동")
                                actuators.get_actuator_manager().buzzer_beep(1.0)
                                self.warning_issued = True
                                status += " | 🔊 부저 울림"

                # 조도에 따른 LED 제어
                if dark:
                    actuators.led_on()
                    status += " | LED: ON"
                else:
                    actuators.led_off()
                    status += " | LED: OFF"

                # 공부 시간 추가
                study_time = self.timer.get_study_time()
                if study_time > 0:
                    minutes = int(study_time // 60)
                    seconds = int(study_time % 60)
                    status += f" | 공부시간: {minutes:02d}:{seconds:02d}"

                # GUI 업데이트
                self.gui.update_status(status)

            except Exception as e:
                print(f"[오류] 센서 읽기 실패: {e}")
                self.gui.update_status("센서 오류 발생")

            time.sleep(SENSOR_CHECK_INTERVAL)

    def cleanup(self):
        """리소스 정리"""
        print("\n[시스템] 정리 중...")
        self.running = False
        sensors.get_sensor_manager().cleanup()
        actuators.get_actuator_manager().cleanup()
        print("[시스템] 정리 완료")

    def run(self):
        """시스템 실행"""
        try:
            print("[시스템] 집중도 측정 시스템 시작")
            threading.Thread(target=self.monitor_loop, daemon=True).start()
            self.gui.run()
        except KeyboardInterrupt:
            print("\n[시스템] 사용자 중단")
        finally:
            self.cleanup()