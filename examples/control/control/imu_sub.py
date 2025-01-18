import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu


class IMUSubscriber(Node):
    def __init__(self):
        super().__init__("imu_subscriber_node")
        self.imuSub = self.create_subscription(
            Imu, "/model/auv4/imu", self.subscribe_imu, 10
        )

    def subscribe_imu(self, msg: Imu):
        self.get_logger().info(f"IMU Orientation: {msg.orientation}")


def main(args=None):
    rclpy.init(args=args)
    imu_subscriber = IMUSubscriber()
    rclpy.spin(imu_subscriber)
    imu_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == "main":
    main()
