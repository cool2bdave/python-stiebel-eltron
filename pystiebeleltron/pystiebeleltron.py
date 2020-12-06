"""
Connection to a Stiebel Eltron ModBus API.

See API details:
https://www.stiebel-eltron.ch/content/dam/ste/ch/de/downloads/kundenservice/smart-home/Modbus/Modbus%20Bedienungsanleitung.pdf

Types of data:

Data | Value      | Multiplier  | Multiplier  | Signed | Step   | Step
type | range      | for reading | for writing |        | size 1 | size 5
-----|------------|-------------|-------------|--------|--------|-------
2    | -3276.8 to | 0.1         | 10          | Yes    | 0.1    | 0.5
     |  3276.7    |             |             |        |        |
6    | 0 to 65535 | 1           | 1           | No     | 1      | 5
7    | -327.68 to | 0.01        | 100         | Yes    | 0.01   | 0.05
     |  327.67    |             |             |        |        |
8    | 0 to 255   | 1           | 1           | No     | 1      | 5
"""

# Error - sensor lead is missing or disconnected.
ERROR_NOTAVAILABLE = -60
# Error - short circuit of the sensor lead.
ERROR_SHORTCUT = -50
# Error - object unavailable.
ERROR_OBJ_UNAVAILBLE = 0x8000

UNAVAILABLE_OBJECT = 32768

# Block 1 System values (Read input register) - page 29
B1_START_ADDR = 0

B1_REGMAP_INPUT = {
    # HC = Heating Circuit
    'ACTUAL_ROOM_TEMPERATURE_HC1':      {'addr':  0, 'type': 2, 'value': 0},
    'SET_ROOM_TEMPERATURE_HC1':         {'addr':  1, 'type': 2, 'value': 0},
    'RELATIVE_HUMIDITY_HC1':            {'addr':  2, 'type': 2, 'value': 0},
    'ACTUAL_ROOM_TEMPERATURE_HC2':      {'addr':  3, 'type': 2, 'value': 0},
    'SET_ROOM_TEMPERATURE_HC2':         {'addr':  4, 'type': 2, 'value': 0},
    'RELATIVE_HUMIDITY_HC2':            {'addr':  5, 'type': 2, 'value': 0},
    'OUTSIDE_TEMPERATURE':              {'addr':  6, 'type': 2, 'value': 0},
    'ACTUAL_VALUE_HC1':                 {'addr':  7, 'type': 2, 'value': 0},
    'SET_VALUE_HC1':                    {'addr':  8, 'type': 2, 'value': 0},
    'ACTUAL_VALUE_HC2':                 {'addr':  9, 'type': 2, 'value': 0},
    'SET_VALUE_HC2':                    {'addr': 10, 'type': 2, 'value': 0},
    'FLOW_TEMPERATURE':                 {'addr': 11, 'type': 2, 'value': 0},
    'RETURN_TEMPERATURE':               {'addr': 12, 'type': 2, 'value': 0},
    'PRESSURE_HEATING_CIRCUIT':         {'addr': 13, 'type': 2, 'value': 0},
    'FLOW_RATE':                        {'addr': 14, 'type': 2, 'value': 0},
    'ACTUAL_DHW_TEMPERATURE':           {'addr': 15, 'type': 2, 'value': 0},
    'SET_DHW_TEMPERATURE':              {'addr': 16, 'type': 2, 'value': 0},
    'VENTILATION_AIR_ACTUAL_FAN_SPEED': {'addr': 17, 'type': 6, 'value': 0},
    'VENTILATION_AIR_SET_FLOW_RATE':    {'addr': 18, 'type': 6, 'value': 0},
    'EXTRACT_AIR_ACTUAL_FAN_SPEED':     {'addr': 19, 'type': 6, 'value': 0},
    'EXTRACT_AIR_SET_FLOW_RATE':        {'addr': 20, 'type': 6, 'value': 0},
    'EXTRACT_AIR_HUMIDITY':             {'addr': 21, 'type': 6, 'value': 0},
    'EXTRACT_AIR_TEMPERATURE':          {'addr': 22, 'type': 2, 'value': 0},
    'EXTRACT_AIR_DEW_POINT':            {'addr': 23, 'type': 2, 'value': 0},
    'DEW_POINT_TEMPERATUR_HC1':         {'addr': 24, 'type': 2, 'value': 0},
    'DEW_POINT_TEMPERATUR_HC2':         {'addr': 25, 'type': 2, 'value': 0},
    'COLLECTOR_TEMPERATURE':            {'addr': 26, 'type': 2, 'value': 0},
    'HOT_GAS_TEMPERATURE':              {'addr': 27, 'type': 2, 'value': 0},
    'HIGH_PRESSURE':                    {'addr': 28, 'type': 7, 'value': 0},
    'LOW_PRESSURE':                     {'addr': 29, 'type': 7, 'value': 0},
    'COMPRESSOR_STARTS':                {'addr': 30, 'type': 6, 'value': 0},
    'COMPRESSOR_SPEED':                 {'addr': 31, 'type': 2, 'value': 0},
    'MIXED_WATER_AMOUNT':               {'addr': 32, 'type': 6, 'value': 0}
}


