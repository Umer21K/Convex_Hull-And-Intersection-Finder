import tkinter as tk
from math import atan2
import time


class GeometryApp:
    def __init__(self, master):
        self.master = master
        master.title("Algo Project AUA")

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

        self.are_lines_intersecting_button = tk.Button(master, text=" Check intersection", command=self.are_lines_intersecting)
        self.are_lines_intersecting_button.pack()



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

            # Check for intersection when a line is added
            # self.are_lines_intersecting()

    def are_lines_intersecting(self):
        self.Determinant_button = tk.Button(self.master, text="Determinant method", command=self.Determinant)
        self.Determinant_button.pack()

        self.CCW_button = tk.Button(self.master, text="Counter clockwise method", command=self.CCW)
        self.CCW_button.pack()

        self.bounding_box_button = tk.Button(self.master, text="Bounding box", command=self.bounding_box)
        self.bounding_box_button.pack()

    def Determinant(self):
        if len(self.vertices) < 4:
            self.result_label.config(text="Not enough vertices to form two lines.")
            return

        # Extract coordinates of the last two vertices to form two lines
        line1 = [self.vertices[-4], self.vertices[-3]]
        line2 = [self.vertices[-2], self.vertices[-1]]

        x1, y1 = line1[0]
        x2, y2 = line1[1]
        x3, y3 = line2[0]
        x4, y4 = line2[1]

        # Check if the lines are parallel
        det = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if det == 0:
            result = "Lines are parallel and do not intersect"
        else:
            # Calculate the intersection point
            intersect_x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / det
            intersect_y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / det

            # Check if the intersection point is within the line segments
            if (
                    min(x1, x2) <= intersect_x <= max(x1, x2)
                    and min(y1, y2) <= intersect_y <= max(y1, y2)
                    and min(x3, x4) <= intersect_x <= max(x3, x4)
                    and min(y3, y4) <= intersect_y <= max(y3, y4)
            ):
                result = "Lines intersect at ({:.2f}, {:.2f})".format(intersect_x, intersect_y)
            else:
                result = "Lines do not intersect"

        # Print the result on the GUI screen
        self.result_label.config(text=result)

    def CCW(self):
        if len(self.vertices) < 4:
            return None

            # Extract coordinates of the last two vertices to form two lines
        line1 = [self.vertices[-4], self.vertices[-3]]
        line2 = [self.vertices[-2], self.vertices[-1]]

        # Check for intersection logic here...
        if self.is_ccw(line1[0], line1[1], line2[1]) != self.is_ccw(line1[0], line1[1], line2[0]) \
                and self.is_ccw(line2[0], line2[1], line1[1]) != self.is_ccw(line2[0], line2[1], line1[0]):
            # Calculate the intersection point
            x1, y1 = line1[0]
            x2, y2 = line1[1]
            x3, y3 = line2[0]
            x4, y4 = line2[1]

            det = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            intersect_x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / det
            intersect_y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / det

            result = "Lines intersect at ({:.2f}, {:.2f})".format(intersect_x, intersect_y)

            self.result_label.config(text=result)

        return None

    @staticmethod
    def is_ccw(p1, p2, p3):
        """
        Determine if the orientation of three points is counter-clockwise.
        """
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3
        return (y2 - y1) * (x3 - x2) > (y3 - y2) * (x2 - x1)

    def bounding_box(self):
        if len(self.vertices) < 4:
            return None

            # Extract coordinates of the last two vertices to form two lines
        line1 = [self.vertices[-4], self.vertices[-3]]
        line2 = [self.vertices[-2], self.vertices[-1]]

        # Check for bounding box intersection logic here
        if self.bounding_box_intersect(line1, line2):
            # Calculate the intersection point
            x1, y1 = line1[0]
            x2, y2 = line1[1]
            x3, y3 = line2[0]
            x4, y4 = line2[1]

            det = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            intersect_x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / det
            intersect_y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / det

            result = "Lines intersect at ({:.2f}, {:.2f})".format(intersect_x, intersect_y)

            self.result_label.config(text=result)

        return None

    @staticmethod
    def bounding_box_intersect(line1, line2):
        """
        Check if the bounding boxes of two line segments overlap.
        """
        x1, y1 = line1[0]
        x2, y2 = line1[1]
        x3, y3 = line2[0]
        x4, y4 = line2[1]

        return (
                max(x1, x2) >= min(x3, x4) and
                max(x3, x4) >= min(x1, x2) and
                max(y1, y2) >= min(y3, y4) and
                max(y3, y4) >= min(y1, y2)
        )

    def compute_convex_hull(self):
        if len(self.vertices) < 3:
            self.result_label.config(text="Not enough vertices to compute convex hull.")
            return


        hull_vertices = tk.Button(self.master, text="Graham Scan", command=lambda: self.display_convex_hull(self.convex_hull_graham_scan(self.vertices)))
        hull_vertices.pack()


        hull_vertices = tk.Button(self.master, text="Quick Elimination", command=lambda: self.display_convex_hull(self.quick_hull(self.vertices)))
        hull_vertices.pack()


        hull_vertices = tk.Button(self.master, text="Jarvis March", command=lambda: self.display_convex_hull(self.convex_hull_gift_wrapping(self.vertices)))
        hull_vertices.pack()


        hull_vertices = tk.Button(self.master, text="Andrews Monotone Chain", command=lambda: self.display_convex_hull(self.andrews_monotone_chain(self.vertices)))
        hull_vertices.pack()

        hull_vertices = tk.Button(self.master, text="Brute Force", command=lambda: self.display_convex_hull(self.brute_force_convex_hull(self.vertices)))
        hull_vertices.pack()



    def convex_hull_graham_scan(self, points):
        start_time = 0.0000000
        end_time = 0.0000000
        ms = 0.0000000
        start_time = time.time()
        n = len(points)
        if n < 3:
            return points  # Convex hull requires at least 3 points

        # Find the point with the lowest y-coordinate (and leftmost if ties)
        pivot = min(points, key=lambda p: (p[1], p[0]))

        # Sort the points based on polar angle from the pivot
        sorted_points = sorted(points, key=lambda p: (atan2(p[1] - pivot[1], p[0] - pivot[0]), p))

        # Initialize the convex hull with the first three sorted points
        hull = [sorted_points[0], sorted_points[1], sorted_points[2]]

        # Iterate over the remaining sorted points
        for i in range(3, n):
            while len(hull) > 1 and self.orientation(hull[-2], hull[-1], sorted_points[i]) != 2:
                hull.pop()
            hull.append(sorted_points[i])

        end_time = time.time()
        ms = (end_time - start_time)

        self.result_label.config(text="Convex Hull Computed in {:.7f} seconds".format(ms))

        return hull

    def quick_hull(self, points):
        start_time = 0.0000000
        end_time = 0.0000000
        ms = 0.0000000
        start_time = time.time()
        if len(points) < 3:
            return points

        # Find the leftmost and rightmost points
        leftmost = min(points, key=lambda p: p[0])
        rightmost = max(points, key=lambda p: p[0])

        # Divide the points into two sets based on their position relative to the line formed by the leftmost and rightmost points
        points_left = [point for point in points if self.orientation(leftmost, rightmost, point) == 1]
        points_right = [point for point in points if self.orientation(leftmost, rightmost, point) == 2]

        # Recursively find the convex hull on each side
        hull_left = self.quick_hull_recursive(leftmost, rightmost, points_left)
        hull_right = self.quick_hull_recursive(rightmost, leftmost, points_right)

        end_time = time.time()
        ms = (end_time - start_time)

        self.result_label.config(text="Convex Hull Computed in {:.7f} seconds".format(ms))

        # Combine the results
        return hull_left + hull_right

    def quick_hull_recursive(self, p1, p2, points):
        if not points:
            return []

        # Find the point farthest from the line formed by p1 and p2
        farthest = max(points, key=lambda p: self.distance(p1, p2, p))

        # Divide the points into two sets based on their position relative to the line formed by p1, farthest
        points_left = [point for point in points if self.orientation(p1, farthest, point) == 1]
        points_right = [point for point in points if self.orientation(farthest, p2, point) == 1]

        # Recursively find the convex hull on each side
        hull_left = self.quick_hull_recursive(p1, farthest, points_left)
        hull_right = self.quick_hull_recursive(farthest, p2, points_right)

        # Combine the results
        return [p1] + hull_left + [farthest] + hull_right

    def convex_hull_gift_wrapping(self, points):
        start_time = 0.0000000
        end_time = 0.0000000
        ms = 0.0000000
        start_time = time.time()
        n = len(points)
        if n < 3:
            return points  # Convex hull requires at least 3 points

        hull = []
        point_on_hull = min(points)

        while True:
            hull.append(point_on_hull)
            endpoint = points[0]
            for j in range(1, n):
                if endpoint == point_on_hull or self.orientation(point_on_hull, endpoint, points[j]) == 1:
                    endpoint = points[j]
            point_on_hull = endpoint
            if endpoint == hull[0]:
                break

        end_time = time.time()
        ms = (end_time - start_time)

        self.result_label.config(text="Convex Hull Computed in {:.7f} seconds".format(ms))

        return hull

    def andrews_monotone_chain(self, points):
        start_time = 0.0000000
        end_time = 0.0000000
        ms = 0.0000000
        start_time = time.time()
        # Sort points lexicographically
        sorted_points = sorted(set(points))

        # Compute the lower hull
        lower_hull = []
        for p in sorted_points:
            while len(lower_hull) >= 2 and self.orientation(lower_hull[-2], lower_hull[-1], p) != 2:
                lower_hull.pop()
            lower_hull.append(p)

        # Compute the upper hull
        upper_hull = []
        for p in reversed(sorted_points):
            while len(upper_hull) >= 2 and self.orientation(upper_hull[-2], upper_hull[-1], p) != 2:
                upper_hull.pop()
            upper_hull.append(p)

        end_time = time.time()
        ms = (end_time - start_time)

        self.result_label.config(text="Convex Hull Computed in {:.7f} seconds".format(ms))

        # Combine the lower and upper hulls to form the convex hull
        return lower_hull[:-1] + upper_hull[:-1]

    def brute_force_convex_hull(self, points):
        start_time = 0.0000000
        end_time = 0.0000000
        elapsed_time_ms = 0.0000000
        start_time = time.time()
        n = len(points)

        if n < 3:
            return points  # Convex hull requires at least 3 vertices

        hull = []  # Convex hull vertices

        # Find the leftmost point as the starting point
        start_point = min(points, key=lambda p: p[0])

        current_point = start_point
        next_point = None

        while next_point != start_point:
            hull.append(current_point)

            # Find the next point in the convex hull
            next_point = points[0]
            for candidate_point in points:
                if candidate_point != current_point:
                    orientation = self.orientation(current_point, next_point, candidate_point)

                    if (next_point == current_point) or (orientation == 1) or \
                            (orientation == 0 and self.dis(current_point, candidate_point) > self.dis(
                                current_point, next_point)):
                        next_point = candidate_point

            current_point = next_point

        end_time = time.time()
        elapsed_time_ms = (end_time - start_time)

        self.result_label.config(text="Convex Hull Computed in {:.7f} seconds".format(elapsed_time_ms))

        return hull

    def orientation(self, p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0  # colinear
        return 1 if val > 0 else 2  # clock or counterclockwise

    def distance(self, p1, p2, p3):
        return abs((p2[1] - p1[1]) * p3[0] - (p2[0] - p1[0]) * p3[1] + p2[0] * p1[1] - p2[1] * p1[0])

    def dis(self, p1, p2):
        return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2

    def display_convex_hull(self, hull_vertices):
        # Clear previous convex hull display
        self.canvas.delete("convex_hull")

        if len(hull_vertices) < 3:
            return  # Convex hull requires at least 3 vertices

        # Display the convex hull on the canvas
        for i in range(len(hull_vertices) - 1):
            x1, y1 = hull_vertices[i]
            x2, y2 = hull_vertices[i + 1]
            self.canvas.create_line(x1, y1, x2, y2, fill="red", tags="convex_hull")

        # Connect the last and first vertices to close the polygon
        x1, y1 = hull_vertices[-1]
        x2, y2 = hull_vertices[0]
        self.canvas.create_line(x1, y1, x2, y2, fill="red", tags="convex_hull")


if __name__ == "__main__":
    root = tk.Tk()
    app = GeometryApp(root)
    root.mainloop()
