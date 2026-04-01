
from motors.control_table import ControlTable
from motors.motor_control import MotorController

class MotorCommands:
    """
    A class to encapsulate motor command operations, providing a clean interface for reading and writing to motor registers.
    """

    def __init__(self):
        self.motor_control = MotorController()


    def read_temperature(self, motor_id: int) -> int:
        """
        Reads the present temperature of the motor with the given ID.
        """
        return self.motor_control.read(motor_id, ControlTable.RAM.PRESENT_TEMPERATURE.value, byte_size=1)
    
    def torque_enable(self, motor_id: int, enable: bool) -> None:
        """
        Enables or disables torque on the motor with the given ID.
        """
        enable_value = 1 if enable else 0
        self.motor_control.write(motor_id, ControlTable.RAM.TORQUE_ENABLE.value, enable_value, byte_size=1)

    def set_goal_position(self, motor_id: int, position: int) -> None:
        """
        Sets the goal position for the motor with the given ID.
        """
        self.motor_control.write(motor_id, ControlTable.RAM.GOAL_POSITION_L.value, position, byte_size=4)

    def get_present_position(self, motor_id: int) -> int:
        """
        Gets the present position of the motor with the given ID.
        """
        return self.motor_control.read(motor_id, ControlTable.RAM.PRESENT_POSITION_L.value, byte_size=4)
    
if __name__ == '__main__':
    motor_commands = MotorCommands()
    # Example usage:
    motor_commands.torque_enable(motor_id=1, enable=True)
    motor_commands.set_goal_position(motor_id=1, position=512)
    current_position = motor_commands.get_present_position(motor_id=1)
    print(f"Current position of motor 1: {current_position}")