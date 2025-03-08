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
        target = self.find_raid_target(village)
        if target:
            if random.random() < PERCENT_OF_SUCCESS:
                stolen_supply = random.randint(15, 40)
                village.resources["supply"] += stolen_supply
                target.resources["supply"] -= stolen_supply
                target.resources["security"] -= 10
                self.raid_log.append((village.position, target.position, True))

    def calculate_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    
