from time import perf_counter, time

from dynamixel_sdk import (COMM_SUCCESS, PortHandler,PacketHandler, GroupSyncWrite, GroupBulkRead)
from concurrent.futures import ThreadPoolExecutor


PORTS = ['/dev/ttyACM0','/dev/ttyACM1']
PROTOCOL = 1.0
ID_RANGE = range(0, 55)
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
        
        if not byte_size in self.read_methods:
            raise ValueError(f"Unsupported byte size {byte_size} for read operation")
        
        port_handler = self.id_port_map[motor_id]
        read_method = self.read_methods[byte_size]
        value, result, error = read_method(port_handler, motor_id, address)

        if result != COMM_SUCCESS:
            raise IOError(f"Failed to read from motor ID {motor_id} at address {address}: {self.packet_handler.getTxRxResult(result)}")
        elif error != 0:
            raise IOError(f"Error from motor ID {motor_id} at address {address}: {self.packet_handler.getRxPacketError(error)}")
        
        return value  
    
    def sync_write(self, address: int, values_by_id: dict[int, int], byte_size: int) -> None:
        """
        Protocol 1.0 Sync Write:
        Write the same register address/size for multiple motors in one packet per port.
        """
        if not values_by_id:
            return
        if byte_size not in (1, 2, 4):
            raise ValueError(f"Unsupported byte size {byte_size} for sync_write")

        ids_by_port = self._group_ids_by_port(list(values_by_id.keys()))

        for port_handler, motor_ids in ids_by_port.items():
            if not motor_ids:
                continue

            group = GroupSyncWrite(port_handler, self.packet_handler, address, byte_size)

            for motor_id in motor_ids:
                param_bytes = self._value_to_little_endian_bytes(values_by_id[motor_id], byte_size)
                if not group.addParam(motor_id, param_bytes):
                    group.clearParam()
                    raise IOError(f"Failed to add sync_write param for motor ID {motor_id}")

            result = group.txPacket()
            group.clearParam()

            if result != COMM_SUCCESS:
                raise IOError(
                    f"Sync write failed on port {port_handler.getPortName()} at address {address}: "
                    f"{self.packet_handler.getTxRxResult(result)}"
                )
            
    def bulk_read(self, requests_by_id: dict[int, tuple[int, int]]) -> dict[int, int]:
        """
        Protocol 1.0 Bulk Read:
        reading from multiple addresses at the same time
        """
        if not requests_by_id:
            return {}

        results: dict[int, int] = {}
        ids_by_port = self._group_ids_by_port(list(requests_by_id.keys()))

        for port_handler, motor_ids in ids_by_port.items():
            if not motor_ids:
                continue

            group = GroupBulkRead(port_handler, self.packet_handler)

            for motor_id in motor_ids:
                address, byte_size = requests_by_id[motor_id]
                if byte_size not in (1, 2, 4):
                    raise ValueError(f"Unsupported byte size {byte_size} for motor ID {motor_id}")

                if not group.addParam(motor_id, address, byte_size):
                    group.clearParam()
                    raise IOError(f"Failed to add bulk read param for motor ID {motor_id}")

            result = group.txRxPacket()
            if result != COMM_SUCCESS:
                group.clearParam()
                raise IOError(
                    f"Bulk read failed on port {port_handler.getPortName()}: "
                    f"{self.packet_handler.getTxRxResult(result)}"
                )

            for motor_id in motor_ids:
                address, byte_size = requests_by_id[motor_id]
                if not group.isAvailable(motor_id, address, byte_size):
                    group.clearParam()
                    raise IOError(f"Data not available for motor ID {motor_id} at address {address}")

                results[motor_id] = group.getData(motor_id, address, byte_size)

            group.clearParam()

        return results
    
    def _create_id_port_map(self):
        """
        Scans all port_handlers and maps detected motor IDs in ID_RANGE to their
        corresponding ports in id_port_map by pinging each motor.
        """
        with ThreadPoolExecutor(max_workers=len(self.port_handlers)) as executor:
            for port_mappings in executor.map(self._scan_port_for_motors, self.port_handlers):
                self.id_port_map.update(port_mappings)


    def _scan_port_for_motors(self, port_handler: PortHandler) -> dict[int, PortHandler]:
        """
        Scan a single port for all possible motor IDs and return the detected
        mappings for that port.
        """
        port_mappings: dict[int, PortHandler] = {}
        for motor_id in ID_RANGE:
            _, result, _ = self.packet_handler.ping(port_handler, motor_id)
            if result == COMM_SUCCESS:
                port_mappings[motor_id] = port_handler
        return port_mappings
    
    
    
    def _group_ids_by_port(self, motor_ids: list[int]) -> dict[PortHandler, list[int]]:
        grouped: dict[PortHandler, list[int]] = {port_handler: [] for port_handler in self.port_handlers}
        for motor_id in motor_ids:
            if motor_id not in self.id_port_map:
                raise ValueError(f"Motor ID {motor_id} not found on any port")
            grouped[self.id_port_map[motor_id]].append(motor_id)
        return grouped


    def _value_to_little_endian_bytes(self, value: int, byte_size: int) -> list[int]:
        if byte_size not in (1, 2, 4):
            raise ValueError(f"Unsupported byte size {byte_size}")
        # Keep only the requested width, then pack little-endian
        mask = (1 << (byte_size * 8)) - 1
        value &= mask
        return [(value >> (8 * i)) & 0xFF for i in range(byte_size)]
    
    def get_motors(self) -> list:
        """
        Returns a list of all motor IDs that are currently mapped to ports.
        """
        return list(self.id_port_map.keys())


    def close(self):
        """
        Closes all port handlers managed by the MotorController.
        """
        for port_handler in self.port_handlers:
            port_handler.closePort()
    
    
#if __name__ == "__main__":
#    start = perf_counter()
#    controller = MotorController()
#    elapsed = perf_counter() - start
#    print(f"_create_id_port_map took {elapsed:.3f}s")
#    print("Detected motors:", controller.get_motors())
#    controller.sync_write(address=30, values_by_id={54: 3000,44:512}, byte_size=2) 
#    print(controller.bulk_read(requests_by_id={54: (36, 2), 44: (36, 2)}))
#    controller.close() 
        