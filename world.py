import random
from village import Village
from managers import *
from visualization import plot_world_map, plot_migration_events

class World:
    def __init__(self, map_size, biome_map, num_villages=5):
        self.map_size = map_size
        self.biome_map = biome_map
        self.villages = []
        self.migration_manager = MigrationManager(self)
        self.trade_manager = TradeManager(self)
        self.conflict_manager = ConflictManager(self)
        self.relationship_manager = RelationshipManager(self)  # Added RelationshipManager
        self.num_villages = num_villages
        self.migration_log = []  # Track migration events
        self.collapsed_villages = []  # Track collapsed village locations
        self.spawn_villages()
        
    def find_valid_village_start(self):
        """Finds a valid (non-ocean) starting position for a village."""
        while True:
            x, y = random.randint(0, self.map_size - 1), random.randint(0, self.map_size - 1)
            if self.biome_map[x, y].name != "Ocean":
                return x, y
    
    def create_village(self, position):
        """Creates a new village at a specified position and registers it."""
        new_village = Village(position[0], position[1], self.biome_map)
        self.villages.append(new_village)
        self.relationship_manager.initialize_village(new_village)  # Register village
        return new_village
    
    def spawn_villages(self):
        """Creates initial villages at random valid locations."""
        for _ in range(self.num_villages):
            x, y = self.find_valid_village_start()
            new_village = self.create_village((x, y))
            print(f"Spawned {new_village.tier} at ({x}, {y}).")

    def update(self, turn):
        """Updates all villages each turn, handles migration, trade, relationships, and removes collapsed villages."""
        total_migrants = 0
        self.relationship_manager.check_proximity_meetings()  # Check relationships each turn

        for village in self.villages[:]:  # Copy list to avoid modification issues
            migrants = self.migration_manager.handle_migration(village)
            if migrants:
                total_migrants += migrants
            if not village.update():
                self.collapsed_villages.append(village.position)  # Track collapsed villages
                self.villages.remove(village)
                print("A village has collapsed!")
        
        self.migration_log.append((turn, total_migrants))  # Log migration events
        self.relationship_manager.update_relationships()  # Apply relationship decay
    
    def visualize_world(self):
        """Displays the world map, migration, and trade trends."""
        plot_world_map(self.map_size, self.biome_map, self.villages, self.trade_manager.trade_log, self.collapsed_villages)
        plot_migration_events(self.migration_log)

    def display_relationship_logs(self):
        """Displays relationship logs for debugging."""
        self.relationship_manager.display_logs()
