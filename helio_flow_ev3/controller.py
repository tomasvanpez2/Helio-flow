import time
from .motors import build_motor
from .sensors import build_light_reader
from .energy import build_panel_meter, build_battery_bank, EnergyManager
from .water import build_water_system, WaterController
from .config import LUMINANCE_DIFF_THRESHOLD, SAMPLE_INTERVAL_SECONDS, OPERATION_WATTS, PUMP_WATTS

class HelioFlowController:
    def __init__(self):
        self.motor = build_motor()
        self.light = build_light_reader()
        self.panel = build_panel_meter()
        self.battery = build_battery_bank()
        self.energy = EnergyManager(self.battery)
        self.water = WaterController(build_water_system())

    def setup(self):
        self.motor.reset()

    def compute_direction(self):
        reading = self.light.read()
        if isinstance(reading, tuple):
            left, right = reading
            diff = right - left
            if abs(diff) < LUMINANCE_DIFF_THRESHOLD:
                return 0
            return 1 if diff > 0 else -1
        return 0

    def run(self):
        self.setup()
        try:
            while True:
                d = self.compute_direction()
                if d != 0:
                    self.motor.rotate_step(d)
                r = self.light.read()
                if isinstance(r, tuple):
                    left, right = r
                    print(f"pos={self.motor.position} left={left:.2f} right={right:.2f}", end=" ")
                else:
                    print(f"pos={self.motor.position} light={r:.2f}", end=" ")
                v, i, p = self.panel.read()
                pump_on, level, temp = self.water.decide_pump()
                self.water.water.tick(SAMPLE_INTERVAL_SECONDS)
                pump_w = PUMP_WATTS if pump_on else 0.0
                status = self.energy.update(p, OPERATION_WATTS, pump_w, SAMPLE_INTERVAL_SECONDS)
                print(f"V={v:.2f}V I={i:.2f}A P={p:.2f}W pump={pump_on} lvl={level:.2f}L temp={temp:.1f}C vital={status['vital']} sec={status['secondary']} soc={status['soc']*100:.1f}% loads={status['loads_w']:.2f}W")
                time.sleep(SAMPLE_INTERVAL_SECONDS)
        except KeyboardInterrupt:
            self.motor.stop()