# Block 2 System parameters (Read/write holding register) - page 30
B2_START_ADDR = 1000

B2_REGMAP_HOLDING = {
    'OPERATING_MODE':           {'addr': 1000, 'type': 8, 'value': 0},
    'ROOM_TEMP_HEAT_DAY_HC1':   {'addr': 1001, 'type': 2, 'value': 0},
    'ROOM_TEMP_HEAT_NIGHT_HC1': {'addr': 1002, 'type': 2, 'value': 0},
    'MANUAL_SET_TEMP_HC1':      {'addr': 1003, 'type': 2, 'value': 0},
    'ROOM_TEMP_HEAT_DAY_HC2':   {'addr': 1004, 'type': 2, 'value': 0},
    'ROOM_TEMP_HEAT_NIGHT_HC2': {'addr': 1005, 'type': 2, 'value': 0},
    'MANUAL_SET_TEAMP_HC2':     {'addr': 1006, 'type': 2, 'value': 0},
    'GRADIENT_HC1':             {'addr': 1007, 'type': 7, 'value': 0},
    'LOW_END_HC1':              {'addr': 1008, 'type': 2, 'value': 0},
    'GRADIENT_HC2':             {'addr': 1009, 'type': 7, 'value': 0},
    'LOW_END_HC2':              {'addr': 1010, 'type': 2, 'value': 0},
    'DHW_TEMP_SET_DAY':         {'addr': 1011, 'type': 2, 'value': 0},
    'DHW_TEMP_SET_NIGHT':       {'addr': 1012, 'type': 2, 'value': 0},
    'DHW_TEMP_SET_MANUAL':      {'addr': 1013, 'type': 2, 'value': 0},
    'MWM_SET_DAY':              {'addr': 1014, 'type': 6, 'value': 0},
    'MWM_SET_NIGHT':            {'addr': 1015, 'type': 6, 'value': 0},
    'MWM_SET_MANUAL':           {'addr': 1016, 'type': 6, 'value': 0},
    'DAY_STAGE':                {'addr': 1017, 'type': 6, 'value': 0},
    'NIGHT_STAGE':              {'addr': 1018, 'type': 6, 'value': 0},
    'PARTY_STAGE':              {'addr': 1019, 'type': 6, 'value': 0},
    'MANUAL_STAGE':             {'addr': 1020, 'type': 6, 'value': 0},
    'ROOM_TEMP_COOL_DAY_HC1':   {'addr': 1021, 'type': 2, 'value': 0},
    'ROOM_TEMP_COOL_NIGHT_HC1': {'addr': 1022, 'type': 2, 'value': 0},
    'ROOM_TEMP_COOL_DAY_HC2':   {'addr': 1023, 'type': 2, 'value': 0},
    'ROOM_TEMP_COOL_NIGHT_HC2': {'addr': 1024, 'type': 2, 'value': 0},
    'RESET':                    {'addr': 1025, 'type': 6, 'value': 0},
    'RESTART_ISG':              {'addr': 1026, 'type': 6, 'value': 0}
}

B2_OPERATING_MODE_READ = {
    # AUTOMATIK
    11: 'AUTOMATIC',
    # BEREITSCHAFT
    1: 'STANDBY',
    # TAGBETRIEB
    3: 'DAY MODE',
    # ABSENKBETRIEB
    4: 'SETBACK MODE',
    # WARMWASSER
    5: 'DHW',
    # HANDBETRIEB
    14: 'MANUAL MODE',
    # NOTBETRIEB
    0: 'EMERGENCY OPERATION'
}

