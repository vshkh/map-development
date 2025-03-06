import random

class SupplyManager:
    def __init__(self, settlement):
        self.settlement = settlement

    def consume_resources(self):
        """Increase food consumption dynamically, but allow villages to survive longer."""
        base_consumption = 2  # Lower base consumption
        scaling_factor = max(1, self.settlement.population // 80)  # Slower scaling
        total_consumption = base_consumption + scaling_factor

        self.settlement.resources["supply"] -= total_consumption

    def store_resources(self):
        """Transfers excess supply into storage."""
        if self.settlement.resources["supply"] > 80:  # Lower threshold to store
            stored = min(self.settlement.resources["supply"] - 80, 10)  # Reduce max storage per turn
            self.settlement.resources["supply"] -= stored
            self.settlement.resources["storage"] += stored

    def use_storage(self):
        """If supply is too low, villages use storage, preventing sudden collapses."""
        if self.settlement.resources["supply"] < 20 and self.settlement.resources["storage"] > 0:  # Lower trigger point
            retrieval_amount = min(self.settlement.resources["storage"], 20)  # Reduce retrieval amount
            self.settlement.resources["supply"] += retrieval_amount
            self.settlement.resources["storage"] -= retrieval_amount
            
    def harvest_resources(self):
        """Gather food/resources based on biome type with the possibility of bad harvests."""
        current_biome = self.settlement.biome_map[self.settlement.position[0], self.settlement.position[1]]
        biome_harvest_yield = {
            "Plains": (3, 8), "Rainforest": (8, 12), "Coast": (3, 8),  # Reduced yields
            "Tundra": (1, 4), "Desert": (1, 6), "Mountain": (2, 6)
        }

        if current_biome.name in biome_harvest_yield:
            if random.random() < 0.25:  # Increase bad harvest chance to 25%
                harvested = random.randint(0, biome_harvest_yield[current_biome.name][0])  # Lower bound
                #print(f"Bad harvest! Only {harvested} supply gathered.")
            else:
                harvested = random.randint(*biome_harvest_yield[current_biome.name])
            self.settlement.resources["supply"] += harvested