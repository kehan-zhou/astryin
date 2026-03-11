import typer
from rich import print

from astryin.bag.reader import read_data

from astryin.metrics.trajectory_metrics import compute_length, compute_velocity_profile, compute_tracking_error, trim_motion_window, unpack_cmd_vel
from astryin.visualization.odom_plot import plot_odom
from astryin.visualization.velocity_plot import plot_velocity_profile
from astryin.visualization.plan_plot import plot_plan
from astryin.visualization.local_plan_plot import plot_local_plan
from astryin.visualization.trajectory_plot import plot_trajectory


app = typer.Typer(help="Astryin - Navigation behavior analysis toolkit")

plot_app = typer.Typer(help="Visualization tools")

app.add_typer(plot_app, name="plot")


@app.command()
def analyze(bag_path: str):
    odom, cmd_vel, plan, local_plan = read_data(bag_path)

    if not odom:
        print("[red]No /odom data found[/red]")
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


@plot_app.command("odom")
def plot_odom_cmd(bag_path: str):
    odom, _, _, _ = read_data(bag_path)

    if not odom:
        print("[red]No /odom data found[/red]")
        raise typer.Exit()

    plot_odom(odom)


@plot_app.command("velocity")
def plot_velocity_cmd(bag_path: str):
    odom, cmd_vel, _, _ = read_data(bag_path)

    if not odom:
        print("[red]No /odom data found[/red]")
        raise typer.Exit()
    
    motion_odom = trim_motion_window(odom)

    motion_start = motion_odom[0].timestamp - odom[0].timestamp
    motion_end = motion_odom[-1].timestamp - odom[0].timestamp

    if not cmd_vel:
        print("[red]No /cmd_vel data found[/red]")
        raise typer.Exit()
    
    cmd_vel_times, cmd_vel_velocities = unpack_cmd_vel(cmd_vel)

    odom_times, odom_velocities = compute_velocity_profile(odom)

    plot_velocity_profile(odom_times, motion_start, odom_velocities, cmd_vel_times, cmd_vel_velocities)


@plot_app.command("plan")
def plot_plan_cmd(bag_path: str):
    _, _, plan, _ = read_data(bag_path)

    if not plan:
        print("[yellow]No /plan found in bag[/yellow]")
        raise typer.Exit()

    plot_plan(plan)


@plot_app.command("local_plan")
def plot_local_plan_cmd(bag_path: str):
    _, _, _, local_plan = read_data(bag_path)

    if not local_plan:
        print("[yellow]No /local_plan found in bag[/yellow]")
        raise typer.Exit()

    plot_local_plan(local_plan)


@plot_app.command("trajectory")
def plot_trajectory_cmd(bag_path: str):
    odom, _, plan, local_plan = read_data(bag_path)

    if odom:
        print("odom (/odom): loaded")
    else:
        print("odom (/odom): missing")

    if plan:
        print("plan (/plan): loaded")
    else:
        print("plan (/plan): missing")

    if local_plan:
        print("local_plan (/local_plan): loaded")
    else:
        print("local_plan (/local_plan): missing")

    plot_trajectory(odom, plan, local_plan)


if __name__ == "__main__":
    app()