import matplotlib.pyplot as plt


def plot_velocity_profile(odom_times, motion_start, odom_velocities, cmd_vel_times, cmd_vel_velocities, output_file="outputs/velocity_profile.png"):
    if not odom_times or not odom_velocities or not cmd_vel_times or not cmd_vel_velocities:
        print("No velocity data to plot")
        return
    
    plt.figure(figsize=(8, 4))

    plt.plot(odom_times, odom_velocities, alpha=0.5, label="Actual Velocity", color='red')

    adjusted_cmd_vel_times = [t + motion_start for t in cmd_vel_times]

    plt.plot(adjusted_cmd_vel_times, cmd_vel_velocities, alpha=0.6, label="Commanded Velocity", color='green')

    plt.title("Velocity Profile")

    plt.xlabel("Time (s)")
    plt.ylabel("Velocity (m/s)")

    plt.legend()

    plt.grid(True)

    plt.savefig(output_file, dpi=150)
    
    print(f"Velocity profile plot saved to {output_file}")