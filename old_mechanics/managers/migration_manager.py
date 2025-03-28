import random

class MigrationManager:
    def __init__(self, world):
        self.world = world
    
    def find_migration_target(self, village):
        """Finds suitable migration targets based on relationship and conditions."""
        candidates = []
        for other in self.world.villages:
            if other != village:
                # Get relationship status
                relationship = self.world.relationship_manager.get_relationship_status(village.id, other.id)
                
                # Calculate migration potential based on relationship and conditions
                migration_potential = 0
                
                # Base potential from relationship
                if relationship == "Allied":
                    migration_potential = 100
                elif relationship == "Friendly":
                    migration_potential = 80
                elif relationship == "Cordial":
                    migration_potential = 60
                elif relationship == "Neutral":
                    migration_potential = 40
                elif relationship == "Tense":
                    migration_potential = 20
                elif relationship == "Hostile":
                    migration_potential = 10
                elif relationship == "Enemy":
                    migration_potential = 0
                
                # Add to candidates if there's migration potential
                if migration_potential > 0:
                    # Check if target village has good conditions
                    if other.resources["supply"] > 40 and other.resources["satisfaction"] > 50:
                        migration_potential += 20
                    
                    candidates.append((other, migration_potential))
        
        if candidates:
            # Weight selection by migration potential
            total_potential = sum(potential for _, potential in candidates)
            weights = [potential/total_potential for _, potential in candidates]
            return random.choices([v for v, _ in candidates], weights=weights)[0]
        return None

    def handle_migration(self, village):
        """Handles migration from struggling villages to more prosperous ones."""
        if village.resources["satisfaction"] < 30 or village.resources["supply"] < 20:
            # Calculate migration amount based on conditions
            base_migration = random.randint(10, 25)
            if village.resources["satisfaction"] < 20:
                base_migration *= 1.5
            if village.resources["supply"] < 10:
                base_migration *= 1.5
            
            migrating_pop = min(base_migration, village.population)
            village.population -= migrating_pop
            
            # Find migration target
            target = self.find_migration_target(village)
            
            if target:
                # Successful migration
                target.population += migrating_pop
                
                # Update relationships based on successful migration
                self.world.relationship_manager.modify_relationship(
                    village, target, random.randint(5, 10), "migration_success")
                
                # Improve target village's resources slightly
                target.resources["supply"] += random.randint(5, 10)
                target.resources["satisfaction"] += random.randint(2, 5)
            else:
                # Failed migration (people leave but don't find a new home)
                self.world.relationship_manager.modify_relationship(
                    village, village, random.randint(-5, -10), "migration_failure")
            
            if village.population <= 0:
                village.collapse_reason = "Mass Migration"
            
            return migrating_pop
        return 0