B2_OPERATING_MODE_WRITE = {
    value: key for key, value in B2_OPERATING_MODE_READ.items()
}

B2_RESET = {
    'OFF': 0,
    'ON': 1
}

B2_RESTART_ISG = {
    'OFF': 0,
    'RESET': 1,
    'MENU': 2
}

# Block 3 System status (Read input register) - page 31
B3_START_ADDR = 2000

B3_REGMAP_INPUT = {
    'OPERATING_STATUS': {'addr': 2000, 'type': 6, 'value': 0},
    'FAULT_STATUS':     {'addr': 2001, 'type': 6, 'value': 0},
    'BUS_STATUS':       {'addr': 2002, 'type': 6, 'value': 0}
}

B3_OPERATING_STATUS = {
    'SWITCHING_PROGRAM_ENABLED': (1 << 0),
    'COMPRESSOR': (1 << 1),
    'HEATING': (1 << 2),
    'COOLING': (1 << 3),
    'DHW': (1 << 4),
    'ELECTRIC_REHEATING': (1 << 5),
    'SERVICE': (1 << 6),
    'POWER-OFF': (1 << 7),
    'FILTER': (1 << 8),
    'VENTILATION': (1 << 9),
    'HEATING_CIRCUIT_PUMP': (1 << 10),
    'EVAPORATOR_DEFROST': (1 << 11),
    'FILTER_EXTRACT_AIR': (1 << 12),
    'FILTER_VENTILATION_AIR': (1 << 13),
    'HEAT-UP_PROGRAM': (1 << 14)
}

B3_FAULT_STATUS = {
    'NO_FAULT': 0,
    'FAULT': 1
}

B3_BUS_STATUS = {
    'STATUS OK': 0,
    'STATUS ERROR': -1,
    'ERROR-PASSIVE': -2,
    'BUS-OFF': -3,
    'PHYSICAL-ERROR': -4
}

# WPM 3(i) Block 1 System values (Read input register) - page 22-23
#TODO: The addresses were out by one, 1 has been deducted from each. Why???
WPM3i_B1_START_ADDR = 500

