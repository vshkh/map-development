# terrain.py
import numpy as np
import noise

def generate_plates(map_size, same_plate_prob=0.95, new_plate_prob=0.05):
    """Generates a plate map using a simple transition probability model."""
    plates = np.zeros((map_size, map_size), dtype=int)
    plate_id = 1
    plates[0, 0] = plate_id

    for i in range(map_size):
        for j in range(map_size):
            if i == 0 and j == 0:
                continue
            neighbors = []
            if i > 0:
                neighbors.append(plates[i-1, j])
            if j > 0:
                neighbors.append(plates[i, j-1])
            if neighbors and np.random.rand() < same_plate_prob:
                plates[i, j] = np.random.choice(neighbors)
            elif np.random.rand() < new_plate_prob:
                plate_id += 1
                plates[i, j] = plate_id
            else:
                plates[i, j] = np.random.choice(neighbors) if neighbors else plate_id
    return plates

def generate_noise_map(map_size):
    """Generates a noise map using multiple layers of Perlin noise."""
    noise_map = np.zeros((map_size, map_size))
    for i in range(map_size):
        for j in range(map_size):
            low_freq = noise.pnoise2(i * 0.01, j * 0.01, octaves=2) * 0.4
            med_freq = noise.pnoise2(i * 0.05, j * 0.05, octaves=3) * 0.3
            high_freq = noise.pnoise2(i * 0.1, j * 0.1, octaves=4) * 0.3
            noise_map[i, j] = low_freq + med_freq + high_freq
    return noise_map

def combine_plates_and_noise(plates, noise_map):
    """Combines the plate biases with the noise map to generate the final elevation."""
    map_size = noise_map.shape[0]
    unique_plates = np.unique(plates)
    plate_elevation = {plate: np.random.uniform(0.3, 1) for plate in unique_plates}
    elevation_map = np.zeros((map_size, map_size))
    for i in range(map_size):
        for j in range(map_size):
            base_elev = plate_elevation[plates[i, j]] * 0.3
            elev = (base_elev + noise_map[i, j] + 0.3) * 2 - 1
            elevation_map[i, j] = np.tanh(elev * 2)
    return elevation_map

def generate_elevation(map_size):
    """Generates the elevation map by combining plate generation and noise."""
    plates = generate_plates(map_size)
    noise_map = generate_noise_map(map_size)
    elevation_map = combine_plates_and_noise(plates, noise_map)
    return elevation_map

def generate_temperature(map_size, elevation_map):
    """Generates a temperature map (warmer at the center, cooler at the edges, adjusted by elevation)."""
    temperature_map = np.zeros((map_size, map_size))
    for y in range(map_size):
        temperature_map[y, :] = 1 - abs((y - map_size // 2) / (map_size // 2))
    for i in range(map_size):
        for j in range(map_size):
            temperature_map[i, j] -= max(0, elevation_map[i, j]) * 0.3
    return np.clip(temperature_map, 0, 1)

def generate_moisture(map_size, elevation_map, temperature_map):
    """Generates a base moisture map based on temperature and elevation."""
    moisture_map = np.zeros((map_size, map_size))
    for i in range(map_size):
        for j in range(map_size):
            base_moist = temperature_map[i, j] * np.exp(-max(0, elevation_map[i, j]))
            moist_noise = noise.pnoise2(i * 0.1, j * 0.1, octaves=2) * 0.3
            moisture_map[i, j] = base_moist + moist_noise
    return np.clip(moisture_map, 0, 1)

def adjust_moisture_for_rivers(moisture_map, river_map, influence_radius=5, moisture_boost=0.1):
    """Adjusts moisture map to increase moisture near rivers."""
    map_size = moisture_map.shape[0]
    for i in range(map_size):
        for j in range(map_size):
            if river_map[i, j]:
                for di in range(-influence_radius, influence_radius + 1):
                    for dj in range(-influence_radius, influence_radius + 1):
                        ni, nj = i + di, j + dj
                        if 0 <= ni < map_size and 0 <= nj < map_size:
                            distance = np.sqrt(di**2 + dj**2)
                            if distance <= influence_radius:
                                moisture_increase = moisture_boost * (1 - distance / influence_radius)
                                moisture_map[ni, nj] += moisture_increase
    return np.clip(moisture_map, 0, 1)