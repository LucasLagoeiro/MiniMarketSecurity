import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import json

from std_srvs.srv import SetBool
from sensor_msgs.msg import Image
from yolov8_msgs.msg import Point2D
from yolov8_msgs.msg import BoundingBox2D
from yolov8_msgs.msg import Mask
from yolov8_msgs.msg import KeyPoint2D
from yolov8_msgs.msg import KeyPoint2DArray
from yolov8_msgs.msg import Detection
from yolov8_msgs.msg import DetectionArray
from yolov8_msgs.msg import DetectionPerson

import time

  
class ImageSubscriber(Node):
  
  def __init__(self):
    super().__init__('image_subscriber')

    self.countOfClassfication = 0
    self.countPeople = 0
    self.personStates = {}
    self.exitTimes = {}
    self.personOut = []
    self.isInside = False

    #subs
    self.subscription = self.create_subscription(
      Image, 
      '/yolo/dbg_image_human', 
      self.listener_callback, 
      10)
    self.subscription # prevent unused variable warning
    self.br = CvBridge()

    self.subscribePersonPos = self.create_subscription(
      DetectionArray, 
      '/yolo/detections_human', 
      self.listener_callback_personPos, 
      10)

    #pubs
    self.publisherPersonPos = self.create_publisher(DetectionPerson,'/yolo/is_inside',10)
    self.timer = self.create_timer(0.1, self.publish_person)

    
  def listener_callback(self, data):
    self.get_logger().info('Receiving video frame')
    current_frame = self.br.imgmsg_to_cv2(data)
    print(current_frame.shape)
    
    verde = (0,255,0)
    cv2.line(current_frame,(600,0),(600,current_frame.shape[1]),verde,3)

    cv2.imshow("camera", current_frame)
    cv2.waitKey(1)

  def listener_callback_personPos(self, msg):
    self.get_logger().info('Receiving person pos')
    self.countOfClassfication = len(msg.detections)



    for i in range(self.countOfClassfication): 
      posX = msg.detections[i].bbox.center.position.x


      alreadyInside = self.personStates.get(i, False)

      # self.personPosList.append(msg.detections[i].bbox.center.position)
      if posX > 600: 
        self.isInside = True 
      else: 
        self.isInside = False

      if self.isInside and not alreadyInside: 
        self.countPeople+=1
        self.personStates[i] = True
        if i in self.exitTimes: del self.exitTimes[i]
      elif not self.isInside and alreadyInside:
        self.countPeople-=1
        self.personStates[i] = False
        self.exitTimes[i] = time.time() 


    time_limitOut = 3
    
    # Verificar o tempo decorrido e remover pessoas que saíram há mais de 'time_limit' segundos
    # list comprehension = [nova_lista_item for item in iterável if condição]
    keys_to_remove = [key for key, exit_time in self.exitTimes.items() if time.time() - exit_time > time_limitOut]

    for key in keys_to_remove:
      del self.personStates[key]
      del self.exitTimes[key]

    
    # self.get_logger().info("Contagem: " + str(self.countPeople))
    # self.get_logger().info("Inside: " + str(self.personStates))
    # self.get_logger().info("Pessoas que sairam: " + str(keys_to_remove))

      
  def publish_person(self):
    msg = DetectionPerson()

    # Serializando o dicionário para JSON
    json_data = json.dumps(self.personStates)
    msg.count_people.data = json_data
    msg.inside = self.isInside
    
    self.publisherPersonPos.publish(msg)

    
   
def main(args=None):
  rclpy.init(args=args)
  image_subscriber = ImageSubscriber()
  rclpy.spin(image_subscriber)
  image_subscriber.destroy_node()
  rclpy.shutdown()
   
if __name__ == '__main__':
  main()