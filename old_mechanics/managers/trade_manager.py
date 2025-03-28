import random

MIN_TILES_FOR_TRADE = 8
SUPPLY_THRESH_TRADE = 60
TRADE_SUCCESS_RATE = 0.85

class TradeManager:
    def __init__(self, world):
        self.world = world
        self.trade_log = []  # Track trade events
        self.trade_agreements = {}  # Track active trade agreements

    def find_trade_partner(self, village):
        """Finds a suitable trade partner based on relationship and proximity."""
        candidates = []
        for other in self.world.villages:
            if other != village:
                distance = self.calculate_distance(village.position, other.position)
                if distance <= MIN_TILES_FOR_TRADE:
                    # Get relationship status
                    relationship = self.world.relationship_manager.get_relationship_status(village.id, other.id)
                    
                    # Calculate trade potential based on relationship
                    trade_potential = 0
                    if relationship == "Allied":
                        trade_potential = 100
                    elif relationship == "Friendly":
                        trade_potential = 80
                    elif relationship == "Cordial":
                        trade_potential = 60
                    elif relationship == "Neutral":
                        trade_potential = 40
                    elif relationship == "Tense":
                        trade_potential = 20
                    elif relationship == "Hostile":
                        trade_potential = 10
                    elif relationship == "Enemy":
                        trade_potential = 0
                    
                    # Add to candidates if there's trade potential
                    if trade_potential > 0:
                        candidates.append((other, trade_potential))
        
        if candidates:
            # Weight selection by trade potential
            total_potential = sum(potential for _, potential in candidates)
            weights = [potential/total_potential for _, potential in candidates]
            return random.choices([v for v, _ in candidates], weights=weights)[0]
        return None

    def attempt_trade(self, village):
        """Attempts to trade with another village based on relationship status."""
        partner = self.find_trade_partner(village)
        if partner:
            relationship = self.world.relationship_manager.get_relationship_status(village.id, partner.id)
            
            # Base trade success rate
            success_rate = TRADE_SUCCESS_RATE
            
            # Modify success rate based on relationship
            if relationship == "Allied":
                success_rate += 0.15
            elif relationship == "Friendly":
                success_rate += 0.1
            elif relationship == "Cordial":
                success_rate += 0.05
            elif relationship == "Tense":
                success_rate -= 0.1
            elif relationship == "Hostile":
                success_rate -= 0.2
            elif relationship == "Enemy":
                success_rate -= 0.3

            if random.random() < success_rate:
                # Calculate trade amount based on relationship
                base_amount = random.randint(15, 30)
                if relationship == "Allied":
                    base_amount *= 1.5
                elif relationship == "Friendly":
                    base_amount *= 1.2
                elif relationship == "Cordial":
                    base_amount *= 1.1
                elif relationship == "Tense":
                    base_amount *= 0.8
                elif relationship == "Hostile":
                    base_amount *= 0.6
                elif relationship == "Enemy":
                    base_amount *= 0.4

                village.resources["supply"] += base_amount
                partner.resources["supply"] -= base_amount
                self.trade_log.append((partner.position, village.position, True))

                # Update relationships based on successful trade
                self.world.relationship_manager.modify_relationship(
                    village, partner, random.randint(5, 10), "trade_success")
            else:
                # Failed trade attempt
                self.world.relationship_manager.modify_relationship(
                    village, partner, random.randint(-5, -10), "trade_failure")

    def calculate_distance(self, pos1, pos2):
        """Calculates Manhattan distance between two positions."""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
