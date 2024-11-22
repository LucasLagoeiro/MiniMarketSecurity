import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
  
class ImagePublisher(Node):
  
  def __init__(self):
    super().__init__('image_publisher')
    self.publisher_ = self.create_publisher(Image, 'tomato_image_raw', 10)
    

    self.cap = cv2.VideoCapture('/home/llagoeiro/Desktop/FEI/8_semestre/VisaoComputacionalFolder/projeto-visaoComputaria/src/opencv_tools/data/tomatoInHome.mp4')
    video_fps = self.cap.get(cv2.CAP_PROP_FPS)
    self.get_logger().info(f'FPS original do vídeo: {video_fps}')

    timer_period = 1 / (video_fps-1)
    self.timer = self.create_timer(timer_period, self.timer_callback)


    #self.cap = cv2.imread('/home/robo/llagoeiro/MiniMarketSecurity/src/opencv_tools/opencv_tools/image.png')


    if not self.cap.isOpened(): self.get_logger().error('Error opening video stream or file')

    self.br = CvBridge()
    
  def timer_callback(self):
    ret, frame = self.cap.read()
    if ret == True:
      print(frame.shape)
      frame_resized = cv2.resize(frame, (1280,720))
      print(frame_resized.shape)
      self.publisher_.publish(self.br.cv2_to_imgmsg(frame))
      self.get_logger().info('Publishing video frame')
    else:
      # Reinicia o vídeo se chegar ao final
      self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
   
def main(args=None):
  rclpy.init(args=args)
  image_publisher = ImagePublisher()
  rclpy.spin(image_publisher)
  image_publisher.destroy_node()
  rclpy.shutdown()
   
if __name__ == '__main__':
  main()