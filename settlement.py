import random

class Settlement:
    def __init__(self, start_x, start_y, biome_map):
        self.position = (start_x, start_y)
        self.controlled_tiles = {(start_x, start_y)}
        self.population = 50
        self.resources = {
            "supply": 50,
            "storage": 50,
            "security": 50,
            "satisfaction": 50,
        }
        self.biome_map = biome_map
        self.tier = "Hamlet"
    
    def evolve_settlement(self):
        """Handles settlement evolution based on population and conditions."""
        if self.tier == "Hamlet" and self.population >= 100 and len(self.controlled_tiles) >= 3 and self.resources["security"] >= 50:
            self.tier = "Village"
            print("Hamlet promoted to Village!")
        elif self.tier == "Village" and self.population >= 500 and self.resources["satisfaction"] >= 60:
            self.tier = "Town"
            print("Village promoted to Town!")
        elif self.tier == "Town" and self.population >= 1000 and len(self.controlled_tiles) >= 10 and self.resources["security"] >= 80:
            self.tier = "City-State"
            print("Town promoted to City-State!")
    
    def update_population(self):
        """Adjusts population growth dynamically, slowing as population increases."""
        if self.resources["supply"] <= 0:
            starvation_loss = random.randint(10, 20)  # Increase starvation impact
            self.population -= starvation_loss
            self.resources["satisfaction"] -= random.randint(15, 25)  # More unhappiness
        else:
            growth_rate = max(1, int(6 - (self.population / 150)))
            if random.random() < 0.9:
                self.population += random.randint(1, growth_rate)
                
    def trigger_disaster(self):
        """Random disasters that impact population, supply, or security."""
        disaster_chance = random.random()
        disasters = [
            (0.15, "Famine! Supply reduced", "supply", -max(30, int(self.resources["supply"] * 0.3))),  # Scales with supply
            (0.08, "Plague! Population -15%", "population", -int(self.population * 0.15)),  # Increase impact
            (0.10, "Raiders attack! Security -20", "security", -20),  # Increase chance
            (0.12, "Fire! Storage -30", "storage", -30)  # Increase impact
        ]
        
        for chance, message, resource, impact in disasters:
            if disaster_chance < chance:
                if resource == "population":
                    self.population = max(0, self.population + impact)
                else:
                    self.resources[resource] = max(0, self.resources[resource] + impact)
                print(f"Disaster: {message}")
                break

    def trigger_migration(self):
        """Causes population migration if conditions are bad before total collapse."""
        if self.resources["satisfaction"] < 30 or self.resources["supply"] < 20:
            migrating_pop = random.randint(10, 25)  # Increase migration numbers
            self.population = max(0, self.population - migrating_pop)

            # Instead of just leaving, migrants try to form a new village
            if random.random() < 0.2:  # 20% chance of forming a new village
                print(f"{migrating_pop} people migrated and founded a new village!")
                return ("new_village", migrating_pop)  # Signal to World to create a new village

    def update(self):
        """Advance one turn of settlement life."""
        self.update_population()
        self.trigger_disaster()
        self.trigger_migration()
        self.evolve_settlement()
        
        if self.population <= 0:
            #print(f"{self.tier} at {self.position} has declined into ruins.")
            return False
        return True
