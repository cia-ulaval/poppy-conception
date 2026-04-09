import json

from poppy_motors.motor_msg_mapper import MotorMsgMapper
import rclpy
from std_msgs.msg import String
from rclpy.node import Node
from poppy_motors.motors import MotorCommands

class MotorNode(Node):
    def __init__(self):
        super().__init__('motor_node')
        self.message_mapper = MotorMsgMapper()
        self.get_logger().info('Motor Node has been started.')
        self.motor_commands = MotorCommands()
        self.motor_commands.torque_disable_all()  # Ensure all motors are disabled before starting
        self.motor_commands.torque_enable_all()
        self.motor_commands.set_all_moving_speed(200)  # Set a default moving speed for all motors
        self.motor_commands.set_all_torque_limit(500)  # Set a default torque limit for all motors
        self.create_subscription(String, 'poppy_motor_state', self.listener_callback, 10)


    def listener_callback(self, msg):
        message = json.loads(msg.data)
        self._send_motor_commands(message["motor_ids"], message["angles_rad"])
        
    def _send_motor_commands(self, motor_ids:list[String], angles_rad:list[float]):
        motor_ids = self.message_mapper.map_motor_names_to_ids(motor_ids)
        motor_positions = self.convert_angles_to_motor_positions(angles_rad, motor_ids)
        self.get_logger().info(f"Received motor command for IDs {motor_ids}.\nConverted to positions {motor_positions}.")
        for motor_id, position in zip(motor_ids, motor_positions):
            self.motor_commands.set_goal_position(motor_id, position)

    def convert_angles_to_motor_positions(self, angles_rad:list[float],ids:list[int]) -> list[int]:
        # Placeholder conversion function - replace with actual conversion logic
        zero_mx = 2048  # Example zero position for MX series motors
        zero_Ax = 512   # Example zero position for AX series motors
        motor_positions = []
       
        for motor_id, angle in zip(ids, angles_rad):
            # Simple linear conversion for demonstration purposes
            if motor_id == 37 or motor_id == 36:  # Example for MX series motor
                motor_position = int(zero_Ax + (angle / (2 * 3.14159)) * 1024)  # Convert radians to motor position
            else:
                motor_position = int(zero_mx + (angle / (2 * 3.14159)) * 4096)  # Convert radians to motor position
            motor_positions.append(motor_position)
        return motor_positions

    def shutdown(self):
        self.motor_commands.torque_disable_all()
        self.motor_commands.close_motors()


    def destroy_node(self):
        self.shutdown()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    motor_node = MotorNode()

    try:
        rclpy.spin(motor_node)
    except KeyboardInterrupt:
        print("Shutting down motor node...")
    finally:
        motor_node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()