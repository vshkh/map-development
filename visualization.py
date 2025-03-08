import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import matplotlib.patches as mpatches

def plot_livestock_map(biome_map):
    """
    Visualizes livestock distribution using colored dots directly from biome objects.

    Parameters:
        biome_map (np.array): 2D array of Biome objects.
    """
    map_size = biome_map.shape[0]

    # Define colors for different livestock.
    livestock_colors = {
        "Camel": "brown",
        "Reindeer": "white",
        "Yak": "gray",
        "Elephant": "purple",
        "Cattle": "red",
        "Horse": "darkred",
        "Sheep": "lightgray",
        "Pig": "pink",
        "Mountain Goat": "darkgreen",
        "Seal": "navy",
        "Fish": "blue",
        "Dolphin": "aqua",
        "Whale": "teal"
    }

    plt.figure(figsize=(12, 12))

    # Background Biome Map (Grayscale for Clarity)
    biome_color_map = np.zeros((map_size, map_size, 3))
    for i in range(map_size):
        for j in range(map_size):
            biome_color_map[i, j] = (0.7, 0.7, 0.7)  # Light gray background

    plt.imshow(biome_color_map, origin="upper")

    # Overlay livestock dots (directly from biome objects)
    for i in range(map_size):
        for j in range(map_size):
            animals = biome_map[i, j].livestock  # Get livestock from biome object
            for animal in animals:
                if animal in livestock_colors:
                    plt.scatter(j, i, color=livestock_colors[animal], s=15, alpha=0.8)

    plt.title("Livestock Map", fontsize=16)
    plt.axis("off")

    # Legend for livestock colors
    handles = [plt.Line2D([0], [0], marker='o', color='w', markersize=8, markerfacecolor=color, label=animal)
               for animal, color in livestock_colors.items()]
    plt.legend(handles=handles, bbox_to_anchor=(1.05, 1), loc="upper left")

    plt.show()


def plot_enlarged_biome_map(biome_map, river_map):
    """
    Displays an enlarged biome map with special feature annotations.
    
    Parameters:
        biome_map (np.array): 2D array of Biome objects.
        river_map (np.array): 2D boolean array indicating river locations.
    """
    # Define colors for each biome.
    biome_colors = {
        "Ocean": "#1f77b4", 
        "Coast": "#2ca02c", 
        "Plains": "#bcbd22",
        "Rainforest": "#17becf", 
        "Desert": "#e377c2", 
        "Tundra": "#7f7f7f",
        "Mountain": "#8c564b", 
        "Unknown": "#d62728"
    }
    
    map_size = biome_map.shape[0]
    # Build a color map for visualization.
    biome_color_map = np.zeros((map_size, map_size, 3))
    for i in range(map_size):
        for j in range(map_size):
            biome_name = biome_map[i, j].name if biome_map[i, j] else "Unknown"
            color_hex = biome_colors.get(biome_name, "#d62728")
            # Convert hex to RGB tuple (normalized to 0-1).
            biome_color_map[i, j] = tuple(int(color_hex[k:k+2], 16) / 255 for k in (1, 3, 5))
    
    # Create a larger figure for better visibility.
    plt.figure(figsize=(12, 12))
    plt.imshow(biome_color_map, origin="upper")
    plt.title("Enlarged Biome Map", fontsize=16)
    
    # Overlay rivers in blue.
    river_i, river_j = np.where(river_map)
    plt.scatter(river_j, river_i, c="blue", s=20, alpha=0.7)
    
    # Add text annotations for special features.
    # For clarity, we use a larger font size.
    for i in range(map_size):
        for j in range(map_size):
            features = biome_map[i, j].special_features if biome_map[i, j] else []
            if features:
                # Create a label with the first letter of each feature.
                label = ",".join([f[0] for f in features])
                plt.text(j, i, label, color="white", fontsize=12, ha="center", va="center", weight="bold")
    
    # Build custom legend for biomes.
    patches = [mpatches.Patch(color=color, label=biome) for biome, color in biome_colors.items()]
    plt.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc="upper left")
    
    plt.axis("off")
    plt.tight_layout()
    plt.show()


