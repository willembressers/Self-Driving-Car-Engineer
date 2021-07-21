#include <cmath>
#include <iostream>
#include <fstream>
#include "Twiddle.h"

Twiddle::Twiddle() {}

Twiddle::~Twiddle() {}

using namespace std;

void Twiddle::Init(double Kp, double Ki, double Kd, bool status) {

  // initialize the variables
  p = {Kp, Ki, Kd};
  dp = {1, 1, 1};
  n = 0;
  state = INIT;
  i = 0;
  total_err = 0.0;
  best_err = 1.0;
  sum = 0.0;
  it = 0;
  running = status;
}

void Twiddle::incrementCount(double cte) {
  // add the current error to the total error
  total_err += fabs(cte);

  // increment the count
  n++;
}

bool Twiddle::getStatus() {
  return running;
}

std::vector<double> Twiddle::updateParams(double tol) {
  // calculate the current error
  double err = total_err / n;

  // reset the count and total error
  n = 0;
  total_err = 0;

  // calulate the sum of all delta coefficients
  sum = dp[0] + dp[1] + dp[2];

  // flag for updating to the next paramter value
  bool next_p = false;
  
  // check if we're in tolerance (if not, let's twiddle)
  if (sum > tol) {
    std::cout << "Iteration " << ++it << ", best error = " << best_err << ", p = [" << p[0] << "," << p[1] << "," << p[2] << "]" << std::endl;

    // whats the current state 
    switch (state) {

      // if this is the first round 
      case INIT:

        // increment the coefficient (with the delta)
        p[i] += dp[i];

        // flag that we're in the incrementing state
        state = INCREMENT;
        break;

      case INCREMENT:

        // if the current error is better than the best error
        if (err < best_err) {

          // update the best error
          best_err = err;

          // increment the coefficient delta
          dp[i] *= 1.1;

          // let's go to the next coefficient
          next_p = true;

        // if the current error is NOT better than the best error
        } else {

          // decrease the coefficient
          p[i] -= 2 * dp[i];

          // flag that we're in the decrementing state
          state = DECREMENT;
        }
        break;

      case DECREMENT:

        // if the current error is better than the best error
        if (err < best_err) {

          // update the best error
          best_err = err;

          // increment the coefficient delta
          dp[i] *= 1.1;

        // if the current error is NOT better than the best error          
        } else {      

          // decrease the coefficient
          p[i] += dp[i];

          // decrease the coefficient delta
          dp[i] *= 0.9;
        }
        
        // flag that we're in the incrementing state
        state = INCREMENT;

        // let's go to the next coefficient
        next_p = true;
        break;

    }

    // increment the index (i) and if we hit 3 go back to 0
    if (next_p && (++i == 3)) {
      i = 0;
    }
  }

  return p;
}

void Twiddle::log() {
  // define some streams
  ofstream foutput; 
  ifstream finput;
  finput.open ("twiddle.log");
  foutput.open ("twiddle.log",ios::app); 

  // write the current coefficients to a file.
  if(finput.is_open()) {
    foutput << "Kp:" << p[0] << ", Ki:" << p[1] << ", Kd:" << p[2] << ", sum:" << sum << std::endl;
  }

  // close the streams
  finput.close();
  foutput.close(); 
}