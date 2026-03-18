import os

from astryin.models.pose import Pose
from astryin.models.velocity import Velocity

from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry, Path
from rclpy.serialization import deserialize_message
from rosbag2_py import SequentialReader, StorageOptions, ConverterOptions


def read_data(bag_path: str):
    if not os.path.exists(bag_path):
        raise FileNotFoundError(f"Bag file not found: {bag_path}")

    storage_options = StorageOptions(uri=bag_path, storage_id="sqlite3")
    converter_options = ConverterOptions("", "")
    reader = SequentialReader()
    
    try:
        reader.open(storage_options, converter_options)
    except Exception as e:
        raise RuntimeError(f"Failed to open the bag file: {str(e)}")

    odom, cmd_vel, plan, local_plan = [], [], [], []

    plan_found = False

    while reader.has_next():
        topic, data, timestamp = reader.read_next()

        if topic == "/odom":
            msg = deserialize_message(data, Odometry)
            t = timestamp / 1e9
            x = msg.pose.pose.position.x
            y = msg.pose.pose.position.y
            odom.append(Pose(t, x, y))
        
        if topic == "/cmd_vel":
            msg = deserialize_message(data, Twist)
            t = timestamp / 1e9
            lv = msg.linear.x
            cmd_vel.append(Velocity(t, lv))
        
        if topic == "/plan" and not plan_found:
            msg = deserialize_message(data, Path)
            for pose in msg.poses:
                t = timestamp / 1e9
                x = pose.pose.position.x
                y = pose.pose.position.y
                plan.append(Pose(t, x, y))
            plan_found = True
            continue

        if topic == "/local_plan":
            msg = deserialize_message(data, Path)
            lp = []
            for pose in msg.poses:
                t = timestamp / 1e9
                x = pose.pose.position.x
                y = pose.pose.position.y
                lp.append(Pose(t, x, y))
            local_plan.append(lp)

    return odom, cmd_vel, plan, local_plan


