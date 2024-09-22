from cost_model import CostModel
from util import INFINITE

X_DISTANCE = 10.29 # meters
Y_DISTANCE = 7.55 # meters

costs = [
    CostModel('Open Land', (248, 148, 18), 1.0),
    CostModel('Rough Meadow', (255, 192, 0), 1.5),
    CostModel('Easy Movement Forest', (255, 255, 255), 1.2),
    CostModel('Slow Run Forest', (2, 208, 60), 1.8),
    CostModel('Walk Forest', (2, 136, 40), 2.0),
    CostModel('Impassable Vegetation', (5, 73, 24), INFINITE),
    CostModel('Lake/Swamp/Marsh', (0, 0, 255), 15.0),
    CostModel('Paved Road', (71, 51, 3), 0.8),
    CostModel('Footpath', (0, 0, 0), 1.0),
    CostModel('Out of Bounds', (205, 0, 101), INFINITE)
]
cost_map: dict[tuple[int, int, int], CostModel] = {cost.rgb_value: cost for cost in costs}