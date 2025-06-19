import tkinter as tk
from tkinter import StringVar

class ConcentrationGUI:
    def __init__(self, root, toggle_buzzer_callback):
        self.root = root
        self.root.title("집중도 측정 시스템")

        # 라즈베리파이에서 전체화면
        self.root.attributes('-fullscreen', True)  # ESC 키로 종료 가능

        # 전체 프레임 (중앙 정렬)
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(expand=True)

        # 상태 표시 라벨 (제목)
        self.status_var = StringVar(value="시스템 대기 중...")
        self.status_label = tk.Label(self.main_frame, textvariable=self.status_var,
                                      font=("NanumGothic", 36), justify='center')
        self.status_label.pack(pady=40)

        # 센서값 표시
        self.light_var = StringVar(value="조도: -")
        self.pir_var = StringVar(value="자리 감지: -")
        self.time_var = StringVar(value="공부 시간: -")

        self.light_label = tk.Label(self.main_frame, textvariable=self.light_var, font=("NanumGothic", 28))
        self.pir_label = tk.Label(self.main_frame, textvariable=self.pir_var, font=("NanumGothic", 28))
        self.time_label = tk.Label(self.main_frame, textvariable=self.time_var, font=("NanumGothic", 28))

        self.light_label.pack(pady=10)
        self.pir_label.pack(pady=10)
        self.time_label.pack(pady=10)

        # 부저 제어 버튼
        self.buzzer_button = tk.Button(self.main_frame, text="🔔 부저 ON/OFF",
                                        font=("NanumGothic", 24), command=toggle_buzzer_callback)
        self.buzzer_button.pack(pady=30)

        # 종료용 ESC 바인딩
        self.root.bind("<Escape>", lambda event: self.root.destroy())

    def update_status(self, status_text):
        self.status_var.set(status_text)

    def update_sensor_values(self, light=None, pir=None, time_min=None):
        if light is not None:
            self.light_var.set(f"조도: {light}")
        if pir is not None:
            self.pir_var.set(f"자리 감지: {'감지됨' if pir else '없음'}")
        if time_min is not None:
            self.time_var.set(f"공부 시간: {time_min}분")

    def run(self):
        self.root.mainloop()
