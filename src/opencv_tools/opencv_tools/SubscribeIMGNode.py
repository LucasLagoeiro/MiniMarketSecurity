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

    self.haveInside = False
    self.inside = 0
    self.posX = 0
    self.countOfClassfication = 0
    self.countPeople = 0
    self.personPosList = []

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
    cv2.line(current_frame,(140,0),(140,current_frame.shape[1]),verde,3)
    cv2.line(current_frame,(200,0),(200,current_frame.shape[1]),verde,3)


    # for i in range(len(self.personPosList)):
    #   if self.personPosList[i].x > 140: self.haveInside = True
    #   else: self.haveInside = False

    #   if not self.haveInside: self.countOfClassfication -= 1

    # if self.haveInside: 
    #   self.inside = self.countOfClassfication

    # self.get_logger().info(str(self.inside))

    cv2.imshow("camera", current_frame)
    cv2.waitKey(1)

  def listener_callback_personPos(self, msg):
    self.get_logger().info('Receiving person pos')
    self.countOfClassfication = len(msg.detections)

    if not hasattr(self, 'personStates'): self.personStates = {}



    # self.personPosList = []
    # countPeople = 0
    for i in range(self.countOfClassfication): 
      isInside = msg.detections[i].bbox.center.position.inside
      # alreadyInside = msg.detections[i].bbox.center.position.alreadyinside
      posX = msg.detections[i].bbox.center.position.x


      alreadyInside = self.personStates.get(i, False)

      # self.personPosList.append(msg.detections[i].bbox.center.position)
      if posX > 140: isInside = True
      else: isInside = False

      if isInside and not alreadyInside: 
        self.countPeople+=1
        self.personStates[i] = True
      elif not isInside and alreadyInside:
        self.countPeople-=1
        self.personStates[i] = False
    
    self.get_logger().info(str(self.countPeople))
    self.get_logger().info(str(self.personStates))

    

    # self.get_logger().info(str(self.personPosList[0].x) + "\n -------------------------") 

    
   
def main(args=None):
  rclpy.init(args=args)
  image_subscriber = ImageSubscriber()
  rclpy.spin(image_subscriber)
  image_subscriber.destroy_node()
  rclpy.shutdown()
   
if __name__ == '__main__':
  main()