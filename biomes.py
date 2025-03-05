import random
import numpy as np

class Biome:
    def __init__(self, name, terrain_type, temperature, humidity, fertility, climate_zone, 
                 elevation, livestock, special_features, supply, security, satisfaction):
        self.name = name
        self.terrain_type = terrain_type
        self.temperature = temperature
        self.humidity = humidity
        self.fertility = fertility
        self.climate_zone = climate_zone
        self.elevation = elevation
        self.livestock = livestock
        self.special_features = special_features
        self.supply = supply
        self.security = security
        self.satisfaction = satisfaction

    def __repr__(self):
        return (f"Biome(name={self.name}, terrain_type={self.terrain_type}, temperature={self.temperature:.2f}°C, "
                f"humidity={self.humidity:.2f}, fertility={self.fertility:.2f}, climate_zone={self.climate_zone}, "
                f"elevation={self.elevation:.2f}m, special_features={self.special_features})\n"
                f"{{'Supply': {self.supply}, 'Security': {self.security}, 'Satisfaction': {self.satisfaction}}}")

# Biome data dictionary
biome_data = {
    "Ocean": {"terrain": "Water", "climate_zone": "Marine", "special_features": ["Coastal Waters"], "supply": 50, "security": 40, "satisfaction": 80},
    "Coast": {"terrain": "Sandy/Marshy", "climate_zone": "Temperate", "special_features": ["Beaches", "Wetlands"], "supply": 60, "security": 50, "satisfaction": 85},
    "Plains": {"terrain": "Grassy", "climate_zone": "Temperate", "special_features": [], "supply": 63, "security": 70, "satisfaction": 86},
    "Rainforest": {"terrain": "Dense Forest", "climate_zone": "Tropical", "special_features": ["Dense Canopy"], "supply": 71, "security": 70, "satisfaction": 93},
    "Desert": {"terrain": "Arid", "climate_zone": "Dry", "special_features": ["Oasis", "Sand Dunes", "Rocky Outcrops"], "supply": 36, "security": 70, "satisfaction": 69},
    "Tundra": {"terrain": "Frozen", "climate_zone": "Continental", "special_features": [], "supply": 36, "security": 70, "satisfaction": 71},
    "Mountain": {"terrain": "Rocky", "climate_zone": "Continental", "special_features": ["Snow Peaks"], "supply": 34, "security": 60, "satisfaction": 68},
}

def determine_livestock(biome_name: str) -> list:
    """
    Probabilistically assigns livestock/animals based on the given biome name.
    
    Parameters:
        biome_name (str): The name of the biome (e.g., "Desert", "Tundra", "Rainforest", etc.)
        
    Returns:
        list: A list of animals that were randomly chosen for that biome.
    """
    livestock_probabilities = {
        "Desert": [("Camel", 0.2)],
        "Tundra": [("Reindeer", 0.1), ("Yak", 0.2)],
        "Rainforest": [("Elephant", 0.1)],
        "Plains": [("Cattle", 0.15), ("Horse", 0.2), ("Sheep", 0.3), ("Pig", 0.3)],
        "Mountain": [("Mountain Goat", 0.5)],
        "Coast": [("Seal", 0.2), ("Fish", 0.8)],
        "Ocean": [("Dolphin", 0.02), ("Whale", 0.01)],
    }
    
    animals = []
    if biome_name in livestock_probabilities:
        for animal, probability in livestock_probabilities[biome_name]:
            if random.random() < probability:
                animals.append(animal)
    return animals


def determine_special_features(biome_name: str) -> list:
    """
    Probabilistically assigns special features based on the given biome name.
    
    Parameters:
        biome_name (str): The name of the biome (e.g., "Desert", "Tundra", etc.)
        
    Returns:
        list: A list of special features that were randomly chosen.
    """
    feature_probabilities = {
        "Desert": [("Oasis", 0.01), ("Sand Dunes", 0.2), ("Rocky Outcrops", 0.2)],
        "Tundra": [("Permafrost", 0.1), ("Glacier", 0.1)],
        "Rainforest": [("Dense Canopy", 0.2), ("Hidden Waterfalls", 0.05)],
        "Plains": [("Rolling Hills", 0.1), ("Wildflower Fields", 0.1)],
        "Mountains": [("Caves", 0.2), ("Snow Peaks", 0.3)],
    }
    
    features = []
    if biome_name in feature_probabilities:
        for feature, probability in feature_probabilities[biome_name]:
            if random.random() < probability:
                features.append(feature)
    return features