WPM3i_B1_REGMAP_INPUT =             {
    'ACTUAL_TEMPERATURE_FE7':       {'addr': 500, 'type': 2, 'value': 0},
    'SET_TEMPERATURE_FE7':          {'addr': 501, 'type': 2, 'value': 0},
    'ACTUAL_TEMPERATURE_FEK':       {'addr': 502, 'type': 2, 'value': 0},
    'SET_TEMPERATURE_FEK':          {'addr': 503, 'type': 2, 'value': 0},
    'RELATIVE_HUMIDITY':            {'addr': 504, 'type': 2, 'value': 0},
    'DEW_POINT_TEMPERATURE':        {'addr': 505, 'type': 2, 'value': 0},
    'OUTSIDE_TEMPERATURE':          {'addr': 506, 'type': 2, 'value': 0},
    'ACTUAL_TEMPERATURE_HK_1':      {'addr': 507, 'type': 2, 'value': 0},
    'SET_TEMPERATURE_HK_1_A':       {'addr': 508, 'type': 2, 'value': 0},
    'SET_TEMPERATURE_HK_1_B':       {'addr': 509, 'type': 2, 'value': 0},
    'ACTUAL_TEMPERATURE_HK_2':      {'addr': 510, 'type': 2, 'value': 0},
    'SET_TEMPERATURE_HK_2':         {'addr': 511, 'type': 2, 'value': 0},
    'ACTUAL_FLOW_TEMPERATURE_WP':   {'addr': 512, 'type': 2, 'value': 0},
    'ACTUAL_FLOW_TEMPERATURE_NHZ':  {'addr': 513, 'type': 2, 'value': 0},
    'ACTUAL_FLOW_TEMPERATURE':      {'addr': 514, 'type': 2, 'value': 0},
    'ACTUAL_RETURN_TEMPERATURE':    {'addr': 515, 'type': 2, 'value': 0},
    'SET_FIXED_TEMPERATURE':        {'addr': 516, 'type': 2, 'value': 0},
    'ACTUAL_BUFFER_TEMPERATURE':    {'addr': 517, 'type': 2, 'value': 0},
    'SET_BUFFER_TEMPERATURE':       {'addr': 518, 'type': 2, 'value': 0},
    'HEATING_PRESSURE':             {'addr': 519, 'type': 7, 'value': 0},
    'FLOW_RATE':                    {'addr': 520, 'type': 2, 'value': 0},
    'ACTUAL_TEMPERATURE_A':         {'addr': 521, 'type': 2, 'value': 0},
    'SET_TEMPERATURE_A':            {'addr': 522, 'type': 2, 'value': 0},
    'ACTUAL_TEMPERATURE_FAN':       {'addr': 523, 'type': 2, 'value': 0},
    'SET_TEMPERATURE_FAN':          {'addr': 524, 'type': 2, 'value': 0},
    'ACTUAL_TEMPERATURE_AREA':      {'addr': 525, 'type': 2, 'value': 0},
    'SET_TEMPERATURE_AREA':         {'addr': 526, 'type': 2, 'value': 0},
    'COLLECTOR_TEMPERATURE':        {'addr': 527, 'type': 2, 'value': 0},
    'CYLINDER_TEMPERATURE':         {'addr': 528, 'type': 2, 'value': 0},
    'RUNTIME_A':                    {'addr': 529, 'type': 6, 'value': 0},
    'ACTUAL_TEMPERATURE_B':         {'addr': 530, 'type': 2, 'value': 0},
    'SET_TEMPERATURE_B':            {'addr': 531, 'type': 2, 'value': 0},
    'APPLICATION_LIMIT_HZG':        {'addr': 532, 'type': 2, 'value': 0},
    'APPLICATION_LIMIT_WW':         {'addr': 533, 'type': 2, 'value': 0},
    'RUNTIME_B':                    {'addr': 534, 'type': 6, 'value': 0},
    'SOURCE_TEMPERATURE':           {'addr': 535, 'type': 2, 'value': 0},
    'MIN_SOURCE_TEMPERATURE':       {'addr': 536, 'type': 2, 'value': 0},
    'SOURCE_PRESSURE':              {'addr': 537, 'type': 7, 'value': 0},
    'HOT_GAS_TEMPERATURE_A':        {'addr': 538, 'type': 2, 'value': 0},
    'HIGH_PRESSURE_A':              {'addr': 539, 'type': 2, 'value': 0},
    'LOW_PRESSURE_A':               {'addr': 540, 'type': 2, 'value': 0},
    'RETURN_TEMPERATURE_A':         {'addr': 541, 'type': 2, 'value': 0},
    'FLOW_TEMPERATURE_B':           {'addr': 542, 'type': 2, 'value': 0},
    'HOT_GAS_TEMPERATURE_B':        {'addr': 543, 'type': 2, 'value': 0},
    'LOW_PRESSURE_B':               {'addr': 544, 'type': 7, 'value': 0},
    'MEAN_PRESSURE_B':              {'addr': 545, 'type': 7, 'value': 0},
    'HIGH_PRESSURE_B':              {'addr': 546, 'type': 7, 'value': 0},
    'WP_WATER_FLOW_RATE_B':         {'addr': 547, 'type': 2, 'value': 0},
    'RETURN_TEMPERATURE_B':         {'addr': 548, 'type': 2, 'value': 0},
    'FLOW_TEMPERATURE_C':           {'addr': 549, 'type': 2, 'value': 0},
    'HOT_GAS_TEMPERATURE_C':        {'addr': 550, 'type': 2, 'value': 0},
    'LOW_PRESSURE_C':               {'addr': 551, 'type': 7, 'value': 0},
    'MEAN_PRESSURE_C':              {'addr': 552, 'type': 7, 'value': 0},
    'HIGH_PRESSURE_C':              {'addr': 553, 'type': 7, 'value': 0},
    'WP_WATER_FLOW_RATE_C':         {'addr': 554, 'type': 2, 'value': 0},
    'RETURN_TEMPERATURE_C':         {'addr': 555, 'type': 2, 'value': 0},
    'FLOW_TEMPERATURE_D':           {'addr': 556, 'type': 2, 'value': 0},
    'HOT_GAS_TEMPERATURE_D':        {'addr': 557, 'type': 2, 'value': 0},
    'LOW_PRESSURE_D':               {'addr': 558, 'type': 7, 'value': 0},
    'MEAN_PRESSURE_D':              {'addr': 559, 'type': 7, 'value': 0},
    'HIGH_PRESSURE_D':              {'addr': 560, 'type': 7, 'value': 0},
    'WP_WATER_FLOW_RATE_D':         {'addr': 561, 'type': 2, 'value': 0},
    'RETURN_TEMPERATURE_D':         {'addr': 562, 'type': 2, 'value': 0},
    'FLOW_TEMPERATURE_E':           {'addr': 563, 'type': 2, 'value': 0},
    'HOT_GAS_TEMPERATURE_E':        {'addr': 564, 'type': 2, 'value': 0},
    'LOW_PRESSURE_E':               {'addr': 565, 'type': 7, 'value': 0},
    'MEAN_PRESSURE_E':              {'addr': 566, 'type': 7, 'value': 0},
    'HIGH_PRESSURE_E':              {'addr': 567, 'type': 7, 'value': 0},
    'WP_WATER_FLOW_RATE_E':         {'addr': 568, 'type': 2, 'value': 0},
    'RETURN_TEMPERATURE_E':         {'addr': 569, 'type': 2, 'value': 0},
    'FLOW_TEMPERATURE_F':           {'addr': 570, 'type': 2, 'value': 0},
    'HOT_GAS_TEMPERATURE_F':        {'addr': 571, 'type': 2, 'value': 0},
    'LOW_PRESSURE_F':               {'addr': 572, 'type': 7, 'value': 0},
    'MEAN_PRESSURE_F':              {'addr': 573, 'type': 7, 'value': 0},
    'HIGH_PRESSURE_F':              {'addr': 574, 'type': 7, 'value': 0},
    'WP_WATER_FLOW_RATE_F':         {'addr': 575, 'type': 2, 'value': 0},
    'RETURN_TEMPERATURE_F':         {'addr': 576, 'type': 2, 'value': 0},
    'FLOW_TEMPERATURE_G':           {'addr': 577, 'type': 2, 'value': 0},
    'HOT_GAS_TEMPERATURE_G':        {'addr': 578, 'type': 2, 'value': 0},
    'LOW_PRESSURE_G':               {'addr': 579, 'type': 7, 'value': 0},
    'MEAN_PRESSURE_G':              {'addr': 580, 'type': 7, 'value': 0},
    'HIGH_PRESSURE_G':              {'addr': 581, 'type': 7, 'value': 0},
    'WP_WATER_FLOW_RATE_G':         {'addr': 582, 'type': 2, 'value': 0}
}