def plot_maps(elevation_map, temperature_map, moisture_map, biome_map, river_map):
    """Visualizes multiple maps side-by-side with biome special feature annotations."""
    
    fig, ax = plt.subplots(1, 4, figsize=(24, 5))

    # Elevation Map
    elev_plot = ax[0].imshow(elevation_map, cmap="terrain", origin="upper")
    ax[0].set_title("Elevation Map")
    plt.colorbar(elev_plot, ax=ax[0])

    # Temperature Map (Converted to Celsius)
    temp_celsius = temperature_map * 40 - 10  # Convert to -10°C to 30°C
    temp_plot = ax[1].imshow(temp_celsius, cmap="coolwarm", origin="upper")
    ax[1].set_title("Temperature Map (°C)")
    plt.colorbar(temp_plot, ax=ax[1])

    # Moisture Map
    moist_plot = ax[2].imshow(moisture_map, cmap="Blues", origin="upper")
    ax[2].set_title("Moisture Map")
    plt.colorbar(moist_plot, ax=ax[2])

    # Biome Map with Custom Colors
    biome_colors = {
        "Ocean": "#1f77b4", "Coast": "#2ca02c", "Plains": "#bcbd22",
        "Rainforest": "#17becf", "Desert": "#e377c2", "Tundra": "#7f7f7f",
        "Mountain": "#8c564b", "Unknown": "#d62728"
    }
    
    biome_color_map = np.zeros((biome_map.shape[0], biome_map.shape[1], 3))
    for i in range(biome_map.shape[0]):
        for j in range(biome_map.shape[1]):
            # Use the biome name stored in the object
            biome_name = biome_map[i, j].name if biome_map[i, j] else "Unknown"
            color_hex = biome_colors.get(biome_name, "#d62728")
            biome_color_map[i, j] = tuple(int(color_hex[k:k+2], 16) / 255 for k in (1, 3, 5))

    ax[3].imshow(biome_color_map, origin="upper")
    ax[3].set_title("Biome Map")

    # Overlay Rivers on Biome Map
    river_i, river_j = np.where(river_map)
    ax[3].scatter(river_j, river_i, c="blue", s=5, alpha=0.7)  # Blue dots for rivers
    
    # Build custom legend for biomes
    patches = [mpatches.Patch(color=color, label=biome) for biome, color in biome_colors.items()]
    ax[3].legend(handles=patches, bbox_to_anchor=(1.05, 1), loc="upper left")

    plt.tight_layout()
    plt.show()

def plot_resource_map(biome_map, resource_map):
    """
    Visualizes the resource distribution using colored markers on the biome map.

    Parameters:
        biome_map (np.array): 2D array of Biome objects.
        resource_map (dict): Dictionary mapping (i, j) to resource names.
    """
    map_size = biome_map.shape[0]

    # Assign colors to resources
    resource_colors = {
        "Salt": "gray", "Copper": "orange",
        "Fur": "brown", "Iron": "darkgray",
        "Rubber": "black", "Herbs": "green",
        "Wheat": "yellow", 
        "Gold": "gold", "Coal": "black",
        "Pearls": "pink", "Coral": "cyan"
    }

    plt.figure(figsize=(12, 12))
    
    # Background Biome Map (Grayscale for clarity)
    biome_color_map = np.zeros((map_size, map_size, 3))
    for i in range(map_size):
        for j in range(map_size):
            biome_color_map[i, j] = (0.7, 0.7, 0.7)  # Light gray background

    plt.imshow(biome_color_map, origin="upper")

    # Overlay resources using colored dots
    for (i, j), resource in resource_map.items():
        if resource in resource_colors:
            plt.scatter(j, i, color=resource_colors[resource], s=20, alpha=0.8)

    plt.title("Resource Map with Cellular Automata", fontsize=16)
    plt.axis("off")

    # Legend for resource colors
    handles = [plt.Line2D([0], [0], marker='o', color='w', markersize=8, markerfacecolor=color, label=resource)
               for resource, color in resource_colors.items()]
    plt.legend(handles=handles, bbox_to_anchor=(1.05, 1), loc="upper left")

    plt.show()

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

