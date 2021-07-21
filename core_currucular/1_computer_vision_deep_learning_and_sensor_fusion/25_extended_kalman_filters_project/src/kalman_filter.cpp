#include "kalman_filter.h"

using Eigen::MatrixXd;
using Eigen::VectorXd;

/*
 * Please note that the Eigen library does not initialize
 *   VectorXd or MatrixXd objects with zeros upon creation.
 */

KalmanFilter::KalmanFilter() {}

KalmanFilter::~KalmanFilter() {}

//=============================================================================
// initialize the class variables
//=============================================================================

void KalmanFilter::Init(VectorXd &x_in, MatrixXd &P_in, MatrixXd &F_in,
                        MatrixXd &H_in, MatrixXd &R_in, MatrixXd &Q_in) {
  x_ = x_in;
  P_ = P_in;
  F_ = F_in;
  H_ = H_in;
  R_ = R_in;
  Q_ = Q_in;
}

//=============================================================================
// Predict the state
//=============================================================================

void KalmanFilter::Predict() {
  x_ = F_ * x_;
  MatrixXd Ft = F_.transpose();
  P_ = F_ * P_ * Ft + Q_;
}

//=============================================================================
// Update the state
//=============================================================================

void KalmanFilter::Update(const VectorXd &z) {
  VectorXd z_pred = H_ * x_;
  VectorXd y = z - z_pred;

  MatrixXd Ht = H_.transpose();
  MatrixXd S = H_ * P_ * Ht + R_;
  MatrixXd PHt = P_ * Ht;
  MatrixXd Si = S.inverse();
  MatrixXd K = PHt * Si;

  //new estimate
  x_ = x_ + (K * y);
  long x_size = x_.size();
  MatrixXd I = MatrixXd::Identity(x_size, x_size);
  P_ = (I - K * H_) * P_;
}

//=============================================================================
// Calculate Root Mean Square
//=============================================================================

void KalmanFilter::UpdateEKF(const VectorXd &z) {
  float px = x_(0);
  float py = x_(1);
  float vx = x_(2);
  float vy = x_(3);

  // convert readings from polar to cartesian
  float rho = sqrt((px * px) + (py * py));
  float phi = atan2(py, px);
  float rho_dot;

  // what if rho is zero?
  if (fabs(rho) < 0.0001) {
    rho_dot = 0.0;
  } else {
    rho_dot = (px * vx + py * vy) / rho;
  }

  VectorXd z_pred(3);
  z_pred << rho,
         phi,
         rho_dot;

  VectorXd y = z - z_pred;

  // make sure that the angle is between -pi and pi
  if (y(1) < -M_PI) {
    y(1) += 2 * M_PI;
  } else if (
    y(1) > M_PI) {
    y(1) -= 2 * M_PI;
  }

  MatrixXd Ht = H_.transpose();
  MatrixXd S = H_ * P_ * Ht + R_;
  MatrixXd PHt = P_ * Ht;
  MatrixXd Si = S.inverse();
  MatrixXd K = PHt * Si;

  //new estimate
  x_ = x_ + (K * y);
  long x_size = x_.size();
  MatrixXd I = MatrixXd::Identity(x_size, x_size);
  P_ = (I - K * H_) * P_;
}
