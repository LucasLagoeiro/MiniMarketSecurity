import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import os

class ImageSaver(Node):
    def __init__(self):
        super().__init__('image_saver')
        # Substitua pelo seu tópico de imagem
        self.subscription = self.create_subscription(
            Image,
            '/yolo/dbg_image_food',  # Nome do tópico
            self.listener_callback,
            10)
        self.bridge = CvBridge()
        self.frame_count = 0
        self.output_dir = "./frames"
        os.makedirs(self.output_dir, exist_ok=True)
        self.get_logger().info("ImageSaver node initialized. Listening to the topic")

    def listener_callback(self, msg):
        try:
            # Tratamento do encoding 8UC3
            if msg.encoding == "8UC3":
                cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")
                # Converte para BGR, caso necessário
                # cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)
            else:
                cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")

            # Nome do arquivo e salvamento
            frame_path = os.path.join(self.output_dir, f"frame_{self.frame_count:04d}.jpg")
            cv2.imwrite(frame_path, cv_image)
            self.get_logger().info(f"Frame salvo: {frame_path}")
            self.frame_count += 1

        except Exception as e:
            self.get_logger().error(f"Erro ao processar a imagem: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = ImageSaver()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Node encerrado.")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