# WPM 3(i) Block 2 System parameters (Read/write holding register) - page 24
WPM3i_B2_START_ADDR = 1501

WPM3i_B2_REGMAP_HOLDING = {
    'OPERATING_MODE':           {'addr': 1501, 'type': 8, 'value': 0},
    'COMFORT_TEMPERATURE_A':    {'addr': 1502, 'type': 2, 'value': 0},
    'ECO_TEMPERATURE_A':        {'addr': 1503, 'type': 2, 'value': 0},
    'HEATING_CURVE_RISE_A':     {'addr': 1504, 'type': 7, 'value': 0},
    'COMFORT_TEMPERATURE_B':    {'addr': 1505, 'type': 2, 'value': 0},
    'ECO_TEMPERATURE_B':        {'addr': 1506, 'type': 2, 'value': 0},
    'HEATING_CURVE_RISE_B':     {'addr': 1507, 'type': 7, 'value': 0},
    'FIXED_VALUE_OPERATION':    {'addr': 1508, 'type': 2, 'value': 0},
    'DUAL_MODE_TEMP_HZG':       {'addr': 1509, 'type': 2, 'value': 0},
    'COMFORT_TEMPERATURE_C':    {'addr': 1510, 'type': 2, 'value': 0},
    'ECO_TEMPERATURE_C':        {'addr': 1511, 'type': 2, 'value': 0},
    'DHW_STAGES':               {'addr': 1512, 'type': 8, 'value': 0},
    'DUAL_MODE_TEMP_WW':        {'addr': 1513, 'type': 2, 'value': 0},
    'SET_FLOW_TEMPERATURE_A':   {'addr': 1514, 'type': 2, 'value': 0},
    'FLOW_TEMP_HYSTERESIS_A':   {'addr': 1515, 'type': 2, 'value': 0},
    'SET_ROOM_TEMPERATURE_A':   {'addr': 1516, 'type': 2, 'value': 0},
    'SET_FLOW_TEMPERATURE_B':   {'addr': 1517, 'type': 2, 'value': 0},
    'FLOW_TEMP_HYSTERESIS_B':   {'addr': 1518, 'type': 2, 'value': 0},
    'SET_ROOM_TEMPERATURE_B':   {'addr': 1519, 'type': 2, 'value': 0},
    'RESET':                    {'addr': 1520, 'type': 6, 'value': 0},
    'RESTART_ISG':              {'addr': 1521, 'type': 6, 'value': 0}
}

