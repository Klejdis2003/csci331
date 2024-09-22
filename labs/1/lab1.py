from util import get_run_args
from path_finder import ShortestPathFinder

def main():
    #setup data
    args = get_run_args()

    if len(args) != 4:
        print("Usage: python3 lab1.py <terrain_image> <elevation_file> <path_file> <output_image_file>")
        return

    path_finder = ShortestPathFinder(*args)
    print(path_finder.solve())


if __name__ == "__main__":
    main()