def generate_resource_map_ca(biome_map, map_size, iterations=3):
    """
    Uses cellular automata to generate naturally clustered resource distributions 
    while considering resource rarity.

    Parameters:
        biome_map (np.array): 2D array of Biome objects.
        map_size (int): The size of the map (assuming square).
        iterations (int): Number of cellular automata iterations.

    Returns:
        dict: Dictionary mapping tile positions (i, j) to a resource name.
    """

    # Define biome-specific resources with rarity levels
    biome_resources = {
        "Desert": [("Salt", "common"), ("Copper", "rare")],
        "Tundra": [("Fur", "rare"), ("Iron", "uncommon")],
        "Rainforest": [("Rubber", "uncommon"), ("Herbs", "common")],
        "Plains": [("Wheat", "common")],
        "Mountain": [("Gold", "rare"), ("Iron", "uncommon"), ("Coal", "common")],
        "Coast": [("Pearls", "rare")],
        "Ocean": [("Coral", "rare")]
    }

    # Rarity modifiers: affects initial placement & spread probability
    rarity_settings = {
        "common": {"init_prob": 0.15, "spread_prob": 0.8},  # High start, easy spread
        "uncommon": {"init_prob": 0.08, "spread_prob": 0.6},  # Moderate start, moderate spread
        "rare": {"init_prob": 0.04, "spread_prob": 0.4},  # Few initial tiles, harder to spread
        "very_rare": {"init_prob": 0.02, "spread_prob": 0.25}  # Extremely rare, very small spread
    }

    resource_map = {}

    # Step 1: Initialize resource "seeds" based on rarity
    ca_grid = np.full((map_size, map_size), None, dtype=object)

    for i in range(map_size):
        for j in range(map_size):
            biome_name = biome_map[i, j].name
            if biome_name in biome_resources:
                for resource, rarity in biome_resources[biome_name]:
                    if random.random() < rarity_settings[rarity]["init_prob"]:  # Rarity-controlled start
                        ca_grid[i, j] = resource

    # Step 2: Cellular Automata Iterations
    for _ in range(iterations):
        new_grid = np.full((map_size, map_size), None, dtype=object)

        for i in range(map_size):
            for j in range(map_size):
                biome_name = biome_map[i, j].name

                # Count neighboring resources
                neighbors = []
                for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # 4-way adjacency
                    ni, nj = i + di, j + dj
                    if 0 <= ni < map_size and 0 <= nj < map_size and ca_grid[ni, nj]:
                        neighbors.append(ca_grid[ni, nj])

                if ca_grid[i, j]:  # If tile already has a resource, it persists
                    rarity = next((r for res, r in biome_resources[biome_name] if res == ca_grid[i, j]), "common")
                    if random.random() < rarity_settings[rarity]["spread_prob"]:  
                        new_grid[i, j] = ca_grid[i, j]
                elif neighbors:  # If tile is empty but has neighbors with resources
                    chosen_neighbor = random.choice(neighbors)
                    rarity = next((r for res, r in biome_resources[biome_name] if res == chosen_neighbor), "common")
                    if random.random() < rarity_settings[rarity]["spread_prob"]:  # Lower chance for rare
                        new_grid[i, j] = chosen_neighbor

        ca_grid = new_grid  # Update for next iteration

    # Step 3: Convert CA Grid to Resource Map
    for i in range(map_size):
        for j in range(map_size):
            if ca_grid[i, j]:
                resource_map[(i, j)] = ca_grid[i, j]

    return resource_map
