# map.py
import numpy as np
from .terrain import generate_elevation, generate_temperature, generate_moisture, adjust_moisture_for_rivers
from .biomes import biome_data, Biome, determine_special_features, determine_livestock, generate_resource_map_ca
from .rivers import generate_multiple_rivers

class MapGenerator:
    def __init__(self, map_size):
        self.map_size = map_size
        self.elevation_map = None
        self.temperature_map = None
        self.moisture_map = None
        self.biome_map = None
        self.river_map = None
        self.resource_map = None

    def generate_base_maps(self):
        """Generate elevation, temperature, and initial moisture maps."""
        self.elevation_map = generate_elevation(self.map_size)
        self.temperature_map = generate_temperature(self.map_size, self.elevation_map)
        self.moisture_map = generate_moisture(self.map_size, self.elevation_map, self.temperature_map)

    def generate_biome_map(self):
        if self.elevation_map is None or self.temperature_map is None or self.moisture_map is None:
            raise ValueError("Base maps must be generated before biome map.")

        self.biome_map = np.empty((self.map_size, self.map_size), dtype=object)
        for i in range(self.map_size):
            for j in range(self.map_size):
                elev = self.elevation_map[i, j]
                moist = self.moisture_map[i, j]
                temp = self.temperature_map[i, j]

                if elev < -0.05:
                    biome_name = "Ocean"
                elif -0.2 <= elev <= 0.2 and moist > 0.4:
                    biome_name = "Coast"
                elif elev > 0.7:
                    biome_name = "Mountain"
                elif moist > 0.6 and temp > 0.6:
                    biome_name = "Rainforest"
                elif moist < 0.4 and temp > 0.5:
                    biome_name = "Desert"
                elif temp < 0.3:
                    biome_name = "Tundra"
                else:
                    biome_name = "Plains"

                biome_info = biome_data[biome_name]
                self.biome_map[i, j] = Biome(
                    name=biome_name,
                    terrain_type=biome_info["terrain"],
                    temperature=temp * 40 - 10,
                    humidity=moist,
                    fertility=np.clip(moist * (1 - abs(temp * 40 - 10) / 40), 0.1, 1.0),
                    climate_zone=biome_info["climate_zone"],
                    elevation=(elev + 1) * 1000,
                    livestock=determine_livestock(biome_name),
                    special_features=determine_special_features(biome_name),
                    supply=biome_info["supply"],
                    security=biome_info["security"],
                    satisfaction=biome_info["satisfaction"]
                )

    def generate_river_map(self, num_rivers=10, min_elev_start=0.3):
        if self.elevation_map is None or self.biome_map is None:
            raise ValueError("Elevation and biome maps must be generated before river map.")
        
        self.river_map = np.zeros((self.map_size, self.map_size), dtype=bool)
        generate_multiple_rivers(self.elevation_map, self.river_map, self.biome_map, num_rivers, min_elev_start)
        # Adjust moisture after rivers are generated
        self.moisture_map = adjust_moisture_for_rivers(self.moisture_map, self.river_map)

    def generate_resource_map(self, iterations=3):
        if self.biome_map is None:
            raise ValueError("Biome map must be generated before resource map.")
        
        self.resource_map = generate_resource_map_ca(self.biome_map, self.map_size, iterations)

    def generate_all(self, num_rivers=10, min_elev_start=0.3, resource_iterations=3):
        self.generate_base_maps()
        self.generate_biome_map()
        self.generate_river_map(num_rivers, min_elev_start)  # This now adjusts moisture
        self.generate_resource_map(resource_iterations)

    def get_elevation_map(self):
        return self.elevation_map

    def get_temperature_map(self):
        return self.temperature_map

    def get_moisture_map(self):
        return self.moisture_map

    def get_biome_map(self):
        return self.biome_map

    def get_river_map(self):
        return self.river_map

    def get_resource_map(self):
        return self.resource_map