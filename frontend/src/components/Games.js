import React from "react";
import Game from "./Game";

const Games = (props) => {
  return (
    <div className="games-block">
      {props.games.map((game, index) => (
        <div key={index} className="game-block-wrapper mb-5">
          <Game {...game} />
        </div>
      ))}
    </div>
  );
};

export default Games;
