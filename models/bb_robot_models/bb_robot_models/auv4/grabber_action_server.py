#!/usr/bin/env python3

import rclpy
from bb_auv_msgs.action import Grabber
from bb_robot_models.dummy_action_server import DummyActionServer


def main(args=None):
    rclpy.init(args=args)

    grabber_action_server = DummyActionServer(
        "grabber_action_server", Grabber, "/auv4/actuation/grabber"
    )

    try:
        rclpy.spin(grabber_action_server)
    except KeyboardInterrupt:
        pass
    finally:
        grabber_action_server.destroy_node()
        rclpy.try_shutdown()


if __name__ == "__main__":
    main()
