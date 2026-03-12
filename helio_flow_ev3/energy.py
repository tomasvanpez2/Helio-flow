from .config import (
    SIMULATION,
    PANEL_VOLTAGE_V,
    PANEL_BASE_CURRENT_A,
    PANEL_VARIATION_A,
    BATTERY_CAPACITY_WH,
    INITIAL_BATTERY_SOC,
    RESERVE_RATIO,
    OPERATION_WATTS,
    PUMP_WATTS,
    VITAL_WATTS,
    SECONDARY_WATTS,
    SAMPLE_INTERVAL_SECONDS,
)
import time

def build_panel_meter():
    if SIMULATION:
        from .sim import SimPanelMeter
        return SimPanelMeter(PANEL_VOLTAGE_V, PANEL_BASE_CURRENT_A, PANEL_VARIATION_A)
    return _FixedPanelMeter(PANEL_VOLTAGE_V, PANEL_BASE_CURRENT_A)

class _FixedPanelMeter:
    def __init__(self, voltage_v, current_a):
        self.voltage_v = voltage_v
        self.current_a = current_a
    def read(self):
        p = self.voltage_v * self.current_a
        return self.voltage_v, self.current_a, p

class BatteryBank:
    def __init__(self, capacity_wh, initial_soc):
        self.capacity_wh = capacity_wh
        self.energy_wh = capacity_wh * initial_soc
    @property
    def soc(self):
        return max(0.0, min(1.0, self.energy_wh / self.capacity_wh)) if self.capacity_wh > 0 else 0.0
    def tick(self, generation_w, loads_w, dt_s):
        delta_wh = generation_w * dt_s / 3600.0 - loads_w * dt_s / 3600.0
        self.energy_wh = max(0.0, min(self.capacity_wh, self.energy_wh + delta_wh))

def build_battery_bank():
    return BatteryBank(BATTERY_CAPACITY_WH, INITIAL_BATTERY_SOC)

class EnergyManager:
    def __init__(self, battery):
        self.battery = battery
        self.vital_enabled = False
        self.secondary_enabled = False
        self.last_update = time.time()
    def update(self, generation_w, op_w, pump_w, dt_s=SAMPLE_INTERVAL_SECONDS):
        reserve_wh = self.battery.capacity_wh * RESERVE_RATIO
        op_wh = op_w * dt_s / 3600.0 + pump_w * dt_s / 3600.0
        available_wh = max(0.0, self.battery.energy_wh - reserve_wh)
        vital_wh = VITAL_WATTS * dt_s / 3600.0
        secondary_wh = SECONDARY_WATTS * dt_s / 3600.0
        vital_ok = available_wh >= op_wh + vital_wh
        secondary_ok = available_wh >= op_wh + vital_wh + secondary_wh
        self.vital_enabled = vital_ok
        self.secondary_enabled = secondary_ok
        loads_w = op_w + pump_w + (VITAL_WATTS if self.vital_enabled else 0.0) + (SECONDARY_WATTS if self.secondary_enabled else 0.0)
        self.battery.tick(generation_w, loads_w, dt_s)
        return {
            "vital": self.vital_enabled,
            "secondary": self.secondary_enabled,
            "generation_w": generation_w,
            "loads_w": loads_w,
            "soc": self.battery.soc,
        }