def plot_combined_maps(biome_map, river_map, resource_map):
    """
    Generates a side-by-side visualization of the Biome Map, Livestock Map (scatter), and Resource Map (scatter).

    Parameters:
        biome_map (np.array): 2D array of Biome objects.
        river_map (np.array): 2D boolean array indicating river locations.
        resource_map (dict): Dictionary mapping (i, j) to resource names.
    """
    map_size = biome_map.shape[0]

    # Define colors for biomes
    biome_colors = {
        "Ocean": "#1f77b4", "Coast": "#2ca02c", "Plains": "#bcbd22",
        "Rainforest": "#17becf", "Desert": "#e377c2", "Tundra": "#7f7f7f",
        "Mountain": "#8c564b", "Unknown": "#d62728"
    }

    # Define colors for livestock
    livestock_colors = {
        "Camel": "brown", "Reindeer": "white", "Yak": "gray",
        "Elephant": "purple", "Cattle": "red", "Horse": "darkred",
        "Sheep": "lightgray", "Pig": "pink", "Mountain Goat": "darkgreen",
        "Seal": "navy", "Fish": "blue", "Dolphin": "aqua", "Whale": "teal"
    }

    # Define colors for resources
    resource_colors = {
        "Salt": "gray", "Copper": "orange", "Fur": "brown", "Iron": "darkgray",
        "Rubber": "black", "Herbs": "green", "Wheat": "yellow",
        "Gold": "gold", "Coal": "black", "Pearls": "pink", "Coral": "cyan"
    }

    # Generate the biome color map
    biome_color_map = np.zeros((map_size, map_size, 3))
    for i in range(map_size):
        for j in range(map_size):
            biome_name = biome_map[i, j].name if biome_map[i, j] else "Unknown"
            color_hex = biome_colors.get(biome_name, "#d62728")
            biome_color_map[i, j] = tuple(int(color_hex[k:k+2], 16) / 255 for k in (1, 3, 5))

    # Create figure with 3 side-by-side maps
    fig, ax = plt.subplots(1, 3, figsize=(24, 8))

    # --- Biome Map ---
    ax[0].imshow(biome_color_map, origin="upper")
    ax[0].set_title("Biome Map", fontsize=16)
    ax[0].axis("off")

    # Overlay Rivers on Biome Map
    river_i, river_j = np.where(river_map)
    ax[0].scatter(river_j, river_i, c="blue", s=5, alpha=0.7)  # Blue dots for rivers

    # --- Livestock Map (Scatter Plot) ---
    ax[1].set_xlim(0, map_size)
    ax[1].set_ylim(0, map_size)
    ax[1].invert_yaxis()
    ax[1].set_title("Livestock Map", fontsize=16)

    # Scatter livestock data
    for i in range(map_size):
        for j in range(map_size):
            animals = biome_map[i, j].livestock if biome_map[i, j] else []
            for animal in animals:
                if animal in livestock_colors:
                    ax[1].scatter(j, i, color=livestock_colors[animal], s=15, alpha=0.8)

    # --- Resource Map (Scatter Plot) ---
    ax[2].set_xlim(0, map_size)
    ax[2].set_ylim(0, map_size)
    ax[2].invert_yaxis()
    ax[2].set_title("Resource Map", fontsize=16)

    # Scatter resource data
    for (i, j), resource in resource_map.items():
        if resource in resource_colors:
            ax[2].scatter(j, i, color=resource_colors[resource], marker="o", s=30, alpha=0.9)

    # Build legends
    biome_patches = [mpatches.Patch(color=color, label=biome) for biome, color in biome_colors.items()]
    livestock_patches = [plt.Line2D([0], [0], marker='o', color='w', markersize=8, markerfacecolor=color, label=animal)
                         for animal, color in livestock_colors.items()]
    resource_patches = [plt.Line2D([0], [0], marker='o', color='w', markersize=10, markerfacecolor=color, label=resource)
                        for resource, color in resource_colors.items()]

    # Add legends next to each map
    ax[0].legend(handles=biome_patches, bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=10)
    ax[1].legend(handles=livestock_patches, bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=10)
    ax[2].legend(handles=resource_patches, bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=10)

    plt.tight_layout()
    plt.show()

