
"""
Dynamixel Protocol 1.0 — Control Table Addresses
=================================================
Structure
---------
  EEPROM          — addresses shared across AX, MX-28/64, and MX-106
  RAM             — addresses shared across AX, MX-28/64, and MX-106
                    (addresses 26–29 are excluded: they differ per family)

  AXRAMDiff       — AX-only RAM registers (compliance, addresses 26–29)
  MXEEPROMDiff    — MX-28/64-only EEPROM registers (multi-turn, resolution)
  MXRAMDiff       — MX-28/64-only RAM registers (PID gains 26–29, realtime
                    tick, goal acceleration)
  MX106EEPROMDiff — MX-106-only EEPROM registers (same extras as MX + higher
                    voltage limit default — documented in class docstring)
  MX106RAMDiff    — MX-106-only RAM registers (PID, realtime tick, current,
                    torque control mode, goal torque, goal acceleration)

Sources (ROBOTIS e-Manual):
    AX-12A : https://emanual.robotis.com/docs/en/dxl/ax/ax-12a/
    MX-28  : https://emanual.robotis.com/docs/en/dxl/mx/mx-28/
"""

from enum import IntEnum


# ===========================================================================
# Common EEPROM  —  identical address and meaning on AX, MX-28/64, MX-106
# ===========================================================================

class EEPROMAddress(IntEnum):
    MODEL_NUMBER        = 0   # 2-byte  R    Model number
    FIRMWARE_VERSION    = 2   # 1-byte  R    Firmware version
    ID                  = 3   # 1-byte  RW   Motor ID (0–253; 254 = broadcast)
    BAUD_RATE           = 4   # 1-byte  RW   Baud rate selector (see BaudRate enum)
    RETURN_DELAY_TIME   = 5   # 1-byte  RW   Status packet delay (unit: 2 µs)
    CW_ANGLE_LIMIT      = 6   # 2-byte  RW   CW  angle limit (0–1023 AX / 0–4095 MX)
    CCW_ANGLE_LIMIT     = 8   # 2-byte  RW   CCW angle limit (0–1023 AX / 0–4095 MX)
    TEMPERATURE_LIMIT   = 11  # 1-byte  RW   Max internal temperature (°C)
    MIN_VOLTAGE_LIMIT   = 12  # 1-byte  RW   Min operating voltage (unit: 0.1 V)
    MAX_VOLTAGE_LIMIT   = 13  # 1-byte  RW   Max operating voltage (unit: 0.1 V)
    MAX_TORQUE          = 14  # 2-byte  RW   Max torque (0–1023, unit: ~0.1 %)
    STATUS_RETURN_LEVEL = 16  # 1-byte  RW   When to send status packets
    ALARM_LED           = 17  # 1-byte  RW   Bitmask: LED blinks on these errors
    SHUTDOWN            = 18  # 1-byte  RW   Bitmask: motor shuts down on these errors


# ===========================================================================
# Common RAM  —  identical address and meaning on AX, MX-28/64, MX-106
# ===========================================================================

class RAMAddress(IntEnum):
   
    TORQUE_ENABLE       = 24  # 1-byte  RW   0 = free / 1 = torque on
    LED                 = 25  # 1-byte  RW   0 = off  / 1 = on
    # 26–29 differ per family — see AXRAMDiff / MXRAMDiff / MX106RAMDiff
    GOAL_POSITION       = 30  # 2-byte  RW   Target position
    MOVING_SPEED        = 32  # 2-byte  RW   Target speed (0–1023 joint / 0–2047 wheel)
    TORQUE_LIMIT        = 34  # 2-byte  RW   Runtime torque limit (0–1023)
    PRESENT_POSITION    = 36  # 2-byte  R    Current position
    PRESENT_SPEED       = 38  # 2-byte  R    Current speed
    PRESENT_LOAD        = 40  # 2-byte  R    Current load (bit10 = direction)
    PRESENT_VOLTAGE     = 42  # 1-byte  R    Input voltage (unit: 0.1 V)
    PRESENT_TEMPERATURE = 43  # 1-byte  R    Internal temperature (°C)
    REGISTERED          = 44  # 1-byte  R    1 if REG_WRITE instruction is pending
    MOVING              = 46  # 1-byte  R    1 while motor is moving toward goal
    LOCK                = 47  # 1-byte  RW   1 = EEPROM locked until power cycle
    PUNCH               = 48  # 2-byte  RW   Minimum drive current


