from rclpy.action import ActionServer
from rclpy.node import Node


class DummyActionServer(Node):

    def __init__(self, node_name: str, action_type: any, action_topic: str):
        super().__init__(node_name)
        self._action_server = ActionServer(
            self, action_type, action_topic, self.execute_callback
        )
        self.action_type = action_type

    def execute_callback(self, goal_handle):
        self.get_logger().info("Executing goal...")
        result = self.action_type.Result()
        goal_handle.succeed()
        result.success = True  # Assuming success for the dummy action
        return result
