import React, { useState, useEffect } from "react";
import { Games } from "../components";
import predictPenaltyService from "../services/predictPenaltyService";

const Home = () => {
  const [games, setGames] = useState(null);

  useEffect(() => {
    if (!games) {
      getGames();
    }
  });

  const getGames = async () => {
    let res = await predictPenaltyService.get();
    setGames(res);
  };

  return (
    <div className="row justify-content-center">
      <div className="col col-lg-11 games-block-wrapper">
        {console.log(JSON.stringify(games, null, 4))}
        {games ? <Games {...games} /> : <p>loading</p>}
      </div>
    </div>
  );
};

export default Home;
