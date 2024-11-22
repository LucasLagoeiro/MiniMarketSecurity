import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from yolov8_msgs.msg import DetectionArray

  
class ImageSubscriber(Node):
  
  def __init__(self):
    super().__init__('image_subscriber')
    self.subscription = self.create_subscription(
      Image, 
      '/yolo/dbg_image_food', 
      self.listener_callback, 
      10)
    self.subscription # prevent unused variable warning
    self.br = CvBridge()
    self.subscribePersonPos = self.create_subscription(DetectionArray, '/yolo/detections_food', self.listener_callback_foodPos, 10)

    
  def listener_callback(self, data):
    self.get_logger().info('Receiving video frame')

    azul = (255, 0, 0)
    verde = (0, 255, 0)
    vermelho = (0, 0, 255)
    roxo = (255, 0, 255)

    current_frame = self.br.imgmsg_to_cv2(data)


    # área pra passar o produto
    cv2.rectangle(current_frame, (650, 450), (1100, 720), verde, 5)
    # # círculo pra marcar o centro
    # cv2.circle(current_frame, center=(100, 150), radius=2, color=vermelho, thickness=5)

    # área onde o produto vai ficar
    cv2.rectangle(current_frame, (900, 100), (1200, 350), roxo, 5)
    # # círculo pra marcar o centro
    # cv2.circle(current_frame, center=(400, 150), radius=2, color=vermelho, thickness=5)


    cv2.imshow("camera", current_frame)
    cv2.waitKey(1)


  def listener_callback_foodPos(self, msg):
    self.get_logger().info('Receiving food pos')
    self.countOfClassfication = len(msg.detections)

    for i in range(self.countOfClassfication): 
      posX = msg.detections[i].bbox.center.position.x
      posY = msg.detections[i].bbox.center.position.y
      self._logger.info("X: " + str(posX) + " Y: " + str(posY))


   
def main(args=None):
  rclpy.init(args=args)
  image_subscriber = ImageSubscriber()
  rclpy.spin(image_subscriber)
  image_subscriber.destroy_node()
  rclpy.shutdown()
   
if __name__ == '__main__':
  main()