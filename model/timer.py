# 공부 시간 측정
import time

class StudyTimer:
    def __init__(self):
        self.start_time = None
        self.total_study_time = 0
        self.running = False

    def start(self):
        if not self.running:
            self.start_time = time.time()
            self.running = True

    def stop(self):
        if self.running:
            self.total_study_time += time.time() - self.start_time
            self.running = False

    def reset(self):
        self.start_time = None
        self.total_study_time = 0
        self.running = False

    def get_study_time(self):
        if self.running:
            return self.total_study_time + (time.time() - self.start_time)
        return self.total_study_time