# ===========================================================================
# AX-series differences
# ===========================================================================

class AXRAMAddress(IntEnum):
    CW_COMPLIANCE_MARGIN    = 26  # 1-byte  RW   Dead-band CW  (0–255)
    CCW_COMPLIANCE_MARGIN   = 27  # 1-byte  RW   Dead-band CCW (0–255)
    CW_COMPLIANCE_SLOPE     = 28  # 1-byte  RW   Torque slope CW  (7 steps: 2,4,8,16,32,64,128)
    CCW_COMPLIANCE_SLOPE    = 29  # 1-byte  RW   Torque slope CCW (7 steps: 2,4,8,16,32,64,128)


# ===========================================================================
# MX-28 / MX-64 differences
# ===========================================================================

class MXEEPROMAddress(IntEnum):
    MULTI_TURN_OFFSET  = 20  # 2-byte  RW   Position offset applied in multi-turn mode
    RESOLUTION_DIVIDER = 22  # 1-byte  RW   Divides encoder resolution (1–4)


class MXRAMAddress(IntEnum):
    D_GAIN            = 26  # 1-byte  RW   Derivative gain
    I_GAIN            = 27  # 1-byte  RW   Integral gain
    P_GAIN            = 28  # 1-byte  RW   Proportional gain
    REALTIME_TICK     = 50  # 2-byte  R    Time counter (ms); wraps at 32767
    GOAL_ACCELERATION = 73  # 1-byte  RW   Goal acceleration (~8.583 °/s² per unit; 0 = max)





# ===========================================================================
# Helper enums for common register values
# ===========================================================================

class BaudRate(IntEnum):
    """
    Selector values for EEPROM.BAUD_RATE (address 4).
    Formula:  Speed (bps) = 2,000,000 / (Value + 1)
    """
    BPS_1000000 = 1
    BPS_500000  = 3
    BPS_400000  = 4
    BPS_250000  = 7
    BPS_200000  = 9
    BPS_115200  = 16
    BPS_57600   = 34
    BPS_19200   = 103
    BPS_9600    = 207


class StatusReturn(IntEnum):
    """Values for EEPROM.STATUS_RETURN_LEVEL (address 16)."""
    PING_ONLY = 0   # Reply only to PING
    READ_ONLY = 1   # Reply to READ instructions as well
    ALL       = 2   # Reply to every instruction (default)


class AlarmBit(IntEnum):
    """
    Bitmask constants for EEPROM.ALARM_LED (addr 17) and EEPROM.SHUTDOWN (addr 18).
    Combine with bitwise OR:
        AlarmBit.OVERHEATING | AlarmBit.OVERLOAD
    """
    INPUT_VOLTAGE = 0x01
    ANGLE_LIMIT   = 0x02
    OVERHEATING   = 0x04
    RANGE         = 0x08
    CHECKSUM      = 0x10
    OVERLOAD      = 0x20
    INSTRUCTION   = 0x40


class TorqueEnable(IntEnum):
    """Values for RAM.TORQUE_ENABLE (address 24)."""
    OFF = 0
    ON  = 1


class LEDState(IntEnum):
    """Values for RAM.LED (address 25)."""
    OFF = 0
    ON  = 1


class LockState(IntEnum):
    """Values for RAM.LOCK (address 47)."""
    UNLOCKED = 0
    LOCKED   = 1   # Requires power cycle to unlock


class TorqueCtrlMode(IntEnum):
    """Values for MX106RAMDiff.TORQUE_CTRL_MODE (address 70)."""
    DISABLED = 0   # Normal position / speed control
    ENABLED  = 1   # Pure torque control via MX106RAMDiff.GOAL_TORQUE

class ControlTable():
    """
    Unified control table for both AX and MX series, combining shared addresses
    and MX-exclusive addresses. Use ControlTable.ADDRESS_NAME.value to get the
    integer address for read/write operations.
    """
    # Shared EEPROM addresses 
    EEPROM: EEPROMAddress  = EEPROMAddress
    # Shared RAM addresses 
    RAM: RAMAddress  = RAMAddress
    # AX-exclusive RAM addresses
    AX_RAM: AXRAMAddress  = AXRAMAddress
    # MX-exclusive EEPROM addresses
    MX_EEPROM: MXEEPROMAddress  = MXEEPROMAddress
    # MX-exclusive RAM addresses 
    MX_RAM: MXRAMAddress  = MXRAMAddress
    






