from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, GroupAction
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    # Declaração de argumentos
    input_image_topic_arg = DeclareLaunchArgument(
        'input_image_topic',
        default_value='/tomato_image_raw',
        description='Tópico de entrada para imagens'
    )

    device_arg = DeclareLaunchArgument(
        'device',
        default_value='cpu',
        description='Dispositivo para processamento (e.g., cuda:0, cpu)'
    )

    detect_arg = DeclareLaunchArgument(
        'detect',
        default_value='food',
        description='O que voce vai detectar (e.g., human, food)'
    )

    model_arg = DeclareLaunchArgument(
        'model',
        default_value='weightsFoods/best.pt',
        description='Caminho para o modelo da YOLO'
    )    

    # Configuração do launch principal
    yolov8_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare('yolov8_bringup'), '/launch/yolov8.launch.py'
        ]),
        launch_arguments={
            'input_image_topic': LaunchConfiguration('input_image_topic'),
            'device': LaunchConfiguration('device'),
            'detect': LaunchConfiguration('detect'),
            'model': LaunchConfiguration('model')
        }.items()
    )
    
    pub_video_node = Node(
        name='publisherTomatoVIDEO',
        package='opencv_tools',
        executable='publisherTomatoVIDEO'
    )

    sub_video_node = Node(
        name='subscribeTomatoVIDEO',
        package='opencv_tools',
        executable='subscribeTomatoVIDEO'
    )

    


    # Retornar a descrição do launch
    return LaunchDescription([
        input_image_topic_arg,
        device_arg,
        detect_arg,
        model_arg,
        yolov8_launch,
        pub_video_node,
        sub_video_node,

    ])