WPM3i_B2_OPERATING_MODE_READ = {
    # BEREITSCHAFTSBETRIEB
    1: 'STANDBY_MODE',
    # PROGRAMMBETRIEB
    2: 'PROGRAMMED_OPERATION',
    # KOMFORTBETRIEB
    3: 'COMFORT_MODE',
    # ECO-BETRIEB
    4: 'ECO_MODE',
    # WARMWASSERBETRIEB
    5: 'DHW_MODE',
    # NOTBETRIEB
    0: 'EMERGENCY_OPERATION'
}

WPM3i_B2_OPERATING_MODE_WRITE = {
    value: key for key, value in WPM3i_B2_OPERATING_MODE_READ.items()
}

WPM3i_B2_RESET = {
    'FAULT_LIST_RESET': 2,
    'HEAT_PUMP_RESET': 3,
    'SYSTEM_RESET': 1
}

WPM3i_B2_RESTART_ISG = {
    'OFF': 0,
    'RESTART': 1,
    'SERVICE_KEY': 2
}

# Block 3 System status (Read input register) - page 31
WPM3i_B3_START_ADDR = 2501

WPM3i_B3_REGMAP_INPUT = {
    'OPERATING_STATUS_A':   {'addr': 2501, 'type': 6, 'value': 0},
    'POWER-OFF':            {'addr': 2502, 'type': 8, 'value': 0},
    'OPERATING_STATUS_B':   {'addr': 2503, 'type': 6, 'value': 0},
    'FAULT_STATUS':         {'addr': 2504, 'type': 6, 'value': 0},
    'BUS_STATUS':           {'addr': 2505, 'type': 6, 'value': 0}
}

WPM3i_B3_OPERATING_STATUS_A = {
    'HC_1_PUMP': (1 << 0),
    'HC_2_PUMP': (1 << 1),
    'HEAT-UP_PROGRAM': (1 << 2),
    'NHZ_STAGES_RUNNING': (1 << 3),
    'HP_IN_HEATING_MODE': (1 << 4),
    'HP_IN_DHW_MODE': (1 << 5),
    'COMPRESSOR_RUNNING': (1 << 6),
    'SUMMER_MODE_ACTIVE': (1 << 7),
    'COOLING_MODE_ACTIVE': (1 << 8),
    'MIN_ONE_IWS_IN_DEFROST_MODE': (1 << 9),
    'SILENT_MODE_1_ACTIVE': (1 << 10),
    'SILENT_MODE_2_ACTIVE_(HP_OFF)': (1 << 11)
}

WPM3i_B3_POWER_OFF_STATUS = {
    'POWER-OFF': (1 << 0)
}

WPM3i_B3_OPERATING_STATUS_B = {
    'COMPRESSOR-1': (1 << 0),
    'COMPRESSOR-2': (1 << 1),
    'COMPRESSOR-3': (1 << 2),
    'COMPRESSOR-4': (1 << 3),
    'COMPRESSOR-5': (1 << 4),
    'COMPRESSOR-6': (1 << 5),
    'BUFFER_CHARGING_PUMP-1': (1 << 6),
    'BUFFER_CHARGING_PUMP-2': (1 << 7),
    'BUFFER_CHARGING_PUMP-3': (1 << 8),
    'BUFFER_CHARGING_PUMP-4': (1 << 9),
    'BUFFER_CHARGING_PUMP-5': (1 << 10),
    'BUFFER_CHARGING_PUMP-6': (1 << 11),
    'NHZ-1': (1 << 12),
    'NHZ-2': (1 << 13),
}
WPM3i_B3_FAULT_STATUS = {
    'NO_FAULT': 0,
    'FAULT': 1
}

