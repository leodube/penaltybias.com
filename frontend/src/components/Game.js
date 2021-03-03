import React, { Fragment } from "react";
const roundTo = require('round-to');

const Game = (props) => {
  const renderGameData = (state, timeLeft) => {
    if (
      state == "Overtime" ||
      state == "Period 1" ||
      state == "Period 2" ||
      state == "Period 3"
    ) {
      return (
        <div className="row border border-top-0 justify-content-center mt-0">
          <p className="my-0 font-weight-light">
            Remaining: {timeLeft}
          </p>
        </div>
      );
    }
  };

  const getPPOdds = (team, odds) => {
    if (team == 'home'){
      return roundTo((1 - odds) * 100, 2)
    } else {
      return roundTo(odds * 100, 2)
    }
  }

  return (
    <Fragment>
      <p className="text-center mb-0">{props.gameState}</p>
      <div className="game-block row border">
        <div className="home-block col py-2 border-right">
          <div className="row">
            <div className="home-logo col-4 p-0 m-auto">
              <img
                className="img-fluid mr-auto"
                src={props.teams.home.logo}
                alt=""
              />
            </div>
            <div className="home-goals col-md-auto px-0 v-center">
              <h4 className="goals m-auto">{props.teams.home.goals}</h4>
            </div>
            <div className="home-details col my-auto ml-3">
              <h3 className="team-name text-right mt-2">
                {props.teams.home.name}
              </h3>
              <p className="powerplays font-weight-light text-right mb-0">
                Powerplay opportunities: {props.teams.home.powerplays}
              </p>
              <p className="chance-of-pp font-weight-light text-right mb-2">
                Chance of getting next powerplay:
              </p>
              <h4 className="powerplay-odds text-right">{getPPOdds('home', props.penaltyOnHomeTeamOdds)}%</h4>
            </div>
          </div>
        </div>
        <div className="away-block col py-2">
          <div className="row">
            <div className="away-logo col-4 order-md-3 p-0 m-auto">
              <img
                className="img-fluid ml-auto"
                src={props.teams.away.logo}
                alt=""
              />
            </div>
            <div className="away-goals col-md-auto order-md-2 px-0 v-center">
              <h4 className="goals m-auto">{props.teams.away.goals}</h4>
            </div>
            <div className="away-details col order-md-1 my-auto mr-3">
              <h3 className="team-name text-left mt-2">
                {props.teams.away.name}
              </h3>
              <p className="powerplays font-weight-light text-left mb-0">
                Powerplay opportunities: {props.teams.away.powerplays}
              </p>
              <p className="chance-of-pp font-weight-light text-left mb-2">
                Chance of getting next powerplay:
              </p>
              <h4 className="powerplay-odds text-left">{getPPOdds('away', props.penaltyOnHomeTeamOdds)}%</h4>
            </div>
          </div>
        </div>
      </div>
      {renderGameData(props.gameState, props.periodRemaining)}
    </Fragment>
  );
};

export default Game;
