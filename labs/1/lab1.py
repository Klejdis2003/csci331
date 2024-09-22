from queue import PriorityQueue

from PIL import Image

from point import Point3d
from setup import *
from util import read_csv, read_image, get_run_args, read_points


def setup_data(terrain_image_file: str, elevation_file: str, path_file: str, output_image_file: str):
    terrain_image = Image.open(terrain_image_file)
    elevation_data = [[float(x) for x in row] for row in read_csv(elevation_file, 395)]
    path_points = read_points(path_file)
    output_path= output_image_file
    return terrain_image, elevation_data, path_points, output_path

def hx(p1: Point3d, p2: Point3d) -> float:
    return p2.distance_from(p1, X_DISTANCE, Y_DISTANCE)


def get_neighbors(point: Point3d, terrain_data: list, elevation_data: list[float]) -> list[Point3d]:
    """
    8-connected neighbors for North, South, East, West, and diagonals.
    :param point:  The point to get neighbors for.
    :param terrain_data:  The terrain data.
    :param elevation_data:  The elevation data.
    :return:  The neighbors of the point.
    """
    possible_moves = [(x,y) for x in range(-1, 2) for y in range(-1, 2) if (x, y) != (0, 0)]
    neighbors = []
    for dx, dy in possible_moves:
        x, y = point.x + dx, point.y + dy
        if 0 <= x < len(terrain_data) and 0 <= y < len(terrain_data):
            z = elevation_data[x][y]
            neighbors.append(Point3d(x, y, z))
    return neighbors


def a_star_search(start: Point3d, goal: Point3d, terrain_data: list, elevation_data: list) -> list[Point3d]:
    """
    A* search algorithm to find the shortest path from the start to the goal.
    :param start:  The starting point.
    :param goal:  The goal point.
    :param terrain_data:  The terrain data.
    :param elevation_data:  The elevation data.
    :return:  The path from the start to the goal.
    """
    frontier = PriorityQueue()
    frontier.put(start)
    came_from = {start: None}
    cost_so_far = {start: 0}

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        neighbors = get_neighbors(current, terrain_data, elevation_data)
        for next_node in neighbors:
            new_cost = cost_so_far[current] + 1
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost + hx(goal, next_node)
                frontier.put(next_node, priority)
                came_from[next_node] = current

    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path


def draw_path(path: list[Point3d], terrain_image: Image, output_image_path: str):
    """
    Draws the path on the output image data.
    :param terrain_image: The terrain image.
    :param path:  The path to draw.
    :param output_image_path:  The output image path.
    """

    pixels = terrain_image.load()
    for point in path:
        #modify rgb values of pixels
        pixels[point.x, point.y] = (118, 63, 231)
    return terrain_image



def main():
    args = get_run_args()
    terrain_path = args[0]
    if len(args) != 4:
        print("Usage: python3 lab1.py <terrain_image> <elevation_file> <path_file> <output_image_file>")
        return
    terrain_image, elevation_data, path_points, output_path = setup_data(*args)

    paths: list[list[Point3d]] = []
    for point in path_points:
        start = Point3d(*path_points[0], elevation_data[path_points[0][0]][path_points[0][1]])
        goal = Point3d(*path_points[1], elevation_data[path_points[1][0]][path_points[1][1]])

        path = a_star_search(start, goal, list(terrain_image.getdata()), elevation_data)
        terrain_image = draw_path(path, terrain_image , output_path)
        paths.append(path)

    terrain_image.save(output_path)
    path_length_meters = sum(sum(point.distance_from(path[i+1]) for i, point in enumerate(path[:-1])) for path in paths)
    print(f"Path length in meters: {path_length_meters}")



if __name__ == "__main__":
    main()