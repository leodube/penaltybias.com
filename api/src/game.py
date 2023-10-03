import requests
import json 
import math
import re

class Game():
  def __init__(self, gamepk):
    # Call NHL API
    linescore = requests.get("https://statsapi.web.nhl.com/api/v1/game/{}/linescore".format(gamepk)).json()
    boxscore = requests.get("https://statsapi.web.nhl.com/api/v1/game/{}/boxscore".format(gamepk)).json()
    home_team = requests.get("https://statsapi.web.nhl.com{}".format(boxscore["teams"]["home"]["team"]["link"])).json()
    away_team = requests.get("https://statsapi.web.nhl.com{}".format(boxscore["teams"]["away"]["team"]["link"])).json()

    # Attempt to get skater stats
    try:
      home_stats = boxscore["teams"]["home"]["teamStats"]["teamSkaterStats"]
      away_stats = boxscore["teams"]["away"]["teamStats"]["teamSkaterStats"]
    except:
      home_stats = {"goals":0, "powerPlayOpportunities":0}
      away_stats = {"goals":0, "powerPlayOpportunities":0}

    # Set game time and state variables
    self.period = linescore["currentPeriod"]
    try:
      self.period_remaining = linescore["currentPeriodTimeRemaining"]
    except:
      self.period_remaining = 20

    if self.period == 0:
      self.game_time = 0
      self.game_state = "Scheduled"
    else:
      self.game_time, self.game_state = self.set_game_time(self.period, self.period_remaining)

    try:
      currentPeriodOrdinal = linescore["currentPeriodOrdinal"]
      if currentPeriodOrdinal == "SO":
        self.game_state = "Final (SO)"
      elif currentPeriodOrdinal == "OT":
        self.game_state = "Final (OT)"
    except:
      pass

    # Team Variables
    self.home_name = home_team["teams"]["name"]
    self.home_id = home_team["teams"]["id"]
    self.home_abbr = home_team["teams"]["abbreviation"]
    self.home_svg = "https://assets.nhle.com/logos/nhl/svg/{}_light.svg".format(self.home_abbr)
    self.home_goals = home_stats["goals"]
    self.home_pps = home_stats["powerPlayOpportunities"]
    self.next_pp_odds = 0

    self.away_name = away_team["teams"]["name"]
    self.away_id = away_team["teams"]["name"]
    self.away_abbr = away_team["teams"]["abbreviation"]
    self.away_svg = "https://assets.nhle.com/logos/nhl/svg/{}_light.svg".format(self.away_abbr)
    self.away_goals = away_stats["goals"]
    self.away_pps = away_stats["powerPlayOpportunities"]

    # Get team abbreviations
    self.team_stats = requests.get("https://statsapi.web.nhl.com/api/v1/teams?teamId={},{}&expand=team.stats".format(self.home_id, self.away_id)).json()
    if self.team_stats["teams"][0]["id"] == self.home_id:
      self.home_abbreviation = self.team_stats["teams"][0]["teamName"]
      self.away_abbreviation = self.team_stats["teams"][1]["teamName"]
    else:
      self.home_abbreviation = self.team_stats["teams"][1]["teamName"]
      self.away_abbreviation = self.team_stats["teams"][0]["teamName"]

    # Adjust goals for SO
    if self.game_state == "Final (SO)":
      self.home_goals = linescore["teams"]["home"]["goals"]
      self.away_goals = linescore["teams"]["away"]["goals"]


  def set_game_time(self, period, period_time_remaining):
    if period_time_remaining == 'Final':
      if period == '4':
        return 65, 'Final (OT)'
      else:
        return 60, 'Final'

    elif period_time_remaining == 'END':
      return ((period-1)*20)+20, 'End of period {}'.format(period)

    elif not re.match(r'^[0-2][0-9]:[0-5][0-9]', period_time_remaining):
      return 20, 'Error'

    else:
      (m,s) = period_time_remaining.split(':')
      if period == 4:
        period_time = 300 - int(m)*60 + int(s)
        game_state = 'Overtime'
      else:
        period_time = 1200 - int(m)*60 + int(s)
        game_state = 'Period {}'.format(period)
      game_time = ((period-1) * 1200) + period_time

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
    B = -0.1237 + (0.4014*x1) - (0.0520*x2) - (0.0299*x4) - (0.0046*x1*x3)
    self.next_penalty_odds = round(math.exp(B) / (1+math.exp(B)), 4)
    return round(B, 4)

  # Based on regular season points.
  # If within 10 places in the standings, then teams considered even match
  def find_team_strength_param(self):
    try:
      home_pts = self.team_stats["teams"][0]["teamStats"][0]["splits"][1]["stat"]["pts"]
      away_pts = self.team_stats["teams"][1]["teamStats"][0]["splits"][1]["stat"]["pts"]
    except:
      return 0
    home_pts = int(re.sub(r"(?<=\d)(st|nd|rd|th)\b", '', home_pts))
    away_pts = int(re.sub(r"(?<=\d)(st|nd|rd|th)\b", '', away_pts))

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
        "period" : obj.period,
        "periodRemaining" : obj.period_remaining,
        "gameState" : obj.game_state,
        "gameTime" : obj.game_time,
        "teams" : {
          "away" : {
            "id" : obj.away_id,
            "name" : obj.away_name,
            "abbreviation": obj.away_abbreviation,
            "logo" : obj.away_svg,
            "goals" : obj.away_goals,
            "powerplays" : obj.away_pps,
          },
          "home" : {
            "id" : obj.home_id,
            "name" : obj.home_name,
            "abbreviation": obj.home_abbreviation,
            "logo" : obj.home_svg,
            "goals" : obj.home_goals,
            "powerplays" : obj.home_pps,
          }
        },
        "penaltyOnHomeTeamOdds" : obj.next_penalty_odds
      }
    return json.JSONEncoder.default(self, obj)