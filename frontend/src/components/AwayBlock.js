import React from "react";

const AwayBlock = (props) => {
  return (
    <div className="away-block col py-2">
      <div className="row h-100">
        {/* <p></p> */}
        <div className="logo col-12 col-md-5 order-md-3 p-0 m-auto">
          <div className="row h-100 pr-3">
            <div className="col order-lg-2 py-2">
              <img className="img-fluid ml-auto" src={props.logo} alt="" />
            </div>
            <div className="col-lg-auto order-lg-1 ml-lg-2 px-0 v-center">
              <h4 className="goals m-auto">{props.goals}</h4>
            </div>
          </div>
        </div>
        {/* <p></p> */}
        <div className="details col order-md-1 mr-3">
          <div className="d-flex flex-column h-100">
            <h3 className="team-name text-center text-md-left mt-2 mb-auto">
              {props.name}
            </h3>
            <div className="team-details">
              <p className="powerplays font-weight-light text-center text-md-left mb-0">
                Powerplay opportunities: <strong>{props.powerplays}</strong>
              </p>
              <p className="chance-of-pp font-weight-light text-center text-md-left mb-2">
                Chance of getting next powerplay
              </p>
              <h4 className="powerplay-odds text-center text-md-left">
                {props.nextPPChance}%
              </h4>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AwayBlock;
