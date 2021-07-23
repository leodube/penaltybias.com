import React from "react";
import Game from "./Game";

const Games = (props) => {
  return (
    <div className="games-block">
      {props.games.length > 0 ? (
        props.games.map((game, index) => (
          <div key={index} className="game-block-wrapper mb-5">
            <Game {...game} />
          </div>
        ))
      ) : (
        <div className="text-center">
          <p className="mt-3">No games today</p>
        </div>
      )}
    </div>
  );
};

export default Games;
