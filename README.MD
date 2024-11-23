<h1>Commands</h1>

<h3>To run yolo detect<h3>

human:

ros2 launch yolov8_bringup yolov8.launch.py input_image_topic:=/human_image_raw device:=cpu

food:

ros2 launch yolov8_bringup yolov8.launch.py input_image_topic:=/tomato_image_raw device:=cpu detect:=tomato model:=weightsFoods/best.pt


<h3>To pause/play the emulation of people entering:<h3>

ros2 topic pub /video_control std_msgs/String "data: 'play'"

 
