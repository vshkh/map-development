# rivers.py
import numpy as np

def get_neighbors(i, j, size):
    """Return all eight neighboring coordinates within bounds."""
    neighbors = []
    for di, dj in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
        ni, nj = i + di, j + dj
        if 0 <= ni < size and 0 <= nj < size:
            neighbors.append((ni, nj))
    return neighbors

def simulate_river(start_i, start_j, elev_map, river_map, biome_map, max_length=150):
    """
    Simulate a river starting from (start_i, start_j), flowing to lower elevations.
    """
    current_i, current_j = start_i, start_j
    river_path = [(current_i, current_j)]
    river_map[current_i, current_j] = True
    visited = {(current_i, current_j)}

    for _ in range(max_length):
        neighbors = get_neighbors(current_i, current_j, elev_map.shape[0])
        if not neighbors:
            break

        unvisited_neighbors = [n for n in neighbors if n not in visited]
        if not unvisited_neighbors:
            break

        lowest_neighbor = min(unvisited_neighbors, key=lambda n: elev_map[n[0], n[1]])
        next_i, next_j = lowest_neighbor

        if biome_map[next_i, next_j].name in ["Ocean", "Coast"] or elev_map[next_i, next_j] < -0.05:
            river_path.append((next_i, next_j))
            river_map[next_i, next_j] = True
            break

        river_path.append((next_i, next_j))
        river_map[next_i, next_j] = True
        visited.add((next_i, next_j))
        current_i, current_j = next_i, next_j

    return river_path

def generate_multiple_rivers(elev_map, river_map, biome_map, num_rivers=20, min_elev_start=0.2):
    """
    Generate multiple rivers starting from high elevation points.

    Returns:
        list: List of river paths (each path is a list of (i, j) coordinates).
    """
    map_size = elev_map.shape[0]
    potential_starts = [(i, j) for i in range(map_size) for j in range(map_size) 
                        if elev_map[i, j] > min_elev_start and biome_map[i, j].name not in ["Ocean", "Coast"]]
    
    if not potential_starts:
        return []

    # Sample more starting points to ensure we get the desired number of rivers
    start_points = np.random.choice(len(potential_starts), min(num_rivers, len(potential_starts)), replace=False)
    river_paths = []
    
    for idx in start_points:
        start_i, start_j = potential_starts[idx]
        path = simulate_river(start_i, start_j, elev_map, river_map, biome_map)
        river_paths.append(path)

    return river_paths