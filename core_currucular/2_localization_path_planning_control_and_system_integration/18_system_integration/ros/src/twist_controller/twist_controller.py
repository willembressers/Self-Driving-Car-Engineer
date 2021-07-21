#!/usr/bin/env python

import rospy
from pid import PID
from lowpass import LowPassFilter
from yaw_controller import YawController

GAS_DENSITY = 2.858
ONE_MPH = 0.44704

class Controller(object):
    def __init__(self, vehicle_mass, fuel_capacity, brake_deadband, decel_limit, 
        accel_limit, wheel_radius, wheel_base, steer_ratio, max_lat_accel, max_steer_angle):
         
        # instantiate the yaw controller 
        self.yaw_controller = YawController(wheel_base, steer_ratio, 0.1, max_lat_accel, max_steer_angle)

        # instantiate the PID controller
        self.throttle_controller = PID(0.3, 0.1, 0., 0., 0.2)

        # instantiate the lowpass filter
        self.vel_lpf = LowPassFilter(0.5, .02)

        # collect the other variables
        self.vehicle_mass = vehicle_mass
        self.fuel_capacity = fuel_capacity
        self.brake_deadband = brake_deadband
        self.decel_limit = decel_limit
        self.accel_limit = accel_limit
        self.wheel_radius = wheel_radius
        self.last_time = rospy.get_time()

    def control(self, current_vel, dbw_enabled, linear_vel, angular_vel):
        # if the drive-by-wire is disabled
        if not dbw_enabled:

            # stop collecting the errors
            self.throttle_controller.reset()

            # return some values (these are ignored)
            return 0., 0., 0.
        
        # smooth the velocity peaks and troughs with an lowpass filter
        current_vel = self.vel_lpf.filt(current_vel)
        
        # calculate the steering angle based on the current and desired velocities
        steering = self.yaw_controller.get_steering(linear_vel, angular_vel, current_vel)

        # determine the velocity error
        vel_err = linear_vel - current_vel
        self.last_vel = current_vel

        # get the sampling time
        current_time = rospy.get_time()
        sample_time = current_time - self.last_time
        self.last_time = current_time

        # apply the PID controller for the throttle
        throttle = self.throttle_controller.step(vel_err, sample_time)

        # by default don't break
        brake = 0

        # if the car is standing still and it is desired to stay still
        if linear_vel == 0. and current_vel < 0.1:
            # don't throttle and apply full breaks
            throttle = 0 
            brake = 700

        # if there is no throttle and a small velocity error
        elif throttle < .1 and vel_err < 0:
            # don't throttle and apply calculated (smooth) breaks
            throttle = 0
            decel = max(vel_err, self.decel_limit)
            brake = abs(decel) * self.vehicle_mass * self.wheel_radius # (Torque per meter) 

        # return the new "movement"
        return throttle, brake, steering