from visualization import plot_maps, plot_enlarged_biome_map, plot_livestock_map, plot_resource_map, plot_village_expansion, plot_world_map, plot_migration_events
from map import MapGenerator
from world import World
import matplotlib.pyplot as plt

def plot_resource_trends(turns, population_data, avg_supply_data, num_villages_data):
    """Generates a graph tracking village statistics over time."""
    plt.figure(figsize=(10, 6))
    plt.plot(turns, population_data, label="Total Population", marker='o', linestyle='-')
    plt.plot(turns, avg_supply_data, label="Average Supply", marker='s', linestyle='--')
    plt.plot(turns, num_villages_data, label="Number of Villages", marker='^', linestyle='-.')
    
    plt.xlabel("Turns")
    plt.ylabel("Statistics")
    plt.title("Village Growth & Survival Trends Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()


# Map generation
map_size = 100
map_gen = MapGenerator(map_size)
map_gen.generate_all(num_rivers=15, min_elev_start=0.3, resource_iterations=5)

# Get biome map
biome_map = map_gen.get_biome_map()

# Create the world with multiple villages
world = World(map_size, biome_map, num_villages=70)

# Track statistics
turns = []
population_data = []
num_villages_data = []
avg_supply_data = []

# Run simulation
turn = 0
while turn < 1000 and len(world.villages) > 0:
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

world.visualize_world()
plot_resource_trends(turns, population_data, avg_supply_data, num_villages_data)
