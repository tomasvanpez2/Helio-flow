from .config import LIGHT_SENSOR_LEFT_PORT, LIGHT_SENSOR_RIGHT_PORT, USE_DUAL_LIGHT_SENSORS, SIMULATION

def build_light_reader():
    if SIMULATION:
        from .sim import SimDualLightSensors, SimSingleLightSensor
        if USE_DUAL_LIGHT_SENSORS:
            return SimDualLightSensors()
        return SimSingleLightSensor()
    from ev3dev2.sensor.lego import LightSensor
    from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
    def input_const(port):
        if port == "1":
            return INPUT_1
        if port == "2":
            return INPUT_2
        if port == "3":
            return INPUT_3
        return INPUT_4
    if USE_DUAL_LIGHT_SENSORS:
        left = LightSensor(input_const(LIGHT_SENSOR_LEFT_PORT))
        right = LightSensor(input_const(LIGHT_SENSOR_RIGHT_PORT))
        return _DualLightReader(left, right)
    sensor = LightSensor(input_const(LIGHT_SENSOR_LEFT_PORT))
    return _SingleLightReader(sensor)

class _DualLightReader:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def read(self):
        return float(self.left.ambient_light_intensity), float(self.right.ambient_light_intensity)

class _SingleLightReader:
    def __init__(self, sensor):
        self.sensor = sensor
    def read(self):
        return float(self.sensor.ambient_light_intensity)
