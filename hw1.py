from string import ascii_lowercase
import sys
from collections import deque

def load_dictionary(file_name):
    with open(file_name) as f:
        return set(word.strip().lower() for word in f)

def get_neighbors(word, dictionary):
    neighbors = []
    for i in range(len(word)):
        for letter in ascii_lowercase:
            new_word = word[:i] + letter + word[i+1:] # Replace the i-th letter of the word with letter
            if new_word in dictionary and new_word != word:
                neighbors.append(new_word)
    return neighbors

def bfs(dictionary, start, target):
    queue = deque([[start]])
    visited = set([start])

    while queue:
        path = queue.popleft()
        current_word = path[-1]

        if current_word == target:
            return path

        for neighbor in get_neighbors(current_word, dictionary):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])

    return None

def main():
    if len(sys.argv) != 4:
        print("Usage: python hw1.py <dictionary_file> <start_word> <target_word>")
        return

    dictionary_file = sys.argv[1]
    start_word = sys.argv[2].lower()
    target_word = sys.argv[3].lower()

    dictionary = load_dictionary(dictionary_file)

    path = bfs(dictionary, start_word, target_word)

    if path:
        print("\n".join(path))
    else:
        print("No solution")

if __name__ == "__main__":
    main()
