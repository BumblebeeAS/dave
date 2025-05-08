import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Quaternion
from tf_transformations import quaternion_multiply

class OdomToNED(Node):
    def __init__(self):
        super().__init__('odom_to_ned')
        self.sub = self.create_subscription(Odometry, '/auv4/nav/odom', self.cb, 10)
        self.pub = self.create_publisher(Odometry, '/auv4/nav/odom_ned', 10)

    def cb(self, msg):
        ned_msg = Odometry()
        ned_msg.header = msg.header

        # Position
        ned_msg.pose.pose.position.x = msg.pose.pose.position.y
        ned_msg.pose.pose.position.y = msg.pose.pose.position.x
        ned_msg.pose.pose.position.z = -msg.pose.pose.position.z

        # Orientation: q_ned = q_rot * q_enu
        q_enu = msg.pose.pose.orientation
        q_rot = [0, 1, 0, 0]  # 180 deg rotation around X-axis
        q_orig = [q_enu.x, q_enu.y, q_enu.z, q_enu.w]
        q_new = quaternion_multiply(q_rot, q_orig)
        ned_msg.pose.pose.orientation = Quaternion(x=q_new[0], y=q_new[1], z=q_new[2], w=q_new[3])

        # Twist
        ned_msg.twist.twist.linear.x = msg.twist.twist.linear.y
        ned_msg.twist.twist.linear.y = msg.twist.twist.linear.x
        ned_msg.twist.twist.linear.z = -msg.twist.twist.linear.z

        ned_msg.twist.twist.angular.x = msg.twist.twist.angular.y
        ned_msg.twist.twist.angular.y = msg.twist.twist.angular.x
        ned_msg.twist.twist.angular.z = -msg.twist.twist.angular.z

        self.pub.publish(ned_msg)

def main(args=None):
    rclpy.init(args=args)
    node = OdomToNED()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
