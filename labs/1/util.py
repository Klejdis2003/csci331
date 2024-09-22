from typing import Tuple

from PIL import Image

INFINITE = float('inf')

def get_run_args() -> tuple[str, ...]:
    import sys
    return tuple(sys.argv[1:])

def read_csv(file_path: str, max_cols: int = INFINITE) -> list[list[str]]:
    with open(file_path, "r") as file:
        rows = []
        for line in file:
            elements = line.strip().split()
            max_cols = min(max_cols, len(elements))
            rows.append(elements[:max_cols])
        return rows

def read_points(file_path: str) -> list[Tuple[int, int]]:
    points = read_csv(file_path)
    return [(int(x), int(y)) for x, y in points]

def read_image(file_path: str) -> Image.Image:
    image = Image.open(file_path)
    return image.getdata()