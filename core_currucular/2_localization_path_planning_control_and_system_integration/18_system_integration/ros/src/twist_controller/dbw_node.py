#!/usr/bin/env python

import rospy
from std_msgs.msg import Bool, Int32
from dbw_mkz_msgs.msg import ThrottleCmd, SteeringCmd, BrakeCmd, SteeringReport
from geometry_msgs.msg import TwistStamped
import math

from twist_controller import Controller

class DBWNode(object):
    def __init__(self):
        rospy.init_node('dbw_node')

        # get settings from the ros configuration
        vehicle_mass = rospy.get_param('~vehicle_mass', 1736.35)
        fuel_capacity = rospy.get_param('~fuel_capacity', 13.5)
        brake_deadband = rospy.get_param('~brake_deadband', .1)
        decel_limit = rospy.get_param('~decel_limit', -5)
        accel_limit = rospy.get_param('~accel_limit', 1.)
        wheel_radius = rospy.get_param('~wheel_radius', 0.2413)
        wheel_base = rospy.get_param('~wheel_base', 2.8498)
        steer_ratio = rospy.get_param('~steer_ratio', 14.8)
        max_lat_accel = rospy.get_param('~max_lat_accel', 3.)
        max_steer_angle = rospy.get_param('~max_steer_angle', 8.)

        # subscribe to these topics
        rospy.Subscriber('/vehicle/dbw_enabled', Bool, self.dbw_enabled_cb)
        rospy.Subscriber('/twist_cmd', TwistStamped, self.twist_cb)
        rospy.Subscriber('/current_velocity', TwistStamped, self.velocity_cb)
        rospy.Subscriber('/traffic_waypoint', Int32, self.traffic_cb)
        rospy.Subscriber('/stop_for_tl', Int32, self.stop_for_tl_cb)

        # publish to these topics
        self.steer_pub = rospy.Publisher('/vehicle/steering_cmd', SteeringCmd, queue_size=1)
        self.throttle_pub = rospy.Publisher('/vehicle/throttle_cmd', ThrottleCmd, queue_size=1)
        self.brake_pub = rospy.Publisher('/vehicle/brake_cmd', BrakeCmd, queue_size=1)

        # Instantiate the "movement" controller
        self.controller = Controller(
            vehicle_mass=vehicle_mass, 
            fuel_capacity=fuel_capacity, 
            brake_deadband=brake_deadband, 
            decel_limit=decel_limit, 
            accel_limit=accel_limit, 
            wheel_radius=wheel_radius, 
            wheel_base=wheel_base, 
            steer_ratio=steer_ratio, 
            max_lat_accel=max_lat_accel, 
            max_steer_angle=max_steer_angle
        )
        
        # other variables
        self.current_vel = None
        self.curr_ang_vel = None
        self.dbw_enabled = None
        self.linear_vel = None
        self.angular_vel = None
        self.throttle = self.steering = self.brake = 0
        self.traffic = None
        self.stop_for_tl = None

        # start the main loop
        self.loop()

    def loop(self):
        # define a refresh frequency of 50hz (DON'T CHANGE THIS)
        rate = rospy.Rate(50)

        # repeat until the program ends
        while not rospy.is_shutdown():
            
            # check if the car is moving
            if not None in (self.current_vel, self.linear_vel, self.angular_vel):

                # get the throttle, brake and steering from the comntroller
                self.throttle, self.brake, self.steering = self.controller.control(
                    self.current_vel,
                    self.dbw_enabled,
                    self.linear_vel,
                    self.angular_vel
                )
            
            # if the stop signal is published
            if self.stop_for_tl:

                # release the throtlle and apply the break
                self.throttle = 0.0
                self.brake = 10.0
   
            # only publish the new controls, if the drive-by-wire is enables
            if self.dbw_enabled:
              self.publish(self.throttle, self.brake, self.steering)

            # just wait
            rate.sleep()

    def dbw_enabled_cb(self, msg):
        # callback for setting the drive-by-wire flag in the object
        self.dbw_enabled = msg

    def twist_cb(self, msg):
        # callback for setting the linear and angular motion in the object
        self.linear_vel = msg.twist.linear.x
        self.angular_vel = msg.twist.angular.z

    def velocity_cb(self, msg):
        # callback for setting the current velocity in the object
        self.current_vel = msg.twist.linear.x
        
    def traffic_cb(self, msg):
        # callback for setting the stopline waypoint index in the object
        self.traffic = msg.data

    def stop_for_tl_cb(self, msg):
        # callback for setting stopping flag in the object
        self.stop_for_tl = msg.data

    def publish(self, throttle, brake, steer):

        # publish the new throttle value to the topic
        tcmd = ThrottleCmd()
        tcmd.enable = True
        tcmd.pedal_cmd_type = ThrottleCmd.CMD_PERCENT
        tcmd.pedal_cmd = throttle
        self.throttle_pub.publish(tcmd)

        # publish the new steering angle to the topic
        scmd = SteeringCmd()
        scmd.enable = True
        scmd.steering_wheel_angle_cmd = steer
        self.steer_pub.publish(scmd)

        # publish the new brake value to the topic
        bcmd = BrakeCmd()
        bcmd.enable = True
        bcmd.pedal_cmd_type = BrakeCmd.CMD_TORQUE
        bcmd.pedal_cmd = brake
        self.brake_pub.publish(bcmd)

if __name__ == '__main__':
    DBWNode()
