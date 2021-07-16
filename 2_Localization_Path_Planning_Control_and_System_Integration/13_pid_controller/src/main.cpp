#include <math.h>
#include <uWS/uWS.h>
#include <iostream>
#include <string>
#include "json.hpp"
#include "PID.h"
#include "Twiddle.h"

// for convenience
using nlohmann::json;
using std::string;

static int counter = 0;
double throttle = 0.3;

// For converting back and forth between radians and degrees.
constexpr double pi() { return M_PI; }
double deg2rad(double x) { return x * pi() / 180; }
double rad2deg(double x) { return x * 180 / pi(); }

// Checks if the SocketIO event has JSON data.
// If there is data the JSON object in string format will be returned,
// else the empty string "" will be returned.
string hasData(string s) {
  auto found_null = s.find("null");
  auto b1 = s.find_first_of("[");
  auto b2 = s.find_last_of("]");
  if (found_null != string::npos) {
    return "";
  }
  else if (b1 != string::npos && b2 != string::npos) {
    return s.substr(b1, b2 - b1 + 1);
  }
  return "";
}

int main() {
  uWS::Hub h;

  PID pid;
  Twiddle twiddle;

  // Initialize the pid variable.
//   double Kp = 0.0;  
//   double Ki = 0.0;
//   double Kd = 0.0;
  
//   final run
  double Kp = 0.15;  
  double Ki = 0.001;
  double Kd = 0.8;

  // initialize the pid
  pid.Init(Kp, Ki, Kd);
  
  // initialize twiddle
  twiddle.Init(Kp, Ki, Kd, false);

  h.onMessage([&pid, &twiddle](uWS::WebSocket<uWS::SERVER> ws, char *data, size_t length, 
                     uWS::OpCode opCode) {
    // "42" at the start of the message means there's a websocket message event.
    // The 4 signifies a websocket message
    // The 2 signifies a websocket event
    if (length && length > 2 && data[0] == '4' && data[1] == '2') {
      auto s = hasData(string(data).substr(0, length));

      if (s != "") {
        auto j = json::parse(s);

        string event = j[0].get<string>();

        if (event == "telemetry") {
          // j[1] is the data JSON object
          double cte = std::stod(j[1]["cte"].get<string>());
          double speed = std::stod(j[1]["speed"].get<string>());
//           double angle = std::stod(j[1]["steering_angle"].get<string>());
          double steer_value;

          // update the errors
          pid.UpdateError(cte);

          // get the steering value
          steer_value = pid.TotalError();

          // ensure the steering value is between [-1, 1]
          if (steer_value > 1) {
            steer_value = 1;
          } else if (steer_value < -1) {
            steer_value = -1;
          }
          
          // Of the road (restart)
          if (abs(cte) >= 4) {
            // notify whats happening
            std::cout << "of the road > restart simulator" << std::endl;

            // reset the values
            steer_value = 0;
            throttle = 0.1;
            counter = 0;

            // trigger the reset
            std::string msg("42[\"reset\", {}]");
            ws.send(msg.data(), msg.length(), uWS::OpCode::TEXT);
          }
          
          // update the counter
          counter++;

          if (twiddle.getStatus()) {
            twiddle.incrementCount(cte);

            // update every 100 steps the parameters
            if (counter % 100 == 0) {
              // increment the speed
              throttle = throttle + 0.1;

              // update the parameters
              std::vector<double> params = twiddle.updateParams(0.2);

              // log the current parameters to a file (sometimes the workspace crashes)
              twiddle.log();

              // continue with the new parameters
              pid.UpdateParams(params[0], params[1], params[2]);
            }

            // don't accelerate while we're twiddling
            if (speed > 5) {
              throttle = 0;
            }
          }
          
//           // DEBUG
//           if (counter % 10 == 0) {
//             std::cout << "counter: " << counter << " CTE: " << cte << " Steering Value: " << steer_value << " angle: " << angle << " speed: " << speed << " throttle: " << throttle << std::endl;
//           }

          json msgJson;
          msgJson["steering_angle"] = steer_value;
          msgJson["throttle"] = throttle;
          auto msg = "42[\"steer\"," + msgJson.dump() + "]";
//           std::cout << msg << std::endl;
          ws.send(msg.data(), msg.length(), uWS::OpCode::TEXT);
        }  // end "telemetry" if
      } else {
        // Manual driving
        string msg = "42[\"manual\",{}]";
        ws.send(msg.data(), msg.length(), uWS::OpCode::TEXT);
      }
    }  // end websocket message if
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