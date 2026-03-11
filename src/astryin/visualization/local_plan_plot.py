import matplotlib.pyplot as plt


def plot_local_plan(local_plan, output_file="outputs/local_plan.png"):
    if not local_plan:
        print("No local plan data to plot")
        return

    plt.figure(figsize=(6, 6))

    for lp in local_plan:

        xs = []
        ys = []

        for p in lp:
            xs.append(p.x)
            ys.append(p.y)

        plt.plot(xs, ys, linewidth=1, alpha=0.4)

    plt.title("Local Plan Data Visualization")

    plt.xlabel("X (m)")
    plt.ylabel("Y (m)")

    plt.axis("equal")

    plt.grid(True)

    plt.savefig(output_file, dpi=150)

    print(f"Local plan plot saved to {output_file}")