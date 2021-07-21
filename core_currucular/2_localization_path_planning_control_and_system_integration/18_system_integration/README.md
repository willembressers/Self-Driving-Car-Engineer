This is the project repo for the final project of the Udacity Self-Driving Car Nanodegree: Programming a Real Self-Driving Car. For more information about the project, see the project introduction [here](https://classroom.udacity.com/nanodegrees/nd013/parts/6047fe34-d93c-4f50-8336-b70ef10cb4b2/modules/e1a23b06-329a-4684-a717-ad476f0d8dff/lessons/462c933d-9f24-42d3-8bdc-a08a5fc866e4/concepts/5ab4b122-83e6-436d-850f-9f4d26627fd9).

Please use **one** of the two installation options, either native **or** docker installation.

### Native Installation

* Be sure that your workstation is running Ubuntu 16.04 Xenial Xerus or Ubuntu 14.04 Trusty Tahir. [Ubuntu downloads can be found here](https://www.ubuntu.com/download/desktop).
* If using a Virtual Machine to install Ubuntu, use the following configuration as minimum:
  * 2 CPU
  * 2 GB system memory
  * 25 GB of free hard drive space

  The Udacity provided virtual machine has ROS and Dataspeed DBW already installed, so you can skip the next two steps if you are using this.

* Follow these instructions to install ROS
  * [ROS Kinetic](http://wiki.ros.org/kinetic/Installation/Ubuntu) if you have Ubuntu 16.04.
  * [ROS Indigo](http://wiki.ros.org/indigo/Installation/Ubuntu) if you have Ubuntu 14.04.
* [Dataspeed DBW](https://bitbucket.org/DataspeedInc/dbw_mkz_ros)
  * Use this option to install the SDK on a workstation that already has ROS installed: [One Line SDK Install (binary)](https://bitbucket.org/DataspeedInc/dbw_mkz_ros/src/81e63fcc335d7b64139d7482017d6a97b405e250/ROS_SETUP.md?fileviewer=file-view-default)
* Download the [Udacity Simulator](https://github.com/udacity/CarND-Capstone/releases).

### Docker Installation
[Install Docker](https://docs.docker.com/engine/installation/)

Build the docker container
```bash
docker build . -t capstone
```

Run the docker file
```bash
docker run -p 4567:4567 -v $PWD:/capstone -v /tmp/log:/root/.ros/ --rm -it capstone
```

### Port Forwarding
To set up port forwarding, please refer to the [instructions from term 2](https://classroom.udacity.com/nanodegrees/nd013/parts/40f38239-66b6-46ec-ae68-03afd8a601c8/modules/0949fca6-b379-42af-a919-ee50aa304e6a/lessons/f758c44c-5e40-4e01-93b5-1a82aa4e044f/concepts/16cf4a78-4fc7-49e1-8621-3450ca938b77)

### Usage

1. Clone the project repository
```bash
git clone https://github.com/udacity/CarND-Capstone.git
```

2. Install python dependencies
```bash
cd CarND-Capstone
pip install -r requirements.txt
```
3. Make and run styx
```bash
cd ros
./compile_and_run.sh
```

## Final Result

my (youtube) results: https://www.youtube.com/watch?v=oSip2g0C8qc
![](https://www.youtube.com/watch?v=oSip2g0C8qc)

For this project i had to develop and ROS implementation that controls the Udacity car in a simulator. The project consisted of 4 parts

### Waypoint updater
The Waypoint updater is the first part to develop. It recieves all the trajectory waypoints from the `\base_waypoints` ROS topic. The updater will the build an `KDTree` of all the waypoints which is fast and searchable. Once the tree is build, the updater will constantly publish a set of waypoints to `final_waypoints`. These waypoints are published with a frequency of 10 Hertz, and consist of 150 waypoints ahead. If within these 150 waypoints a traffic light is detected, then the updater will automatically adjust the waypoints in order to decelerate.

### Drive-by-wire
The next part is the ROS DBW (drooive-by-wire) node. This node reads the car parameters (like, vehicle mass, wheel radius, steer ratio, etc) from the ROS configuration, and uses it to initialize the `twist` controller. Once the `twist` controller is initialized, the DBW node will run with a frequency of 50Hz and collect the new throttle, brake and steering angle, in order to publish it to the vehicle command topics (like `/vehicle/steering_cmd`). If for some reason the `drive-by-wire` is disabled, then the node WONT publish any commands to the topic and let the user (passengers) take over control.

### Twist controller
The twist controller is initialized from within the `drive-by-wire` node. The main purpose of this controller is to calculate the throtlle, brake and steering angle in order to achieve the appropriate speed and direction according to the waypoints. The twist controllor incorporates a `yaw` controller which is responsible for steering angle. It takes the `wheel base`, `steer ratio`, `maximum lateral acceleration` and `maximum steering angle` into considderation. The twist controller uses a PID (Proportional Integral Differential) model in order to control the throttle. The PID controller calculates the appropriate throttle based on the current velocity and target velocity, so that it doesn't accelerate to slow, but also not to fast and overshoot it's target velocity and passing the speed limit. Default the brakes are released within the twist controller, but when the car must decelerate it will calculate the deceleration so that it will transition smoothly.

### Traffic light detector
The last part is the traffic light detector. This detector loads a predefined list of all traffic lights and maps them onto the waypoints. The traffic light detector will look for the closest traffic light within the waypoints and fetch the state (red, orange, green). This will be used by the waypoint updater to update the waypoints, and this will trigger the drive-by-wire and twist controller in order to stop the car (when there is a red sign detected).

### Development
I've had several issues getting the code up and running locally. i've tried 4 times to setup a Ubuntu virtual machine locally, (i'm used to work in virtual machined) but i've had many difficulties setting up the python environment, and the simulator. So eventually i chose to work in the Udacity workspace. This was quite conveniant, but i had to take an eye on the GPU hours. Also here were many difficulties, most of them resided in that the car dodn't follow it's waypoint trajectory. I'vre refreshed the workspace 3 times, until i eventually got the car following the waypoints. Due to all these difficulties i burnt most of the GPU hours, so training a image classifier wasnt an option anymore.

When i finalized my code, i've setup a screen recording for the (youtube) video. I noticed that my car passed a red traffic light. I noticed that this is because the drive-by-wire has an hardcode brake of 10. so this means that it's a linear function and overshoots the target waypoint (stopline). I choose the easiest sollution and that is to look futher ahead, so a red traffic light is noticed earlier, and thus the linear breaking suffies.

