import tkinter as tk
import time
import matplotlib.pyplot as plt

class GeometryApp:
    def __init__(self, master):
        self.master = master
        master.title("Jarvice March")

        self.canvas = tk.Canvas(master, width=500, height=500, bg="white")
        self.canvas.pack()

        self.vertices = []
        self.lines = []

        self.canvas.bind("<Button-1>", self.add_vertex)
        self.canvas.bind("<Button-3>", self.add_line)

        self.result_label = tk.Label(master, text="")
        self.result_label.pack()

        self.convex_hull_button = tk.Button(master, text="Compute Convex Hull", command=self.compute_convex_hull)
        self.convex_hull_button.pack()



        self.hull = []
        self.step = 0

    def add_vertex(self, event):
        x, y = event.x, event.y
        self.vertices.append((x, y))
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="black")

    def add_line(self, event):
        x, y = event.x, event.y
        if self.vertices:
            self.lines.append((x, y))
            last_vertex = self.vertices[-1]
            self.canvas.create_line(last_vertex[0], last_vertex[1], x, y, fill="blue")

    def compute_convex_hull(self):
        if len(self.vertices) < 3:
            self.result_label.config(text="Not enough vertices to compute convex hull.")
            return

        # Visualization setup
        fig, ax = plt.subplots()
        ax.set_xlim(0, 500)
        ax.set_ylim(0, 500)
        plt.scatter([point[0] for point in self.vertices], [point[1] for point in self.vertices], color='black')

        start_time = time.time()

        # Convex hull computation using Jarvis March algorithm
        self.hull, self.step = self.convex_hull_jarvis_march(self.vertices, ax, step_by_step=True)

        end_time = time.time()
        elapsed_time_ms = (end_time - start_time)   # Convert to microseconds

        # Display the elapsed time
        self.result_label.config(text="Convex Hull Computed in {:.3f} seconds".format(elapsed_time_ms))

        # Show the plot
        plt.show()

    def convex_hull_jarvis_march(self, points, ax, step_by_step=False):
        n = len(points)
        if n < 3:
            return points, 0  # Convex hull requires at least 3 points

        # Find the point with the lowest y-coordinate (and leftmost if ties)
        start_point = min(points, key=lambda p: (p[1], p[0]))

        hull = [start_point]
        endpoint = None

        while endpoint != start_point:
            endpoint = points[0]

            for i in range(1, n):
                ax.plot([hull[-1][0], points[i][0]], [hull[-1][1], points[i][1]], linestyle='-', color='gray')
                plt.pause(1) if step_by_step else plt.pause(0.1)

                if endpoint == hull[-1] or self.orientation(hull[-1], endpoint, points[i]) == 2:
                    endpoint = points[i]

            hull.append(endpoint)

        # Visualization: Display edges with annotations
        for i in range(1, len(hull)):
            x1, y1 = hull[i - 1]
            x2, y2 = hull[i]
            ax.annotate(str(i), ((x1 + x2) / 2, (y1 + y2) / 2), color='blue')  # Annotate edge number
            ax.plot([x1, x2], [y1, y2], linestyle='-', color='blue')
            plt.pause(1) if step_by_step else plt.pause(0.1)

        return hull, len(hull)

    def orientation(self, p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0  # colinear
        return 1 if val > 0 else 2  # clock or counterclockwise

    def next_step(self):
        if self.step < len(self.hull) - 1:
            # Visualization: Display next step
            fig, ax = plt.subplots()
            ax.set_xlim(0, 500)
            ax.set_ylim(0, 500)
            plt.scatter([point[0] for point in self.vertices], [point[1] for point in self.vertices], color='black')
            ax.plot([point[0] for point in self.hull[: self.step + 2]], [point[1] for point in self.hull[: self.step + 2]], marker='o', linestyle='-', color='green')
            for i in range(1, self.step + 2):
                x1, y1 = self.hull[i - 1]
                x2, y2 = self.hull[i]
                ax.annotate(str(i), ((x1 + x2) / 2, (y1 + y2) / 2), color='blue')  # Annotate edge number
                ax.plot([x1, x2], [y1, y2], linestyle='-', color='blue')

            # Show the plot for the next step
            plt.show()
            self.step += 1

def main():
    root = tk.Tk()
    app = GeometryApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
