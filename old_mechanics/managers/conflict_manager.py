import random

RAID_TILE_TARGET_DIST = 8
PERCENT_OF_RAID = 0.2
PERCENT_OF_SUCCESS = 0.3

class ConflictManager:
    def __init__(self, world):
        self.world = world
        self.raid_log = []
    
    def find_raid_target(self, village):
        """Finds suitable raid targets based on relationship and proximity."""
        candidates = []
        for other in self.world.villages:
            if other != village:
                distance = self.calculate_distance(village.position, other.position)
                if distance <= RAID_TILE_TARGET_DIST and other.resources["supply"] > 50:
                    # Get relationship status
                    relationship = self.world.relationship_manager.get_relationship_status(village.id, other.id)
                    
                    # Calculate raid potential based on relationship
                    raid_potential = 0
                    if relationship == "Enemy":
                        raid_potential = 100
                    elif relationship == "Hostile":
                        raid_potential = 80
                    elif relationship == "Tense":
                        raid_potential = 60
                    elif relationship == "Neutral":
                        raid_potential = 40
                    elif relationship == "Cordial":
                        raid_potential = 20
                    elif relationship == "Friendly":
                        raid_potential = 10
                    elif relationship == "Allied":
                        raid_potential = 0
                    
                    # Add to candidates if there's raid potential
                    if raid_potential > 0:
                        candidates.append((other, raid_potential))
        
        if candidates:
            # Weight selection by raid potential
            total_potential = sum(potential for _, potential in candidates)
            weights = [potential/total_potential for _, potential in candidates]
            return random.choices([v for v, _ in candidates], weights=weights)[0]
        return None

    def attempt_raid(self, village):
        """Attempts to raid another village based on relationship status."""
        target = self.find_raid_target(village)
        if target:
            relationship = self.world.relationship_manager.get_relationship_status(village.id, target.id)
            
            # Base raid success rate
            success_rate = PERCENT_OF_SUCCESS
            
            # Modify success rate based on relationship
            if relationship == "Enemy":
                success_rate += 0.2
            elif relationship == "Hostile":
                success_rate += 0.1
            elif relationship == "Tense":
                success_rate += 0.05
            elif relationship == "Neutral":
                success_rate -= 0.05
            elif relationship == "Cordial":
                success_rate -= 0.1
            elif relationship == "Friendly":
                success_rate -= 0.2

            if random.random() < success_rate:
                # Calculate raid amount based on relationship
                base_amount = random.randint(15, 40)
                if relationship == "Enemy":
                    base_amount *= 1.5
                elif relationship == "Hostile":
                    base_amount *= 1.2
                elif relationship == "Tense":
                    base_amount *= 1.1
                elif relationship == "Neutral":
                    base_amount *= 0.8
                elif relationship == "Cordial":
                    base_amount *= 0.6
                elif relationship == "Friendly":
                    base_amount *= 0.4

                village.resources["supply"] += base_amount
                target.resources["supply"] -= base_amount
                target.resources["security"] -= 10
                self.raid_log.append((village.position, target.position, True))
                
                # Update relationships based on successful raid
                self.world.relationship_manager.modify_relationship(
                    village, target, random.randint(-20, -30), "raid_success")
            else:
                # Failed raid attempt
                self.world.relationship_manager.modify_relationship(
                    village, target, random.randint(-10, -15), "raid_failure")

    def calculate_distance(self, pos1, pos2):
        """Calculates Manhattan distance between two positions."""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
