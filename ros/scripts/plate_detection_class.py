#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image

class Plate_Detector():

    def __init__(self):
        self.prepare_subscribers()
        self.prepare_publishers()

    def eventin_handler(self, msg):
        rospy.loginfo('eventin msg received, data = %s', msg.data)

    def image_handler(self, msg):
        rospy.loginfo('image msg received')

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

        
