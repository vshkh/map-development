import random

class ExpansionManager:
    def __init__(self, settlement):
        self.settlement = settlement

    def find_expansion_tile(self):
        """Find the best adjacent tile to expand into."""
        possible_tiles = []
        for x, y in self.settlement.controlled_tiles:
            neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
            for nx, ny in neighbors:
                if (nx, ny) not in self.settlement.controlled_tiles and 0 <= nx < len(self.settlement.biome_map) and 0 <= ny < len(self.settlement.biome_map[0]):
                    biome = self.settlement.biome_map[nx, ny]
                    if biome.name != "Ocean":
                        score = biome.supply * 0.6 + biome.security * 0.2 + biome.satisfaction * 0.2
                        possible_tiles.append((score, (nx, ny)))
        if possible_tiles:
            return max(possible_tiles, key=lambda x: x[0])[1]
        return None

    def expand(self):
        """Expand the settlement into a new tile."""
        if self.settlement.population >= 15 and self.settlement.resources["supply"] > 40 and random.random() < 0.6:
            new_tile = self.find_expansion_tile()
            if new_tile:
                self.settlement.controlled_tiles.add(new_tile)
                self.settlement.population -= random.randint(3, 8)
