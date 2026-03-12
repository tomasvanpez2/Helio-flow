from .config import SIMULATION, WATER_LEVEL_MIN_L, TEMP_THRESHOLD_C

def build_water_system():
    if SIMULATION:
        from .sim import SimWaterSystem
        return SimWaterSystem()
    return _PlaceholderWaterSystem()

class _PlaceholderWaterSystem:
    def __init__(self):
        self.level_l = 0.0
        self.temperature_c = 25.0
        self.pump_on = False
    def read_level(self):
        return self.level_l
    def read_temperature(self):
        return self.temperature_c
    def set_pump(self, on):
        self.pump_on = bool(on)
    def tick(self, dt_s):
        pass

class WaterController:
    def __init__(self, water_system):
        self.water = water_system
    def decide_pump(self):
        level = self.water.read_level()
        temp = self.water.read_temperature()
        on = level >= WATER_LEVEL_MIN_L and temp >= TEMP_THRESHOLD_C
        self.water.set_pump(on)
        return on, level, temp
