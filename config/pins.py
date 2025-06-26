# config/pins.py
# 모든 핀 번호를 한 곳에서 관리

# 센서 핀
PIR_SENSOR_PIN = 17      # PIR 모션 센서

# 액츄에이터 핀
LED_PIN = 23             # LED
BUZZER_PIN = 18          # 부저

# 타이밍 설정
MOTION_WARNING_TIME = 10  # 1차 경고 시간 (초)
MOTION_BUZZER_TIME = 15   # 2차 경고 시간 (초)
SENSOR_CHECK_INTERVAL = 1 # 센서 체크 간격 (초)