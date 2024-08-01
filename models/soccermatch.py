import random
from models.player import Player
from models.team import Team


class SoccerMatch:
    def __init__(self):
        self.teams = []
        self.players = []

    def remove_team(self, remove_team):
        length = len(self.teams)
        self.teams = [team for team in self.teams if team.name != remove_team]
        return length > len(self.teams)

    def add_team(self, team_name, color):
        length = len(self.teams)
        if any(team.name == team_name for team in self.teams):
            raise ValueError("Team already exists")
        new_team = Team(name=team_name, color=color)
        self.teams.append(new_team)
        return length < len(self.teams)

    def get_team(self, team_name):
        for team in self.teams:
            if team.name == team_name:
                return team

    def add_player(self, player_name, skill_level):
        if any(player.name == player_name for player in self.players):
            raise ValueError("Player already exists")
        new_player = Player(name=player_name, skill_level=skill_level)
        self.players.append(new_player)

    def remove_player(self, player_name):
        self.players = [player for player in self.players if player.name != player_name]

    def initialize_teams(self):
        if len(self.players) < len(self.teams):
            raise ValueError(f"number of players is less then the number of teams")

        for team in self.teams:
            team.players.clear()

        random.shuffle(self.players)

        num_teams = len(self.teams)

        index = 0
        for player in self.players:
            curr_team = index % num_teams
            self.teams[curr_team].add_player(player)
            index += 1

    def balance_teams(self, epsilon_threshold=0.1, max_iterations=1000):
        def find_extreme_teams(teams):
            teams_sorted = sorted(teams, key=lambda t: t.average_skill())
            return teams_sorted[0], teams_sorted[-1]

        def swap_players(team_a, player_a, team_b, player_b):
            if player_a in team_a.players and player_b in team_b.players:
                team_a.remove_player(player_a)
                team_b.remove_player(player_b)
                team_a.add_player(player_b)
                team_b.add_player(player_a)
            else:
                raise ValueError(f"Error: Player not found in respective team")

        for _ in range(max_iterations):  # Limit iterations
            min_team, max_team = find_extreme_teams(self.teams)
            if max_team.average_skill() - min_team.average_skill() <= epsilon_threshold:
                break  # Teams are balanced

            options = []  # Will hold all the tuples (better player, abs(teams difference))
            weakest_player, lowest_rating = min_team.find_weakest_player()

            iterations = 1
            while iterations * 0.5 <= 5:  # Creates all the differences possible

                epsilon = iterations * 0.5
                stronger_player, stronger_player_rating = max_team.find_similar_player(weakest_player, epsilon)
                if stronger_player is not None:  # Found stronger player in the stronger Team
                    diff = stronger_player_rating - lowest_rating  # Evaluates the impact on each team
                    # new difference between the teams total skill level
                    new_diff = ((max_team.total_skill() - diff) - (min_team.total_skill() + diff))
                    options.append((stronger_player, abs(new_diff)))

                iterations += 1

            options = sorted(options, key=lambda t: t[1])  # Sorts options by lowes difference between teams
            if options and options[0][1] < (
                    max_team.total_skill() - min_team.total_skill()):  # If an option lowers the original difference
                swap_players(min_team, weakest_player, max_team, options[0][0])
            else:
                break  # We reached the best solution

    def __str__(self):
        return ''.join(str(team) for team in self.teams)
