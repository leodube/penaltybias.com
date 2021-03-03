import React from "react";
import { Link } from "react-router-dom";
import brand from "../images/whistle.svg";

const Navbar = () => {
  return (
    <div className="row border-bottom mt-5">
      <div className="col v-center">
        <a className="brand-logo align-middle" href="/">
          <img src={brand} width="50" height="50" alt="Brand"></img>
        </a>
      </div>
      <div className="col-8">
        <h1 className="main text-center">Penalty Bias</h1>
        <h2 className="subtitle text-center">
          Predicting which NHL team will get the next powerplay opportunity.
        </h2>
      </div>
      <div className="col d-flex justify-content-end align-items-center">
        <Link to="/about" className="about-link">
          About
        </Link>
      </div>
    </div>
  );
};

export default Navbar;
