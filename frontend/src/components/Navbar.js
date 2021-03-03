import React from "react";
import { Link } from "react-router-dom";
import brand from "../images/whistle.svg";

const Navbar = () => {
  return (
    <div className="row border-bottom mt-5">
      <div className="col-12 col-sm-8 order-sm-2">
        <h1 className="main-wrapper text-center"><a className="main" href="/">Penalty Bias</a></h1>
        <h2 className="subtitle text-center">
          Predicting which NHL team will get the next powerplay opportunity.
        </h2>
      </div>
      <div className="col v-center order-sm-1 py-2 pl-3 p-sm-0">
        <a className="brand-logo align-middle" href="/">
          <img src={brand} width="50" height="50" alt="Brand"></img>
        </a>
      </div>
      <div className="col d-flex justify-content-end align-items-center order-sm-3 py-2 pr-3 p-sm-0">
        <Link to="/about" className="about-link">
          About
        </Link>
      </div>
    </div>
  );
};

export default Navbar;
