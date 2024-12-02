import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge
import cv2
  
class ImagePublisher(Node):
  
  def __init__(self):
    super().__init__('image_publisher')
    self.publisher_ = self.create_publisher(Image, 'human_image_raw', 10)
    

    self.cap = cv2.VideoCapture('src/opencv_tools/data/enterInMarket.mp4')
    video_fps = self.cap.get(cv2.CAP_PROP_FPS)
    # self.get_logger().info(f'FPS original do vídeo: {video_fps}')

    timer_period = 1 / (video_fps-1)
    self.timer = self.create_timer(timer_period, self.timer_callback)


    if not self.cap.isOpened(): self.get_logger().error('Error opening video stream or file')

    self.br = CvBridge()
    self.is_paused = False  # Variável de controle para pausa

            # Subscription para controlar play/pause
    self.subscription = self.create_subscription(
            String, 'video_control', self.control_callback, 10)
    
  def timer_callback(self):
    if not self.is_paused:
      ret, frame = self.cap.read()
      if ret == True:
        # print(frame.shape)
        frame_resized = cv2.resize(frame, (1280,720))
        # print(frame_resized.shape)
        self.publisher_.publish(self.br.cv2_to_imgmsg(frame_resized))
        self.get_logger().info('Publishing video frame')
      else:
        # Reinicia o vídeo se chegar ao final
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    else:
      self.get_logger().info("Video paused")

  def control_callback(self, msg):
      command = msg.data  # Supondo que o dado recebido seja 'play' ou 'pause'
      if command == "pause":
          self.is_paused = True
          self.get_logger().info('Video paused')
      elif command == "play":
          self.is_paused = False
          self.get_logger().info('Video resumed')

   
def main(args=None):
  rclpy.init(args=args)
  image_publisher = ImagePublisher()
  rclpy.spin(image_publisher)
  image_publisher.destroy_node()
  rclpy.shutdown()
   
if __name__ == '__main__':
  main()