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
#TODO: Istead of using A B C as the suffix to differentiate between registers use the comments in the datasheet
#TODO: The addresses were out by one, 1 has been deducted from each. Why???
WPM3i_B1_START_ADDR = 501-1

WPM3i_B1_REGMAP_INPUT = {
    'ACTUAL_TEMPERATURE_FE7':                       {'addr': 501-1, 'type': 2, 'value': 0},
    'SET_TEMPERATURE_FE7':                          {'addr': 502-1, 'type': 2, 'value': 0},
    'ACTUAL_TEMPERATURE_FEK':                       {'addr': 503-1, 'type': 2, 'value': 0},
    'SET_TEMPERATURE_FEK':                          {'addr': 504-1, 'type': 2, 'value': 0},
    'RELATIVE_HUMIDITY':                            {'addr': 505-1, 'type': 2, 'value': 0},
    'DEW_POINT_TEMPERATURE':                        {'addr': 506-1, 'type': 2, 'value': 0},
    'OUTSIDE_TEMPERATURE':                          {'addr': 507-1, 'type': 2, 'value': 0},
    'ACTUAL_TEMPERATURE_HK_1':                      {'addr': 508-1, 'type': 2, 'value': 0},
    'SET_TEMPERATURE_HK_1_A':                       {'addr': 509-1, 'type': 2, 'value': 0},
    'SET_TEMPERATURE_HK_1_B':                       {'addr': 510-1, 'type': 2, 'value': 0},
    'ACTUAL_TEMPERATURE_HK_2':                      {'addr': 511-1, 'type': 2, 'value': 0},
    'SET_TEMPERATURE_HK_2':                         {'addr': 512-1, 'type': 2, 'value': 0},
    'ACTUAL_FLOW_TEMPERATURE_WP':                   {'addr': 513-1, 'type': 2, 'value': 0},
    'ACTUAL_FLOW_TEMPERATURE_NHZ':                  {'addr': 514-1, 'type': 2, 'value': 0},
    'ACTUAL_FLOW_TEMPERATURE':                      {'addr': 515-1, 'type': 2, 'value': 0},
    'ACTUAL_RETURN_TEMPERATURE':                    {'addr': 516-1, 'type': 2, 'value': 0},
    'SET_FIXED_TEMPERATURE':                        {'addr': 517-1, 'type': 2, 'value': 0},
    'ACTUAL_BUFFER_TEMPERATURE':                    {'addr': 518-1, 'type': 2, 'value': 0},
    'SET_BUFFER_TEMPERATURE':                       {'addr': 519-1, 'type': 2, 'value': 0},
    'HEATING_PRESSURE':                             {'addr': 520-1, 'type': 7, 'value': 0},
    'FLOW_RATE':                                    {'addr': 521-1, 'type': 2, 'value': 0},
    'DHW__ACTUAL_TEMPERATURE':                      {'addr': 522-1, 'type': 2, 'value': 0},
    'DHW__SET_TEMPERATURE':                         {'addr': 523-1, 'type': 2, 'value': 0},
    'COOLING__ACTUAL_TEMPERATURE_FAN':              {'addr': 524-1, 'type': 2, 'value': 0},
    'COOLING__SET_TEMPERATURE_FAN':                 {'addr': 525-1, 'type': 2, 'value': 0},
    'COOLING__ACTUAL_TEMPERATURE_AREA':             {'addr': 526-1, 'type': 2, 'value': 0},
    'COOLING__SET_TEMPERATURE_AREA':                {'addr': 527-1, 'type': 2, 'value': 0},
    'SOLAR_THERMAL__COLLECTOR_TEMPERATURE':         {'addr': 528-1, 'type': 2, 'value': 0},
    'SOLAR_THERMAL__CYLINDER_TEMPERATURE':          {'addr': 529-1, 'type': 2, 'value': 0},
    'SOLAR_THERMAL__RUNTIME':                       {'addr': 530-1, 'type': 6, 'value': 0},
    'EXTERNAL_HEAT_SOURCE__ACTUAL_TEMPERATURE':     {'addr': 531-1, 'type': 2, 'value': 0},
    'EXTERNAL_HEAT_SOURCE__SET_TEMPERATURE':        {'addr': 532-1, 'type': 2, 'value': 0},
    'LOWER_HEATING_LIMIT__APPLICATION_LIMIT_HZG':   {'addr': 533-1, 'type': 2, 'value': 0},
    'LOWER_DHW_LIMIT__APPLICATION_LIMIT_WW':        {'addr': 534-1, 'type': 2, 'value': 0},
    'RUNTIME':                                      {'addr': 535-1, 'type': 6, 'value': 0},
    'SOURCE_TEMPERATURE':                           {'addr': 536-1, 'type': 2, 'value': 0},
    'MIN_SOURCE_TEMPERATURE':                       {'addr': 537-1, 'type': 2, 'value': 0},
    'SOURCE_PRESSURE':                              {'addr': 538-1, 'type': 7, 'value': 0},
    'HOT_GAS_TEMPERATURE':                          {'addr': 539-1, 'type': 2, 'value': 0},
    'HIGH_PRESSURE':                                {'addr': 540-1, 'type': 2, 'value': 0},
    'LOW_PRESSURE':                                 {'addr': 541-1, 'type': 2, 'value': 0},
    'HEAT_PUMP_1__RETURN_TEMPERATURE':              {'addr': 542-1, 'type': 2, 'value': 0},
    'HEAT_PUMP_1__FLOW_TEMPERATURE':                {'addr': 543-1, 'type': 2, 'value': 0},
    'HEAT_PUMP_1__HOT_GAS_TEMPERATURE':             {'addr': 544-1, 'type': 2, 'value': 0},
    'HEAT_PUMP_1__LOW_PRESSURE':                    {'addr': 545-1, 'type': 7, 'value': 0},
    'HEAT_PUMP_1__MEAN_PRESSURE':                   {'addr': 546-1, 'type': 7, 'value': 0},
    'HEAT_PUMP_1__HIGH_PRESSURE':                   {'addr': 547-1, 'type': 7, 'value': 0},
    'HEAT_PUMP_1__WP_WATER_FLOW_RATE':              {'addr': 548-1, 'type': 2, 'value': 0},
    'HEAT_PUMP_2__RETURN_TEMPERATURE':              {'addr': 549-1, 'type': 2, 'value': 0},
    'HEAT_PUMP_2__FLOW_TEMPERATURE':                {'addr': 550-1, 'type': 2, 'value': 0},
    'HEAT_PUMP_2__HOT_GAS_TEMPERATURE':             {'addr': 551-1, 'type': 2, 'value': 0},
    'HEAT_PUMP_2__LOW_PRESSURE':                    {'addr': 552-1, 'type': 7, 'value': 0},
    'HEAT_PUMP_2__MEAN_PRESSURE':                   {'addr': 553-1, 'type': 7, 'value': 0},
    'HEAT_PUMP_2__HIGH_PRESSURE':                   {'addr': 554-1, 'type': 7, 'value': 0},
    'HEAT_PUMP_2__WP_WATER_FLOW_RATE':              {'addr': 555-1, 'type': 2, 'value': 0},
    'HEAT_PUMP_3__RETURN_TEMPERATURE':              {'addr': 556-1, 'type': 2, 'value': 0},
    'HEAT_PUMP_3__FLOW_TEMPERATURE':                {'addr': 557-1, 'type': 2, 'value': 0},
    'HEAT_PUMP_3__HOT_GAS_TEMPERATURE':             {'addr': 558-1, 'type': 2, 'value': 0},
    'HEAT_PUMP_3__LOW_PRESSURE':                    {'addr': 559-1, 'type': 7, 'value': 0},
    'HEAT_PUMP_3__MEAN_PRESSURE':                   {'addr': 560-1, 'type': 7, 'value': 0},
    'HEAT_PUMP_3__HIGH_PRESSURE':                   {'addr': 561-1, 'type': 7, 'value': 0},
    'HEAT_PUMP_3__WP_WATER_FLOW_RATE':              {'addr': 562-1, 'type': 2, 'value': 0},
    'HEAT_PUMP_4__RETURN_TEMPERATURE':              {'addr': 563-1, 'type': 2, 'value': 0},
    'HEAT_PUMP_4__FLOW_TEMPERATURE':                {'addr': 564-1, 'type': 2, 'value': 0},
    'HEAT_PUMP_4__HOT_GAS_TEMPERATURE':             {'addr': 565-1, 'type': 2, 'value': 0},
    'HEAT_PUMP_4__LOW_PRESSURE':                    {'addr': 566-1, 'type': 7, 'value': 0},
    'HEAT_PUMP_4__MEAN_PRESSURE':                   {'addr': 567-1, 'type': 7, 'value': 0},
    'HEAT_PUMP_4__HIGH_PRESSURE':                   {'addr': 568-1, 'type': 7, 'value': 0},
    'HEAT_PUMP_4__WP_WATER_FLOW_RATE':              {'addr': 569-1, 'type': 2, 'value': 0},
    'HEAT_PUMP_5__RETURN_TEMPERATURE':              {'addr': 570-1, 'type': 2, 'value': 0},
    'HEAT_PUMP_5__FLOW_TEMPERATURE':                {'addr': 571-1, 'type': 2, 'value': 0},
    'HEAT_PUMP_5__HOT_GAS_TEMPERATURE':             {'addr': 572-1, 'type': 2, 'value': 0},
    'HEAT_PUMP_5__LOW_PRESSURE':                    {'addr': 573-1, 'type': 7, 'value': 0},
    'HEAT_PUMP_5__MEAN_PRESSURE':                   {'addr': 574-1, 'type': 7, 'value': 0},
    'HEAT_PUMP_5__HIGH_PRESSURE':                   {'addr': 575-1, 'type': 7, 'value': 0},
    'HEAT_PUMP_5__WP_WATER_FLOW_RATE':              {'addr': 576-1, 'type': 2, 'value': 0},
    'HEAT_PUMP_6__RETURN_TEMPERATURE':              {'addr': 577-1, 'type': 2, 'value': 0},
    'HEAT_PUMP_6__FLOW_TEMPERATURE':                {'addr': 578-1, 'type': 2, 'value': 0},
    'HEAT_PUMP_6__HOT_GAS_TEMPERATURE':             {'addr': 579-1, 'type': 2, 'value': 0},
    'HEAT_PUMP_6__LOW_PRESSURE':                    {'addr': 580-1, 'type': 7, 'value': 0},
    'HEAT_PUMP_6__MEAN_PRESSURE':                   {'addr': 581-1, 'type': 7, 'value': 0},
    'HEAT_PUMP_6__HIGH_PRESSURE':                   {'addr': 582-1, 'type': 7, 'value': 0},
    'HEAT_PUMP_6__WP_WATER_FLOW_RATE':              {'addr': 583-1, 'type': 2, 'value': 0}
}

