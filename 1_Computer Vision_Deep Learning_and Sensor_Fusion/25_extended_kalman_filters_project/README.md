# Extended Kalman Filter
[![Udacity - Self-Driving Car NanoDegree](https://s3.amazonaws.com/udacity-sdc/github/shield-carnd.svg)](http://www.udacity.com/drive)

In this project i've utilized a kalman filter to estimate the state of a moving object of interest with noisy lidar and radar measurements. 

## Environment
I was unable to setup the simulator on my mac, so i chose to use the Udacity workspace.

## Data
The data consist of `Radar` and `Lidar` data. `Radar` is based on radio signals and can "see" through rain and fog. `Lidar` is based on infrared light and can 

## Usage
Instead of deleting, creating folders and compile and run, every try. i've created an convienance script
```bash
./compile_and_run.sh

```

![Compile and run](./images/compile_and_run.png)

When the extended kalman filter is running, you can start the simulator. 

![Simulator](./images/simulator.png)

## Flow

![Flow](./images/flow.png)

- First we initialize the matrices and the vectors
- on each measurement
-  predict the new transition
-  update the matrices