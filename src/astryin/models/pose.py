from dataclasses import dataclass


@dataclass
class Pose:
    timestamp: float # timestamp (seconds)
    x: float # x position (meters)
    y: float # y position (meters)
    v: float # linear velocity (m/s)