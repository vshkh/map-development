from visualization import plot_maps, plot_resource_trends
from world_gen import MapGenerator
from world import World
import matplotlib.pyplot as plt

# Map generation
map_size = 100
map_gen = MapGenerator(map_size)
map_gen.generate_all(num_rivers=15, min_elev_start=0.3, resource_iterations=5)

# Get biome map
biome_map = map_gen.get_biome_map()

# Create the world (no villages yet)
world = World(map_size, biome_map)

# Run placeholder simulation
turns = list(range(100))
for turn in turns:
    world.update(turn)

# Visualize world (biomes and terrain only)
world.visualize_world()
