from dynamixel_sdk import COMM_SUCCESS, PortHandler,PacketHandler


PORTS = ['/dev/ttyACM0','/dev/ttyACM1']
PROTOCOL = 1.0
ID_RANGE = range(0, 253)
BAUDRATE = 1000000





class MotorController:
    """
    Manages communication with multiple motors over serial ports, handling
    port initialization, baud rate configuration, motor ID mapping, and
    resource cleanup.
    """


   


    def __init__(self):
        self.port_handlers : list[PortHandler] = [PortHandler(port) for port in PORTS]
        self.packet_handler : PacketHandler = PacketHandler(PROTOCOL)
        self.id_port_map : dict[int, PortHandler] = {}
        self.write_methods: dict[int, callable] = {
            1: self.packet_handler.write1ByteTxRx,
            2: self.packet_handler.write2ByteTxRx,
            4: self.packet_handler.write4ByteTxRx,
        }
        self.read_methods: dict[int, callable] = {
            1: self.packet_handler.read1ByteTxRx,
            2: self.packet_handler.read2ByteTxRx,
            4: self.packet_handler.read4ByteTxRx,
        }

        print("Opening Port Handlers...")
        for port_handler in self.port_handlers:
            if not port_handler.openPort():
                raise IOError(f"Cannot open port {port_handler.getPortName()}")

        print("Setting Baud Rates...")
        for port_handler in self.port_handlers:
            if not port_handler.setBaudRate(BAUDRATE):
                raise IOError(f"Failed to set baud rate for port {port_handler.getPortName()}")
            
            
        print("Scanning for motors and creating ID to port mapping...")
        self._create_id_port_map()
        print("MotorController initialized successfully")
        

    def _create_id_port_map(self):
        """
        Scans all port_handlers and maps detected motor IDs in ID_RANGE to their
        corresponding ports in id_port_map by pinging each motor.
        """
        for port_handler in self.port_handlers:
            for motor_id in ID_RANGE:
                _ , result, _ = self.packet_handler.ping(port_handler, motor_id)
                if result == COMM_SUCCESS:
                    self.id_port_map[motor_id] = port_handler

    def get_motors(self) -> list:
        """
        Returns a list of all motor IDs that are currently mapped to ports.
        """
        return list(self.id_port_map.keys())

    def write(self, motor_id: int, address: int,value: int, byte_size: int) -> None:
        """
        Writes data to a motor with the specified ID at the given address.
        Raises KeyError if the motor ID is not found in id_port_map.
        """
        if motor_id not in self.id_port_map:
            raise ValueError(f"Motor ID {motor_id} not found on any port")
        
        if not byte_size in self.write_methods:
            raise ValueError(f"Unsupported byte size {byte_size} for write operation")
        
        
        port_handler = self.id_port_map[motor_id]
        write_method = self.write_methods[byte_size]
        result, error = write_method(port_handler, motor_id, address, value)

        if result != COMM_SUCCESS:
            raise IOError(f"Failed to write to motor ID {motor_id} at address {address}: {self.packet_handler.getTxRxResult(result)}")
        elif error != 0:
            raise IOError(f"Error from motor ID {motor_id} at address {address}: {self.packet_handler.getRxPacketError(error)}")

    def read(self, motor_id: int, address: int, byte_size: int) -> int:
        """
        Reads data from a motor with the specified ID at the given address.
        Returns the read value as an integer. Raises KeyError if the motor ID
        is not found in id_port_map.
        """
        if motor_id not in self.id_port_map:
            raise ValueError(f"Motor ID {motor_id} not found on any port")
        
        if not byte_size in self.write_methods:
            raise ValueError(f"Unsupported byte size {byte_size} for read operation")
        
        port_handler = self.id_port_map[motor_id]
        read_method = self.read_methods[byte_size]
        value, result, error = read_method(port_handler, motor_id, address)

        if result != COMM_SUCCESS:
            raise IOError(f"Failed to read from motor ID {motor_id} at address {address}: {self.packet_handler.getTxRxResult(result)}")
        elif error != 0:
            raise IOError(f"Error from motor ID {motor_id} at address {address}: {self.packet_handler.getRxPacketError(error)}")
        
        return value    


    def close(self):
        """
        Closes all port handlers managed by the MotorController.
        """
        for port_handler in self.port_handlers:
            port_handler.closePort()



if __name__ == '__main__': 
    print("hello world")