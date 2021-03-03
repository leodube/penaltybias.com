import React, { Fragment } from "react";
const roundTo = require("round-to");

import HomeBlock from "./HomeBlock"
import AwayBlock from "./AwayBlock"

const Game = (props) => {
  const renderGameData = (state, timeLeft) => {
    if (
      state != "Scheduled" &&
      state != "Final" &&
      state != "Final (OT)" &&
      state != "Error"
    ) {
      return (
        <div className="row border border-top-0 justify-content-center mt-0">
          <p className="my-0 font-weight-light">Remaining: {timeLeft}</p>
        </div>
      );
    }
  };

  const getPPOdds = (team, odds) => {
    if (team == "home") {
      return roundTo((1 - odds) * 100, 2).toFixed(2);
    } else {
      return roundTo(odds * 100, 2).toFixed(2);
    }
  };

  return (
    <Fragment>
      <p className="text-center mb-0">{props.gameState}</p>
      <div className="game-block row border">
        <HomeBlock 
          logo={props.teams.home.logo}
          goals={props.teams.home.goals}
          name={props.teams.home.name}
          powerplays={props.teams.home.powerplays}
          nextPPChance={getPPOdds("home", props.penaltyOnHomeTeamOdds)}
        />
        <AwayBlock 
          logo={props.teams.away.logo}
          goals={props.teams.away.goals}
          name={props.teams.away.name}
          powerplays={props.teams.away.powerplays}
          nextPPChance={getPPOdds("away", props.penaltyOnHomeTeamOdds)}
        />
      </div>
      {renderGameData(props.gameState, props.periodRemaining)}
    </Fragment>
  );
};

export default Game;
