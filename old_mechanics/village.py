from managers import *
from settlement import Settlement
import uuid

import random

class Village(Settlement):
    def __init__(self, start_x, start_y, biome_map):
        super().__init__(start_x, start_y, biome_map)
        self.id = uuid.uuid1()
        self.economy = SupplyManager(self)
        self.security = SecurityManager(self)
        self.satisfaction = SatisfactionManager(self)
        self.expansion = ExpansionManager(self)

    def update(self):
        """Advance one turn of village life."""
        self.economy.store_resources()
        self.economy.use_storage()
        self.economy.harvest_resources()
        self.security.manage_security()
        self.satisfaction.manage_satisfaction()
        self.expansion.expand()

        self.evolve_settlement()  # Ensure village evolves when conditions are met
        self.update_population()  # Ensure population changes based on supply

        if self.population <= 0:
            #print(f"{self.tier} at {self.position} has declined into ruins.")
            return False
        return True
