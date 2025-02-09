#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, Float64

class ThrustRepublisher(Node):
    def __init__(self):
        super().__init__("thrust_republisher")
        
        # Create subscribers and publishers for each thruster
        self.thrust_subs = [
            self.create_subscription(
                Float32,
                f"/auv4/thruster/t{i}/force",
                lambda msg, i=i: self.republish(msg, i),
                10
            ) for i in range(7)
        ]
        
        self.thrust_pubs = [
            self.create_publisher(
                Float64,
                f"/auv4/sim/thruster/t{i}/force",
                10
            ) for i in range(7)
        ]
        
        self.get_logger().info("Thrust republisher node initialized")

    def republish(self, msg: Float32, thruster_index: int):
        """
        Republish thrust messages from Float32 to Float64
        
        Args:
            msg (Float32): Input thrust message
            thruster_index (int): Index of the thruster (0-6)
        """
        try:
            # Create new Float64 message
            float64_msg = Float64()
            float64_msg.data = float(msg.data)
            
            # Publish the converted message
            self.thrust_pubs[thruster_index].publish(float64_msg)
            
        except Exception as e:
            self.get_logger().error(f"Error republishing thrust {thruster_index}: {str(e)}")

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
