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
        default_value='/human_image_raw',
        description='Tópico de entrada para imagens'
    )

    device_arg = DeclareLaunchArgument(
        'device',
        default_value='cpu',
        description='Dispositivo para processamento (e.g., cuda:0, cpu)'
    )

    # Configuração do launch principal
    yolov8_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare('yolov8_bringup'), '/launch/yolov8.launch.py'
        ]),
        launch_arguments={
            'input_image_topic': LaunchConfiguration('input_image_topic'),
            'device': LaunchConfiguration('device')
        }.items()
    )
    
    pub_video_node = Node(
        name='publisherHumanVIDEO',
        package='opencv_tools',
        executable='publisherHumanVIDEO'
    )

    sub_video_node = Node(
        name='subscribeHumanVIDEO',
        package='opencv_tools',
        executable='subscribeHumanVIDEO'
    )

    


    # Retornar a descrição do launch
    return LaunchDescription([
        input_image_topic_arg,
        device_arg,
        yolov8_launch,
        pub_video_node,
        sub_video_node
    ])