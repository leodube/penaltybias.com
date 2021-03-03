import React from "react";

const About = () => {
  return (
    <div className="row justify-content-center">
      <div className="col-11 col-md-8 mb-3">
        <h2 className="mt-3 mb-4">About penaltybias.com</h2>
        <p>
          This website is based solely off the work done by David Beaudoin,
          Oliverr Schulte, and Tim B. Swartz. The equation used to make the
          prediction comes from{" "}
          <a
            href="https://www.sfu.ca/~tswartz/papers/penalty.pdf"
            target="_blank"
          >
            their paper on biased penalty calls in the National Hockey League.
          </a>
        </p>
        <p>
          Code for this project can be found on{" "}
          <a href="https://github.com/leodube/penalty-bias" target="_blank">
            my Github.
          </a>
        </p>
      </div>
    </div>
  );
};

export default About;
