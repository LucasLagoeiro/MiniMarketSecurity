import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from yolov8_msgs.msg import DetectionPerson, DetectionTomato


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')

        #pubs
        self.publisher_ = self.create_publisher(DetectionPerson, 'steal', 10)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

        #subs
        self.inside = False
        self.count_person = []
        self.subscriberPerson = self.create_subscription(
            DetectionPerson, 
            '/yolo/is_inside', 
            self.subscriber_person_cb,
            10)
        
        self.shelf = False
        self.pay = False
        self.subscriberTomato = self.create_subscription(
            DetectionTomato,
            'yolo/pay',
            self.subscriber_tomato_cb,
            10
        )


    def subscriber_person_cb(self,msg):
        self.inside = msg.inside
        self.count_person = msg.count_people.data


    def subscriber_tomato_cb(self,msg):
        self.shelf = msg.shelf
        self.pay = msg.pay

    def timer_callback(self):
        msg = DetectionPerson()
        msg.steal = False
        
        if not self.inside and not self.shelf and not self.pay:
            msg.steal = True
        else:
            msg.steal = False  

        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()