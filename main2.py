def create_player(name, xp, team):
    return {
        "name": name,
        "xp": xp,
        "team": team
    }


class Player:
    def __init__(self, name, team):
        self.name = name
        self.xp = 1500
        self.team = team

    def introduce(self):
        print(f"I am {self.name} and I play for {self.team}")


class Team:
    def __init__(self, team_name):
        self.team_name = team_name
        self.players = []

    def show_player(self):
        for player in self.players:
            player.introduce()

    def add_player(self, name):
        new_player = Player(name, self.team_name)
        self.players.append(new_player)

    def rem_player(self, name):
        for player in self.players:
            if player.name == name:
                self.players.remove(player)

    def total_Xp(self):
        return sum(player.xp for player in self.players)


eunb = Team("Team EB")
rdy = Team("Team EB")

eunb.add_player("eunbie")
eunb.add_player("rudie")
eunb.add_player("lily")
eunb.add_player("nick")


eunb.rem_player("lily")

eunb.show_player()
print(eunb.total_Xp())