def plot_village_expansion(biome_map, village_tiles):
    """
    Visualizes village expansion on the biome map.
    
    Parameters:
        biome_map (np.array): 2D array of Biome objects.
        village_tiles (set): Set of (x, y) coordinates controlled by the village.
    """
    map_size = biome_map.shape[0]
    
    # Define colors for biomes
    biome_colors = {
        "Ocean": "#1f77b4", "Coast": "#2ca02c", "Plains": "#bcbd22",
        "Rainforest": "#17becf", "Desert": "#e377c2", "Tundra": "#7f7f7f",
        "Mountain": "#8c564b", "Unknown": "#d62728"
    }
    
    # Create a color map for visualization
    biome_color_map = np.zeros((map_size, map_size, 3))
    for i in range(map_size):
        for j in range(map_size):
            biome_name = biome_map[i, j].name if biome_map[i, j] else "Unknown"
            color_hex = biome_colors.get(biome_name, "#d62728")
            biome_color_map[i, j] = tuple(int(color_hex[k:k+2], 16) / 255 for k in (1, 3, 5))
    
    # Create figure
    plt.figure(figsize=(12, 12))
    plt.imshow(biome_color_map, origin="upper")
    plt.title("Village Expansion", fontsize=16)
    
    # Overlay village-controlled tiles in red
    village_x, village_y = zip(*village_tiles)
    plt.scatter(village_y, village_x, color="red", s=20, alpha=0.8, label="Village Territory")
    
    # Build legend
    patches = [mpatches.Patch(color=color, label=biome) for biome, color in biome_colors.items()]
    plt.legend(handles=patches + [mpatches.Patch(color="red", label="Village")], 
               bbox_to_anchor=(1.05, 1), loc="upper left")
    
    plt.axis("off")
    plt.show()

def plot_world_map(map_size, biome_map, villages, trade_log, collapsed_villages):
    """Visualizes the world map with village locations, trade routes, and collapsed villages."""
    fig, ax = plt.subplots(figsize=(10, 10))
    world_map = np.zeros((map_size, map_size))
    
    # Assign colors for biomes
    biome_colors = {
        "Ocean": 0, "Plains": 1, "Rainforest": 2, "Coast": 3,
        "Tundra": 4, "Desert": 5, "Mountain": 6
    }
    
    for i in range(map_size):
        for j in range(map_size):
            world_map[i, j] = biome_colors.get(biome_map[i, j].name, 7)  # Default color for unknown biomes
    
    ax.imshow(world_map, cmap="tab10", origin="upper")
    
    # Plot active villages
    for village in villages:
        ax.scatter(village.position[1], village.position[0], c="red", s=50, edgecolors="black", label="Active Village" if village == villages[0] else "")
    
    # Plot collapsed villages in dark purple
    for pos in collapsed_villages:
        ax.scatter(pos[1], pos[0], c="purple", s=50, edgecolors="black", label="Collapsed Village" if pos == collapsed_villages[0] else "")
    
    # Plot trade routes
    for trade in trade_log:
        v1, v2, success = trade
        color = "green" if success else "red"  # Green for successful trade, red for failed
        ax.plot([v1[1], v2[1]], [v1[0], v2[0]], linestyle="--", color=color, linewidth=1.5, alpha=0.7)
    
    ax.set_title("World Map with Villages, Trade Routes, and Collapsed Settlements")
    ax.set_xlabel("X Coordinate")
    ax.set_ylabel("Y Coordinate")
    ax.legend()
    plt.show()

def plot_migration_events(migration_log):
    """Visualizes migration events over time."""
    fig, ax = plt.subplots(figsize=(10, 5))
    turns, migration_counts = zip(*migration_log) if migration_log else ([], [])
    
    ax.plot(turns, migration_counts, marker="o", linestyle="-", color="blue", label="Migration Events")
    
    ax.set_title("Migration Events Over Time")
    ax.set_xlabel("Turns")
    ax.set_ylabel("Number of Migrants")
    ax.legend()
    ax.grid(True)
    plt.show()

def plot_relationship_graph(relationship_manager):
    """Visualizes village relationships as a graph."""
    G = nx.Graph()

    # Add nodes (villages)
    for village_id in relationship_manager.relationships:
        G.add_node(village_id)

    # Add edges (relationships)
    edge_colors = []
    edge_weights = []
    for village_id, relations in relationship_manager.relationships.items():
        for other_id, score in relations.items():
            if village_id < other_id:  # Avoid duplicate edges (undirected graph)
                G.add_edge(village_id, other_id)
                edge_colors.append("green" if score > 0 else "red")
                edge_weights.append(abs(score) / 50)  # Normalize weight for visibility

    # Draw the graph
    plt.figure(figsize=(10, 6))
    pos = nx.spring_layout(G, seed=42)  # Position nodes nicely
    nx.draw(G, pos, with_labels=True, node_color="lightblue", edge_color=edge_colors, width=edge_weights, font_size=10, node_size=500)
    
    # Create a legend
    red_patch = mpatches.Patch(color='red', label='Hostile (-)')
    green_patch = mpatches.Patch(color='green', label='Friendly (+)')
    plt.legend(handles=[red_patch, green_patch], loc="upper right")
    plt.title("Village Relationship Graph")
    plt.show()
