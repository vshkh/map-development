import random

class RelationshipManager:
    def __init__(self, world):
        self.world = world
        self.relationships = {}  # Stores relationships as {(village1, village2): value}

    def get_relationship(self, village1, village2):
        """Returns the relationship value between two villages, defaults to neutral (50)."""
        key = tuple(sorted([village1.position, village2.position]))
        return self.relationships.get(key, 50)

    def modify_relationship(self, village1, village2, amount):
        """Modifies the relationship between two villages by a certain amount."""
        key = tuple(sorted([village1.position, village2.position]))
        self.relationships[key] = max(0, min(100, self.get_relationship(village1, village2) + amount))

    def handle_event(self, village1, village2, event_type):
        """Updates relationships based on trade or raid events."""
        if event_type == "trade":
            self.modify_relationship(village1, village2, random.randint(5, 15))  # Trade improves relations
        elif event_type == "raid":
            self.modify_relationship(village1, village2, -random.randint(20, 40))  # Raids worsen relations
