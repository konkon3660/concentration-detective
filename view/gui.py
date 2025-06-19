# tkinter GUI 구성
import tkinter as tk
from tkinter import StringVar

class ConcentrationGUI:
    def __init__(self, root, toggle_buzzer_callback):
        self.root = root
        self.root.title("집중도 측정 시스템")

        self.status_var = StringVar()
        self.status_var.set("시스템 대기 중...")

        self.label = tk.Label(root, textvariable=self.status_var, font=("Arial", 16))
        self.label.pack(pady=10)

        self.buzzer_button = tk.Button(root, text="부저 ON/OFF", command=toggle_buzzer_callback)
        self.buzzer_button.pack(pady=5)

    def update_status(self, status_text):
        self.status_var.set(status_text)

    def run(self):
        self.root.mainloop()
