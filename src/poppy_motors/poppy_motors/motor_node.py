import time

import rclpy
from std_msgs.msg import String
from rclpy.node import Node
from poppy_motors.motors import MotorCommands

class MotorNode(Node):
    def __init__(self):
        super().__init__('motor_node')
        self.get_logger().info('Motor Node has been started.')
        self.motor_commands = MotorCommands()
        self.start = time.perf_counter()
        self.create_timer(1.0, self.timer_callback)
        self.publisher =  self.create_publisher(String, 'my_topic', 10)
        self.create_subscription(String, 'your_topic', self.listener_callback, 10)


    def timer_callback(self):
        elapsed_time = time.perf_counter() - self.start
        msg = String()
        msg.data = f'Hello, world! {elapsed_time:.2f} seconds have passed.'
        self.publisher.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')

    def listener_callback(self, msg):
        # This function runs every time a message is received
        self.get_logger().info('I heard: "%s"' % msg.data)
            
    def shutdown(self):
        self.motor_commands.torque_disable_all()
    
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