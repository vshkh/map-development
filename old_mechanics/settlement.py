import random
import uuid

CHANCE_OF_MIGRATION = 0.2

class Settlement:

    def __init__(self, start_x, start_y, biome_map):
        # Assign a unique identifier to the settlement, which should aid with tracking:
        self.id = uuid.uuid4()
        
        # Determines state, if collapsed or active:
        self.is_active = True  # Added attribute to track if the settlement is collapsed
        self.collapse_reason = None  # Track the reason for collapse

        # Maintain track of the starting coordinate.
        self.position = (start_x, start_y)

        # Maintain track of starting tiles.
        self.controlled_tiles = {(start_x, start_y)}

        # Initial population (subject to change, need to find and develop scale).
        self.population = 50

        # Starting resources.
        self.resources = {
            "supply": 50,
            "storage": 50,
            "security": 50,
            "satisfaction": 50,
        }

        # Keep track of met civilizations, create a dictionary to keep track of existing civilizations?
        self.met_settlements = []

        # Keeping track of the biome map
        self.biome_map = biome_map
        
        # To be explored eventually...
        self.tier = "Hamlet"
    
    def evolve_settlement(self):
        """Handles settlement evolution based on population and conditions."""
        if self.tier == "Hamlet" and self.population >= 80 and len(self.controlled_tiles) >= 3 and self.resources["security"] >= 40:
            self.tier = "Village"
            print("Hamlet promoted to Village!")
        elif self.tier == "Village" and self.population >= 400 and self.resources["satisfaction"] >= 50:
            self.tier = "Town"
            print("Village promoted to Town!")
        elif self.tier == "Town" and self.population >= 800 and len(self.controlled_tiles) >= 8 and self.resources["security"] >= 70:
            self.tier = "City-State"
            print("Town promoted to City-State, and a sense of nationalism rises within the population!")
    
    def update_population(self):
        """Adjusts population growth dynamically, with diminishing returns as population increases."""
        if self.resources["supply"] <= 0:
            # Starvation impact increases with population size
            base_starvation = random.randint(5, 15)
            population_factor = (self.population / 200) ** 1.2  # Population density increases starvation impact
            starvation_loss = int(base_starvation * population_factor)
            self.population -= starvation_loss
            self.resources["satisfaction"] -= random.randint(10, 20)
            if self.population <= 0:
                self.collapse_reason = "Starvation"
        else:
            # Calculate carrying capacity based on resources and territory
            territory_factor = len(self.controlled_tiles) * 50  # Each tile can support 50 people
            resource_factor = self.resources["supply"] * 2  # Each supply point can support 2 people
            carrying_capacity = min(territory_factor, resource_factor)
            
            # Calculate growth rate with diminishing returns
            if self.population < carrying_capacity:
                # Growth rate decreases as population approaches carrying capacity
                growth_factor = (carrying_capacity - self.population) / carrying_capacity
                base_growth = random.randint(1, 3)
                growth_rate = int(base_growth * growth_factor)
                
                # Additional scaling based on population size
                population_scale = max(0.3, 1 - (self.population / 500))
                growth_rate = int(growth_rate * population_scale)
                
                if random.random() < 0.85:  # Growth chance
                    self.population += growth_rate
            else:
                # Population decline if exceeding carrying capacity
                if random.random() < 0.3:  # 30% chance of decline when over capacity
                    decline = random.randint(1, 3)
                    self.population -= decline
                    self.resources["satisfaction"] -= 1

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
                if self.population <= 0:
                    self.collapse_reason = message
                break

    def trigger_migration(self):
        """Causes population migration if conditions are bad before total collapse."""
        if self.resources["satisfaction"] < 30 or self.resources["supply"] < 20:
            migrating_pop = random.randint(10, 25)  # Increase migration numbers
            self.population = max(0, self.population - migrating_pop)
            if self.population <= 0:
                self.collapse_reason = "Mass Migration"

            # Instead of just leaving, migrants try to form a new village
            if random.random() < CHANCE_OF_MIGRATION: 
                print(f"{migrating_pop} people migrated and founded a new village!")
                return ("new_village", migrating_pop)  # Signal to World to create a new village

    def update(self):
        """Advance one turn of settlement life."""
        if not self.is_active:
            return False  # Skip updates if settlement is already collapsed

        self.update_population()
        self.trigger_disaster()
        self.trigger_migration()
        self.evolve_settlement()
        
        if self.population <= 0:
            self.is_active = False  # Mark settlement as collapsed
            print(f"Settlement {self.id} has collapsed due to {self.collapse_reason}")
            return False
        return True