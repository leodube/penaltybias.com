import React, { Fragment } from "react";

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
          <p className="my-0 font-weight-light">{state} - Remaining: {timeLeft}</p>
        </div>
      );
    }
  };

  return (
    <Fragment>
      <p className="text-center mb-0">{props.gameState}</p>
      <div className="row game-block border">
        <div className="col home-block py-2 border-right">
          <div className="row">
            <div className="col-4 home-logo p-0">
              <img
                className="img-fluid mr-auto"
                src={props.teams.home.logo}
                alt=""
              />
            </div>
            <div className="col-md-auto home-goals px-0 v-center">
              <h4 className="goals">{props.teams.home.goals}</h4>
            </div>
            <div className="col home-details">
              <h3 className="text-center team-name mt-2 ml-1">
                {props.teams.home.name}
              </h3>
            </div>
          </div>
        </div>
        <div className="col away-block py-2">
          <div className="row">
            <div className="col-4 order-md-3 away-logo p-0">
              <img
                className="img-fluid ml-auto"
                src={props.teams.away.logo}
                alt=""
              />
            </div>
            <div className="col-md-auto order-md-2 away-goals px-0 v-center">
              <h4 className="goals">{props.teams.home.goals}</h4>
            </div>
            <div className="col order-md-1 away-details">
              <h3 className="text-center team-name mt-2 mr-1">
                {props.teams.away.name}
              </h3>
            </div>
          </div>
        </div>
      </div>
      {renderGameData(props.gameState, props.periodRemaining)}
    </Fragment>
  );
};

export default Game;
