import React from "react";

const HomeBlock = (props) => {
  return (
    <div className="home-block col py-2 border-right">
      <div className="row h-100">
        {/* <p></p> */}
        <div className="logo col-12 col-md-5 p-0 m-auto">
          <div className="row h-100 pl-3">
            <div className="col py-2">
              <img className="img-fluid mr-auto" src={props.logo} alt="" />
            </div>
            <div className="col-lg-auto px-0 mr-lg-2 v-center">
              <h4 className="goals m-auto">{props.goals}</h4>
            </div>
          </div>
        </div>
        {/* <p></p> */}
        <div className="details col ml-3">
          <div className="d-flex flex-column h-100">
            <h3 className="team-name text-center text-md-right mt-2 mb-auto">
              {props.name}
            </h3>
            <div className="team-details">
              <p className="powerplays font-weight-light text-center text-md-right mb-0">
                Powerplay opportunities: <strong>{props.powerplays}</strong>
              </p>
              <p className="chance-of-pp font-weight-light text-center text-md-right mb-2">
                Chance of getting next powerplay
              </p>
              <h4 className="powerplay-odds text-center text-md-right">
                {props.nextPPChance}%
              </h4>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomeBlock;
