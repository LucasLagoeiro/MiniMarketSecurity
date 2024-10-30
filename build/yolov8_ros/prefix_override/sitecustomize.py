import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/robo/Desktop/lagoeiro/MiniMarketSecurity/MiniMarketSecurity/install/yolov8_ros'
