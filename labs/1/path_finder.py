from queue import PriorityQueue
from PIL import Image
from point import Point3d
from util import read_csv, read_points
from constants import cost_map, X_DISTANCE, Y_DISTANCE, INFINITE


class ShortestPathFinder:
    def __init__(self, terrain_image_file: str, elevation_file: str, path_file: str, output_image_file: str):
        """
        Initializes the ShortestPathFinder.
        :param terrain_image_file: The terrain image file.
        :param elevation_file: The elevation file.
        :param path_file: The path file.
        :param output_image_file: The output image file.
        """
        self.output_image_path = output_image_file
        self.terrain_image = Image.open(terrain_image_file).convert("RGB")
        self.elevation_data = [[float(x) for x in row] for row in read_csv(elevation_file)]
        self.path = [(int(x), int(y)) for x, y in read_points(path_file)]
        self.output_image = self.terrain_image.copy()

    def solve(self) -> float:
        """
        Solves the shortest path problem.
        :return: The total distance of the paths.
        """
        paths = self._get_all_paths()
        return self._get_total_distance(paths)


    def _hx(self, p1: Point3d, p2: Point3d) -> float:
        """
        Heuristic function for A* search. Uses Euclidean distance to calculate the distance between two points in 3D space.
        :param p1: Point 1
        :param p2: Point 2
        :return: The distance between the two points.
        """
        return p1.distance_from(p2, X_DISTANCE, Y_DISTANCE)

    def _get_neighbors(self, point: Point3d) -> list[Point3d]:
        """
        8-connected neighbors for North, South, East, West, and diagonals.
        :param point:  The point to get neighbors for.
        :return:  The neighbors of the point.
        """
        possible_moves = [(x,y) for x in range(-1, 2) for y in range(-1, 2) if (x, y) != (0, 0)]
        neighbors = []
        cols, rows = self.terrain_image.size
        for dx, dy in possible_moves:
            x, y = point.x + dx, point.y + dy
            if 0 <= x < cols and 0 <= y < rows:
                z = self.elevation_data[y][x]
                neighbors.append(Point3d(x, y, z))
        return neighbors

    def _reconstruct_path(self, came_from: dict[Point3d, Point3d], start: Point3d, goal: Point3d) -> list[Point3d]:
        """
        Reconstructs the path from the start to the goal.
        :param came_from: The dictionary of nodes and their parent nodes.
        :param start: The starting node.
        :param goal: The goal node.
        :return: The path from the start to the goal.
        """
        current = goal
        if current not in came_from: #check if no solution
            return []

        path = []
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()
        return path

    def _a_star_search(self, start: Point3d, goal: Point3d) -> list[Point3d]:
        """
        A* search algorithm to find the shortest path from the start to the goal.
        """
        frontier = PriorityQueue()
        frontier.put((0, start))

        came_from = {start: None}
        cost_so_far = {start: 0}

        while not frontier.empty():
            current_priority, current = frontier.get()

            if current == goal:
                break

            neighbors = self._get_neighbors(current)

            for next_node in neighbors:
                terrain_cost = cost_map[self.terrain_image.getpixel((next_node.x, next_node.y))].cost
                if terrain_cost == INFINITE:
                    continue

                new_cost = terrain_cost + cost_so_far[current]

                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + self._hx(next_node, goal)
                    frontier.put((priority, next_node))
                    came_from[next_node] = current

        return self._reconstruct_path(came_from, start, goal)

    def _draw_path(self, path: list[Point3d]):
        """
        Draws the path on the output image data.
        :param path:  The path to draw.
        """
        pixels = self.output_image.load()
        for point in path:
            pixels[point.x, point.y] = (118, 63, 231)
        return self.output_image

    def _get_all_paths(self) -> list[list[Point3d]]:
        """
        Gets all the paths from the path points.
        :return: The paths from the path points.
        """
        paths = []
        for i in range(len(self.path) - 1):
            x1, y1 = self.path[i]
            x2, y2 = self.path[i + 1]
            start = Point3d(x1, y1, self.elevation_data[y1][x1])
            goal = Point3d(x2, y2, self.elevation_data[y2][x2])
            path = self._a_star_search(start, goal)
            self.output_image = self._draw_path(path)
            paths.append(path)

        self.output_image.save(self.output_image_path)

        return paths

    def _get_total_distance(self, paths: list[list[Point3d]]) -> float:
        """
        Finds the total distance of the paths.
        :param paths: The paths.
        :return: The total distance of the paths.
        """
        flattened_paths = [point for path in paths for point in path]
        return sum(flattened_paths[i].distance_from(flattened_paths[i + 1], X_DISTANCE, Y_DISTANCE)
                   for i in range(len(flattened_paths) - 1))


