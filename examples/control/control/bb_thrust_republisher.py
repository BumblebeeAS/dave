#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, Float64
from bb_controls_msgs.msg import Thrusters

class ThrustRepublisher(Node):
    def __init__(self):
        super().__init__("thrust_republisher")
        
        # Create subscribers and publishers for each thruster
        self.thruster_sub = self.create_subscription(
            Thrusters,
            '/auv4/thrusters/input',
            self.thruster_callback,
            10)
        
        self.thrust_pubs = [
            self.create_publisher(
                Float64,
                f"/auv4/sim/thruster/t{i}/force",
                10
            ) for i in range(7)
        ]
        
        self.get_logger().info("Thrust republisher node initialized")

    def thruster_callback(self, msg: Thrusters):
        self.get_logger().info(f'Published {msg}')

        if len(msg.values) != 7:
            self.get_logger().warn(f'Expected 7 values, but got {len(msg.values)}')
            return
        
        for i in range(7):
            force_msg = Float64()
            force_msg.data = float(msg.values[i])
            # self.get_logger().info(f'got thruster {i} with force {force_msg.data}')
            self.thrust_pubs[i].publish(force_msg)
            self.get_logger().info(f'Published {force_msg.data} to /auv4/sim/thruster/t{i}/force')

def main():
    rclpy.init()
    node = ThrustRepublisher()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        node.get_logger().error(f"Error in thrust republisher node: {str(e)}")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
