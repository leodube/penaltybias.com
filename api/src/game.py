import requests
import json
import math
import re


class Game:
    def __init__(self, gamepk):
        # Call NHL API
        boxscore = requests.get(
            "https://api-web.nhle.com/v1/gamecenter/{}/boxscore".format(gamepk)
        ).json()
        linescore = boxscore.get("summary", {}).get("linescore", {})
        team_game_stats = boxscore.get("summary", {}).get("teamGameStats", [])

        # Set game time and state variables
        if boxscore["gameState"] == "FUT":
            self.period = 0
            self.period_remaining = "20:00"
            self.game_time = 0
            self.game_state = "Scheduled"
        else:
            self.period = boxscore["periodDescriptor"]["number"]
            self.period_remaining = boxscore["clock"]["timeRemaining"]
            self.game_time, self.game_state = self.set_game_time(
                self.period, self.period_remaining
            )

            # TODO: confirm still works with new NHL api
            currentPeriodOrdinal = boxscore["periodDescriptor"]["periodType"]
            if currentPeriodOrdinal == "SO":
                self.game_state = "Final (SO)"
            elif currentPeriodOrdinal == "OT":
                self.game_state = "Final (OT)"

        # Get specific game stat
        power_play = next(
            (stat for stat in team_game_stats if stat.category == "powerPlay"), {}
        )

        # Team Variables
        home_team = boxscore["homeTeam"]
        self.home_name = (
            home_team["placeName"]["default"] + " " + home_team["name"]["default"]
        )
        self.home_id = home_team["id"]
        self.home_abbr = home_team["abbrev"]
        self.home_svg = home_team["logo"]
        self.home_goals = home_team.get("score", 0)
        self.home_pps = int(power_play.get("homeValue", "0/0").split("/")[1])
        self.next_pp_odds = 0

        away_team = boxscore["awayTeam"]
        self.away_name = (
            away_team["placeName"]["default"] + " " + away_team["name"]["default"]
        )
        self.away_id = away_team["id"]
        self.away_abbr = away_team["abbrev"]
        self.away_svg = away_team["logo"]
        self.away_goals = away_team.get("score", 0)
        self.away_pps = int(power_play.get("awayValue", "0/0").split("/")[1])

        # Adjust goals for SO
        # TODO: confirm if this is needed
        # if self.game_state == "Final (SO)":
        #   self.home_goals = linescore["totals"]["home"]
        #   self.away_goals = linescore["totals"]["away"]

    # TODO: confirm still works with new NHL api
    def set_game_time(self, period, period_time_remaining):
        if period_time_remaining == "Final":
            if period == "4":
                return 65, "Final (OT)"
            else:
                return 60, "Final"

        elif period_time_remaining == "END":
            return ((period - 1) * 20) + 20, "End of period {}".format(period)

        elif not re.match(r"^[0-2][0-9]:[0-5][0-9]", period_time_remaining):
            return 20, "Error"

        else:
            (m, s) = period_time_remaining.split(":")
            if period == 4:
                period_time = 300 - int(m) * 60 + int(s)
                game_state = "Overtime"
            else:
                period_time = 1200 - int(m) * 60 + int(s)
                game_state = "Period {}".format(period)
            game_time = ((period - 1) * 1200) + period_time

        return (game_time / 60), game_state

    # From "Biased Penalty Calls in the National Hockey League"
    # By: David Beaudoin, Oliver Schulte and Tim B. Swartz
    # Covariates:
    # x1 = (road penalties) - (home penalties)
    #      relative influence: ~79.18
    # x2 = (road goals) - (home goals)
    #      relative influence: ~11.11
    # x3 = time in match (0-65)
    #      relative influence: ~8.98
    # x4 = team strength  parameter
    #      values: 1/0/-1 (stronger home / even match / stronger away)
    #      relative influence: ~0.78
    def predict_next_penalty(self):
        x1 = self.home_pps - self.away_pps
        x2 = self.away_goals - self.home_goals
        x3 = self.game_time
        x4 = self.find_team_strength_param()
        B = -0.1237 + (0.4014 * x1) - (0.0520 * x2) - (0.0299 * x4) - (0.0046 * x1 * x3)
        self.next_penalty_odds = round(math.exp(B) / (1 + math.exp(B)), 4)
        return round(B, 4)

    # Based on regular season points.
    # If within 10 places in the standings, then teams considered even match
    def find_team_strength_param(self):
        standings = requests.get("https://api-web.nhle.com/v1/standings/now").json().get("standings", {})
        home_pts = next(
            (
                stg
                for stg in standings
                if stg["teamAbbrev"]["default"] == self.home_abbr
            ),
            {},
        ).get("points", 0)
        home_pts
        away_pts = next(
            (
                stg
                for stg in standings
                if stg["teamAbbrev"]["default"] == self.away_abbr
            ),
            {},
        ).get("points", 0)

        pts_diff = home_pts - away_pts
        if abs(pts_diff) <= 5:
            x4 = 0
        elif pts_diff < 0:
            x4 = -1
        else:
            x4 = 1
        return x4


class GameEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Game):
            return {
                "period": obj.period,
                "periodRemaining": obj.period_remaining,
                "gameState": obj.game_state,
                "gameTime": obj.game_time,
                "teams": {
                    "away": {
                        "id": obj.away_id,
                        "name": obj.away_name,
                        "abbreviation": obj.away_abbr,
                        "logo": obj.away_svg,
                        "goals": obj.away_goals,
                        "powerplays": obj.away_pps,
                    },
                    "home": {
                        "id": obj.home_id,
                        "name": obj.home_name,
                        "abbreviation": obj.home_abbr,
                        "logo": obj.home_svg,
                        "goals": obj.home_goals,
                        "powerplays": obj.home_pps,
                    },
                },
                "penaltyOnHomeTeamOdds": obj.next_penalty_odds,
            }
        return json.JSONEncoder.default(self, obj)
