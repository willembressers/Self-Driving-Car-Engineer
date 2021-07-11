#include <uWS/uWS.h>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include "Eigen-3.3/Eigen/Core"
#include "Eigen-3.3/Eigen/QR"
#include "helpers.h"
#include "json.hpp"
#include "spline.h"

// for convenience
using nlohmann::json;
using std::string;
using std::vector;

int main() {
  uWS::Hub h;

  // Load up map values for waypoint's x,y,s and d normalized normal vectors
  vector<double> map_waypoints_x;
  vector<double> map_waypoints_y;
  vector<double> map_waypoints_s;
  vector<double> map_waypoints_dx;
  vector<double> map_waypoints_dy;

  // Waypoint map to read from
  string map_file_ = "../data/highway_map.csv";
  // The max s value before wrapping around the track back to 0
  double max_s = 6945.554;

  std::ifstream in_map_(map_file_.c_str(), std::ifstream::in);

  string line;
  while (getline(in_map_, line)) {
    std::istringstream iss(line);
    double x;
    double y;
    float s;
    float d_x;
    float d_y;
    iss >> x;
    iss >> y;
    iss >> s;
    iss >> d_x;
    iss >> d_y;
    map_waypoints_x.push_back(x);
    map_waypoints_y.push_back(y);
    map_waypoints_s.push_back(s);
    map_waypoints_dx.push_back(d_x);
    map_waypoints_dy.push_back(d_y);
  }
    
  // [0:left, 1:center, 2:right]
  int lane = 1;

  // convert [mp/h -> m/s] = / 2.237
  double max_speed = 49.5 / 2.237;
  double speed_limit = 50 / 2.237;

  // front and back distance (in meters)
  double safe_distance = 50;

  // end speed
  double reference_speed = 0.0;

  h.onMessage([&map_waypoints_x,&map_waypoints_y,&map_waypoints_s,
               &map_waypoints_dx,&map_waypoints_dy,
               &max_speed,&lane,&speed_limit,&safe_distance,&reference_speed,&max_s]
              (uWS::WebSocket<uWS::SERVER> ws, char *data, size_t length,
               uWS::OpCode opCode) {
    // "42" at the start of the message means there's a websocket message event.
    // The 4 signifies a websocket message
    // The 2 signifies a websocket event
    if (length && length > 2 && data[0] == '4' && data[1] == '2') {

      auto s = hasData(data);

      if (s != "") {
        auto j = json::parse(s);
        
        string event = j[0].get<string>();
        
        if (event == "telemetry") {
          // j[1] is the data JSON object
          
          // Main car's localization Data
          double car_x = j[1]["x"];
          double car_y = j[1]["y"];
          double car_s = j[1]["s"];
          double car_d = j[1]["d"];
          double car_yaw = j[1]["yaw"];
          double car_speed = j[1]["speed"];

          // Previous path data given to the Planner
          auto previous_path_x = j[1]["previous_path_x"];
          auto previous_path_y = j[1]["previous_path_y"];

          // Previous path's end s and d values 
          double end_path_s = j[1]["end_path_s"];
          double end_path_d = j[1]["end_path_d"];

          // Sensor Fusion Data, a list of all other cars on the same side 
          //   of the road.
          auto sensor_fusion = j[1]["sensor_fusion"];

          json msgJson;

          vector<double> next_x_vals;
          vector<double> next_y_vals;
          
          // ==================================================================
          // PROCESS SENSOR DATA
          // ==================================================================
          bool front_car = false;
          double front_car_speed;
          double front_car_distance = safe_distance + 1;
          bool left_lane_free  = true;
          bool right_lane_free = true; 

          for(int i=0; i < sensor_fusion.size(); i++) { 

            // get the fusion data of the other car
            double other_car_x = sensor_fusion[i][3];
            double other_car_y = sensor_fusion[i][4];
            double other_car_s = sensor_fusion[i][5];
            float other_car_d = sensor_fusion[i][6];

            // calculate it's speed and distance (to us)
            double other_car_speed = sqrt(other_car_x * other_car_x + other_car_y * other_car_y);
            double other_car_distance = other_car_s - car_s;
            
            // Check my lane --------------------------------------------------
            if (other_car_d > (2 + 4 * lane - 2) && other_car_d < (2 + 4 * lane + 2)) { 
              if (other_car_s > car_s && other_car_distance < safe_distance ) {
                front_car = true;
                front_car_speed = other_car_speed;
                front_car_distance = other_car_distance; 
              }
            }

            // Check right lane -----------------------------------------------
            if (lane == 2) {
              right_lane_free = false; 
            } else if (lane < 2) {
              if (other_car_d > (2 + 4 * (lane + 1) - 2) && other_car_d < (2 + 4 * (lane + 1) + 2)) { 
                if (other_car_distance < safe_distance && other_car_distance >- safe_distance) {
                  right_lane_free = false;
                }
              }
            }

            // Check left lane ------------------------------------------------
            if (lane == 0) {
              left_lane_free = false;
            } else if (lane > 0) {
              if (other_car_d > (2 + 4 * (lane - 1) - 2) && other_car_d < (2 + 4 * (lane - 1) + 2)) { 
                if (other_car_distance < safe_distance && other_car_distance >- safe_distance ) {
                  left_lane_free = false;
                }
              }
            }
          }


          // ==================================================================
          // BEHAVIOUR
          // ==================================================================
          double target_speed;

          // If there is a car in front of us
          if (front_car) {

            // match its speed
            target_speed = front_car_speed;

            // pass it on the right side (illegal in the Netherlands, (i hate this rule))
            if (right_lane_free) {
              lane += 1;
              target_speed = max_speed;

            // pass it on the left side
            } else if (left_lane_free) {
              lane -= 1;
              target_speed = max_speed;
            }

            // nothing ahead let's go.....
          } else {
            target_speed = max_speed;
          }

          
          // ==================================================================
          // TRAJECTORY
          // ==================================================================
          double reference_x;
          double reference_y;
          double previous_reference_x;
          double previous_reference_y;
          double reference_yaw; 

          // create a list of (x,y) waypoints
          vector<double> ptsx;
          vector<double> ptsy;

          // Collect previous and current 'pts(x,y)' waypoints
          int prev_size = previous_path_x.size(); 

          // at start  --------------------------------------------------------
          if (prev_size < 1) {

            // get the current position (x,y) and direction (yaw)
            reference_x = car_x;
            reference_y = car_y;
            reference_yaw = deg2rad(car_yaw);

            // fake previous position based on the inversed yaw
            previous_reference_x = reference_x - cos(car_yaw);
            previous_reference_y = reference_y - sin(car_yaw); 
            end_path_s = car_s; 

            ptsx.push_back(previous_reference_x);
            ptsx.push_back(reference_x); 
            ptsy.push_back(previous_reference_y);
            ptsy.push_back(reference_y);

          // driving  ---------------------------------------------------------
          } else {

            // get the last position
            reference_x = previous_path_x[prev_size - 1];
            reference_y = previous_path_y[prev_size - 1]; 

            // get the second to last position
            previous_reference_x = previous_path_x[prev_size - 2];
            previous_reference_y = previous_path_y[prev_size - 2];

            // calculate the last direction (yaw)
            reference_yaw = atan2(reference_y - previous_reference_y, reference_x - previous_reference_x); 

            ptsx.push_back(previous_reference_x);
            ptsx.push_back(reference_x); 
            ptsy.push_back(previous_reference_y);
            ptsy.push_back(reference_y); 
          } 

          // Collect the waypoints [30m, 60m, 90m]
          vector<double> next_wp0 = getXY(end_path_s + 30, (2 + 4 * lane), map_waypoints_s, map_waypoints_x, map_waypoints_y);
          vector<double> next_wp1 = getXY(end_path_s + 60, (2 + 4 * lane), map_waypoints_s, map_waypoints_x, map_waypoints_y);
          vector<double> next_wp2 = getXY(end_path_s + 90, (2 + 4 * lane), map_waypoints_s, map_waypoints_x, map_waypoints_y); 

          // push x points
          ptsx.push_back(next_wp0[0]);
          ptsx.push_back(next_wp1[0]);
          ptsx.push_back(next_wp2[0]); 
          ptsy.push_back(next_wp0[1]);
          ptsy.push_back(next_wp1[1]);
          ptsy.push_back(next_wp2[1]);


          // ==================================================================
          // PATH PLANNER
          // ==================================================================
          // Refill empty 'next_val' slots with new points that the car will visit every .02 seconds
          double x_local = 0.0; // (x,y) end point of trajectory in local car's end point reference
          double y_local;
          double time_delta = 0.02;
          
          // Transform to car coordinate system
          for (int i = 0; i < ptsx.size(); i++ ) { 
            double shift_x = ptsx[i] - reference_x;
            double shift_y = ptsy[i] - reference_y; 

            ptsx[i] = (shift_x * cos(0 - reference_yaw) - shift_y * sin(0 - reference_yaw));
            ptsy[i] = (shift_x * sin(0 - reference_yaw) + shift_y * cos(0 - reference_yaw));
          }

          // create a spline
          tk::spline s;
          s.set_points(ptsx,ptsy);

          // calculate how to break up the spline points
          double target_x = 30.0;
          double target_y = s(target_x);
          double target_dist = sqrt((target_x) * (target_x) + (target_y) * (target_y));

          // start with all of the previous path points from last time
          for (int i=1; i < previous_path_x.size(); i++) {
            next_x_vals.push_back(previous_path_x[i]);
            next_y_vals.push_back(previous_path_y[i]);
          } 

          // fill up the rest of our path planner 
          for (int i=1; i <= 50 - previous_path_x.size(); i++) { 

            // decelerate
            if (reference_speed > target_speed || front_car_distance < safe_distance / 2 ) {
              reference_speed -= 0.1;

              // prevent reversing
              reference_speed = std::max(0.00001,reference_speed);

            // accelerate
            } else if (reference_speed < target_speed) {
              reference_speed += 0.1;
            }
            
            // N is the number of points along our spline
            double N = (target_dist / (time_delta * reference_speed));

            // calculate the local steps in the spline
            x_local = x_local + (target_x) / N; 
            y_local = s(x_local);
            
            // go back to global coordinates form car coordinates
            double x_map = x_local * cos(reference_yaw) - y_local * sin(reference_yaw) + reference_x;
            double y_map = x_local * sin(reference_yaw) + y_local * cos(reference_yaw) + reference_y; 

            // update next vals for simulator
            next_x_vals.push_back(x_map);
            next_y_vals.push_back(y_map); 
          }

          // ==================================================================

          msgJson["next_x"] = next_x_vals;
          msgJson["next_y"] = next_y_vals;

          auto msg = "42[\"control\","+ msgJson.dump()+"]";

          ws.send(msg.data(), msg.length(), uWS::OpCode::TEXT);
        }  // end "telemetry" if
      } else {
        // Manual driving
        std::string msg = "42[\"manual\",{}]";
        ws.send(msg.data(), msg.length(), uWS::OpCode::TEXT);
      }
    }  // end websocket if
  }); // end h.onMessage

  h.onConnection([&h](uWS::WebSocket<uWS::SERVER> ws, uWS::HttpRequest req) {
    std::cout << "Connected!!!" << std::endl;
  });

  h.onDisconnection([&h](uWS::WebSocket<uWS::SERVER> ws, int code,
                         char *message, size_t length) {
    ws.close();
    std::cout << "Disconnected" << std::endl;
  });

  int port = 4567;
  if (h.listen(port)) {
    std::cout << "Listening to port " << port << std::endl;
  } else {
    std::cerr << "Failed to listen to port" << std::endl;
    return -1;
  }
  
  h.run();
}