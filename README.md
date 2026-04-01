# Astryin - ROS2 Navigation Behavior Analysis Toolkit

**Astryin** is a post-mortem analysis tool for ROS 2 navigation. It enables developers to visualize and quantify robot behavior from recorded bag files.

## Why Astryin?

Tuning Nav2 is often an exercise in trial and error. When a robot oscillates or hesitates, developers typically rely on subjective observations.

Astryin solves this by providing structured, data-driven insights into velocity profiles, tracking errors, and trajectory consistency.

## Installation

Clone the repository and install in editable mode:

```bash
git clone https://github.com/kehan-zhou/astryin.git
cd astryin
pip install -e .
```

**Note:** Requires a ROS 2 environment installed.

## Core Features & Usage

### 1. Quantitative Metrics

Extract hard numbers to compare performance across different parameter sets.

```bash
astryin analyze examples/turtlebot3_navigation
```

Output:

```bash
[INFO] [1774939863.695093815] [rosbag2_storage]: Opened database 'examples/turtlebot3_navigation/turtlebot3_navigation_0.db3' for READ_ONLY.

Bag Summary
-------------------------------
Bag duration:          51.39 s
Odom samples:          1511
Plan samples:          138

Motion Window
-------------------------------
Motion start:          23.21 s
Motion end:            41.97 s
Motion duration:       18.75 s
Motion odom samples:   552

Trajectory Metrics
-------------------------------
Path length:           3.56 m
Mean velocity:         0.18 m/s
Max velocity:          0.23 m/s
Mean tracking error:   0.055 m
Max tracking error:    0.242 m
```

Key Metrics Provided:

- Trajectory Tracking Error: Mean and Max Euclidean distance from the global plan.
- Motion Windowing: Automatically trims stationary data at the start/end for accurate velocity stats.
- Path Efficiency: Total distance traveled vs. planned path length.

### 2. Velocity Profile Analysis

Compare commanded velocity (`/cmd_vel`) vs. actual execution(`/odom`)

```bash
astryin plot velocity examples/turtlebot3_navigation
```

Output:

```bash
[INFO] [1773133209.823054913] [rosbag2_storage]: Opened database 'examples/turtlebot3_navigation/turtlebot3_navigation_0.db3' for READ_ONLY.
```

![velocity_profile_example.png](docs/velocity_profile_example.png "")

### 3. Comprehensive Trajectory Visualization

One view to rule them all: Global Plan, Local Plan clusters, and Odom trajectory.

```bash
astryin plot trajectory examples/turtlebot3_navigation
```

Output:

```bash
[INFO] [1773190749.119507577] [rosbag2_storage]: Opened database 'examples/turtlebot3_navigation/turtlebot3_navigation_0.db3' for READ_ONLY.
```

![trajectory_example.png](docs/trajectory_example.png "")

- **Dynamic TF Compensation:** Automatically extracts `map -> odom` transforms to align disparate coordinate frames.
- **Local Plan Density:** Visualizes how the local controller "thinks" over time.
