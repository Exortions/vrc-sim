from pose import Pose
from util import slew

from dataclasses import dataclass

import time

@dataclass
class Gains:
    kF: float = 0.0
    kA: float = 0.0
    kP: float = 0.0
    kI: float = 0.0
    kD: float = 0.0

class PID:
    def __init__(self, gains: Gains):
        self.gains = gains

        self.previous_target = 0.0
        self.large_error = 0.0
        self.small_error = 0.0

        self.large_timer = 0.0
        self.small_timer = 0.0
        self.start_time = 0.0

        self.error = 0.0
        self.previous_error = 0.0
        self.total_error = 0.0

        self.previous_output = 0.0

        self.max_time = 1000

    def set_gains(self, gains: Gains):
        self.gains = gains
    
    def get_gains(self) -> Gains:
        return self.gains

    def set_exit(self, large_error, small_error, large_time, small_time, timeout):
        self.large_error = large_error
        self.small_error = small_error

        self.large_timer = large_time
        self.small_timer = small_time
        self.max_time = timeout
    
    def update(self, error: float, target: float = 0.0) -> float:
        delta_error = error - self.previous_error

        output = (self.gains.kF * target) + (self.gains.kP * error) + (self.gains.kI * self.total_error) + (self.gains.kD * delta_error)

        if self.gains.kA != 0:
            output = slew(output, self.previous_output, self.gains.kA)

        self.previous_output = output
        self.previous_error = error

        self.total_error += error

        return output

    def settled(self) -> bool:
        if self.start_time == 0:
            self.start_time = time.time() * 1000
        else:
            if time.time() * 1000 - self.start_time > self.max_time:
                return True
            if abs(self.previous_error) < self.large_error:
                if self.large_timer == 0:
                    self.large_timer = time.time() * 1000
                elif time.time() * 1000 - self.large_timer > self.large_time:
                    return True
        # TODO
