from dataclasses import dataclass


@dataclass
class Velocity:
    timestamp: float # timestamp (seconds)
    linear_velocity: float # linear velocity (meters/second)