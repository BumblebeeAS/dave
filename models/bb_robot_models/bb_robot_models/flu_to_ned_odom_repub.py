#!/usr/bin/env python3

import rclpy
from nav_msgs.msg import Odometry
from rclpy.node import Node
from std_msgs.msg import Float32


class FluToNedOdomRepublisher(Node):
    """
    Converts sim odometry (FLU) into controls odometry (NED)
    """

    def __init__(self):
        super().__init__("odom_republisher")
        self.sub = self.create_subscription(Odometry, "nav/odom", self.cb, 10)
        self.pub = self.create_publisher(Odometry, "nav/odom_ned", 10)
        self.depth_pub = self.create_publisher(Float32, "depth", 10)

    def cb(self, msg: Odometry):
        ned_msg = Odometry()
        ned_msg.header.stamp = self.get_clock().now().to_msg()
        # ned_msg.header.stamp = msg.header.stamp
        ned_msg.header.frame_id = "world_ned"
        ned_msg.child_frame_id = "auv4/base_link_ned"

        # Position
        ned_msg.pose.pose.position.x = msg.pose.pose.position.x
        ned_msg.pose.pose.position.y = -msg.pose.pose.position.y
        ned_msg.pose.pose.position.z = -msg.pose.pose.position.z

        # odom gives us f: base_link -> world

        #                       hfg                          g             f        h
        # we need base_link_ned -> world_ned = base_link_ned -> base_link -> world -> world_ned

        # h and g are both given by q = i, t = 0
        # for translation for hfg, this can be achieved by simply negating y and z coordinates
        # for rotation for hfg, we have i * (w + xi + yj + zk) * i = -w -xi + yj + zk

        q = msg.pose.pose.orientation
        ned_msg.pose.pose.orientation.x = -q.x
        ned_msg.pose.pose.orientation.y = q.y
        ned_msg.pose.pose.orientation.z = q.z
        ned_msg.pose.pose.orientation.w = -q.w

        # Twist
        ned_msg.twist.twist.linear.x = msg.twist.twist.linear.x
        ned_msg.twist.twist.linear.y = -msg.twist.twist.linear.y
        ned_msg.twist.twist.linear.z = -msg.twist.twist.linear.z

        ned_msg.twist.twist.angular.x = msg.twist.twist.angular.x
        ned_msg.twist.twist.angular.y = -msg.twist.twist.angular.y
        ned_msg.twist.twist.angular.z = -msg.twist.twist.angular.z

        self.pub.publish(ned_msg)

        depth_msg = Float32()
        depth_msg.data = -msg.pose.pose.position.z
        self.depth_pub.publish(depth_msg)


def main(args=None):
    rclpy.init(args=args)
    node = FluToNedOdomRepublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        node.get_logger().error(f"Error in odom republisher node: {str(e)}")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
