#ifndef TWIDDLE_H
#define TWIDDLE_H
#include <vector>

enum State {INIT, INCREMENT,DECREMENT};

class Twiddle {
 private:
  int n;
  State state;
  int i;
  int it;
  double total_err;
  double best_err;
  double sum;
  bool running;

  std::vector<double> p;
  std::vector<double> dp;

 public:

  /**
   * Constructor.
   */
  Twiddle();

  /*
  * Destructor.
  */
  virtual ~Twiddle();

  /**
   * Initialize Twiddle.
   */
  void Init(double Kp, double Ki, double Kd, bool status);

  /**
   * Increment cross track error
   */
  void incrementCount(double cte);

  /**
   * Returns the twittle status
   */
  bool getStatus();
    
  /**
   * Update the PID coeffiecents
   */
  std::vector<double> updateParams(double tol);
  
  /**
   * Log the current PID coeffiecents to file
   */
  void log();
};

#endif /* TWIDDLE_H */