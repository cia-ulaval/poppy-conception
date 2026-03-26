from dynamixel_sdk import COMM_SUCCESS, PortHandler,PacketHandler


PORTS = ['/dev/ttyACM0','/dev/ttyACM1']
PROTOCOL = 1.0
ID_RANGE = range(1, 25)
BAUDRATE = 1000000

class MotorController:
    """
    Manages communication with multiple motors over serial ports, handling
    port initialization, baud rate configuration, motor ID mapping, and
    resource cleanup.
    """

    def __init__(self):
        self.port_handlers = [PortHandler(port) for port in PORTS]
        self.packet_handler = PacketHandler(PROTOCOL)
        self.id_port_map = {}

        for port_handler in self.port_handlers:
            if not port_handler.openPort():
                raise IOError(f"Cannot open port {port_handler.getPortName()}")
        
        for port_handler in self.port_handlers:
            port_handler.setBaudRate(BAUDRATE)
        
        self._create_id_port_map()

    def _create_id_port_map(self):
        """
        Scans all port_handlers and maps detected motor IDs in ID_RANGE to their
        corresponding ports in id_port_map by pinging each motor.
        """
        for port_handler in self.port_handlers:
            for motor_id in ID_RANGE:
                dxl_comm_result, _, _ = self.packet_handler.ping(port_handler, motor_id)
                if dxl_comm_result == COMM_SUCCESS:
                    self.id_port_map[motor_id] = port_handler
        

    
    
        
        

    def close(self):
        for port_handler in self.port_handlers:
            port_handler.closePort()



if __name__ == '__main__': 
    print("hello world")