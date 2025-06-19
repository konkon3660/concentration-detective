# view/gui.py
import tkinter as tk
from tkinter import StringVar, Frame, Button, Label

class ConcentrationGUI:
    def __init__(self, root, toggle_buzzer_callback):
        self.root = root
        self.root.title("🧠 집중도 측정 시스템")
        self.root.geometry("600x400")
        self.root.configure(bg="#f0f0f0")

        # 메인 프레임
        main_frame = Frame(root, bg="#f0f0f0", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 제목
        title_label = Label(
            main_frame, 
            text="🧠 집중도 측정 시스템",
            font=("Arial", 20, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        title_label.pack(pady=(0, 20))

        # 상태 표시
        self.status_var = StringVar()
        self.status_var.set("시스템 초기화 중...")

        status_frame = Frame(main_frame, bg="white", relief=tk.RAISED, bd=2)
        status_frame.pack(fill=tk.X, pady=(0, 20))

        self.status_label = Label(
            status_frame, 
            textvariable=self.status_var, 
            font=("Consolas", 12),
            bg="white",
            fg="#34495e",
            justify=tk.LEFT,
            anchor="w",
            padx=15,
            pady=10
        )
        self.status_label.pack(fill=tk.X)

        # 컨트롤 버튼들
        button_frame = Frame(main_frame, bg="#f0f0f0")
        button_frame.pack(fill=tk.X, pady=(0, 20))

        self.buzzer_button = Button(
            button_frame,
            text="🔊 부저 ON/OFF",
            command=toggle_buzzer_callback,
            font=("Arial", 12, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            relief=tk.RAISED,
            bd=3,
            padx=20,
            pady=10
        )
        self.buzzer_button.pack(side=tk.LEFT, padx=(0, 10))

        # 종료 버튼
        quit_button = Button(
            button_frame,
            text="❌ 종료",
            command=self.root.quit,
            font=("Arial", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            activebackground="#c0392b",
            activeforeground="white",
            relief=tk.RAISED,
            bd=3,
            padx=20,
            pady=10
        )
        quit_button.pack(side=tk.RIGHT)

        # 정보 패널
        info_frame = Frame(main_frame, bg="white", relief=tk.RAISED, bd=2)
        info_frame.pack(fill=tk.BOTH, expand=True)

        info_title = Label(
            info_frame,
            text="📋 시스템 정보",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        info_title.pack(pady=(10, 5))

        info_text = """
🔍 PIR 센서: 움직임 감지로 자리 확인
💡 조도 센서: 주변 밝기 측정 (어두우면 LED 자동 점등)
⏰ 타이머: 착석 시간 자동 측정
⚠️  경고 시스템: 10초 후 1차 경고, 15초 후 부저 울림
🎛️  부저 제어: 언제든지 ON/OFF 가능
        """

        info_label = Label(
            info_frame,
            text=info_text.strip(),
            font=("Arial", 10),
            bg="white",
            fg="#34495e",
            justify=tk.LEFT
        )
        info_label.pack(pady=(5, 10))

    def update_status(self, status_text):
        """상태 텍스트 업데이트"""
        self.status_var.set(status_text)
        self.root.update_idletasks()

    def run(self):
        """GUI 실행"""
        self.root.mainloop()