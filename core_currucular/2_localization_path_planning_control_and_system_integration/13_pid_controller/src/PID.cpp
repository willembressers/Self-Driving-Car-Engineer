#include "PID.h"

PID::PID() {}

PID::~PID() {}

void PID::Init(double Kp_, double Ki_, double Kd_) {
  // Initialize PID coefficients
  Kp = Kp_;
  Ki = Ki_;
  Kd = Kd_;

  // Initialize coeffiecent errors
  d_error = 0;
  i_error = 0;
  p_error = 0;
}

void PID::UpdateParams(double Kp_, double Ki_, double Kd_) {
  // Update the parameters
  Kp = Kp_;
  Ki = Ki_;
  Kd = Kd_;
}

void PID::UpdateError(double cte) {
  // Update PID errors based on cte.

  // calculate the difference between the previous and the current cross track error
  d_error = cte - p_error;

  // set the most recent cross track error
  p_error = cte;

  // update the sum of all cross track errors so far
  i_error += cte;
}

double PID::TotalError() {
  // calculate the proportional, derivative, integral
  return -Kp * p_error - Kd * d_error - Ki * i_error;
}