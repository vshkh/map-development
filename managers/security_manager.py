import random

class SecurityManager:
    def __init__(self, settlement):
        self.settlement = settlement

    def manage_security(self):
        """Security can improve through village actions or worsen due to environment."""
        if random.random() < 0.2:
            self.settlement.resources["security"] += 5
        if random.random() < 0.15:
            self.settlement.resources["security"] -= 5
