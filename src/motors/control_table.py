
"""
Dynamixel Protocol 1.0 - Control Table Addresses
=================================================
Covers: AX series (AX-12A, AX-18A, AX-12W)
        MX series (MX-12W, MX-28, MX-64, MX-106)

Control Table is split into two memory regions:
  - EEPROM  : Persistent across power cycles (addresses 0–23).
               Write only when Torque Enable = 0.
  - RAM     : Reset to defaults on power-on (addresses 24+).

Byte sizes:
  - 1-byte  : use write1ByteTxRx / read1ByteTxRx
  - 2-byte  : use write2ByteTxRx / read2ByteTxRx
              (stored Little-Endian; low byte at the listed address)

Sources: ROBOTIS e-Manual
  https://emanual.robotis.com/docs/en/dxl/ax/ax-12a/
  https://emanual.robotis.com/docs/en/dxl/mx/mx-28/
  https://emanual.robotis.com/docs/en/dxl/mx/mx-64/
  https://emanual.robotis.com/docs/en/dxl/mx/mx-106/
"""

from enum import  IntEnum

# ---------------------------------------------------------------------------
# Shared EEPROM area  (AX and MX — identical addresses)
# -------------------------------------------------------------------------

class EEPROMAddress(IntEnum):
    """
    Non-volatile EEPROM region.
    Values survive power cycles. Write only while Torque Enable = 0.
    """
    MODEL_NUMBER_L          = 0   # 2-byte  R    Model number (low byte)
    MODEL_NUMBER_H          = 1   # 2-byte  R    Model number (high byte)
    FIRMWARE_VERSION        = 2   # 1-byte  R    Firmware version
    ID                      = 3   # 1-byte  RW   Motor ID  (0–253; 254 = broadcast)
    BAUD_RATE               = 4   # 1-byte  RW   Baud rate selector (see BaudRate enum)
    RETURN_DELAY_TIME       = 5   # 1-byte  RW   Status packet delay  (unit: 2 µs)
    CW_ANGLE_LIMIT_L        = 6   # 2-byte  RW   CW  angle limit low  (0–1023 AX / 0–4095 MX)
    CW_ANGLE_LIMIT_H        = 7   # 2-byte  RW   CW  angle limit high
    CCW_ANGLE_LIMIT_L       = 8   # 2-byte  RW   CCW angle limit low
    CCW_ANGLE_LIMIT_H       = 9   # 2-byte  RW   CCW angle limit high
    # Address 10 reserved
    TEMPERATURE_LIMIT       = 11  # 1-byte  RW   Max internal temp (°C); default 70–80
    MIN_VOLTAGE_LIMIT       = 12  # 1-byte  RW   Min operating voltage (unit: 0.1 V)
    MAX_VOLTAGE_LIMIT       = 13  # 1-byte  RW   Max operating voltage (unit: 0.1 V)
    MAX_TORQUE_L            = 14  # 2-byte  RW   Max torque limit low  (0–1023, unit: ~0.1 %)
    MAX_TORQUE_H            = 15  # 2-byte  RW   Max torque limit high
    STATUS_RETURN_LEVEL     = 16  # 1-byte  RW   When to send status packets (see StatusReturn enum)
    ALARM_LED               = 17  # 1-byte  RW   Bitmask: LED blinks on these errors
    ALARM_SHUTDOWN          = 18  # 1-byte  RW   Bitmask: motor shuts down on these errors
    # Addresses 19–23 reserved / model-specific


# ---------------------------------------------------------------------------
# Shared RAM area  (AX and MX — identical addresses 24–49)
# ---------------------------------------------------------------------------

