import requests
import json 
import math
import re

class Game():
  def __init__(self, gamepk):
    linescore = requests.get("https://statsapi.web.nhl.com/api/v1/game/{}/linescore".format(gamepk)).json()
    boxscore = requests.get("https://statsapi.web.nhl.com/api/v1/game/{}/boxscore".format(gamepk)).json()
    home_stats = boxscore["teams"]["home"]["teamStats"]["teamSkaterStats"]
    away_stats = boxscore["teams"]["away"]["teamStats"]["teamSkaterStats"]

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

    self.home_team = boxscore["teams"]["home"]["team"]["name"]
    self.home_id = boxscore["teams"]["home"]["team"]["id"]
    self.home_svg = "https://www-league.nhlstatic.com/images/logos/teams-current-primary-light/{}.svg".format(self.home_id)
    self.home_goals = home_stats["goals"]
    self.home_pps = home_stats["powerPlayOpportunities"]
    self.next_pp_odds = 0

    self.away_team = boxscore["teams"]["away"]["team"]["name"]
    self.away_id = boxscore["teams"]["away"]["team"]["id"]
    self.away_svg = "https://www-league.nhlstatic.com/images/logos/teams-current-primary-light/{}.svg".format(self.away_id)
    self.away_goals = away_stats["goals"]
    self.away_pps = away_stats["powerPlayOpportunities"]


  def set_game_time(self, period, period_time_remaining):
    if period_time_remaining == 'Final':
      if period == '4':
        return 65, 'Final'
      else:
        return 60, 'Final'

    elif period_time_remaining == 'End':
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
  # x4 = team strength 
  #      values: 1/0/-1 (stronger home / even match / stronger away)
  #      relative influence: ~0.78
  # Note: x4 not implemented
  def predict_next_penalty(self):
    x1 = self.away_pps - self.home_pps
    x2 = self.away_goals - self.home_goals
    x3 = self.game_time
    B = -0.1237 + (0.4014*x1) - (0.0520*x2) - (0.0046*x1*x3)
    self.next_penalty_odds = math.exp(B) / (1+math.exp(B))
    return round(B, 4)

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
            "name" : obj.away_team,
            "logo" : obj.away_svg,
            "goals" : obj.away_goals,
            "powerplays" : obj.away_pps,
          },
          "home" : {
            "id" : obj.home_id,
            "name" : obj.home_team,
            "logo" : obj.home_svg,
            "goals" : obj.home_goals,
            "powerplays" : obj.home_pps,
          }
        },
        "penaltyOnHomeTeamOdds" : obj.next_penalty_odds
      }
    return json.JSONEncoder.default(self, obj)
