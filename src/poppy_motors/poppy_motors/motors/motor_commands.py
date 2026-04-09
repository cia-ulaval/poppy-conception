from .control_table import ControlTable
from .motor_control import MotorController

class MotorCommands:
    """
    A class to encapsulate motor command operations, providing a clean interface for reading and writing to motor registers.
    """

    def __init__(self):
        self.motor_control = MotorController()

    # getters for configuration (EEPROM) operations

    def get_motor_ids(self) -> list:
        """
        Returns a list of motor IDs that are currently mapped to ports.
        """
        return self.motor_control.get_motors()

    def get_model_number(self, motor_id: int) -> int:
        """
        Reads the model number of the motor with the given ID.
        """
        return self.motor_control.read(motor_id, ControlTable.EEPROM.MODEL_NUMBER.value, byte_size=2)

    def get_max_torque(self, motor_id: int) -> int:
        """
        Reads the maximum torque of the motor with the given ID.
        """
        return self.motor_control.read(motor_id, ControlTable.EEPROM.MAX_TORQUE.value, byte_size=2)

    def get_cw_angle_limit(self, motor_id: int) -> int:
        """
        Reads the maximum CW angle limit of the motor with the given ID.
        """
        return self.motor_control.read(motor_id, ControlTable.EEPROM.CW_ANGLE_LIMIT.value, byte_size=2)
    
    def get_ccw_angle_limit(self, motor_id: int) -> int:
        """
        Reads the maximum CCW angle limit of the motor with the given ID.
        """
        return self.motor_control.read(motor_id, ControlTable.EEPROM.CCW_ANGLE_LIMIT.value, byte_size=2)


    # Getters for RAM operations (read operations) 
    
    def get_goal_position(self, motor_id: int) -> int:
        """
        Reads the goal position of the motor with the given ID.
        """
        return self.motor_control.read(motor_id, ControlTable.RAM.GOAL_POSITION.value, byte_size=2)
    
    def get_torque_limit(self, motor_id: int) -> int:
        """
        Reads the torque limit of the motor with the given ID.
        """
        return self.motor_control.read(motor_id, ControlTable.RAM.TORQUE_LIMIT.value, byte_size=2)
    
    def get_moving_speed(self, motor_id: int) -> int:
        """
        Reads the maximum moving speed of the motor with the given ID.
        """
        return self.motor_control.read(motor_id, ControlTable.RAM.MOVING_SPEED.value, byte_size=2)
    

    def get_present_position(self, motor_id: int) -> int:
        """
        Reads the present position of the motor with the given ID.
        """
        return self.motor_control.read(motor_id, ControlTable.RAM.PRESENT_POSITION.value, byte_size=2)

    def get_present_moving_speed(self, motor_id: int) -> int:
        """
        Reads the present moving speed of the motor with the given ID.
        """
        return self.motor_control.read(motor_id, ControlTable.RAM.PRESENT_SPEED.value, byte_size=2)

    def get_present_load(self, motor_id: int) -> int:
        """
        Reads the present load of the motor with the given ID.
        """
        return self.motor_control.read(motor_id, ControlTable.RAM.PRESENT_LOAD.value, byte_size=2)


    def get_temperature(self, motor_id: int) -> int:
        """
        Reads the present temperature of the motor with the given ID.
        """
        return self.motor_control.read(motor_id, ControlTable.RAM.PRESENT_TEMPERATURE.value, byte_size=1)

    # Setters for RAM operations

    def torque_enable(self, motor_id: int, enable: bool) -> None:
        """
        Enables or disables torque on the motor with the given ID.
        """
        enable_value = 1 if enable else 0
        self.motor_control.write(motor_id, ControlTable.RAM.TORQUE_ENABLE.value, enable_value, byte_size=1)
    
    def torque_disable_all(self) -> None:
        """
        Disables torque on all motors.
        """
        for motor_id in self.get_motor_ids():
            self.torque_enable(motor_id, False)

    def torque_enable_all(self) -> None:
        """
        Enables torque on all motors.
        """
        for motor_id in self.get_motor_ids():
            self.torque_enable(motor_id, True)

    def set_goal_position(self, motor_id: int, position: float) -> None:
        """
        Sets the goal position of the motor with the given ID.
        """
        min_angle = self.get_cw_angle_limit(motor_id)
        max_angle = self.get_ccw_angle_limit(motor_id)
        if position > min_angle and position < max_angle:
            self.motor_control.write(motor_id, ControlTable.RAM.GOAL_POSITION.value, position, byte_size=2)

    def set_moving_speed(self, motor_id: int, speed: int) -> None:
        """
        Sets the moving speed of the motor with the given ID.
        """
        self.motor_control.write(motor_id, ControlTable.RAM.MOVING_SPEED.value, speed, byte_size=2)
    
    def set_torque_limit(self, motor_id: int, torque_limit: int) -> None:
        """
        Sets the torque limit of the motor with the given ID.
        """
        self.motor_control.write(motor_id, ControlTable.RAM.TORQUE_LIMIT.value, torque_limit, byte_size=2)

    def set_all_torque_limit(self, torque_limit: int) -> None:
        """
        Sets the torque limit of all motors to the given value.
        """
        for motor_id in self.get_motor_ids():
            self.set_torque_limit(motor_id, torque_limit)

    def set_all_moving_speed(self, speed: int) -> None:
        """
        Sets the moving speed of all motors to the given value.
        """
        for motor_id in self.get_motor_ids():
            self.set_moving_speed(motor_id, speed)

    def reboot_motor(self, motor_id: int) -> None:
        """
        Reboots the motor with the given ID.
        """
       
        current_alarm = self.motor_control.read(motor_id, ControlTable.EEPROM.SHUTDOWN.value, byte_size=1)
        print(f"Motor {motor_id}: alarm shutdown register = {bin(current_alarm)}")
        cleared = current_alarm & ~(1 << 5)  # clear bit 5 (overload)
        self.motor_control.write(motor_id, ControlTable.EEPROM.SHUTDOWN.value, cleared, byte_size=1)
        self.motor_control.write(motor_id, ControlTable.EEPROM.SHUTDOWN.value, 0, byte_size=1)

    def reboot_all_motors(self) -> None:
        """
        Reboots all motors by disabling torque, clearing the overload alarm bit, and re-enabling torque.
        """
        for motor_id in self.get_motor_ids():
            self.reboot_motor(motor_id)


    def close_motors(self):
        """
        Closes the motor control connection.
        """
        self.motor_control.close()

    

    

