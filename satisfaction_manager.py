import random

class SatisfactionManager:
    def __init__(self, settlement):
        self.settlement = settlement

    def manage_satisfaction(self):
        """Satisfaction fluctuates due to village actions and external factors."""
        if random.random() < 0.2:
            self.settlement.resources["satisfaction"] += 5
        if random.random() < 0.15:
            self.settlement.resources["satisfaction"] -= 5
