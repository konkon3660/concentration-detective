# config/pins.py
# 모든 핀 번호를 한 곳에서 관리

# 센서 핀
PIR_SENSOR_PIN = 17      # PIR 모션 센서
LIGHT_SENSOR_CH = 0      # 조도센서 (MCP3008 CH0)

# 액츄에이터 핀
LED_PIN = 23             # LED
BUZZER_PIN = 18          # 부저

# SPI 설정 (MCP3008)
SPI_BUS = 0
SPI_DEVICE = 0
SPI_MAX_SPEED = 1350000

# 타이밍 설정
MOTION_WARNING_TIME = 10  # 1차 경고 시간 (초)
MOTION_BUZZER_TIME = 15   # 2차 경고 시간 (초)
SENSOR_CHECK_INTERVAL = 1 # 센서 체크 간격 (초)

# 조도 센서 임계값
LIGHT_DARK_THRESHOLD = 200  # 이 값 이하면 어두운 것으로 판정