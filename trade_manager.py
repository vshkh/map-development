import random

MIN_TILES_FOR_TRADE = 8
SUPPLY_THRESH_TRADE = 60
TRADE_SUCCESS_RATE = 0.85

class TradeManager:
    def __init__(self, world):
        self.world = world
        self.trade_log = []  # Track trade events

    def find_trade_partner(self, village):
        """Finds a nearby village within 8 tiles to trade with, regardless of supply."""
        candidates = []
        for other in self.world.villages:
            if other != village and self.calculate_distance(village.position, other.position) <= MIN_TILES_FOR_TRADE:
                candidates.append(other)
        return random.choice(candidates) if candidates else None

    def attempt_trade(self, village):
        """Attempts trade between villages without needing low supply, for testing."""
        if village.resources["supply"] < SUPPLY_THRESH_TRADE:
            partner = self.find_trade_partner(village)
            if partner:
                trade_amount = random.randint(15, 30)  # Trade larger amounts
                if random.random() < TRADE_SUCCESS_RATE:  # 85% chance trade succeeds
                    village.resources["supply"] += trade_amount
                    partner.resources["supply"] -= trade_amount
                    #print(f"Trade successful! {trade_amount} supply sent from {partner.position} to {village.position}.")
                    self.trade_log.append((partner.position, village.position, True))  # Log successful trade
                    self.world.relationship_manager.handle_event(village, partner, "trade")  # Increase relationship
                else:
                    lost_pop = random.randint(5, 15)  # Plundering event
                    village.population = max(0, village.population - lost_pop)
                    #print(f"Trade failed! Bandits attacked {village.position}, {lost_pop} people were lost.")
                    self.trade_log.append((partner.position, village.position, False))  # Log failed trade
            
    def calculate_distance(self, pos1, pos2):
        """Calculates Manhattan distance between two positions."""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
