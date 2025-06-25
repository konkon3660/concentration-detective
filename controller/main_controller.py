# controller/main_controller.py
import threading  # 멀티스레딩 사용
import time       # 시간 측정 및 sleep
import tkinter as tk  # GUI
from model import sensors, actuators, timer  # 센서/액추에이터/타이머 모듈
from view.gui import ConcentrationGUI        # GUI 클래스
from config.pins import MOTION_WARNING_TIME, MOTION_BUZZER_TIME, SENSOR_CHECK_INTERVAL  # 설정값

class ConcentrationController:
    def __init__(self):
        self.timer = timer.StudyTimer()  # 공부 시간 측정용 타이머 인스턴스
        self.buzzer_enabled = True       # 부저 활성화 여부
        self.gui = ConcentrationGUI(tk.Tk(), self.toggle_buzzer)  # GUI 인스턴스 생성 및 부저 토글 콜백 연결
        self.motion_last_time = time.time()  # 마지막 움직임 감지 시각
        self.warning_issued = False      # 2차 경고(부저) 발생 여부
        self.running = True              # 메인 루프 실행 플래그

    def toggle_buzzer(self):
        """부저 ON/OFF 토글 및 상태 업데이트"""
        self.buzzer_enabled = not self.buzzer_enabled  # 부저 상태 반전
        status = f"부저 {'활성화' if self.buzzer_enabled else '비활성화'}"  # 상태 문자열 생성
        self.gui.update_status(status)  # GUI 상태 표시
        self.gui.update_buzzer_button(self.buzzer_enabled)  # 버튼 시각적 동기화
        print(f"[설정] {status}")  # 콘솔 로그

    def monitor_loop(self):
        """센서 모니터링 및 제어 메인 루프 (별도 스레드)"""
        while self.running:
            try:
                # 센서 값 읽기
                motion = sensors.is_motion_detected()  # PIR 센서: 움직임 감지
                dark = sensors.is_dark()               # 조도 센서: 어두운지 판정
                light_value = sensors.get_light_value()  # 조도 센서: ADC 값

                # 콘솔 로그 출력
                print(f"[센서] 움직임: {'감지' if motion else '없음'} | "
                      f"조도: {light_value:4d} ({'어두움' if dark else '밝음'})")

                # GUI 상태 문자열 구성
                status = f"움직임: {'감지됨' if motion else '없음'} | "
                status += f"조도: {light_value} ({'어두움' if dark else '밝음'})"

                # 움직임 감지 로직
                if motion:
                    self.motion_last_time = time.time()  # 마지막 감지 시각 갱신
                    self.warning_issued = False          # 경고 플래그 초기화
                    self.timer.start()                   # 공부 시간 측정 시작
                    print("[타이머] 공부 시간 측정 시작")
                else:
                    elapsed = time.time() - self.motion_last_time  # 마지막 감지 후 경과 시간
                    if elapsed > MOTION_WARNING_TIME:
                        print(f"[경고] 1차 경고: {elapsed:.1f}초간 움직임 없음")
                        status += " | ⚠️ 1차 경고"  # 1차 경고 GUI 표시
                        if elapsed > MOTION_BUZZER_TIME and self.buzzer_enabled:
                            if not self.warning_issued:
                                print("[경고] 2차 경고: 부저 작동")
                                actuators.get_actuator_manager().buzzer_beep(1.0)  # 부저 1초 울림
                                self.warning_issued = True
                                status += " | 🔊 부저 울림"  # 2차 경고 GUI 표시

                # 조도에 따른 LED 제어
                if dark:
                    actuators.led_on()  # 어두우면 LED ON
                    status += " | LED: ON"
                else:
                    actuators.led_off()  # 밝으면 LED OFF
                    status += " | LED: OFF"

                # 공부 시간 표시
                study_time = self.timer.get_study_time()  # 누적 공부 시간(초)
                if study_time > 0:
                    minutes = int(study_time // 60)
                    seconds = int(study_time % 60)
                    status += f" | 공부시간: {minutes:02d}:{seconds:02d}"

                # GUI 상태 업데이트
                self.gui.update_status(status)
            except Exception as e:
                import traceback
                err_msg = f"[오류] 센서 읽기 실패: {e}\n{traceback.format_exc()}"  # 상세 오류
                print(err_msg)
                self.gui.update_status(f"센서 오류 발생: {e}")  # GUI에도 표시
            time.sleep(SENSOR_CHECK_INTERVAL)  # 주기적 반복

    def cleanup(self):
        """리소스 정리 및 종료 처리"""
        print("\n[시스템] 정리 중...")
        self.running = False  # 루프 종료
        sensors.get_sensor_manager().cleanup()  # 센서 리소스 해제
        actuators.get_actuator_manager().cleanup()  # 액추에이터 리소스 해제
        print("[시스템] 정리 완료")

    def run(self):
        """시스템 전체 실행 (메인 진입점)"""
        try:
            print("[시스템] 집중도 측정 시스템 시작")
            threading.Thread(target=self.monitor_loop, daemon=True).start()  # 센서 모니터링 스레드 시작
            self.gui.update_buzzer_button(self.buzzer_enabled)  # 부저 버튼 상태 동기화
            self.gui.run()  # GUI 메인루프 실행
        except KeyboardInterrupt:
            print("\n[시스템] 사용자 중단")
        finally:
            self.cleanup()  # 종료 시 리소스 정리