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
        partner = self.find_trade_partner(village)
        if partner:
                if random.random() < TRADE_SUCCESS_RATE:
                    trade_amount = random.randint(15, 30)
                    village.resources["supply"] += trade_amount
                    partner.resources["supply"] -= trade_amount
                    self.trade_log.append((partner.position, village.position, True))
                    # Improve relationship
        
    def calculate_distance(self, pos1, pos2):
        """Calculates Manhattan distance between two positions."""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
