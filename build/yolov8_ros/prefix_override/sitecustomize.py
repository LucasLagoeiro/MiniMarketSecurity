import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/llagoeiro/Desktop/FEI/8_semestre/VisaoComputacionalFolder/projeto-visaoComputaria/install/yolov8_ros'
