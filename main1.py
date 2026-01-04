# # Team class에 player를 삭제하는 메서드 만들기
# # Team Class에 팀의 경험치(xp)의 총합을 보여주는 메서드 만들기

# class Player:

#     def __init__(self, name, team):
#         self.name = name
#         self.xp = 1500
#         self.team = team

#     def introduce(self):
#         print(f"Hello! I'm {self.name} and I play for {self.team}")


# class Team:

#     def __init__(self, team_name):
#         self.team_name = team_name
#         self.players = []

#     def show_players(self):
#         for play in self.players:
#             play.introduce()

#     def add_player(self, name):
#         new_player = Player(name, self.team_name)
#         self.players.append(new_player)

#     def rem_player(self, name):
#         for player in self.players:
#             if player.name == name:
#                 self.players.remove(player)

#     def total_teamxp(self):
#         return sum(player.xp for player in self.players)


# team_x = Team("Team X")
# team_x.add_player("red")

# # Blue Team 인스턴스 생성
# team_blue = Team("Blue Team")
# # team_blue 인스턴스의 add_player 메서드 호출 (팀원 추가)
# team_blue.add_player("lion")
# team_blue.add_player("lily")
# # team_blue 인스턴스의 rem_player 메서드 호출 (팀원 제거)
# team_blue.rem_player("lion")

# # team_blue 인스턴스의 add_player 메서드 호출 (팀원 추가)
# team_blue.add_player("anna")
# team_blue.add_player("inn")
# # team_blue 인스턴스의 show_players 메서드 호출 (팀원 출력)
# team_blue.show_players()

# # team_blue 인스턴스의 total_teamxp 메서드 호출 (팀원 xp총합 출력)
# print(team_blue.total_teamxp())

"""
==============================
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
"""

# 유저의 입력을 활용하는 계산기 만들기
"""
Choose a number:
15
Choose another one:
15
Choose an operation:
    Oprions are: +, -, * or /.
    Write 'exit' to finish.
+
Result: 30
Choose a number:
"""


# import requests
# from bs4 import BeautifulSoup

# url = "https://weworkremotely.com/categories/remote-full-stack-programming-jobs"

# response = requests.get(url)

# soup = BeautifulSoup(
#     response.content,
#     "html.parser",
# )

# jobs = soup.find("section", class_="jobs").find_all("li")[:-1]

# for job in jobs:
#     # title = job.find("p", class_="new-listing__company-name").text
#     position = job.find("h3", class_="new-listing__header__title").text
#     # region = job.find("p", class_="new-listing__company-headquarters").text


# print(position, "========")

"""
# from extractors.indeed import extract_indeed_jobs
# from extractors.wwr import extract_wwr_jobs

# keyword = input("What do you want to search for?")

# indeed = extract_indeed_jobs(keyword)
# wwr = extract_wwr_jobs(keyword)
# jobs = indeed + wwr

# file = open(f"{keyword}.csv", "w")
# file.write("Position, Company, Location, URL\n")

# for job in jobs:
#     file.write(
#         f"{job['position']}, {job['company']}, {job['link']}\n"
#     )

# file.close()
"""
"""
from extractors.wanted import extract_wandted_jobs
from file import save_to_file

keyward = input("What do you want to search for?")

jobs = extract_wandted_jobs(keyward)

save_to_file(keyward, jobs)
"""
from extractors.wanted import extract_wanted_jobs
from export import save_to_file
from flask import Flask, render_template, request, redirect, send_file

app = Flask("JobScrapper")

db = {
}


@app.route("/")
def home():
    return render_template("home.html", name="eb")


@app.route("/search")
def hello():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/")
    if keyword in db:
        jobs = db[keyword]
    else:
        wanted = extract_wanted_jobs(keyword)
        jobs = wanted
        db[keyword] = jobs
    return render_template("search.html", keyword=keyword, jobs=jobs)


@app.route("/export")
def export():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/")
    if keyword not in db:
        return redirect(f"/search?keyword={keyword}")
    save_to_file(keyword, db[keyword])
    return send_file(f"{keyword}.csv", as_attachment=True)


app.run(debug=True)