WPM3i_B3_BUS_STATUS = {
    'STATUS_OK': 0,
    'STATUS_ERROR': -1,
    'ERROR-PASSIVE': -2,
    'BUS-OFF': -3,
    'PHYSICAL-ERROR': -4
}

class StiebelEltronAPI():
    """Stiebel Eltron API."""

    def __init__(self, conn, slave, update_on_read=False, is_wpm3i=False):
        """Initialize Stiebel Eltron communication."""
        self._conn = conn
        if is_wpm3i is False:
            self._block_1_input_regs = B1_REGMAP_INPUT            
            self._block_2_holding_regs = B2_REGMAP_HOLDING
            self._block_3_input_regs = B3_REGMAP_INPUT
            self._block_1_start_address = B1_START_ADDR
            self._block_2_start_address = B2_START_ADDR
            self._block_3_start_address = B3_START_ADDR
        else:
            self._block_1_input_regs = WPM3i_B1_REGMAP_INPUT
            self._block_2_holding_regs = WPM3i_B2_REGMAP_HOLDING
            self._block_3_input_regs = WPM3i_B3_REGMAP_INPUT
            self._block_1_start_address = WPM3i_B1_START_ADDR
            self._block_2_start_address = WPM3i_B2_START_ADDR
            self._block_3_start_address = WPM3i_B3_START_ADDR
        self._slave = slave
        self._update_on_read = update_on_read

    def update(self):
        """Request current values from heat pump."""
        ret = True
        try:
            block_1_result_input = self._conn.read_input_registers(
                unit=self._slave,
                address=self._block_1_start_address,
                count=len(self._block_1_input_regs)).registers
            block_2_result_holding = self._conn.read_holding_registers(
                unit=self._slave,
                address=self._block_2_start_address,
                count=len(self._block_2_holding_regs)).registers
            block_3_result_input = self._conn.read_input_registers(
                unit=self._slave,
                address=self._block_3_start_address,
                count=len(self._block_3_input_regs)).registers
        except AttributeError:
            # The unit does not reply reliably
            ret = False
            print("Modbus read failed")
        else:
            for k in self._block_1_input_regs:
                self._block_1_input_regs[k]['value'] = \
                    block_1_result_input[
                        self._block_1_input_regs[k]['addr'] - self._block_1_start_address]

            for k in self._block_2_holding_regs:
                self._block_2_holding_regs[k]['value'] = \
                    block_2_result_holding[
                        self._block_2_holding_regs[k]['addr'] - self._block_2_start_address]

            for k in self._block_3_input_regs:
                self._block_3_input_regs[k]['value'] = \
                    block_3_result_input[
                        self._block_3_input_regs[k]['addr'] - self._block_3_start_address]

        return ret

    def twos_comp(self, val, bits):
        """compute the 2's complement of int value val"""
        if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
            val = val - (1 << bits)        # compute negative value
        return val                         # return positive value as is

    def get_conv_val(self, name):
        """Read and convert value.

        Args:
            name: Name of value to be read.

        Returns:
            Actual value or None.
        """
        value_entry = self._block_1_input_regs.get(name)
        if value_entry is None:
            value_entry = self._block_2_holding_regs.get(name)
        if value_entry is None:
            value_entry = self._block_3_input_regs.get(name)
        if value_entry is None:
            return None

        if value_entry['type'] == 2:
            return round(self.twos_comp(value_entry['value'], 16) * 0.1, 2)
        if value_entry['type'] == 7:
            return round(self.twos_comp(value_entry['value'], 16) * 0.01, 2)

        return value_entry['value']

#    def get_raw_input_register(self, name):
#        """Get raw register value by name."""
#        if self._update_on_read:
#            self.update()
#        return self._block_1_input_regs[name]

#    def get_raw_holding_register(self, name):
#        """Get raw register value by name."""
#        if self._update_on_read:
#            self.update()
#        return self._block_2_holding_regs[name]

