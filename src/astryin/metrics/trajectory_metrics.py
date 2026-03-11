import math


def compute_length(odom):
    total = 0.0

    for i in range(len(odom) - 1):
        p1 = odom[i]
        p2 = odom[i + 1]

        dx = p2.x - p1.x
        dy = p2.y - p1.y

        dist = math.sqrt(dx * dx + dy * dy)

        total += dist
    
    return total


def compute_velocity_profile(odom):
    velocities = []
    times = []

    for i in range(len(odom) - 1):

        p1 = odom[i]
        p2 = odom[i + 1]

        dt = p2.timestamp - p1.timestamp

        if dt <= 0:
            continue

        dx = p2.x - p1.x
        dy = p2.y - p1.y

        distance = math.sqrt(dx * dx + dy * dy)

        velocity = distance / dt

        velocities.append(velocity)

        times.append(p1.timestamp - odom[0].timestamp)

    return times, velocities


def compute_tracking_error(odom, plan):
    errors = []

    for robot_pose in odom:
        min_dist = float("inf")

        for plan_pose in plan:
            dx = robot_pose.x - plan_pose.x
            dy = robot_pose.y - plan_pose.y

            dist = math.sqrt(dx * dx + dy * dy)

            if dist < min_dist:
                min_dist = dist
        
        errors.append(min_dist)
    
    mean_error = sum(errors) / len(errors)
    max_error = max(errors)

    return mean_error, max_error


def trim_motion_window(odom, velocity_threshold=0.02):

    start = None
    end = None

    for i in range(len(odom) - 1):

        p1 = odom[i]
        p2 = odom[i + 1]

        dt = p2.timestamp - p1.timestamp
        if dt <= 0:
            continue

        dx = p2.x - p1.x
        dy = p2.y - p1.y

        dist = math.sqrt(dx * dx + dy * dy)
        vel = dist / dt

        if vel > velocity_threshold:
            start = i
            break

    for i in reversed(range(len(odom) - 1)):

        p1 = odom[i]
        p2 = odom[i + 1]

        dt = p2.timestamp - p1.timestamp
        if dt <= 0:
            continue

        dx = p2.x - p1.x
        dy = p2.y - p1.y

        dist = math.sqrt(dx * dx + dy * dy)
        vel = dist / dt

        if vel > velocity_threshold:
            end = i + 1
            break

    if start is None or end is None:
        return odom

    return odom[start:end]

def unpack_cmd_vel(cmd_vel):

    if not cmd_vel:
        return [], []

    t0 = cmd_vel[0].timestamp

    times = []
    velocities = []

    for v in cmd_vel:
        times.append(v.timestamp - t0)
        velocities.append(v.linear_velocity)

    return times, velocities