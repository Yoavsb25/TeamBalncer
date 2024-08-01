class Player:
    def __init__(self, name, skill_level):
        self.name = name
        self.skill_level = skill_level

    def __str__(self):
        return f"{self.name}(Skill: {self.skill_level})\n"

    def get_name(self):
        return self.name

    def get_skill_level(self):
        return self.skill_level
