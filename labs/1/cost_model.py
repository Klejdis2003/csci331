class CostModel:
    def __init__(self, terrain_type: str, rgb_value: tuple[int, int, int], cost: float):
        self.terrain_type = terrain_type
        self.rgb_value = rgb_value
        self.cost = cost

    def __str__(self) -> str:
        return f"{self.terrain_type} {self.rgb_value} {self.cost}"

    def __eq__(self, other: 'CostModel') -> bool:
        return self.rgb_value == other.rgb_value

    def __hash__(self) -> int:
        return hash(self.rgb_value)
