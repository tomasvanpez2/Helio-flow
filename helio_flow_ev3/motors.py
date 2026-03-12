from .config import MOTOR_PORT, ROTATION_LIMIT_DEGREES, STEP_DEGREES, SIMULATION

def build_motor():
    if SIMULATION:
        from .sim import SimHorizontalTrackerMotor
        return SimHorizontalTrackerMotor(ROTATION_LIMIT_DEGREES, STEP_DEGREES)
    from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
    from ev3dev2.motor import SpeedPercent
    def output_const(port):
        if port == "A":
            return OUTPUT_A
        if port == "B":
            return OUTPUT_B
        if port == "C":
            return OUTPUT_C
        return OUTPUT_D
    return _HardwareHorizontalTrackerMotor(LargeMotor(output_const(MOTOR_PORT)), ROTATION_LIMIT_DEGREES, STEP_DEGREES, SpeedPercent)

class _HardwareHorizontalTrackerMotor:
    def __init__(self, motor, limit, step, speed_class):
        self.motor = motor
        self.limit = limit
        self.step = step
        self.speed_class = speed_class
        self.position = 0
    def reset(self):
        self.motor.stop()
        self.motor.reset()
        self.position = 0
    def within_limits(self, target):
        return -self.limit <= target <= self.limit
    def rotate_step(self, direction):
        delta = self.step if direction > 0 else -self.step
        target = self.position + delta
        if not self.within_limits(target):
            return False
        self.motor.on_for_degrees(self.speed_class(20), delta, brake=True, block=True)
        self.position = target
        return True
    def stop(self):
        self.motor.stop()
