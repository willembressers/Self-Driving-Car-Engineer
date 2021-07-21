#!/usr/bin/env python
import numpy as np
import rospy
from geometry_msgs.msg import PoseStamped
from styx_msgs.msg import Lane, Waypoint
from std_msgs.msg import Int32
from scipy.spatial import KDTree

import math


LOOKAHEAD_WPS = 150 # Number of waypoints we will publish. You can change this number
MAX_DECEL = .5 # Maximum deceleration to keep up a nice drive-behaviour

class WaypointUpdater(object):
    def __init__(self):
        rospy.init_node('waypoint_updater')

        # subscribe to these topics
        rospy.Subscriber('/current_pose', PoseStamped, self.pose_cb)
        rospy.Subscriber('/base_waypoints', Lane, self.waypoints_cb)
        rospy.Subscriber('/traffic_waypoint', Int32, self.traffic_cb)

        # publish to these topics
        self.final_waypoints_pub = rospy.Publisher('final_waypoints', Lane, queue_size=1)
        self.stop_for_tl_pub = rospy.Publisher('/stop_for_tl', Int32, queue_size=1)

        # other variables
        self.pose = None
        self.base_waypoints = None
        self.waypoints_2d = None
        self.waypoint_tree = None
        self.stopline_wp_idx = -1

        # start the main loop
        self.loop()

    def loop(self):
        # define a refresh frequency of 10hz
        rate = rospy.Rate(10)

        # repeat until the program ends
        while not rospy.is_shutdown():

            # check (on initialization) if we have allready data
            if self.pose and self.base_waypoints:

                # publish the waypoints to the topic
                self.publish_waypoints()

            # just wait
            rate.sleep()

    def get_closest_waypoint_idx(self):
        # get the current x,y position
        x = self.pose.pose.position.x
        y = self.pose.pose.position.y
        
        # look for the closest waypoint (in the KDTree)
        closest_idx = self.waypoint_tree.query([x, y], 1)[1]

        # get the closest and second closest coordinates
        closest_coord = self.waypoints_2d[closest_idx]
        prev_coord = self.waypoints_2d[closest_idx - 1]

        # Equation for hyperplane through closest_coords
        cl_vect = np.array(closest_coord)
        prev_vect = np.array(prev_coord)
        pos_vect = np.array([x, y])

        val = np.dot(cl_vect - prev_vect, pos_vect - cl_vect)
        if val > 0:
            closest_idx = (closest_idx + 1) % len(self.waypoints_2d)

        # return the closest waypoint index
        return closest_idx

    def publish_waypoints(self):
        # generate the lane of the waypoints
        lane = self.generate_lane()

        # publish the lane
        self.final_waypoints_pub.publish(lane)

    def generate_lane(self):
        # initialize an empty lane
        lane = Lane()

        # get the closest and farthest waypoint indicies
        closest_idx = self.get_closest_waypoint_idx()
        farthest_idx = closest_idx + LOOKAHEAD_WPS

        # slice a copy of all the waypoints
        base_waypoints = self.base_waypoints.waypoints[closest_idx:farthest_idx]

        # set the default flag for stopping the car at 0 (don't stop)
        stop = 0

        # if there is no traffic light (stop line) before the lookahead, then don't manipulate the slice
        if self.stopline_wp_idx == -1 or (self.stopline_wp_idx >= farthest_idx):
            lane.waypoints = base_waypoints

        # otherwise, adjust the waypoints slice for a smooth deceleration
        else:
            lane.waypoints = self.decelerate_waypoints(base_waypoints, closest_idx)
            stop = 1

        # tell everyone that we have to stop (or not)
        self.stop_for_tl_pub.publish(stop)

        # and return the lane
        return lane

    def decelerate_waypoints(self, waypoints, closest_idx):
        # don't overwrite the basepoint, just manipulate a copy
        new_waypoints = []

        # loop over the waypoints (in the slice)
        for i, waypoint in enumerate(waypoints):

            # instantiate a new waypoint
            new_waypoint = Waypoint()

            # copy the car pose
            new_waypoint.pose = waypoint.pose
            
            # get the stopline waypoint index (offset by 2 so the car doesn't wait ON the stopline)
            stop_idx = max(self.stopline_wp_idx - closest_idx - 2, 0)

            # calculate the distance between the current (i) waypoint and the stopline waypoint (stop_idx)
            distance = self.distance(waypoints, i, stop_idx) 
            
            # determine the velocity at the waypoint
            velocity = math.sqrt(2 * MAX_DECEL * distance)
            if velocity < 1.:
                velocity = 0.

            # assign the velocity to the waypoint (pick the lowest, from current speed, deceleration speed)
            new_waypoint.twist.twist.linear.x = min(velocity, waypoint.twist.twist.linear.x) 

            # add the new waypoint to the list
            new_waypoints.append(new_waypoint)

        # return the slice of manipulated waypoints
        return new_waypoints

    def pose_cb(self, msg):
        # callback for setting the current car pose in the object
        self.pose = msg

    def waypoints_cb(self, waypoints):
        # callback for setting the waypoints in the object
        self.base_waypoints = waypoints

        # if there are no waypoints set (only at start)
        if not self.waypoints_2d:

            # convert the waypoints to a list
            self.waypoints_2d = [[waypoint.pose.pose.position.x, waypoint.pose.pose.position.y] for waypoint in waypoints.waypoints]

            # construct a searchable tree
            self.waypoint_tree = KDTree(self.waypoints_2d)

    def traffic_cb(self, msg):
        # callback for setting the stopline waypoint index in the object
        self.stopline_wp_idx = msg.data

    def obstacle_cb(self, msg):
        pass

    def get_waypoint_velocity(self, waypoint):
        return waypoint.twist.twist.linear.x

    def set_waypoint_velocity(self, waypoints, waypoint, velocity):
        waypoints[waypoint].twist.twist.linear.x = velocity

    def distance(self, waypoints, wp1, wp2):
        dist = 0
        dl = lambda a, b: math.sqrt((a.x-b.x)**2 + (a.y-b.y)**2  + (a.z-b.z)**2)
        for i in range(wp1, wp2+1):
            dist += dl(waypoints[wp1].pose.pose.position, waypoints[i].pose.pose.position)
            wp1 = i
        return dist

if __name__ == '__main__':
    try:
        WaypointUpdater()
    except rospy.ROSInterruptException:
        rospy.logerr('Could not start waypoint updater node.')

