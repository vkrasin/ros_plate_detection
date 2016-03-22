#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image

class Plate_Detector():

    def __init__(self):
        self.prepare_subscribers()
        self.prepare_publishers()
        # State for the state machine
        self.state = 'e_stop'

    def eventin_handler(self, msg):
        rospy.loginfo('eventin msg received, data = %s', msg.data)
        # Adjust the state
        self.state = msg

    def image_handler(self, msg):
        # If we received an image and are in the start state, we start img recognition
        if (self.state == 'e_start'):
            rospy.loginfo('image msg received')
            # Call the img recognition function with our img (msg) here
            


    def prepare_subscribers(self):
        # Our eventin subscriber, listens to topic event_in
        # and registers a handler function
        self.eventin_sub = rospy.Subscriber("~/event_in", String, self.eventin_handler)

        # Our image subscriber
        self.image_sub = rospy.Subscriber("~/input_image", Image, self.image_handler)


    def prepare_publishers(self):
        # Publishers
        self.eventout_msg_pub = rospy.Publisher("~/event_out", String, queue_size=100)
        self.shape_msg_pub = rospy.Publisher("~/shape", String, queue_size=100)

        
