from queue import PriorityQueue

import PIL.ImageFile
from PIL import Image

from point import Point3d
from setup import *
from util import read_csv, read_image, get_run_args, read_points


def setup_data(terrain_image_file: str, elevation_file: str, path_file: str, output_image_file: str):
    terrain_image = Image.open(terrain_image_file).convert("RGB")
    elevation_data = [[float(x) for x in row] for row in read_csv(elevation_file, 395)]
    path_points = read_points(path_file)
    output_path= output_image_file
    return terrain_image, elevation_data, path_points, output_path

def hx(p1: Point3d, p2: Point3d) -> float:
    return p2.distance_from(p1, X_DISTANCE, Y_DISTANCE)


def get_neighbors(point: Point3d, terrain_data: PIL.ImageFile, elevation_data: list[list[float]]) -> list[Point3d]:
    """
    8-connected neighbors for North, South, East, West, and diagonals.
    :param point:  The point to get neighbors for.
    :param terrain_data:  The terrain data.
    :param elevation_data:  The elevation data.
    :return:  The neighbors of the point.
    """
    possible_moves = [(x,y) for x in range(-1, 2) for y in range(-1, 2) if (x, y) != (0, 0)]
    neighbors = []
    cols, rows = terrain_data.size
    for dx, dy in possible_moves:
        x, y = point.x + dx, point.y + dy
        if 0 <= x < cols and 0 <= y < rows:
            z = elevation_data[y][x]
            neighbors.append(Point3d(x, y, z))
    return neighbors


def a_star_search(start: Point3d, goal: Point3d, terrain_data: PIL.ImageFile, elevation_data: list) -> list[Point3d]:
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

        neighbors = get_neighbors(current, terrain_data, elevation_data)

        for next_node in neighbors:
            new_cost = cost_map[terrain_data.getpixel((next_node.x, next_node.y))].cost + cost_so_far[current]

            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost + hx(goal, next_node)  # f = g + h (cost + heuristic)
                frontier.put((priority, next_node))  # Add to frontier with priority
                came_from[next_node] = current  # Keep track of the path

    # Reconstruct path
    path = []
    current = goal
    while current != start:
        if current not in came_from:  # Safety check to avoid in    finite loop
            print("No valid path found!")
            return []  # Return empty path if something goes wrong
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
    if len(args) != 4:
        print("Usage: python3 lab1.py <terrain_image> <elevation_file> <path_file> <output_image_file>")
        return
    terrain_image, elevation_data, path_points, output_path = setup_data(*args)
    output_image = terrain_image.copy()

    paths: list[list[Point3d]] = []
    for i in range(len(path_points) - 1):
        x1, y1 = path_points[i]
        x2, y2 = path_points[i + 1]
        start = Point3d(x1, y1, elevation_data[y1][x1])
        goal = Point3d(x2, y2, elevation_data[y1][x1])

        path = a_star_search(start, goal, terrain_image, elevation_data)
        output_image = draw_path(path, output_image , output_path)
        paths.append(path)

    output_image.save(output_path)


    paths = [point for path in paths for point in path]
    total_distance_meter = sum(paths[i].distance_from(paths[i + 1], X_DISTANCE, Y_DISTANCE) for i in range(len(paths) - 1))
    print(total_distance_meter)



if __name__ == "__main__":
    main()