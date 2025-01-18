import rclpy
from control.thrust_pub import MultiThrustPublisher
from rclpy.node import Node


class MoveFrontPublisher(Node):
    def __init__(self, thrust_value):
        super().__init__("move_front_publisher_node")
        self.thrust_value = thrust_value
        self.thrust_pub = MultiThrustPublisher()
        self.timer = self.create_timer(1.0, self.publish_thrust)

    def publish_thrust(self):
        thrust_values = [
            self.thrust_value,
            self.thrust_value,
            0,
            0,
            self.thrust_value,
            self.thrust_value,
            5.0,
        ]
        self.thrust_pub.publish_thrust(thrust_values)


def main(args=None):
    rclpy.init(args=args)
    moveFrontPublisher = MoveFrontPublisher(2.0)
    rclpy.spin(moveFrontPublisher)
    moveFrontPublisher.destroy_node()
    rclpy.shutdown()


if __name__ == "main":
    main()
