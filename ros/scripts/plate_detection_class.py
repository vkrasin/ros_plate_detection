#!/usr/bin/env python

import rospy
import cv2
import numpy as np
import rospkg

from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

from plate_detection import *

class Plate_Detector():

    def __init__(self):
        self.bridge = CvBridge()
        self.prepare_templates()
        self.prepare_subscribers()
        self.prepare_publishers()

        # State for the state machine
        self.state = 'e_stop'

    def eventin_handler(self, msg):
        rospy.loginfo('eventin msg received, data = %s', msg.data)
        # Adjust the state
        self.state = msg.data

    def image_handler(self, msg):
        # If we received an image and are in the start state, we start img recognition
        if (self.state == 'e_start'):
            rospy.loginfo('image msg received')
            # Call the img recognition function with our img (msg) here
            target_image = self.bridge.imgmsg_to_cv2(msg)
            result1 = getMatch(self.kp_circle, self.des_circle, target_image)
            result2 = getMatch(self.kp_square, self.des_square, target_image)
            rospy.loginfo('Circle: %s', result1)
            rospy.loginfo('Square: %s', result2)
            


    def prepare_subscribers(self):
        # Our eventin subscriber, listens to topic event_in
        # and registers a handler function
        self.eventin_sub = rospy.Subscriber("~event_in", String, self.eventin_handler)

        # Our image subscriber
        self.image_sub = rospy.Subscriber("~input_image", Image, self.image_handler)


    def prepare_publishers(self):
        # Publishers
        self.eventout_msg_pub = rospy.Publisher("~event_out", String, queue_size=100)
        self.shape_msg_pub = rospy.Publisher("~shape", String, queue_size=100)

    def prepare_templates(self):
        # Get the path to our package
        rospack = rospkg.RosPack()
        filepath = rospack.get_path('ros_plate_detection_node')

        # Load the template images
        img_circle = cv2.imread(filepath + '/ros/img/template_circle.jpg',0)
        img_square = cv2.imread(filepath + '/ros/img/template_square.jpg',0)

        if (img_circle == None):
            rospy.loginfo('circle template missing')

        if (img_square == None):
            rospy.loginfo('square template missing')
        
        # Extract keypoints and features with SURF
        surf = cv2.xfeatures2d.SURF_create()
        
        self.kp_circle, self.des_circle = surf.detectAndCompute(img_circle,None)
        self.kp_square, self.des_square = surf.detectAndCompute(img_square,None)
        
