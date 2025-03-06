import random

class MigrationManager:
    def __init__(self, world):
        self.world = world
    
    def handle_migration(self, village):
        """Handles migration from struggling villages to either reinforce existing ones or form new settlements."""
        if village.resources["satisfaction"] < 30 or village.resources["supply"] < 20:
            migrating_pop = random.randint(10, 25)  # Increased migration numbers
            village.population = max(0, village.population - migrating_pop)
            
            # 70% chance migrants reinforce another village, 30% chance they form a new one
            if random.random() < 0.7 and len(self.world.villages) > 1:
                receiving_village = random.choice([v for v in self.world.villages if v != village])
                receiving_village.population += migrating_pop
                #print(f"{migrating_pop} people migrated from {village.position} to {receiving_village.position}.")
            else:
                new_village_position = self.world.find_valid_village_start()
                new_village = self.world.create_village(new_village_position)
                new_village.population = migrating_pop
                #print(f"{migrating_pop} people migrated and founded a new village at {new_village_position}.")
            
            return migrating_pop  # Return the number of migrants for logging
        return 0