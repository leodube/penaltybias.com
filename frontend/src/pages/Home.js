import React, { useState, useEffect } from "react";
import { Games } from "../components";
import predictPenaltyService from "../services/predictPenaltyService";

const Home = () => {
  const [games, setGames] = useState(null);

  useEffect(() => {
    if (!games) {
      getGames();
    }
    const interval = setInterval(() => {
      getGames();
    }, 3000);
    return () => clearInterval(interval);
  });

  const getGames = async () => {
    let res = await predictPenaltyService.get();
    setGames(res);
  };

  return (
    <div className="row justify-content-center">
      <div className="col col-lg-11 games-block-wrapper">
        {games ? (
          <Games {...games} />
        ) : (
          <div className="text-center"> 
            <div className="row spinner-grow text-center" role="status">
              <span className="sr-only">Loading...</span>
            </div>
            <p className="mt-3">Loading.... This may take a moment</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Home;
