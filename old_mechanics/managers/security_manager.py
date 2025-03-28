import random

class SecurityManager:
    def __init__(self, settlement):
        self.settlement = settlement

    def manage_security(self):
        """Security can improve through village actions or worsen due to environment."""
        # Base security changes
        if random.random() < 0.25:  # Increased positive chance
            self.settlement.resources["security"] += 3  # Reduced positive impact
        if random.random() < 0.2:  # Increased negative chance
            self.settlement.resources["security"] -= 3  # Reduced negative impact
            
        # Population-based security adjustments
        if self.settlement.population > 300:
            self.settlement.resources["security"] -= 1  # Slight penalty for large populations
        elif self.settlement.population < 100:
            self.settlement.resources["security"] += 1  # Bonus for small, manageable populations
            
        # Territory-based security
        if len(self.settlement.controlled_tiles) > 5:
            self.settlement.resources["security"] -= 1  # Penalty for large territory
        elif len(self.settlement.controlled_tiles) < 3:
            self.settlement.resources["security"] += 1  # Bonus for concentrated territory
