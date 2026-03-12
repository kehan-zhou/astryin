import matplotlib.pyplot as plt


def plot_trajectory(odom, plan, local_plan):
    available = sum([
        bool(odom),
        bool(plan),
        bool(local_plan)
    ])

    if available < 2:
        print("Not enough trajectory data to plot (need at least two of: odom, plan, local_plan)")
        return

    plt.figure(figsize=(6, 6))

    # Plan
    if plan:
        xs = [p.x for p in plan]
        ys = [p.y for p in plan]

        plt.plot(xs, ys, linewidth=3, label="Plan")

    # Odom
    if odom:
        xs = [p.x for p in odom]
        ys = [p.y for p in odom]

        plt.plot(xs, ys, linewidth=2, label="Odom")

    # Local plan
    if local_plan:
        first = True
        for lp in local_plan:
            xs = [p.x for p in lp]
            ys = [p.y for p in lp]

            if first:
                plt.plot(xs, ys, linewidth=0.5, alpha=0.3, color='green', label="Local Plan")
                first = False
            else:
                plt.plot(xs, ys, linewidth=0.5, alpha=0.3, color='green')

    plt.xlabel("X (m)")
    plt.ylabel("Y (m)")
    plt.title("Trajectory Visualization")

    plt.axis("equal")
    plt.grid(True)
    plt.legend()

    plt.show()