# WPM 3(i) Block 2 System parameters (Read/write holding register) - page 24
WPM3i_B2_START_ADDR = 1501

WPM3i_B2_REGMAP_HOLDING = {
    'OPERATING_MODE':                           {'addr': 1501, 'type': 8, 'value': 0},
    'HEATING_CIRCUIT_1__COMFORT_TEMPERATURE':   {'addr': 1502, 'type': 2, 'value': 0},
    'HEATING_CIRCUIT_1__ECO_TEMPERATURE':       {'addr': 1503, 'type': 2, 'value': 0},
    'HEATING_CIRCUIT_1__HEATING_CURVE_RISE':    {'addr': 1504, 'type': 7, 'value': 0},
    'HEATING_CIRCUIT_2__COMFORT_TEMPERATURE':   {'addr': 1505, 'type': 2, 'value': 0},
    'HEATING_CIRCUIT_2__ECO_TEMPERATURE':       {'addr': 1506, 'type': 2, 'value': 0},
    'HEATING_CIRCUIT_2__HEATING_CURVE_RISE':    {'addr': 1507, 'type': 7, 'value': 0},
    'FIXED_VALUE_OPERATION':                    {'addr': 1508, 'type': 2, 'value': 0},
    'DUAL_MODE_TEMP_HZG':                       {'addr': 1509, 'type': 2, 'value': 0},
    'DHW__COMFORT_TEMPERATURE':                 {'addr': 1510, 'type': 2, 'value': 0},
    'DHW__ECO_TEMPERATURE':                     {'addr': 1511, 'type': 2, 'value': 0},
    'DHW_STAGES':                               {'addr': 1512, 'type': 8, 'value': 0},
    'DUAL_MODE_TEMP_WW':                        {'addr': 1513, 'type': 2, 'value': 0},
    'AREA_COOLING__SET_FLOW_TEMPERATURE':       {'addr': 1514, 'type': 2, 'value': 0},
    'AREA_COOLING__FLOW_TEMP_HYSTERESIS':       {'addr': 1515, 'type': 2, 'value': 0},
    'AREA_COOLING__SET_ROOM_TEMPERATURE':       {'addr': 1516, 'type': 2, 'value': 0},
    'FAN_COOLING__SET_FLOW_TEMPERATURE':        {'addr': 1517, 'type': 2, 'value': 0},
    'FAN_COOLING__FLOW_TEMP_HYSTERESIS':        {'addr': 1518, 'type': 2, 'value': 0},
    'FAN_COOLING__SET_ROOM_TEMPERATURE':        {'addr': 1519, 'type': 2, 'value': 0},
    'RESET':                                    {'addr': 1520, 'type': 6, 'value': 0},
    'RESTART_ISG':                              {'addr': 1521, 'type': 6, 'value': 0}
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

# Block 4 System status (Read input register) - page 26
WPM3i_B4_START_ADDR = 3501-1

WPM3i_B4_REGMAP_INPUT = {
    'ALL_HEAT_PUMPS__AMOUNT_OF_HEAT__VD_HEATING_DAY__KWH':      {'addr': 3501-1, 'type': 6, 'value': 0},
    'ALL_HEAT_PUMPS__AMOUNT_OF_HEAT__VD_HEATING_TOTAL__KWH':    {'addr': 3502-1, 'type': 6, 'value': 0},
    'ALL_HEAT_PUMPS__AMOUNT_OF_HEAT__VD_HEATING_TOTAL__MWH':    {'addr': 3503-1, 'type': 6, 'value': 0},
    'ALL_HEAT_PUMPS__AMOUNT_OF_HEAT__VD_DHW_DAY__KWH':          {'addr': 3504-1, 'type': 6, 'value': 0},
    'ALL_HEAT_PUMPS__AMOUNT_OF_HEAT__VD_DHW_TOTAL__KWH':        {'addr': 3505-1, 'type': 6, 'value': 0},
    'ALL_HEAT_PUMPS__AMOUNT_OF_HEAT__VD_DHW_TOTAL__MWH':        {'addr': 3506-1, 'type': 6, 'value': 0},
    'ALL_HEAT_PUMPS__AMOUNT_OF_HEAT__NHZ_HEATING_TOTAL__KWH':   {'addr': 3507-1, 'type': 6, 'value': 0},
    'ALL_HEAT_PUMPS__AMOUNT_OF_HEAT__NHZ_HEATING_TOTAL__MWH':   {'addr': 3508-1, 'type': 6, 'value': 0},
    'ALL_HEAT_PUMPS__AMOUNT_OF_HEAT__NHZ_DHW_TOTAL__KWH':       {'addr': 3509-1, 'type': 6, 'value': 0},
    'ALL_HEAT_PUMPS__AMOUNT_OF_HEAT__NHZ_DHW_TOTAL__MWH':       {'addr': 3510-1, 'type': 6, 'value': 0},
    'ALL_HEAT_PUMPS__POWER_CONSUMPTION__VD_HEATING_DAY__KWH':   {'addr': 3511-1, 'type': 6, 'value': 0},
    'ALL_HEAT_PUMPS__POWER_CONSUMPTION__VD_HEATING_TOTAL__KWH': {'addr': 3512-1, 'type': 6, 'value': 0},
    'ALL_HEAT_PUMPS__POWER_CONSUMPTION__VD_HEATING_TOTAL__MWH': {'addr': 3513-1, 'type': 6, 'value': 0},
    'ALL_HEAT_PUMPS__POWER_CONSUMPTION__VD_DHW_DAY__KWH':       {'addr': 3514-1, 'type': 6, 'value': 0},
    'ALL_HEAT_PUMPS__POWER_CONSUMPTION__VD_DHW_TOTAL__KWH':     {'addr': 3515-1, 'type': 6, 'value': 0},
    'ALL_HEAT_PUMPS__POWER_CONSUMPTION__VD_DHW_TOTAL__MWH':     {'addr': 3516-1, 'type': 6, 'value': 0},
    'VD_HEATING_RUNTIME':                                       {'addr': 3517-1, 'type': 6, 'value': 0},
    'VD_DHW_RUNTIME':                                           {'addr': 3518-1, 'type': 6, 'value': 0},
    'VD_COOLING_RUNTIME':                                       {'addr': 3519-1, 'type': 6, 'value': 0},
    'NHZ_1_RUNTIME':                                            {'addr': 3520-1, 'type': 6, 'value': 0},
    'NHZ_2_RUNTIME':                                            {'addr': 3521-1, 'type': 6, 'value': 0},
    'NHZ_1_AND_2_RUNTIME':                                      {'addr': 3522-1, 'type': 6, 'value': 0},
    'HP1__AMOUNT_OF_HEAT__VD_HEATING_DAY__KWH':                 {'addr': 3523-1, 'type': 6, 'value': 0},
    'HP1__AMOUNT_OF_HEAT__VD_HEATING_TOTAL__KWH':               {'addr': 3524-1, 'type': 6, 'value': 0},
    'HP1__AMOUNT_OF_HEAT__VD_HEATING_TOTAL__MWH':               {'addr': 3525-1, 'type': 6, 'value': 0},
    'HP1__AMOUNT_OF_HEAT__VD_DHW_DAY__KWH':                     {'addr': 3526-1, 'type': 6, 'value': 0},
    'HP1__AMOUNT_OF_HEAT__VD_DHW_TOTAL__KWH':                   {'addr': 3527-1, 'type': 6, 'value': 0},
    'HP1__AMOUNT_OF_HEAT__VD_DHW_TOTAL__MWH':                   {'addr': 3528-1, 'type': 6, 'value': 0},
    'HP1__AMOUNT_OF_HEAT__NHZ_HEATING_TOTAL__KWH':              {'addr': 3529-1, 'type': 6, 'value': 0},
    'HP1__AMOUNT_OF_HEAT__NHZ_HEATING_TOTAL__MWH':              {'addr': 3530-1, 'type': 6, 'value': 0},
    'HP1__AMOUNT_OF_HEAT__NHZ_DHW_TOTAL__KWH':                  {'addr': 3531-1, 'type': 6, 'value': 0},
    'HP1__AMOUNT_OF_HEAT__NHZ_DHW_TOTAL__MWH':                  {'addr': 3532-1, 'type': 6, 'value': 0},
    'HP1__POWER_CONSUMPTION__VD_HEATING_DAY__KWH':              {'addr': 3533-1, 'type': 6, 'value': 0},
    'HP1__POWER_CONSUMPTION__VD_HEATING_TOTAL__KWH':            {'addr': 3534-1, 'type': 6, 'value': 0},
    'HP1__POWER_CONSUMPTION__VD_HEATING_TOTAL__MWH':            {'addr': 3535-1, 'type': 6, 'value': 0},
    'HP1__POWER_CONSUMPTION__VD_DHW_DAY__KWH':                  {'addr': 3536-1, 'type': 6, 'value': 0},
    'HP1__POWER_CONSUMPTION__VD_DHW_TOTAL__KWH':                {'addr': 3537-1, 'type': 6, 'value': 0},
    'HP1__POWER_CONSUMPTION__VD_DHW_TOTAL__MWH':                {'addr': 3538-1, 'type': 6, 'value': 0},
    'HP1__RUNTIME__VD_HEATING':                                 {'addr': 3539-1, 'type': 6, 'value': 0},
    'HP1__RUNTIME__VD_2_HEATING':                               {'addr': 3540-1, 'type': 6, 'value': 0},
    'HP1__RUNTIME__VD_1_AND_2_HEATING':                         {'addr': 3541-1, 'type': 6, 'value': 0},
    'HP1__RUNTIME__VD_DHW':                                     {'addr': 3542-1, 'type': 6, 'value': 0},
    'HP1__RUNTIME__VD_2_DHW':                                   {'addr': 3543-1, 'type': 6, 'value': 0},
    'HP1__RUNTIME__VD_1_AND_2_DHW':                             {'addr': 3544-1, 'type': 6, 'value': 0},
    'HP1__RUNTIME__VD_COOLING':                                 {'addr': 3545-1, 'type': 6, 'value': 0},
    'REHEATING_STAGE__RUNTIME__NHZ_1':                          {'addr': 3546-1, 'type': 6, 'value': 0},
    'REHEATING_STAGE__RUNTIME__NHZ_2':                          {'addr': 3547-1, 'type': 6, 'value': 0},
    'REHEATING_STAGE__RUNTIME__NHZ_1_AND_2':                    {'addr': 3548-1, 'type': 6, 'value': 0},
    'HP2__AMOUNT_OF_HEAT__VD_HEATING_DAY__KWH':                 {'addr': 3549-1, 'type': 6, 'value': 0},
    'HP2__AMOUNT_OF_HEAT__VD_HEATING_TOTAL__KWH':               {'addr': 3550-1, 'type': 6, 'value': 0},
    'HP2__AMOUNT_OF_HEAT__VD_HEATING_TOTAL__MWH':               {'addr': 3551-1, 'type': 6, 'value': 0},
    'HP2__AMOUNT_OF_HEAT__VD_DHW_DAY__KWH':                     {'addr': 3552-1, 'type': 6, 'value': 0},
    'HP2__AMOUNT_OF_HEAT__VD_DHW_TOTAL__KWH':                   {'addr': 3553-1, 'type': 6, 'value': 0},
    'HP2__AMOUNT_OF_HEAT__VD_DHW_TOTAL__MWH':                   {'addr': 3554-1, 'type': 6, 'value': 0},
    'HP2__POWER_CONSUMPTION__VD_HEATING_DAY__KWH':              {'addr': 3555-1, 'type': 6, 'value': 0},
    'HP2__POWER_CONSUMPTION__VD_HEATING_TOTAL__KWH':            {'addr': 3556-1, 'type': 6, 'value': 0},
    'HP2__POWER_CONSUMPTION__VD_HEATING_TOTAL__MWH':            {'addr': 3557-1, 'type': 6, 'value': 0},
    'HP2__POWER_CONSUMPTION__VD_DHW_DAY__KWH':                  {'addr': 3558-1, 'type': 6, 'value': 0},
    'HP2__POWER_CONSUMPTION__VD_DHW_TOTAL__KWH':                {'addr': 3559-1, 'type': 6, 'value': 0},
    'HP2__POWER_CONSUMPTION__VD_DHW_TOTAL__MWH':                {'addr': 3560-1, 'type': 6, 'value': 0},
    'HP2__RUNTIME__VD_HEATING':                                 {'addr': 3561-1, 'type': 6, 'value': 0},
    'HP2__RUNTIME__VD_2_HEATING':                               {'addr': 3562-1, 'type': 6, 'value': 0},
    'HP2__RUNTIME__VD_1_AND_2_HEATING':                         {'addr': 3563-1, 'type': 6, 'value': 0},
    'HP2__RUNTIME__VD_DHW':                                     {'addr': 3564-1, 'type': 6, 'value': 0},
    'HP2__RUNTIME__VD_2_DHW':                                   {'addr': 3565-1, 'type': 6, 'value': 0},
    'HP2__RUNTIME__VD_1_AND_2_DHW':                             {'addr': 3566-1, 'type': 6, 'value': 0},
    'HP2__RUNTIME__VD_COOLING':                                 {'addr': 3567-1, 'type': 6, 'value': 0},
    'HP3__AMOUNT_OF_HEAT__VD_HEATING_DAY__KWH':                 {'addr': 3568-1, 'type': 6, 'value': 0},
    'HP3__AMOUNT_OF_HEAT__VD_HEATING_TOTAL__KWH':               {'addr': 3569-1, 'type': 6, 'value': 0},
    'HP3__AMOUNT_OF_HEAT__VD_HEATING_TOTAL__MWH':               {'addr': 3570-1, 'type': 6, 'value': 0},
    'HP3__AMOUNT_OF_HEAT__VD_DHW_DAY__KWH':                     {'addr': 3571-1, 'type': 6, 'value': 0},
    'HP3__AMOUNT_OF_HEAT__VD_DHW_TOTAL__KWH':                   {'addr': 3572-1, 'type': 6, 'value': 0},
    'HP3__AMOUNT_OF_HEAT__VD_DHW_TOTAL__MWH':                   {'addr': 3573-1, 'type': 6, 'value': 0},
    'HP3__POWER_CONSUMPTION__VD_HEATING_DAY__KWH':              {'addr': 3574-1, 'type': 6, 'value': 0},
    'HP3__POWER_CONSUMPTION__VD_HEATING_TOTAL__KWH':            {'addr': 3575-1, 'type': 6, 'value': 0},
    'HP3__POWER_CONSUMPTION__VD_HEATING_TOTAL__MWH':            {'addr': 3576-1, 'type': 6, 'value': 0},
    'HP3__POWER_CONSUMPTION__VD_DHW_DAY__KWH':                  {'addr': 3577-1, 'type': 6, 'value': 0},
    'HP3__POWER_CONSUMPTION__VD_DHW_TOTAL__KWH':                {'addr': 3578-1, 'type': 6, 'value': 0},
    'HP3__POWER_CONSUMPTION__VD_DHW_TOTAL__MWH':                {'addr': 3579-1, 'type': 6, 'value': 0},
    'HP3__RUNTIME__VD_HEATING':                                 {'addr': 3580-1, 'type': 6, 'value': 0},
    'HP3__RUNTIME__VD_2_HEATING':                               {'addr': 3581-1, 'type': 6, 'value': 0},
    'HP3__RUNTIME__VD_1_AND_2_HEATING':                         {'addr': 3582-1, 'type': 6, 'value': 0},
    'HP3__RUNTIME__VD_DHW':                                     {'addr': 3583-1, 'type': 6, 'value': 0},
    'HP3__RUNTIME__VD_2_DHW':                                   {'addr': 3584-1, 'type': 6, 'value': 0},
    'HP3__RUNTIME__VD_1_AND_2_DHW':                             {'addr': 3585-1, 'type': 6, 'value': 0},
    'HP3__RUNTIME__VD_COOLING':                                 {'addr': 3586-1, 'type': 6, 'value': 0},
    'HP4__AMOUNT_OF_HEAT__VD_HEATING_DAY__KWH':                 {'addr': 3587-1, 'type': 6, 'value': 0},
    'HP4__AMOUNT_OF_HEAT__VD_HEATING_TOTAL__KWH':               {'addr': 3588-1, 'type': 6, 'value': 0},
    'HP4__AMOUNT_OF_HEAT__VD_HEATING_TOTAL__MWH':               {'addr': 3589-1, 'type': 6, 'value': 0},
    'HP4__AMOUNT_OF_HEAT__VD_DHW_DA__KWH':                      {'addr': 3590-1, 'type': 6, 'value': 0},
    'HP4__AMOUNT_OF_HEAT__VD_DHW_TOTAL__KWH':                   {'addr': 3591-1, 'type': 6, 'value': 0},
    'HP4__AMOUNT_OF_HEAT__VD_DHW_TOTAL__MWH':                   {'addr': 3592-1, 'type': 6, 'value': 0},
    'HP4__POWER_CONSUMPTION__VD_HEATING_DAY__KWH':              {'addr': 3593-1, 'type': 6, 'value': 0},
    'HP4__POWER_CONSUMPTION__VD_HEATING_TOTAL__KWH':            {'addr': 3594-1, 'type': 6, 'value': 0},
    'HP4__POWER_CONSUMPTION__VD_HEATING_TOTAL__MWH':            {'addr': 3595-1, 'type': 6, 'value': 0},
    'HP4__POWER_CONSUMPTION__VD_DHW_DAY__KWH':                  {'addr': 3596-1, 'type': 6, 'value': 0},
    'HP4__POWER_CONSUMPTION__VD_DHW_TOTAL__KWH':                {'addr': 3597-1, 'type': 6, 'value': 0},
    'HP4__POWER_CONSUMPTION__VD_DHW_TOTAL__MWH':                {'addr': 3598-1, 'type': 6, 'value': 0},
    'HP4__RUNTIME__VD_HEATING':                                 {'addr': 3599-1, 'type': 6, 'value': 0},
    'HP4__RUNTIME__VD_2_HEATING':                               {'addr': 3600-1, 'type': 6, 'value': 0},
    'HP4__RUNTIME__VD_1_AND_2_HEATING':                         {'addr': 3601-1, 'type': 6, 'value': 0},
    'HP4__RUNTIME__VD_DHW':                                     {'addr': 3602-1, 'type': 6, 'value': 0},
    'HP4__RUNTIME__VD_2_DHW':                                   {'addr': 3603-1, 'type': 6, 'value': 0},
    'HP4__RUNTIME__VD_1_AND_2_DHW':                             {'addr': 3604-1, 'type': 6, 'value': 0},
    'HP4__RUNTIME__VD_COOLING':                                 {'addr': 3605-1, 'type': 6, 'value': 0},
    'HP5__AMOUNT_OF_HEAT__VD_HEATING_DAY__KWH':                 {'addr': 3606-1, 'type': 6, 'value': 0},
    'HP5__AMOUNT_OF_HEAT__VD_HEATING_TOTAL__KWH':               {'addr': 3607-1, 'type': 6, 'value': 0},
    'HP5__AMOUNT_OF_HEAT__VD_HEATING_TOTAL__MWH':               {'addr': 3608-1, 'type': 6, 'value': 0},
    'HP5__AMOUNT_OF_HEAT__VD_DHW_DAY__KWH':                     {'addr': 3609-1, 'type': 6, 'value': 0},
    'HP5__AMOUNT_OF_HEAT__VD_DHW_TOTAL__KWH':                   {'addr': 3610-1, 'type': 6, 'value': 0},
    'HP5__AMOUNT_OF_HEAT__VD_DHW_TOTAL__MWH':                   {'addr': 3611-1, 'type': 6, 'value': 0}
#    'HP5__POWER_CONSUMPTION__VD_HEATING_DAY__KWH':              {'addr': 3612-1, 'type': 6, 'value': 0},
#    'HP5__POWER_CONSUMPTION__VD_HEATING_TOTAL__KWH':            {'addr': 3613-1, 'type': 6, 'value': 0},
#    'HP5__POWER_CONSUMPTION__VD_HEATING_TOTAL__MWH':            {'addr': 3614-1, 'type': 6, 'value': 0},
#    'HP5__POWER_CONSUMPTION__VD_DHW_DAY__KWH':                  {'addr': 3615-1, 'type': 6, 'value': 0},
#    'HP5__POWER_CONSUMPTION__VD_DHW_TOTAL__KWH':                {'addr': 3616-1, 'type': 6, 'value': 0},
#    'HP5__POWER_CONSUMPTION__VD_DHW_TOTAL__MWH':                {'addr': 3617-1, 'type': 6, 'value': 0},
#    'HP5__RUNTIME__VD_HEATING':                                 {'addr': 3618-1, 'type': 6, 'value': 0},
#    'HP5__RUNTIME__VD_2_HEATING':                               {'addr': 3619-1, 'type': 6, 'value': 0},
#    'HP5__RUNTIME__VD_1_AND_2_HEATING':                         {'addr': 3620-1, 'type': 6, 'value': 0},
#    'HP5__RUNTIME__VD_DHW':                                     {'addr': 3621-1, 'type': 6, 'value': 0},
#    'HP5__RUNTIME__VD_2_DHW':                                   {'addr': 3622-1, 'type': 6, 'value': 0},
#    'HP5__RUNTIME__VD_1_AND_2_DHW':                             {'addr': 3623-1, 'type': 6, 'value': 0},
#    'HP5__RUNTIME__VD_COOLING':                                 {'addr': 3624-1, 'type': 6, 'value': 0},
#    'HP6__AMOUNT_OF_HEAT__VD_HEATING_DAY__KWH':                 {'addr': 3625-1, 'type': 6, 'value': 0},
#    'HP6__AMOUNT_OF_HEAT__VD_HEATING_TOTAL__KWH':               {'addr': 3626-1, 'type': 6, 'value': 0},
#    'HP6__AMOUNT_OF_HEAT__VD_HEATING_TOTAL__MWH':               {'addr': 3627-1, 'type': 6, 'value': 0},
#    'HP6__AMOUNT_OF_HEAT__VD_DHW_DAY__KWH':                     {'addr': 3628-1, 'type': 6, 'value': 0},
#    'HP6__AMOUNT_OF_HEAT__VD_DHW_TOTAL__KWH':                   {'addr': 3629-1, 'type': 6, 'value': 0},
#    'HP6__AMOUNT_OF_HEAT__VD_DHW_TOTAL__MWH':                   {'addr': 3630-1, 'type': 6, 'value': 0},
#    'HP6__POWER_CONSUMPTION__VD_HEATING_DAY__KWH':              {'addr': 3631-1, 'type': 6, 'value': 0},
#    'HP6__POWER_CONSUMPTION__VD_HEATING_TOTAL__KWH':            {'addr': 3632-1, 'type': 6, 'value': 0},
#    'HP6__POWER_CONSUMPTION__VD_HEATING_TOTAL__MWH':            {'addr': 3633-1, 'type': 6, 'value': 0},
#    'HP6__POWER_CONSUMPTION__VD_DHW_DAY__KWH':                  {'addr': 3634-1, 'type': 6, 'value': 0},
#    'HP6__POWER_CONSUMPTION__VD_DHW_TOTAL__KWH':                {'addr': 3635-1, 'type': 6, 'value': 0},
#    'HP6__POWER_CONSUMPTION__VD_DHW_TOTAL__MWH':                {'addr': 3636-1, 'type': 6, 'value': 0},
#    'HP6__RUNTIME__VD_HEATING':                                 {'addr': 3637-1, 'type': 6, 'value': 0},
#    'HP6__RUNTIME__VD_2_HEATING':                               {'addr': 3638-1, 'type': 6, 'value': 0},
#    'HP6__RUNTIME__VD_1_AND_2_HEATING':                         {'addr': 3639-1, 'type': 6, 'value': 0},
#    'HP6__RUNTIME__VD_DHW':                                     {'addr': 3640-1, 'type': 6, 'value': 0},
#    'HP6__RUNTIME__VD_2_DHW':                                   {'addr': 3641-1, 'type': 6, 'value': 0},
#    'HP6__RUNTIME__VD_1_AND_2_DHW':                             {'addr': 3642-1, 'type': 6, 'value': 0},
#    'HP6__RUNTIME__VD_COOLING':                                 {'addr': 3643-1, 'type': 6, 'value': 0}
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
            self._block_4_input_regs = None
            self._block_1_start_address = B1_START_ADDR
            self._block_2_start_address = B2_START_ADDR
            self._block_3_start_address = B3_START_ADDR
            self._block_4_start_address = None
        else:
            self._block_1_input_regs = WPM3i_B1_REGMAP_INPUT
            self._block_2_holding_regs = WPM3i_B2_REGMAP_HOLDING
            self._block_3_input_regs = WPM3i_B3_REGMAP_INPUT
            self._block_4_input_regs = WPM3i_B4_REGMAP_INPUT
            self._block_1_start_address = WPM3i_B1_START_ADDR
            self._block_2_start_address = WPM3i_B2_START_ADDR
            self._block_3_start_address = WPM3i_B3_START_ADDR
            self._block_4_start_address = WPM3i_B4_START_ADDR
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
            if self._block_4_start_address is not None:
                    block_4_result_input = self._conn.read_input_registers(
                        unit=self._slave,
                        address=self._block_4_start_address,
                        count=len(self._block_4_input_regs)).registers
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

            if self._block_4_start_address is not None:
                for k in self._block_4_input_regs:
                    self._block_4_input_regs[k]['value'] = \
                        block_4_result_input[
                            self._block_4_input_regs[k]['addr'] - self._block_4_start_address]
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
        if self._block_4_start_address is not None:
            if value_entry is None:
                value_entry = self._block_4_input_regs.get(name)
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

    # Get Info->System->Heating Info

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

    def get_heating_or_dhw_flow_rate(self):
        """Get the heating or hot water circuit flow rate."""
        if self._update_on_read:
            self.update()
        return round(self.get_conv_val('FLOW_RATE') / 10, 2)
#TODO: The flow rate seems a factor of 10 too large

    def get_hzg_lower_heating_limit_temp(self):
        """Get the LOWER_HEATING_LIMIT__APPLICATION_LIMIT_HZG."""
        if self._update_on_read:
            self.update()
        return self.get_conv_val('LOWER_HEATING_LIMIT__APPLICATION_LIMIT_HZG')

    # Get Info->System->DHW hot water Info
    def get_actual_dhw_temp(self):
        """Get the hot water circuit DHW temperature."""
        if self._update_on_read:
            self.update()
        return self.get_conv_val('DHW__ACTUAL_TEMPERATURE')

    def get_set_dhw_temp(self):
        """Get the hot water circuit DHW set temperature."""
        if self._update_on_read:
            self.update()
        return self.get_conv_val('DHW__SET_TEMPERATURE')

    def get_ww_lower_dhw_limit_temp(self):
        """Get the LOWER_DHW_LIMIT__APPLICATION_LIMIT_WW."""
        if self._update_on_read:
            self.update()
        return self.get_conv_val('LOWER_DHW_LIMIT__APPLICATION_LIMIT_WW')

    # Get Info->System->Source Info
    def get_source_temp(self):
        """Get the source return temperature."""
        if self._update_on_read:
            self.update()
        return self.get_conv_val('SOURCE_TEMPERATURE')

    def get_min_source_temp(self):
        """Get the minimum source temperature."""
        if self._update_on_read:
            self.update()
        return self.get_conv_val('MIN_SOURCE_TEMPERATURE')

    def get_source_pressure(self):
        """Get the source circuit pressure."""
        if self._update_on_read:
            self.update()
        return self.get_conv_val('SOURCE_PRESSURE')

    # Heat Pump
    def get_hp_hot_gas_temp(self):
        """Get the heat pump hot get temperature."""
        if self._update_on_read:
            self.update()
        return self.get_conv_val('HOT_GAS_TEMPERATURE')

    def get_hp_high_pressure(self):
        """Get the heat pump high pressure."""
        if self._update_on_read:
            self.update()
        return self.get_conv_val('HIGH_PRESSURE')

    def get_hp_low_pressure(self):
        """Get the heat pump low pressure."""
        if self._update_on_read:
            self.update()
        return self.get_conv_val('LOW_PRESSURE')

    # Get Info->Source->Amount of Heat Info
    def get_vd_heating_day_kwh(self):
        """Get the day kWh for vd heating."""
        if self._update_on_read:
            self.update()
        return self.get_conv_val('ALL_HEAT_PUMPS__AMOUNT_OF_HEAT__VD_HEATING_DAY__KWH')

    def get_vd_heating_total_kwh(self):
        """Get the total kWh for vd heating."""
        if self._update_on_read:
            self.update()
        return (self.get_conv_val('ALL_HEAT_PUMPS__AMOUNT_OF_HEAT__VD_HEATING_TOTAL__MWH')*1000) + self.get_conv_val('ALL_HEAT_PUMPS__AMOUNT_OF_HEAT__VD_HEATING_TOTAL__KWH')

    def get_vd_dhw_day_kwh(self):
        """Get the day kWh for vd dhw."""
        if self._update_on_read:
            self.update()
        return self.get_conv_val('ALL_HEAT_PUMPS__AMOUNT_OF_HEAT__VD_DHW_DAY__KWH')

    def get_vd_dhw_total_kwh(self):
        """Get the total kWh for vd dhw."""
        if self._update_on_read:
            self.update()
        return (self.get_conv_val('ALL_HEAT_PUMPS__AMOUNT_OF_HEAT__VD_DHW_TOTAL__MWH')*1000) + self.get_conv_val('ALL_HEAT_PUMPS__AMOUNT_OF_HEAT__VD_DHW_TOTAL__KWH')

    def get_nhz_heating_total_kwh(self):
        """Get the total kWh for nhz heating."""
        if self._update_on_read:
            self.update()
        return (self.get_conv_val('ALL_HEAT_PUMPS__AMOUNT_OF_HEAT__NHZ_HEATING_TOTAL__MWH')*1000) + self.get_conv_val('ALL_HEAT_PUMPS__AMOUNT_OF_HEAT__NHZ_HEATING_TOTAL__KWH')

    def get_nhz_dhw_total_kwh(self):
        """Get the total kWh for nhz dwh."""
        if self._update_on_read:
            self.update()
        return (self.get_conv_val('ALL_HEAT_PUMPS__AMOUNT_OF_HEAT__NHZ_DHW_TOTAL__MWH')*1000) + self.get_conv_val('ALL_HEAT_PUMPS__AMOUNT_OF_HEAT__NHZ_DHW_TOTAL__KWH')

    def get_electricity_vd_headitng_day_kwh(self):
        """Get the total electricity kWh for vd heating."""
        if self._update_on_read:
            self.update()
        return (self.get_conv_val('ALL_HEAT_PUMPS__POWER_CONSUMPTION__VD_HEATING_DAY__KWH'))

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
