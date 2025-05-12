import rclpy
from nav_msgs.msg import Odometry
from rclpy.node import Node


class OdomToNED(Node):
    # Converts sim odometry (NWU) to NED frame

    def __init__(self):
        super().__init__('odom_to_ned')
        self.sub = self.create_subscription(Odometry, '/auv4/odometry', self.cb, 10)
        self.pub = self.create_publisher(Odometry, '/auv4/nav/odom_ned', 10)

    def cb(self, msg: Odometry):
        ned_msg = Odometry()
        ned_msg.header = msg.header

        # Position
        ned_msg.pose.pose.position.x = msg.pose.pose.position.x
        ned_msg.pose.pose.position.y = -msg.pose.pose.position.y
        ned_msg.pose.pose.position.z = -msg.pose.pose.position.z

        # Flip orientation: q_ned = [w, x, -y, -z]
        q = msg.pose.pose.orientation
        ned_msg.pose.pose.orientation.x = q.x
        ned_msg.pose.pose.orientation.y = -q.y
        ned_msg.pose.pose.orientation.z = -q.z
        ned_msg.pose.pose.orientation.w = q.w

        # Twist
        ned_msg.twist.twist.linear.x = msg.twist.twist.linear.x
        ned_msg.twist.twist.linear.y = -msg.twist.twist.linear.y
        ned_msg.twist.twist.linear.z = -msg.twist.twist.linear.z

        ned_msg.twist.twist.angular.x = msg.twist.twist.angular.x
        ned_msg.twist.twist.angular.y = -msg.twist.twist.angular.y
        ned_msg.twist.twist.angular.z = -msg.twist.twist.angular.z

        self.pub.publish(ned_msg)

def main(args=None):
    rclpy.init(args=args)
    node = OdomToNED()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
