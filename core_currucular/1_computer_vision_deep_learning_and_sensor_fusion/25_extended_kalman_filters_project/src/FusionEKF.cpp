#include "FusionEKF.h"
#include <iostream>
#include "Eigen/Dense"
#include "tools.h"

using Eigen::MatrixXd;
using Eigen::VectorXd;
using std::cout;
using std::endl;
using std::vector;

//=============================================================================
// Constructor
//=============================================================================

FusionEKF::FusionEKF() {
  is_initialized_ = false;
  previous_timestamp_ = 0;

  // initializing matrices
  R_laser_ = MatrixXd(2, 2);
  R_radar_ = MatrixXd(3, 3);
  H_laser_ = MatrixXd(2, 4);
  Hj_ = MatrixXd(3, 4);
  ekf_.F_ = MatrixXd(4, 4);
  ekf_.P_ = MatrixXd(4, 4);
  ekf_.Q_ = MatrixXd(4, 4);

  // measurement covariance matrix - laser
  R_laser_ << 0.0225, 0,
           0, 0.0225;

  // measurement covariance matrix - radar
  R_radar_ << 0.09, 0, 0,
           0, 0.0009, 0,
           0, 0, 0.09;

  // measurement matrix H - laser
  H_laser_ << 1, 0, 0, 0,
           0, 1, 0, 0;

  // Jacobian Matrix
  Hj_ << 1, 1, 0, 0,
      1, 1, 0, 0,
      1, 1, 1, 1;

  // state transition matrix
  ekf_.F_ << 1, 0, 1, 0,
          0, 1, 0, 1,
          0, 0, 1, 0,
          0, 0, 0, 1;

  // state covariance matrix
  ekf_.P_ << 1, 0, 0, 0,
          0, 1, 0, 0,
          0, 0, 1000, 0,
          0, 0, 0, 1000;
}

//=============================================================================
// Destructor.
//=============================================================================

FusionEKF::~FusionEKF() {}

//=============================================================================
// Process the measurements
//=============================================================================

void FusionEKF::ProcessMeasurement(const MeasurementPackage &measurement_pack) {
  /**
   * --------------------------------------------------------------------------
   * Initialization
   * --------------------------------------------------------------------------
   */
  if (!is_initialized_) {

    // first measurement
    cout << "EKF: " << endl;
    ekf_.x_ = VectorXd(4);
    ekf_.x_ << 1, 1, 1, 1;

    if (measurement_pack.sensor_type_ == MeasurementPackage::RADAR) {
      // Convert radar from polar to cartesian coordinates and initialize state.
      float rho = measurement_pack.raw_measurements_(0);
      float phi = measurement_pack.raw_measurements_(1);
      float rho_dot = measurement_pack.raw_measurements_(2);

      ekf_.x_(0) = rho * cos(phi);
      ekf_.x_(1) = rho * sin(phi);
      ekf_.x_(2) = rho_dot * cos(phi);
      ekf_.x_(3) = rho_dot * sin(phi);

    } else if (measurement_pack.sensor_type_ == MeasurementPackage::LASER) {
      // Initialize state.
      ekf_.x_(0) = measurement_pack.raw_measurements_(0);
      ekf_.x_(1) = measurement_pack.raw_measurements_(1);
      ekf_.x_(2) = 0;
      ekf_.x_(3) = 0;

    }

    // timestamp
    previous_timestamp_ = measurement_pack.timestamp_;

    // done initializing, no need to predict or update
    is_initialized_ = true;
    return;
  }

  /**
   * --------------------------------------------------------------------------
   * Prediction
   * --------------------------------------------------------------------------
   */

  // calculate the time delta (in seconds)
  float time_delta = (measurement_pack.timestamp_ - previous_timestamp_) / 1000000.0;

  // update the previous timestamp to the current one
  previous_timestamp_ = measurement_pack.timestamp_;

  // Update the state transition matrix
  ekf_.F_(0, 2) = time_delta;
  ekf_.F_(1, 3) = time_delta;

  // Calculate the time deltas
  float time_delta_2 = time_delta * time_delta;
  float time_delta_3 = time_delta_2 * time_delta;
  float time_delta_4 = time_delta_3 * time_delta;

  // measurment noises
  float noise_ax = 9;
  float noise_ay = 9;

  // process covariance Q matrix
  ekf_.Q_ << time_delta_4 / 4 * noise_ax, 0, time_delta_3 / 2 * noise_ax, 0,
          0, time_delta_4 / 4 * noise_ay, 0, time_delta_3 / 2 * noise_ay,
          time_delta_3 / 2 * noise_ax, 0, time_delta_2 * noise_ax, 0,
          0, time_delta_3 / 2 * noise_ay, 0, time_delta_2 * noise_ay;

  // invoke EKF predict()
  ekf_.Predict();

  /**
   * --------------------------------------------------------------------------
   * Update
   * --------------------------------------------------------------------------
   */

  if (measurement_pack.sensor_type_ == MeasurementPackage::RADAR) {

    // Radar updates
    Hj_ = tools.CalculateJacobian(ekf_.x_);
    ekf_.Init(ekf_.x_, ekf_.P_, ekf_.F_, Hj_, R_radar_, ekf_.Q_);
    ekf_.UpdateEKF(measurement_pack.raw_measurements_);

  } else {
    // Laser updates
    ekf_.Init(ekf_.x_, ekf_.P_, ekf_.F_, H_laser_, R_laser_, ekf_.Q_);
    ekf_.Update(measurement_pack.raw_measurements_);

  }

  // print the output
  cout << "x_ = " << ekf_.x_ << endl;
  cout << "P_ = " << ekf_.P_ << endl;
}
