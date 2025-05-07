from rclpy.node import Node
from std_msgs.msg import Float64

PROP_NAMES = [f"t{i}" for i in range(7)]

PROP_TOPICS = [
    f"/auv4/sim/thruster/{prop_name}/force" for prop_name in PROP_NAMES
]


class SingleThrustPublisher(Node):
    def __init__(self, name, topic):
        super().__init__(name)
        self.name = name
        self.publisher_ = self.create_publisher(Float64, topic, 10)

    def publish_thrust(self, thrust):
        msg = Float64()
        msg.data = float(thrust)

        self.publisher_.publish(msg)
        self.get_logger().info(f"{self.name} \tThrust published: {msg.data}")


class MultiThrustPublisher(Node):
    def __init__(self):
        super().__init__("thrust_publisher_node")
        self.thrustPubs = []

        for thrustName, thrustTopic in zip(PROP_NAMES, PROP_TOPICS):
            self.thrustPubs.append(SingleThrustPublisher(thrustName, thrustTopic))

    def publish_thrust(self, thrustValues):
        for thrustValue, thrustPub in zip(thrustValues, self.thrustPubs):
            thrustPub.publish_thrust(thrustValue)
