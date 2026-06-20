

from motor_msg_mapper import MotorMsgMapper
import rclpy
from rclpy.node import Node
from motors import MotorCommands


class MotorNode(Node):
    def __init__(self):
        super().__init__('motor_node_test')
        self.message_mapper = MotorMsgMapper()
        self.get_logger().info('Motor Node has been started.')
        self.motor_commands = MotorCommands()
        self.motor_commands.torque_disable_all()
        self.motor_commands.torque_enable_all()
        self.motor_commands.set_all_moving_speed(100) 
        self.motor_commands.set_all_torque_limit(500)  
        self._set_initial_postion()
        self.create_timer(1, self._send_motor_commands)


        
        
    def _set_initial_postion(self):
        self.motor_commands.set_goal(21, 2048)
        self.motor_commands.set_goal(22, 2048)
        self.motor_commands.set_goal(23, 2048)
        self.motor_commands.set_goal(24, 2048)
        self.motor_commands.set_goal(25, 2048)
        self.motor_commands.set_goal(11, 2048)
        self.motor_commands.set_goal(12, 2048)
        self.motor_commands.set_goal(13, 2048)
        self.motor_commands.set_goal(14, 2048)
        self.motor_commands.set_goal(15, 2048)
        self.motor_commands.set_goal(31, 2048)
        self.motor_commands.set_goal(32, 2048)
        self.motor_commands.set_goal(33, 2048)
        self.motor_commands.set_goal(34, 2048+100)
        self.motor_commands.set_goal(35, 2048)
        self.motor_commands.set_goal(36, 512 )
        self.motor_commands.set_goal(37, 525 )
        self.motor_commands.set_goal(41, 2048 + 1024)
        self.motor_commands.set_goal(42, 2048 + 1024)
        self.motor_commands.set_goal(43, 2048)
        self.motor_commands.set_goal(44, 2048)
        self.motor_commands.set_goal(51, 2048 - 800)
        self.motor_commands.set_goal(52, 2048 )
        self.motor_commands.set_goal(53, 2048 + 800)
        self.motor_commands.set_goal(54, 2048) 

   

    def _send_motor_commands(self):
        if self.motor_commands.get_present_position(54)  < 2100:
            self.motor_commands.set_goal(54, 3500)
        if self.motor_commands.get_present_position(54)  > 3400:
           self.motor_commands.set_goal(54, 2048)
       

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