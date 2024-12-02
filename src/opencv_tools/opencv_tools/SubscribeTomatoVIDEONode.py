import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from yolov8_msgs.msg import DetectionArray, DetectionTomato

  
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

    self.shelf = False
    self.pay = False

    self.subscribePersonPos = self.create_subscription(DetectionArray, '/yolo/detections_food', self.listener_callback_foodPos, 10)
    self.publisherFood = self.create_publisher(DetectionTomato, 'yolo/pay',10)
    self.timer = self.create_timer(0.1, self.publish_food)

    
  def listener_callback(self, data):
    self.get_logger().info('Receiving video frame')

    azul = (255, 0, 0)
    verde = (0, 255, 0)
    vermelho = (0, 0, 255)
    roxo = (255, 0, 255)

    current_frame = self.br.imgmsg_to_cv2(data)


    # # área pra passar o produto
    # cv2.rectangle(current_frame, (250, 450), (700, 970), verde, 5)

    # # área onde o produto vai ficar
    # cv2.rectangle(current_frame, (600, 50), (900, 350), roxo, 5)


    cv2.imshow("camera", current_frame)
    cv2.waitKey(1)


  def listener_callback_foodPos(self, msg):
    self.get_logger().info('Receiving food pos')
    self.countOfClassfication = len(msg.detections)

    for i in range(self.countOfClassfication): 
      posX = msg.detections[i].bbox.center.position.x
      posY = msg.detections[i].bbox.center.position.y
      # self._logger.info("X: " + str(posX) + " Y: " + str(posY))

      # faz a verificação se tá no espaço desejado
      if (600 < posX < 900) and (50 < posY < 350):
          self.shelf = True
          self._logger.info('\n\n\nO PRODUTO ESTÁ NA PRATELEIRA\n\n\n')
          break
      else:
          self.shelf = False

      # faz a verificação se foi pago
      if not self.shelf:
          if (250 < posX < 700) and (450 < posY < 970):
              self.pay = True

          if not self.pay:
              self._logger.info('\n\n\nPRODUTO NÃO FOI PAGO\n\n\n')
          if self.pay:
              self._logger.info('\n\n\nPRODUTO PAGO\n\n\n')
              break
          break
  def publish_food(self):
    msg = DetectionTomato()

    msg.shelf = self.shelf
    msg.pay = self.pay

    self.publisherFood.publish(msg)



   
def main(args=None):
  rclpy.init(args=args)
  image_subscriber = ImageSubscriber()
  rclpy.spin(image_subscriber)
  image_subscriber.destroy_node()
  rclpy.shutdown()
   
if __name__ == '__main__':
  main()