import requests
import json
import sys


class Schedule:
    def __init__(self):
        r = requests.get("https://api-web.nhle.com/v1/schedule/now").json()
        self.totalGames = r["gameWeek"][0]["numberOfGames"]
        if self.totalGames == 0:
            self.games = 0
        else:
            self.games = r["gameWeek"][0]["games"]
            self.date = r["gameWeek"][0]["date"]
            self.gamepks = self.set_gamepks()

    def set_gamepks(self):
        gamepks = []
        for g in self.games:
            gamepks.append(g["id"])
        return gamepks
