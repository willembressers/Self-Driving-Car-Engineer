#!/usr/bin/env python

import rospy
from std_msgs.msg import Int32
from geometry_msgs.msg import PoseStamped, Pose
from styx_msgs.msg import TrafficLightArray, TrafficLight
from styx_msgs.msg import Lane
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from light_classification.tl_classifier import TLClassifier
import tf
import cv2
import yaml
from scipy.spatial import KDTree

STATE_COUNT_THRESHOLD = 3

class TLDetector(object):
    def __init__(self):
        rospy.init_node('tl_detector')

        # get settings from the ros configuration
        config_string = rospy.get_param("/traffic_light_config")

        # subscribe to these topics
        sub1 = rospy.Subscriber('/current_pose', PoseStamped, self.pose_cb)
        sub2 = rospy.Subscriber('/base_waypoints', Lane, self.waypoints_cb)
        sub3 = rospy.Subscriber('/vehicle/traffic_lights', TrafficLightArray, self.traffic_cb)
        sub6 = rospy.Subscriber('/image_color', Image, self.image_cb)

        # publish to these topics
        self.upcoming_red_light_pub = rospy.Publisher('/traffic_waypoint', Int32, queue_size=1)

        # other variables
        self.pose = None
        self.camera_image = None
        self.lights = []
        self.base_waypoints = None
        self.waypoints_2d = None
        self.waypoint_tree = None
        self.bridge = CvBridge()
        self.light_classifier = TLClassifier()
        self.listener = tf.TransformListener()
        self.state = TrafficLight.UNKNOWN
        self.last_state = TrafficLight.UNKNOWN
        self.last_wp = -1
        self.state_count = 0
        
        # load the configuration
        self.config = yaml.load(config_string)

        # ...
        rospy.spin()

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
        # callback for setting the traffic lights in the object
        self.lights = msg.lights

    def image_cb(self, msg):
        """Identifies red lights in the incoming camera image and publishes the index
            of the waypoint closest to the red light's stop line to /traffic_waypoint

        Args:
            msg (Image): image from car-mounted camera

        """
        self.has_image = True
        self.camera_image = msg
        light_wp, state = self.process_traffic_lights()

        '''
        Publish upcoming red lights at camera frequency.
        Each predicted state has to occur `STATE_COUNT_THRESHOLD` number
        of times till we start using it. Otherwise the previous stable state is
        used.
        '''
        if self.state != state:
            self.state_count = 0
            self.state = state
        elif self.state_count >= STATE_COUNT_THRESHOLD:
            self.last_state = self.state
            light_wp = light_wp if state == TrafficLight.RED else -1
            self.last_wp = light_wp
            self.upcoming_red_light_pub.publish(Int32(light_wp))
        else:
            self.upcoming_red_light_pub.publish(Int32(self.last_wp))
        self.state_count += 1

    def get_closest_waypoint(self, x, y):
        # look for the closest waypoint (in the KDTree)
        return self.waypoint_tree.query([x, y], 1)[1]

    def get_light_state(self, light):
        # read the traffic light state from the light
        return light.state

    def process_traffic_lights(self):
        # define the closest traffic light and stopline waypoint
        closest_light = None
        line_wp_idx = -1 

        # List of positions that correspond to the line to stop in front of for a given intersection
        stop_line_positions = self.config['stop_line_positions']

        # ensure we have a position and waypoints
        if(self.pose and self.base_waypoints):

            # get the closest waypoint 
            car_position = self.get_closest_waypoint(self.pose.pose.position.x, self.pose.pose.position.y)

            # get the total number of waypoints
            diff = len(self.base_waypoints.waypoints)

            # loop over the traffic lights
            for i, light in enumerate(self.lights):

                # Get stop line waypoint index
                line = stop_line_positions[i]
                temp_wp_idx = self.get_closest_waypoint(line[0], line[1])

                # Find closest stop line waypoint index
                index_distance = temp_wp_idx - car_position
                if index_distance >= 0 and index_distance < diff:
                    diff = index_distance
                    closest_light = light
                    line_wp_idx = temp_wp_idx

        # if we've found th closest traffic light
        if closest_light:

            # get it's state (red, orange, green)
            state = self.get_light_state(closest_light)

            # return the stopline waypoint index
            return line_wp_idx, state
        
        # if there is no traffic light
        return -1, TrafficLight.UNKNOWN

if __name__ == '__main__':
    try:
        TLDetector()
    except rospy.ROSInterruptException:
        rospy.logerr('Could not start traffic node.')
