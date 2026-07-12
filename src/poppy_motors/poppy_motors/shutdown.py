from motors import MotorCommands
import rclpy
from rclpy.node import Node

to_be_or_not_to_be = MotorCommands()

to_be_or_not_to_be.torque_disable_all()
to_be_or_not_to_be.close_motors()

rclpy.init(args=None)
motor_node = Node(node_name="Executing_shutdown")
motor_node.destroy_node()
rclpy.shutdown()


