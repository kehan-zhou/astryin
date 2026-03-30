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
    if not odom:
        return [], []
    
    times = [p.timestamp for p in odom]
    velocities = [p.v for p in odom]

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

    start = 0
    end = len(odom)

    for i, p in enumerate(odom):
        if abs(p.v) > velocity_threshold:
            start = i
            break

    for i in reversed(range(len(odom))):
        if abs(odom[i].v) > velocity_threshold:
            end = i + 1
            break

    return odom[start:end]


def unpack_cmd_vel(cmd_vel):

    if not cmd_vel:
        return [], []

    times = [v.timestamp for v in cmd_vel]
    velocities = [v.linear_velocity for v in cmd_vel]

    return times, velocities