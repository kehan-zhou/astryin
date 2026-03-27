import os
import math
from typing import Tuple, Optional

from astryin.models.pose import Pose
from astryin.models.velocity import Velocity

from geometry_msgs.msg import Twist, TransformStamped
from nav_msgs.msg import Odometry, Path
from tf2_msgs.msg import TFMessage
from rclpy.serialization import deserialize_message
from rosbag2_py import SequentialReader, StorageOptions, ConverterOptions

def quaternion_to_yaw(q):
    siny_cosp = 2 * (q.w * q.z + q.x * q.y)
    cosy_cosp = 1 - 2 * (q.y * q.y + q.z * q.z)
    return math.atan2(siny_cosp, cosy_cosp)

def apply_transform(x, y, dx, dy, yaw):
    new_x = x * math.cos(yaw) - y * math.sin(yaw) + dx
    new_y = x * math.sin(yaw) + y * math.cos(yaw) + dy
    return new_x, new_y

def read_data(bag_path: str):
    if not os.path.exists(bag_path):
        raise FileNotFoundError(f"Bag file not found: {bag_path}")

    storage_options = StorageOptions(uri=bag_path, storage_id="sqlite3")
    converter_options = ConverterOptions("", "")
    reader = SequentialReader()
    
    reader.open(storage_options, converter_options)

    current_tf = {"dx": 0.0, "dy": 0.0, "yaw": 0.0}

    odom_raw, cmd_vel, plan, local_plan = [], [], [], []
    
    plan_found = False

    while reader.has_next():
        topic, data, timestamp = reader.read_next()

        if topic in ["/tf", "/tf_static"]:
            msg = deserialize_message(data, TFMessage)
            for transform in msg.transforms:
                if transform.header.frame_id == "map" and transform.child_frame_id == "odom":
                    t = transform.transform.translation
                    r = transform.transform.rotation
                    current_tf = {
                        "dx": t.x, 
                        "dy": t.y, 
                        "yaw": quaternion_to_yaw(r)
                    }
                    
        if topic == "/odom":
            msg = deserialize_message(data, Odometry)
            map_x, map_y = apply_transform(
                msg.pose.pose.position.x, 
                msg.pose.pose.position.y,
                current_tf["dx"], 
                current_tf["dy"], 
                current_tf["yaw"]
            )
            
            t = timestamp / 1e9
            odom_raw.append(Pose(t, map_x, map_y))
        
        if topic == "/cmd_vel":
            msg = deserialize_message(data, Twist)
            t = timestamp / 1e9
            cmd_vel.append(Velocity(t, msg.linear.x))
        
        if topic == "/plan" and not plan_found:
            msg = deserialize_message(data, Path)
            for pose in msg.poses:
                plan.append(Pose(timestamp/1e9, pose.pose.position.x, pose.pose.position.y))
            plan_found = True

        if topic == "/local_plan":
            msg = deserialize_message(data, Path)
            lp = [Pose(timestamp/1e9, p.pose.position.x, p.pose.position.y) for p in msg.poses]
            local_plan.append(lp)

    return odom_raw, cmd_vel, plan, local_plan