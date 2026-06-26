class PlayerState:
    def __init__(self):
        self.health = 100
        self.gold = 0
        self.inventory = [
           {"name": "Wooden Sword", "damage": 10, "durability": 10},
           {"name": "Leather Armor", "armor": 5, "durability": 10}
        ]
        self.statuses = []

class WorldState:
    def __init__(self):
        self.current_storyline = "saga_start"
        self.location = "village"
        self.time_played = 0
