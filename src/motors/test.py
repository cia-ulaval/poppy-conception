from dynamixel_sdk import PortHandler, PacketHandler, COMM_SUCCESS
import serial.tools.list_ports


def scan_dynamixels(port, baudrates=None, id_range=range(1, 253), protocol=1.0):
    if baudrates is None:
        baudrates = [9600, 57600, 115200, 1000000, 2000000, 3000000, 4000000]

    portHandler = PortHandler(port)
    packetHandler = PacketHandler(protocol)

    if not portHandler.openPort():
        raise IOError(f"Cannot open port {port}")

    found = {}

    for baud in baudrates:
        portHandler.setBaudRate(baud)
        motors = []

        for dxl_id in id_range:
            model_number, result, error = packetHandler.ping(portHandler, dxl_id)
            if result == COMM_SUCCESS:
                motors.append({
                    'id': dxl_id,
                    'model_number': model_number,
                    'model_name': get_model_name(model_number),
                })
                print(f"  [baud {baud}] Found ID {dxl_id} — {get_model_name(model_number)} (model #{model_number})")

        if motors:
            found[baud] = motors

    portHandler.closePort()
    return found


def get_model_name(model_number):
    models = {
        12:   'AX-12A',
        18:   'AX-18A',
        300:  'AX-12W',
        29:   'MX-28',
        30:   'MX-28 (Protocol 2)',
        310:  'MX-64',
        311:  'MX-64 (Protocol 2)',
        320:  'MX-106',
        321:  'MX-106 (Protocol 2)',
        350:  'XL-320',
        1060: 'XL430-W250',
        1070: 'XC430-W150',
        1080: 'XC430-W240',
        1090: 'XL430-W250 (TTL)',
        1100: 'XM430-W210',
        1110: 'XM430-W350',
        1130: 'XH430-W210',
        1140: 'XH430-W350',
        1160: 'XH430-V210',
        1170: 'XH430-V350',
        1200: 'XM540-W150',
        1210: 'XM540-W270',
        1220: 'XH540-W150',
        1230: 'XH540-W270',
    }
    return models.get(model_number, f'Unknown (#{model_number})')


def get_likely_ports():
    """Filter serial ports that are likely U2D2 or USB-serial adapters."""
    all_ports = serial.tools.list_ports.comports()
    likely = []
    keywords = ['usbserial', 'usbmodem', 'ttyUSB', 'ttyACM', 'U2D2', 'COM']

    for p in all_ports:
        desc = (p.description + p.device).lower()
        if any(k.lower() in desc for k in keywords):
            likely.append(p.device)
            print(f"  {p.device} — {p.description}")
    
    print(likely)
    return likely                                   # ← function ends here
    

if __name__ == '__main__':                          # ← back at column 0
    print("=== Scanning for serial ports ===")
    ports = get_likely_ports()

    if not ports:
        print("No likely ports found. Check USB connection.")
        exit()

    print(f"\n=== Scanning for Dynamixel motors ===")
    print("(This may take a minute — scanning all baud rates and IDs)\n")

    all_found = {}
    for port in ports:
        print(f"-- Port: {port} --")
        try:
            result = scan_dynamixels(port,[1000000])
            if result:
                all_found[port] = result
        except IOError as e:
            print(f"  Skipped: {e}")

    print("\n=== Summary ===")
    if not all_found:
        print("No motors found.")
    else:
        for port, bauds in all_found.items():
            for baud, motors in bauds.items():
                print(f"\n{port} @ {baud} baud:")
                for m in motors:
                    print(f"  ID {m['id']:3d}  {m['model_name']}")