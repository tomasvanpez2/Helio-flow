import math
import time

class SimHorizontalTrackerMotor:
    def __init__(self, limit, step):
        self.limit = limit
        self.step = step
        self.position = 0
    def reset(self):
        self.position = 0
    def within_limits(self, target):
        return -self.limit <= target <= self.limit
    def rotate_step(self, direction):
        delta = self.step if direction > 0 else -self.step
        target = self.position + delta
        if not self.within_limits(target):
            return False
        self.position = target
        return True
    def stop(self):
        pass

class SimDualLightSensors:
    def read(self):
        t = time.time()
        offset = 20.0 * math.sin(t * 0.3)
        base = 50.0
        left = base - offset
        right = base + offset
        return left, right

class SimSingleLightSensor:
    def read(self):
        t = time.time()
        return 50.0 + 10.0 * math.sin(t * 0.2)

class SimPanelMeter:
    def __init__(self, voltage_v, base_current_a, variation_a):
        self.voltage_v = voltage_v
        self.base_current_a = base_current_a
        self.variation_a = variation_a
    def read(self):
        t = time.time()
        current = max(0.0, self.base_current_a + self.variation_a * (0.5 + 0.5 * math.sin(t * 0.15)))
        power = self.voltage_v * current
        return self.voltage_v, current, power

class SimWaterSystem:
    def __init__(self):
        self.level_l = 5.0
        self.temperature_c = 35.0
        self.pump_on = False
    def read_level(self):
        return self.level_l
    def read_temperature(self):
        return self.temperature_c
    def set_pump(self, on):
        self.pump_on = bool(on)
    def tick(self, dt_s):
        t = time.time()
        self.temperature_c = 35.0 + 10.0 * (0.5 + 0.5 * math.sin(t * 0.1))
        if self.pump_on:
            self.level_l = max(0.0, self.level_l - 0.02 * dt_s)
        else:
            self.level_l = min(10.0, self.level_l + 0.005 * dt_s)
