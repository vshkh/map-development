import random

class RelationshipManager:
    def __init__(self, world):
        self.world = world
        self.relationships = {}  # Graph-based storage of relationships
        self.personalities = {}  # Stores AI personalities
        self.log = []  # Stores logs for debugging

    def initialize_village(self, village):
        """Sets up relationship tracking for a new village."""
        self.relationships[village.id] = {}
        self.personalities[village.id] = self.assign_personality()
        self.log_event(f"Village {village.id} initialized with personality {self.personalities[village.id]}")

    def assign_personality(self):
        """Assigns a random personality to a village."""
        personalities = ["Aggressive", "Trade-Oriented", "Isolationist", "Diplomatic"]
        return random.choice(personalities)

    def meet_villages(self, village1, village2):
        """Handles first-time meetings between villages based on proximity."""
        if village2.id not in self.relationships[village1.id]:
            baseline = self.get_baseline_relationship(village1, village2)
            self.relationships[village1.id][village2.id] = baseline
            self.relationships[village2.id][village1.id] = baseline  # Mutual
            self.log_event(f"Villages {village1.id} and {village2.id} met. Initial relationship: {baseline}")

    def get_baseline_relationship(self, village1, village2):
        """Determines initial relationship score."""
        if village1.biome_map[village1.position] == village2.biome_map[village2.position]:
            return random.randint(10, 30)  # Friendly start for shared biomes
        return random.randint(-10, 20)  # Neutral to slightly negative start

    def update_relationships(self):
        """Applies decay and modifies relationships each turn."""
        for village_id, relations in self.relationships.items():
            for other_id in list(relations.keys()):
                old_value = relations[other_id]
                relations[other_id] = max(min(relations[other_id] - 1, 100), -100)  # Decay towards neutral
                if old_value != relations[other_id]:
                    self.log_event(f"Relationship between {village_id} and {other_id} decayed to {relations[other_id]}")

    def modify_relationship(self, village1, village2, amount):
        """Modifies relationship score based on events."""
        if village2.id in self.relationships[village1.id]:
            change = amount
            if self.personalities[village1.id] == "Diplomatic":
                change += 2  # Diplomatic villages get a bonus to relationship changes
            elif self.personalities[village1.id] == "Aggressive":
                change -= 2  # Aggressive villages resist positive changes
            
            old_value = self.relationships[village1.id][village2.id]
            self.relationships[village1.id][village2.id] = max(min(old_value + change, 100), -100)
            self.relationships[village2.id][village1.id] = self.relationships[village1.id][village2.id]  # Mutual adjustment
            self.log_event(f"Relationship between {village1.id} and {village2.id} changed from {old_value} to {self.relationships[village1.id][village2.id]}")

    def check_proximity_meetings(self):
        """Checks if villages meet based on proximity."""
        for village in self.world.villages:
            for other_village in self.world.villages:
                if village.id != other_village.id and other_village.id not in self.relationships[village.id]:
                    distance = abs(village.position[0] - other_village.position[0]) + abs(village.position[1] - other_village.position[1])
                    if distance <= 10:  # Villages meet if within 10 tiles
                        self.meet_villages(village, other_village)

    def log_event(self, message):
        """Logs relationship events for debugging."""
        self.log.append(message)

    def display_logs(self):
        """Prints logs for debugging."""
        for entry in self.log:
            print(entry)