#    def set_raw_holding_register(self, name, value):
#        """Write to register by name."""
#        self._conn.write_register(
#            unit=self._slave,
#            address=(self._holding_regs[name]['addr']),
#            value=value)

    # Handle room temperature & humidity

    def get_current_temp(self):
        """Get the current room temperature."""
        if self._update_on_read:
            self.update()
        return self.get_conv_val('ACTUAL_ROOM_TEMPERATURE_HC1')

    def get_target_temp(self):
        """Get the target room temperature."""
        if self._update_on_read:
            self.update()
        return self.get_conv_val('ROOM_TEMP_HEAT_DAY_HC1')

    def set_target_temp(self, temp):
        """Set the target room temperature (day)(HC1)."""
        self._conn.write_register(
            unit=self._slave,
            address=(
                self._block_2_holding_regs['ROOM_TEMP_HEAT_DAY_HC1']['addr']),
            value=round(temp * 10.0))

    def get_current_humidity(self):
        """Get the current room humidity."""
        if self._update_on_read:
            self.update()
        return self.get_conv_val('RELATIVE_HUMIDITY_HC1')

    # Get Heating Info

    def get_outside_temp(self):
        """Get the outside temperature."""
        if self._update_on_read:
            self.update()
        return self.get_conv_val('OUTSIDE_TEMPERATURE')

    def get_actual_hk1_temp(self):
        """Get the heating circuit HK1 temperature."""
        if self._update_on_read:
            self.update()
        return self.get_conv_val('ACTUAL_TEMPERATURE_HK_1')

    def get_set_hk1_temp(self):
        """Get the heating circuit HK1 set temperature with heating curve rise."""
        if self._update_on_read:
            self.update()
        return self.get_conv_val('SET_TEMPERATURE_HK_1_B')

    def get_actual_wp_flow_temp(self):
        """Get the heating circuit wp flow temperature."""
        if self._update_on_read:
            self.update()
        return self.get_conv_val('ACTUAL_FLOW_TEMPERATURE_WP')

    def get_actual_nhz_flow_temp(self):
        """Get the heating circuit electric booster flow temperature."""
        if self._update_on_read:
            self.update()
        return self.get_conv_val('ACTUAL_FLOW_TEMPERATURE_NHZ')

    def get_actual_return_temp(self):
        """Get the heating circuit return temperature."""
        if self._update_on_read:
            self.update()
        return self.get_conv_val('ACTUAL_RETURN_TEMPERATURE')

    def get_heating_pressure(self):
        """Get the heating circuit pressure."""
        if self._update_on_read:
            self.update()
        return self.get_conv_val('HEATING_PRESSURE')

    def get_heating_flow_rate(self):
        """Get the heating circuit flow rate."""
        if self._update_on_read:
            self.update()
        return self.get_conv_val('FLOW_RATE')
#TODO: The flow rate seems a factor of 10 too large 

    # Handle operation mode

    def get_operation(self):
        """Return the current mode of operation."""
        if self._update_on_read:
            self.update()

        op_mode = self.get_conv_val('OPERATING_MODE')
        return B2_OPERATING_MODE_READ.get(op_mode, 'UNKNOWN')

    def set_operation(self, mode):
        """Set the operation mode."""
        self._conn.write_register(
            unit=self._slave,
            address=(self._block_2_holding_regs['OPERATING_MODE']['addr']),
            value=B2_OPERATING_MODE_WRITE.get(mode))

    # Handle device status

    def get_heating_status(self):
        """Return heater status."""
        if self._update_on_read:
            self.update()
        return bool(self.get_conv_val('OPERATING_STATUS') &
                    B3_OPERATING_STATUS['HEATING'])

    def get_cooling_status(self):
        """Cooling status."""
        if self._update_on_read:
            self.update()
        return bool(self.get_conv_val('OPERATING_STATUS') &
                    B3_OPERATING_STATUS['COOLING'])

    def get_filter_alarm_status(self):
        """Return filter alarm."""
        if self._update_on_read:
            self.update()

        filter_mask = (B3_OPERATING_STATUS['FILTER'] |
                       B3_OPERATING_STATUS['FILTER_EXTRACT_AIR'] |
                       B3_OPERATING_STATUS['FILTER_VENTILATION_AIR'])
        return bool(self.get_conv_val('OPERATING_STATUS') & filter_mask)
