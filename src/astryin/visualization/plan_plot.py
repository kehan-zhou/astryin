import matplotlib.pyplot as plt


def plot_plan(plan):
    if not plan:
        print("No plan data to plot")
        return

    xs = []
    ys = []

    for p in plan:
        xs.append(p.x)
        ys.append(p.y)

    plt.figure(figsize=(6, 6))

    plt.plot(xs, ys, linewidth=3)

    plt.scatter(xs[0], ys[0], color="green", s=100, label="Start")
    plt.scatter(xs[-1], ys[-1], color="red", s=100, label="Goal")

    plt.title("Plan Data Visualization")

    plt.xlabel("X (m)")
    plt.ylabel("Y (m)")

    plt.axis("equal")

    plt.legend()

    plt.grid(True)

    plt.show()