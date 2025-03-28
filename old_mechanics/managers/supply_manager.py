import random

class SupplyManager:
    def __init__(self, settlement):
        self.settlement = settlement

    def consume_resources(self):
        """Increase food consumption dynamically, with increasing demands as population grows."""
        # Base consumption per person increases with population density
        base_consumption = 1.5  # Base consumption per person
        
        # Calculate population density factor (increases more dramatically with larger populations)
        density_factor = 1 + (self.settlement.population / 200) ** 1.5  # Quadratic scaling
        
        # Calculate total consumption with diminishing returns
        total_consumption = base_consumption * density_factor * (self.settlement.population / 50)
        
        # Add a small random fluctuation
        fluctuation = random.uniform(0.9, 1.1)
        total_consumption *= fluctuation
        
        self.settlement.resources["supply"] -= total_consumption

    def store_resources(self):
        """Transfers excess supply into storage, with storage efficiency decreasing with population."""
        if self.settlement.resources["supply"] > 60:
            # Storage efficiency decreases with population size
            efficiency = max(0.5, 1 - (self.settlement.population / 500))
            max_storage = 15 * efficiency
            stored = min(self.settlement.resources["supply"] - 60, max_storage)
            self.settlement.resources["supply"] -= stored
            self.settlement.resources["storage"] += stored

    def use_storage(self):
        """If supply is too low, villages use storage, with efficiency decreasing with population."""
        if self.settlement.resources["supply"] < 15 and self.settlement.resources["storage"] > 0:
            # Storage usage efficiency decreases with population size
            efficiency = max(0.5, 1 - (self.settlement.population / 500))
            retrieval_amount = min(self.settlement.resources["storage"], 25 * efficiency)
            self.settlement.resources["supply"] += retrieval_amount
            self.settlement.resources["storage"] -= retrieval_amount
            
    def harvest_resources(self):
        """Gather food/resources based on biome type with the possibility of bad harvests."""
        current_biome = self.settlement.biome_map[self.settlement.position[0], self.settlement.position[1]]
        biome_harvest_yield = {
            "Plains": (4, 10), "Rainforest": (6, 12), "Coast": (4, 10),  # Balanced yields
            "Tundra": (2, 6), "Desert": (2, 8), "Mountain": (3, 8)
        }

        if current_biome.name in biome_harvest_yield:
            if random.random() < 0.2:  # Reduced bad harvest chance to 20%
                harvested = random.randint(0, biome_harvest_yield[current_biome.name][0])
            else:
                harvested = random.randint(*biome_harvest_yield[current_biome.name])
            self.settlement.resources["supply"] += harvested