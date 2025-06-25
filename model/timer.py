# 공부 시간 측정
import time  # 시간 측정용

class StudyTimer:
    def __init__(self):
        self.start_time = None         # 타이머 시작 시각
        self.total_study_time = 0      # 누적 공부 시간(초)
        self.running = False           # 타이머 동작 여부

    def start(self):
        """타이머 시작 (이미 동작 중이면 무시)"""
        if not self.running:
            self.start_time = time.time()
            self.running = True

    def stop(self):
        """타이머 정지 및 누적 시간 저장"""
        if self.running:
            self.total_study_time += time.time() - self.start_time
            self.running = False

    def reset(self):
        """타이머 및 누적 시간 초기화"""
        self.start_time = None
        self.total_study_time = 0
        self.running = False

    def get_study_time(self):
        """현재까지의 누적 공부 시간(초) 반환"""
        if self.running:
            return self.total_study_time + (time.time() - self.start_time)
        return self.total_study_time
