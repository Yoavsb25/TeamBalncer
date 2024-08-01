class Team:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.players = []

    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player):
        if player in self.players:
            self.players.remove(player)

    def total_skill(self):
        return sum(player.get_skill_level() for player in self.players)

    def average_skill(self):
        res = self.total_skill() / len(self.players) if self.players else 0
        return round(res, 2)

    def find_by_name(self, name):
        for i, player in enumerate(self.players):
            if player.name == name:
                return i, player
        return None, None

    def find_by_skill(self, skill):
        for i, player in enumerate(self.players):
            if player.get_skill_level() == skill:
                return i, player
        return None, None

    def find_weakest_player(self):
        if not self.players:
            return None, 0
        weakest_player = min(self.players, key=lambda player: player.get_skill_level())
        return weakest_player, weakest_player.get_skill_level()

    def find_similar_player(self, player, difference):
        for similar_player in self.players:
            if (similar_player.get_skill_level() - player.get_skill_level()) == difference:
                return similar_player, similar_player.get_skill_level()
        return None, None

    def is_initialized(self):
        return self.name and self.color

    def __str__(self):
        return (f"Team {self.name} (Color: {self.color}) \nPlayers: \n{''.join(str(player) for player in self.players)}\n"
                f"average skill: {self.average_skill()}\n")
