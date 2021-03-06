#!/usr/bin/env python
"""ROS node for the API.ai natural language understanding. It listens to the 'speech' topic, 
on which a string with a sentence must be published. It tries to process this string using 
api.ai. The processed data is published as a json string on the 'command' topic."""

import rospy
import apiai

from std_msgs.msg import String

# Authentication
SESSION_ID = ''

class ApiaiNode(object):
    def __init__(self):
        rospy.init_node('apiai_node')
        rospy.Subscriber("speech", String, self.speech_callback, queue_size=10)
        try:
            CLIENT_ACCESS_TOKEN = rospy.get_param("~client_access_token")
        except Exception as e:
            rospy.logfatal("Missing required ROS parameter client_access_token")
            exit(1)

        self.ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

        self.result_pub = rospy.Publisher("command", String, queue_size=10)

    def speech_callback(self, msg):
        self.request = self.ai.text_request()
        self.request.query = msg.data

        rospy.logdebug("Waiting for response...")
        response = self.request.getresponse()
        rospy.logdebug("Got response, and publishing it.")

        result_msg = String()
        result_msg.data = response.read()

        self.result_pub.publish(result_msg)

if __name__ == "__main__":
    apiai_node = ApiaiNode()
    rospy.spin()