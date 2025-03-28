import random

class SatisfactionManager:
    def __init__(self, settlement):
        self.settlement = settlement

    def manage_satisfaction(self):
        """Satisfaction fluctuates due to village actions and external factors."""
        # Base satisfaction changes
        if random.random() < 0.25:  # Increased positive chance
            self.settlement.resources["satisfaction"] += 3  # Reduced positive impact
        if random.random() < 0.2:  # Increased negative chance
            self.settlement.resources["satisfaction"] -= 3  # Reduced negative impact
            
        # Population-based satisfaction adjustments
        if self.settlement.population > 200:
            self.settlement.resources["satisfaction"] -= 1  # Slight penalty for large populations
        elif self.settlement.population < 50:
            self.settlement.resources["satisfaction"] += 1  # Bonus for small, tight-knit communities
            
        # Supply-based satisfaction
        if self.settlement.resources["supply"] > 80:
            self.settlement.resources["satisfaction"] += 1  # Bonus for food surplus
        elif self.settlement.resources["supply"] < 20:
            self.settlement.resources["satisfaction"] -= 2  # Penalty for food shortage
