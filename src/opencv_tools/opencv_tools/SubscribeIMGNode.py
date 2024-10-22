import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

from std_srvs.srv import SetBool
from sensor_msgs.msg import Image
from yolov8_msgs.msg import Point2D
from yolov8_msgs.msg import BoundingBox2D
from yolov8_msgs.msg import Mask
from yolov8_msgs.msg import KeyPoint2D
from yolov8_msgs.msg import KeyPoint2DArray
from yolov8_msgs.msg import Detection
from yolov8_msgs.msg import DetectionArray

  
class ImageSubscriber(Node):
  
  def __init__(self):
    super().__init__('image_subscriber')
    self.goInside = False
    self.inside = 0
    self.subscription = self.create_subscription(
      Image, 
      '/yolo/dbg_image', 
      self.listener_callback, 
      10)
    self.subscription # prevent unused variable warning
    self.br = CvBridge()

    self.subscribePersonPos = self.create_subscription(DetectionArray, '/yolo/detections', self.listener_callback_personPos, 10)
    
  def listener_callback(self, data):
    self.get_logger().info('Receiving video frame')
    current_frame = self.br.imgmsg_to_cv2(data)
    print(current_frame.shape)
    verde = (0,255,0)
    cv2.line(current_frame,(160,0),(160,480),verde,3)
    cv2.line(current_frame,(200,0),(200,480),verde,3)

    if self.posX == 160: 
      self.goInside = True
    if self.posX == 200 and self.goInside: 
      self.inside += 1
      self.goInside = False

    cv2.imshow("camera", current_frame)
    cv2.waitKey(1)

  def listener_callback_personPos(self, msg):
    self.get_logger().info('Receiving person pos')
    self.get_logger().info(str(msg.detections[0].bbox.center.position.x)) 
    self.posX = msg.detections[0].bbox.center.position.x
    self.posY = msg.detections[0].bbox.center.position.y
   
def main(args=None):
  rclpy.init(args=args)
  image_subscriber = ImageSubscriber()
  rclpy.spin(image_subscriber)
  image_subscriber.destroy_node()
  rclpy.shutdown()
   
if __name__ == '__main__':
  main()