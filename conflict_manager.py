import random

RAID_TILE_TARGET_DIST = 8
PERCENT_OF_RAID  = 0.2
PERCENT_OF_SUCCESS = 0.3

class ConflictManager:
    def __init__(self, world):
        self.world = world
        self.raid_log = []
    
    def find_raid_target(self, village):
        # Goal: find candidates in proximity of the village to raid, about 8-10 tiles.
        candidates = []

        for other in self.world.villages:
            if other != village and self.calculate_distance(village.position, other.position) <= RAID_TILE_TARGET_DIST:
                if other.resources["supply"] > 50:
                    candidates.append(other)

        return random.choice(candidates) if candidates else None 

    def attempt_raid(self, village):
        if random.random() < PERCENT_OF_RAID:
            target = self.find_raid_target(village)
            if target:
                if target.position == village.position:
                    pass
                elif random.random() < PERCENT_OF_SUCCESS:
                    stolen_supply = random.randint(15, 40)
                    village.resources["supply"] += stolen_supply
                    # Reduce both supply (by how much was stolen) and security by 10:
                    target.resources["supply"] = max(0, target.resources["supply"] - stolen_supply)
                    target.resources["security"] = max(0, target.resources["security"] - 10)
                    print(f"Raid successful! {village.position} raided {target.position}, stealing {stolen_supply} supply.")
                    self.raid_log.append((village.position, target.position, True))
                else:
                    # Raid attempt does not work, and is logged as a failure.
                    lost_pop = random.randint(5, 15)
                    village.population = max(0, village.population - lost_pop)
                    print(f"Raid failed! {village.position} raided {target.position}, and were unsuccessful.")
                    self.raid_log.append((village.position, target.position, False))
    
    def calculate_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    
