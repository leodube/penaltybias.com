import React from "react";
import Tex2SVG from "react-hook-mathjax";

const About = () => {
  return (
    <div className="row justify-content-center">
      <div className="col-11 col-md-8 mb-3">
        <h2 className="mt-3 mb-4">About penaltybias.com</h2>
        <p>
          This website is based entirely on the paper{" "}
          <a
            href="https://www.sfu.ca/~tswartz/papers/penalty.pdf"
            target="_blank"
          >
            Biased Penalty Calls in the National Hockey League
          </a>{" "}
          by <i>David Beaudoin</i>, <i>Oliver Schulte</i>, and{" "}
          <i>Tim B. Swartz</i>.
        </p>
        <p>
          The authors created a fitted logistic regression model according to
          whether the next (<Tex2SVG display="inline" latex="i" />th) penalty was called against the home team. This model
          is based on four covariates:
        </p>
        <div className="row ml-3">
          <div className="col-auto">
            <Tex2SVG display="inline" latex="x_{1i}" />
          </div>
          <div className="col-auto">
            <Tex2SVG display="inline" latex="\equiv" />
          </div>
          <div className="col">
            <p className="covariate-info">
              total road penalties minus total home penalties in the particular
              match when the <Tex2SVG display="inline" latex="i" />th penalty was called
            </p>
          </div>
        </div>
        <div className="row ml-3">
          <div className="col-auto">
            <Tex2SVG display="inline" latex="x_{2i}" />
          </div>
          <div className="col-auto">
            <Tex2SVG display="inline" latex="\equiv" />
          </div>
          <div className="col">
            <p className="covariate-info">
              total road goals minus total home goals in the particular
              match when the <Tex2SVG display="inline" latex="i" />th
              penalty was called
            </p>
          </div>
        </div>
        <div className="row ml-3">
          <div className="col-auto">
            <Tex2SVG display="inline" latex="x_{3i}" />
          </div>
          <div className="col-auto">
            <Tex2SVG display="inline" latex="\equiv" />
          </div>
          <div className="col">
            <p className="covariate-info">
              the time in the match when the <Tex2SVG display="inline" latex="i \textrm{}" />th penalty was called; <Tex2SVG display="inline" latex="x_{3i}" /> ranges from the <Tex2SVG display="inline" latex="0" />th minute to the <Tex2SVG display="inline" latex="65" />th minute which is the end of overtime
            </p>
          </div>
        </div>
        <div className="row ml-3">
          <div className="col-auto">
            <Tex2SVG display="inline" latex="x_{4i}" />
          </div>
          <div className="col-auto">
            <Tex2SVG display="inline" latex="\equiv" />
          </div>
          <div className="col">
            <p className="covariate-info">
              team strength parameter wheree values 1/0/-1 correspond to the strongeer home team, evenly matched teams and a stronger road team baseed on regular season points
            </p>
          </div>
        </div>
        <p>
          Using these covariates the fitted logistic regression model can be solved for the predictive value. This predictive value is used to find the <i>chance of getting the next powerplay</i> for a given team. 
        </p>
        <p>All things being equal, penalties are called on the road team in a 11:10 ratio.<a href="https://www.sfu.ca/~tswartz/papers/goalie.pdf" target="_blank">[1]</a></p>
        <br />
        <p className="mb-5">
          Code for this project can be found on{" "}
          <a href="https://github.com/leodube/penalty-bias" target="_blank">
            Github.
          </a>
        </p>
      </div>
    </div>
  );
};

export default About;
