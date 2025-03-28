import random
import math

class RelationshipManager:
    def __init__(self, world):
        self.world = world
        self.relationships = {}  # Graph-based storage of relationships
        self.personalities = {}  # Stores AI personalities
        self.log = []  # Stores logs for debugging
        self.interaction_history = {}  # Track recent interactions between villages
        self.trade_agreements = {}  # Track active trade agreements
        self.alliances = {}  # Track military alliances
        self.wars = {}  # Track active conflicts

    def initialize_village(self, village):
        """Sets up relationship tracking for a new village."""
        self.relationships[village.id] = {}
        self.personalities[village.id] = self.assign_personality()
        self.interaction_history[village.id] = {}
        self.log_event(f"Village {village.id} initialized with personality {self.personalities[village.id]}")

    def assign_personality(self):
        """Assigns a random personality to a village with weighted traits."""
        personalities = {
            "Aggressive": {"weight": 0.2, "traits": ["warfare", "expansion"]},
            "Trade-Oriented": {"weight": 0.3, "traits": ["commerce", "diplomacy"]},
            "Isolationist": {"weight": 0.2, "traits": ["self-sufficiency", "defense"]},
            "Diplomatic": {"weight": 0.3, "traits": ["alliances", "peace"]}
        }
        return random.choices(list(personalities.keys()), 
                            weights=[p["weight"] for p in personalities.values()])[0]

    def meet_villages(self, village1, village2):
        """Handles first-time meetings between villages based on proximity."""
        if village2.id not in self.relationships[village1.id]:
            baseline = self.get_baseline_relationship(village1, village2)
            self.relationships[village1.id][village2.id] = baseline
            self.relationships[village2.id][village1.id] = baseline  # Mutual
            self.interaction_history[village1.id][village2.id] = []
            self.interaction_history[village2.id][village1.id] = []
            self.log_event(f"Villages {village1.id} and {village2.id} met. Initial relationship: {baseline}")

    def get_baseline_relationship(self, village1, village2):
        """Determines initial relationship score based on multiple factors."""
        base_relationship = random.randint(0, 30)  # Base relationship

        # Distance-based modifier (closer = better relations)
        distance = self.calculate_distance(village1.position, village2.position)
        distance_modifier = max(-20, min(20, 20 - distance * 2))
        base_relationship += distance_modifier

        # Biome similarity bonus
        if village1.biome_map[village1.position] == village2.biome_map[village2.position]:
            base_relationship += 10

        # Personality compatibility
        personality_compatibility = self.get_personality_compatibility(village1.id, village2.id)
        base_relationship += personality_compatibility

        # Resource complementarity
        resource_complement = self.get_resource_complementarity(village1, village2)
        base_relationship += resource_complement

        return max(min(base_relationship, 100), -100)

    def calculate_distance(self, pos1, pos2):
        """Calculates Manhattan distance between two positions."""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def get_personality_compatibility(self, village1_id, village2_id):
        """Determines how well two villages' personalities mesh."""
        personality_pairs = {
            ("Aggressive", "Aggressive"): -10,
            ("Aggressive", "Trade-Oriented"): -5,
            ("Aggressive", "Isolationist"): 0,
            ("Aggressive", "Diplomatic"): -15,
            ("Trade-Oriented", "Trade-Oriented"): 15,
            ("Trade-Oriented", "Isolationist"): -5,
            ("Trade-Oriented", "Diplomatic"): 10,
            ("Isolationist", "Isolationist"): 5,
            ("Isolationist", "Diplomatic"): -5,
            ("Diplomatic", "Diplomatic"): 20
        }
        pair = tuple(sorted([self.personalities[village1_id], self.personalities[village2_id]]))
        return personality_pairs.get(pair, 0)

    def get_resource_complementarity(self, village1, village2):
        """Determines how well two villages' resources complement each other."""
        # Calculate resource diversity between villages
        biome1 = village1.biome_map[village1.position].name
        biome2 = village2.biome_map[village2.position].name
        
        if biome1 != biome2:
            return 10  # Different biomes often have complementary resources
        return 0

    def update_relationships(self):
        """Updates relationships based on recent interactions and natural decay."""
        for village_id in list(self.relationships.keys()):
            for other_id in list(self.relationships[village_id].keys()):
                old_value = self.relationships[village_id][other_id]
                
                # Natural relationship decay
                if random.random() < 0.1:  # 10% chance of decay each turn
                    decay = random.randint(-2, 0)
                    self.relationships[village_id][other_id] = max(min(
                        self.relationships[village_id][other_id] + decay, 100), -100)

                # Recent interaction impact
                if village_id in self.interaction_history and other_id in self.interaction_history[village_id]:
                    recent_interactions = self.interaction_history[village_id][other_id][-5:]  # Last 5 interactions
                    for interaction in recent_interactions:
                        self.relationships[village_id][other_id] = max(min(
                            self.relationships[village_id][other_id] + interaction, 100), -100)

                # Clear old interactions
                if village_id in self.interaction_history and other_id in self.interaction_history[village_id]:
                    self.interaction_history[village_id][other_id] = self.interaction_history[village_id][other_id][-10:]

                if old_value != self.relationships[village_id][other_id]:
                    self.log_event(f"Relationship between {village_id} and {other_id} adjusted to {self.relationships[village_id][other_id]}")

    def modify_relationship(self, village1, village2, amount, interaction_type=None):
        """Modifies relationship score based on events and interactions."""
        if village2.id in self.relationships[village1.id]:
            # Base change
            change = amount

            # Personality-based modifiers
            if self.personalities[village1.id] == "Diplomatic":
                change += 2
            elif self.personalities[village1.id] == "Aggressive":
                change -= 2

            # Record interaction
            if interaction_type:
                self.record_interaction(village1.id, village2.id, change, interaction_type)

            # Apply change
            old_value = self.relationships[village1.id][village2.id]
            self.relationships[village1.id][village2.id] = max(min(old_value + change, 100), -100)
            self.relationships[village2.id][village1.id] = self.relationships[village1.id][village2.id]

            # Update alliance/war status
            self.update_diplomatic_status(village1.id, village2.id)

            self.log_event(f"Relationship between {village1.id} and {village2.id} changed from {old_value} to {self.relationships[village1.id][village2.id]}")

    def record_interaction(self, village1_id, village2_id, amount, interaction_type):
        """Records an interaction between villages."""
        if village1_id not in self.interaction_history:
            self.interaction_history[village1_id] = {}
        if village2_id not in self.interaction_history:
            self.interaction_history[village2_id] = {}
        if village2_id not in self.interaction_history[village1_id]:
            self.interaction_history[village1_id][village2_id] = []
        if village1_id not in self.interaction_history[village2_id]:
            self.interaction_history[village2_id][village1_id] = []

        self.interaction_history[village1_id][village2_id].append(amount)
        self.interaction_history[village2_id][village1_id].append(amount)

    def update_diplomatic_status(self, village1_id, village2_id):
        """Updates alliance and war status based on relationship values."""
        relationship = self.relationships[village1_id][village2_id]
        
        # Alliance formation/breaking
        if relationship >= 80 and village1_id not in self.alliances:
            self.alliances[village1_id] = village2_id
            self.log_event(f"Alliance formed between {village1_id} and {village2_id}")
        elif relationship < 60 and village1_id in self.alliances:
            del self.alliances[village1_id]
            self.log_event(f"Alliance broken between {village1_id} and {village2_id}")

        # War declaration/ceasefire
        if relationship <= -60 and village1_id not in self.wars:
            self.wars[village1_id] = village2_id
            self.log_event(f"War declared between {village1_id} and {village2_id}")
        elif relationship > -40 and village1_id in self.wars:
            del self.wars[village1_id]
            self.log_event(f"Ceasefire between {village1_id} and {village2_id}")

    def get_relationship_status(self, village1_id, village2_id):
        """Returns the current relationship status between two villages."""
        relationship = self.relationships.get(village1_id, {}).get(village2_id, 0)
        
        if village1_id in self.alliances and self.alliances[village1_id] == village2_id:
            return "Allied"
        elif village1_id in self.wars and self.wars[village1_id] == village2_id:
            return "At War"
        elif relationship >= 80:
            return "Friendly"
        elif relationship >= 60:
            return "Cordial"
        elif relationship >= 40:
            return "Neutral"
        elif relationship >= 20:
            return "Tense"
        elif relationship >= -20:
            return "Hostile"
        else:
            return "Enemy"

    def trigger_random_event(self):
        """Triggers a random relationship-based event affecting villages."""
        if len(self.world.villages) < 2:
            return  # Not enough villages for an event
        
        village1, village2 = random.sample(self.world.villages, 2)
        event_type = random.choice(["Festival", "Border Dispute", "Shared Innovation", "Trade Dispute"])
        
        if event_type == "Festival":
            self.modify_relationship(village1, village2, random.randint(10, 20))
            self.log_event(f"{village1.id} and {village2.id} held a festival together! Relationship improved.")
        elif event_type == "Border Dispute":
            self.modify_relationship(village1, village2, random.randint(-25, -15))
            self.log_event(f"{village1.id} and {village2.id} had a border dispute! Relationship worsened.")
        elif event_type == "Shared Innovation":
            self.modify_relationship(village1, village2, random.randint(5, 15))
            self.log_event(f"{village1.id} and {village2.id} collaborated on a new technology! Relationship improved.")
        elif event_type == "Trade Dispute":
            self.modify_relationship(village1, village2, random.randint(-20, -10))
            self.log_event(f"{village1.id} and {village2.id} had a trade dispute! Relationship worsened.")

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
        if len(self.log) > 1000:  # Keep log size manageable
            self.log = self.log[-1000:]

    def display_logs(self):
        """Prints logs for debugging."""
        for entry in self.log:
            print(entry)