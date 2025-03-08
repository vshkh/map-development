from visualization import plot_maps, plot_enlarged_biome_map, plot_livestock_map, plot_resource_map, plot_village_expansion, plot_world_map, plot_migration_events, plot_relationship_graph, plot_resource_trends
from world_gen import MapGenerator
from world import World
import matplotlib.pyplot as plt

# Map generation
map_size = 50
map_gen = MapGenerator(map_size)
map_gen.generate_all(num_rivers=15, min_elev_start=0.3, resource_iterations=5)

# Get biome map
biome_map = map_gen.get_biome_map()

# Create the world with multiple villages
world = World(map_size, biome_map, num_villages=50)

# Track statistics
turns = []
population_data = []
num_villages_data = []
avg_supply_data = []

# Run simulation
turn = 0
while turn < 100 and len(world.villages) > 0:
    #print(f"Turn: {turn + 1}:")
    turns.append(turn)
    
    # Log data
    total_population = sum(v.population for v in world.villages)
    avg_supply = sum(v.resources["supply"] for v in world.villages) / max(1, len(world.villages))
    population_data.append(total_population)
    num_villages_data.append(len(world.villages))
    avg_supply_data.append(avg_supply)
    
    world.update(turn)
    turn += 1
    #print(f"Turn {turn}: Villages={len(world.villages)}, Total Pop={total_population}, Avg Supply={avg_supply}")

#world.display_relationship_logs()
world.visualize_world()
plot_relationship_graph(world.relationship_manager)
#plot_resource_trends(turns, population_data, avg_supply_data, num_villages_data)