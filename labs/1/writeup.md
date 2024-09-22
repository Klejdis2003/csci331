# Lab 1 Writeup
#### Name: Klejdis Beshi 
#### Date: 09/22/2024

### Heuristic Choice
Since we have 3 dimensional points where change in elevation also matters,
I chose to use the Euclidean distance as my heuristic. This is because the
Euclidean distance is the shortest distance between two points, even in 3D space.
Therefore, $for$ $P_1 = (x1, y1, z1)$ and $P_2 = (x2, y2, z2)$
$h(x) = \sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2 + (z_1 - z_2)^2}$

### Neighbors Function
Every node/point has 8 neighbors. 1 for each direction (N, S, E, W, NE, NW, SE, SW).
Therefore, the neighbors function will return a list of 8 neighbors for each node/point.

### Path Cost Function
Costs are defined in `constants.py` as follows:
```python
costs = [
    CostModel('Open Land', (248, 148, 18), 1.0),
    CostModel('Rough Meadow', (255, 192, 0), 1.5),
    CostModel('Easy Movement Forest', (255, 255, 255), 1.2),
    CostModel('Slow Run Forest', (2, 208, 60), 1.8),
    CostModel('Walk Forest', (2, 136, 40), 2.0),
    CostModel('Impassable Vegetation', (5, 73, 24), INFINITE),
    CostModel('Lake/Swamp/Marsh', (0, 0, 255), 3.0),
    CostModel('Paved Road', (71, 51, 3), 0.8),
    CostModel('Footpath', (0, 0, 0), 1.0),
    CostModel('Out of Bounds', (205, 0, 101), INFINITE)
]
```
I chose `Open Land`/`Foot Path` as the bases, hence a cost of **1.0**. Everything else is expressed
relative to them. For example, `Rough Meadow` is **1.5** times more costly than `Open Land` because
it is harder to traverse. For water bodies, they significantly slow you down, so they have a cost of **15**.
The `INFINITE` cost is used for `Impassable Vegetation` and `Out of Bounds`
because they are impassable.

### A* Implementation
Traditional implementation of A* algorithm, with a priority queue to keep track of the nodes to visit. The INFINITE
costs are used to avoid visiting impassable nodes. The algorithm will return the path from start to goal, or an empty
list if no path is found.

### Results
All test cases pass, with the largest one being within 50ms. The path is also visually correct.

### Code Structure
The code is structured in the following way:
- `lab1.py` the runnable file that takes the parameters and passes them down to initiate the chain of events.
- `path_finder.py` Contains the ShortestPathFinder class that implements the A* algorithm and everything related to it.
- `constants.py` Contains the constants used in the algorithm, such as costs, x distance, y distance, etc.
- `utils.py` Contains utility functions that are used throughout the code, such as reading from csv, reading points, reading args.
- `point.py` Contains the Point class that represents a point in 3D space.
- `cost_model.py` Contains the CostModel class that represents the cost of traversing a certain type of terrain.