

from poppy_motors.motor_msg_mapper import MotorMsgMapper
import rclpy
from std_msgs.msg import String
from rclpy.node import Node
from poppy_motors.motors import MotorCommands

class MotorNode(Node):
    def __init__(self):
        super().__init__('motor_node_test')
        self.message_mapper = MotorMsgMapper()
        self.get_logger().info('Motor Node has been started.')
        self.motor_commands = MotorCommands()
        self.motor_commands.reboot_all_motors()
        self.motor_commands.torque_enable_all()
        self.motor_commands.set_all_moving_speed(200) 
        self.motor_commands.set_all_torque_limit(500)  
        self._set_initial_postion()
        self.create_subscription(String, 'poppy_motor_state', self.listener_callback, 10)


    def listener_callback(self, msg):
        # message = json.loads(msg.data)
        pass
        
        
    def _set_initial_postion(self):
        self.motor_commands.set_goal_position(21, 2048)
        self.motor_commands.set_goal_position(22, 2048)
        self.motor_commands.set_goal_position(23, 2048)
        self.motor_commands.set_goal_position(24, 2048)
        self.motor_commands.set_goal_position(25, 2048)
        self.motor_commands.set_goal_position(11, 2048)
        self.motor_commands.set_goal_position(12, 2048)
        self.motor_commands.set_goal_position(13, 2048)
        self.motor_commands.set_goal_position(14, 2048)
        self.motor_commands.set_goal_position(15, 2048)
        self.motor_commands.set_goal_position(31, 2048)
        self.motor_commands.set_goal_position(32, 2048)
        self.motor_commands.set_goal_position(33, 2048)
        self.motor_commands.set_goal_position(34, 2048)
        self.motor_commands.set_goal_position(35, 2048)
        self.motor_commands.set_goal_position(36, 512)
        self.motor_commands.set_goal_position(37, 512)
        self.motor_commands.set_goal_position(41, 2048 + 1024)
        self.motor_commands.set_goal_position(42, 2048 + 1024)
        self.motor_commands.set_goal_position(43, 2048)
        self.motor_commands.set_goal_position(44, 2048)
        self.motor_commands.set_goal_position(51, 2048 - 1024)
        self.motor_commands.set_goal_position(52, 2048 - 1024)
        self.motor_commands.set_goal_position(53, 2048)
        self.motor_commands.set_goal_position(54, 2048) 

   

    def _send_motor_commands(self):
        pass
        

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