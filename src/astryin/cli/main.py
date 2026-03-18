import typer
from rich import print

from astryin.bag.reader import read_data

from astryin.metrics.trajectory_metrics import (
    compute_length, 
    compute_velocity_profile, 
    compute_tracking_error, 
    trim_motion_window, 
    unpack_cmd_vel
)
from astryin.visualization.odom_plot import plot_odom
from astryin.visualization.velocity_plot import plot_velocity_profile
from astryin.visualization.plan_plot import plot_plan
from astryin.visualization.local_plan_plot import plot_local_plan
from astryin.visualization.trajectory_plot import plot_trajectory


app = typer.Typer(help="Astryin - A toolkit for analyzing and visualizing ROS2 navigation behavior. Track and visualize navigation behavior from recorded ROS2 bag files.")
plot_app = typer.Typer(help="Visualize data from a ROS2 bag file.")

app.add_typer(plot_app, name="plot")


def error(msg: str):
    print(f"[bold red]✖ {msg}[/bold red]")

def warn(msg: str):
    print(f"[bold yellow]⚠ {msg}[/bold yellow]")


def info(msg: str):
    print(f"[cyan]ℹ {msg}[/cyan]")

@app.command(help="Analyze a ROS2 bag file and extract key navigation metrics.")
def analyze(bag_path: str):
    try:
        odom, cmd_vel, plan, local_plan = read_data(bag_path)
    except Exception as e:
        error(f"Failed to read data from bag file: {str(e)}")
        raise typer.Exit()

    if not odom:
        error("No /odom data found in the bag file.")
        raise typer.Exit()

    motion_odom = trim_motion_window(odom)

    odom_samples = len(odom)
    motion_odom_samples = len(motion_odom)
    plan_samples = len(plan)

    bag_duration = odom[-1].timestamp - odom[0].timestamp

    motion_start = motion_odom[0].timestamp - odom[0].timestamp
    motion_end = motion_odom[-1].timestamp - odom[0].timestamp
    motion_duration = motion_odom[-1].timestamp - motion_odom[0].timestamp

    length = compute_length(motion_odom)

    times, velocities = compute_velocity_profile(motion_odom)

    mean_vel = None
    max_vel = None

    if velocities:
        max_vel = max(velocities)
        mean_vel = sum(velocities) / len(velocities)

    mean_error = None
    max_error = None

    if plan:
        mean_error, max_error = compute_tracking_error(motion_odom, plan)

    print()
    print("[bold]Bag Summary[/bold]")
    print("-------------------------------")

    print(f"Bag duration:          {bag_duration:.2f} s")
    print(f"Odom samples:          {odom_samples}")
    print(f"Plan samples:          {plan_samples}")


    print()
    print("[bold]Motion Window[/bold]")
    print("-------------------------------")

    print(f"Motion start:          {motion_start:.2f} s")
    print(f"Motion end:            {motion_end:.2f} s")
    print(f"Motion duration:       {motion_duration:.2f} s")
    print(f"Motion odom samples:   {motion_odom_samples}")


    print()
    print("[bold]Trajectory Metrics[/bold]")
    print("-------------------------------")

    print(f"Path length:           {length:.2f} m")

    if mean_vel is not None:
        print(f"Mean velocity:         {mean_vel:.2f} m/s")
    if max_vel is not None:
        print(f"Max velocity:          {max_vel:.2f} m/s")
    if mean_error is not None:
        print(f"Mean tracking error:   {mean_error:.3f} m")
    if max_error is not None:
        print(f"Max tracking error:    {max_error:.3f} m")


@plot_app.command("odom", help="Plot odometry data.")
def plot_odom_cmd(bag_path: str):
    try:
        odom, _, _, _ = read_data(bag_path)
    except Exception as e:
        error(f"Failed to read data from bag file: {str(e)}")
        raise typer.Exit()
    
    if not odom:
        error("No /odom data found in the bag file.")
        raise typer.Exit()

    plot_odom(odom)


@plot_app.command("velocity", help="Plot odometry velocity and commanded velocity.")
def plot_velocity_cmd(bag_path: str):
    try:
        odom, cmd_vel, _, _ = read_data(bag_path)
    except Exception as e:
        error(f"Failed to read data from bag file: {str(e)}")
        raise typer.Exit()

    if not odom:
        error("No /odom data found in the bag file.")
        raise typer.Exit()
    
    if not cmd_vel:
        error("No /cmd_vel data found in the bag file.")
        raise typer.Exit()
    
    motion_odom = trim_motion_window(odom)

    motion_start = motion_odom[0].timestamp - odom[0].timestamp
    motion_end = motion_odom[-1].timestamp - odom[0].timestamp
    
    cmd_vel_times, cmd_vel_velocities = unpack_cmd_vel(cmd_vel)

    odom_times, odom_velocities = compute_velocity_profile(odom)

    plot_velocity_profile(
        odom_times, 
        motion_start, 
        odom_velocities, 
        cmd_vel_times, 
        cmd_vel_velocities
    )


@plot_app.command("plan", help="Plot global plan data.")
def plot_plan_cmd(bag_path: str):
    try: 
        _, _, plan, _ = read_data(bag_path)
    except Exception as e:
        error(f"Failed to read data from bag file: {str(e)}")
        raise typer.Exit()

    if not plan:
        error("No /plan data found in the bag file.")
        raise typer.Exit()

    plot_plan(plan)


@plot_app.command("local_plan", help="Plot local plan data.")
def plot_local_plan_cmd(bag_path: str):
    try:
        _, _, _, local_plan = read_data(bag_path)
    except Exception as e:
        error(f"Failed to read data from bag file: {str(e)}")
        raise typer.Exit()

    if not local_plan:
        error("No /local_plan data found in the bag file.")
        raise typer.Exit()

    plot_local_plan(local_plan)


@plot_app.command("trajectory", help="Plot trajectory with odometry, global plan, and local plan.")
def plot_trajectory_cmd(bag_path: str):
    try:
        odom, _, plan, local_plan = read_data(bag_path)
    except Exception as e:
        error(f"Failed to read data from bag file: {str(e)}")
        raise typer.Exit()

    if not odom:
        error("No /odom data found in the bag file.")
        raise typer.Exit()

    if not plan:
        error("No /plan data found in the bag file.")
        raise typer.Exit()

    if not local_plan:
        error("No /local_plan data found in the bag file.")
        raise typer.Exit()

    plot_trajectory(odom, plan, local_plan)


if __name__ == "__main__":
    app()