class RAMAddress(IntEnum):
    """
    Volatile RAM region. Resets to defaults on every power-on.
    All motion-control writes go here.
    """
    TORQUE_ENABLE           = 24  # 1-byte  RW   0 = free / 1 = torque on
    LED                     = 25  # 1-byte  RW   0 = off / 1 = on

    # --- Compliance (AX series only; addresses 26–29) ---
    # MX series replaces these four bytes with PID gains (see MXRAMAddress).
    CW_COMPLIANCE_MARGIN    = 26  # 1-byte  RW   Dead-band CW  side  (0–255)
    CCW_COMPLIANCE_MARGIN   = 27  # 1-byte  RW   Dead-band CCW side  (0–255)
    CW_COMPLIANCE_SLOPE     = 28  # 1-byte  RW   Torque flexibility CW  (7 levels)
    CCW_COMPLIANCE_SLOPE    = 29  # 1-byte  RW   Torque flexibility CCW (7 levels)

    GOAL_POSITION_L         = 30  # 2-byte  RW   Target position low  (0–1023 AX / 0–4095 MX)
    GOAL_POSITION_H         = 31  # 2-byte  RW   Target position high
    MOVING_SPEED_L          = 32  # 2-byte  RW   Target speed low     (0–1023 joint / 0–2047 wheel)
    MOVING_SPEED_H          = 33  # 2-byte  RW   Target speed high
    TORQUE_LIMIT_L          = 34  # 2-byte  RW   Runtime torque limit low  (0–1023)
    TORQUE_LIMIT_H          = 35  # 2-byte  RW   Runtime torque limit high

    PRESENT_POSITION_L      = 36  # 2-byte  R    Current position low
    PRESENT_POSITION_H      = 37  # 2-byte  R    Current position high
    PRESENT_SPEED_L         = 38  # 2-byte  R    Current speed low
    PRESENT_SPEED_H         = 39  # 2-byte  R    Current speed high
    PRESENT_LOAD_L          = 40  # 2-byte  R    Current load low    (0–2047, bit10 = direction)
    PRESENT_LOAD_H          = 41  # 2-byte  R    Current load high
    PRESENT_VOLTAGE         = 42  # 1-byte  R    Current input voltage (unit: 0.1 V)
    PRESENT_TEMPERATURE     = 43  # 1-byte  R    Current temperature  (°C)

    REGISTERED              = 44  # 1-byte  R    1 if REG_WRITE instruction is pending
    # Address 45 reserved
    MOVING                  = 46  # 1-byte  R    1 while motor is moving toward goal
    LOCK                    = 47  # 1-byte  RW   1 = EEPROM locked until power cycle
    PUNCH_L                 = 48  # 2-byte  RW   Minimum drive current low  (0x20–0x3FF)
    PUNCH_H                 = 49  # 2-byte  RW   Minimum drive current high


# ---------------------------------------------------------------------------
# MX-series-only RAM addresses  (replaces compliance bytes 26–29 with PID)
# ---------------------------------------------------------------------------

class MXRAMAddress(IntEnum):
    """
    Extra RAM addresses present on MX-28 / MX-64 / MX-106 (Protocol 1.0).
    Addresses 26–29 are PID gains on MX (not compliance as on AX).
    Addresses 50+ are MX-exclusive features.
    """

    # PID gains (overwrite AX compliance slots 26–29)
    D_GAIN                  = 26  # 1-byte  RW   Derivative  gain
    I_GAIN                  = 27  # 1-byte  RW   Integral    gain
    P_GAIN                  = 28  # 1-byte  RW   Proportional gain
    # Address 29 reserved on MX

    # MX-exclusive EEPROM-region addresses
    MULTI_TURN_OFFSET_L     = 20  # 2-byte  RW   Multi-turn offset low  (EEPROM)
    MULTI_TURN_OFFSET_H     = 21  # 2-byte  RW   Multi-turn offset high (EEPROM)
    RESOLUTION_DIVIDER      = 22  # 1-byte  RW   Resolution divider 1–4 (EEPROM)

    # MX-exclusive RAM addresses
    CURRENT_L               = 68  # 2-byte  R    Present current low   (MX-64 / MX-106 only)
    CURRENT_H               = 69  # 2-byte  R    Present current high
    TORQUE_CTRL_MODE_EN     = 70  # 1-byte  RW   1 = torque control mode (MX-64 / MX-106 only)
    GOAL_TORQUE_L           = 71  # 2-byte  RW   Goal torque low        (MX-64 / MX-106 only)
    GOAL_TORQUE_H           = 72  # 2-byte  RW   Goal torque high
    GOAL_ACCELERATION       = 73  # 1-byte  RW   Goal acceleration (unit: ~8.583 °/s²; 0 = max)


class ControlTable():
    """
    Unified control table for both AX and MX series, combining shared addresses
    and MX-exclusive addresses. Use ControlTable.ADDRESS_NAME.value to get the
    integer address for read/write operations.
    """
    # Shared EEPROM addresses (0–23)
    EEPROM: EEPROMAddress = EEPROMAddress
    # Shared RAM addresses (24–49)
    RAM: RAMAddress = RAMAddress
    # MX-exclusive RAM addresses (26–29 overwritten by PID gains; 50+ are MX-only)
    MX_RAM: MXRAMAddress = MXRAMAddress





