import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/robo/llagoeiro/MiniMarketSecurity/install/opencv_tools'
