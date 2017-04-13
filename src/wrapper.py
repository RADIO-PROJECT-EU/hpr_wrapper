#!/usr/bin/env python
import os
import rospkg
import roslib, rospy
from datetime import datetime
from laser_analysis.msg import Analysis4MetersMsg

analysis_topic = ''
logs_path = ''
robot_id = 0

def init():
    global robot_id, logs_path, analysis_topic
    rospy.init_node('hpr_wrapper')
    analysis_topic = rospy.get_param("~analysis_topic", "/laser_analysis/results4meters")
    robot_id = rospy.get_param("~robot_id", 0)
    rospy.Subscriber(analysis_topic, Analysis4MetersMsg, analysisCallback)
    rospack = rospkg.RosPack()
    filename = 'official_log_walk_'+datetime.today().strftime("%d-%m-%Y")+'_'+dt.strftime("%H%M%S")+'.csv'
    logs_path = rospack.get_path('hpr_wrapper') + '/logs/' + filename
    while not rospy.is_shutdown():
        rospy.spin()

def analysisCallback(msg):
    global logs_path, robot_id
    first_time = False
    if not os.path.isfile(logs_path):
        first_time = True
    with open(logs_path,'ab+') as f:
        if first_time:
            f.write("Human ID, Distance, Time for 4 meters\n")
        f.write(str(msg.human_id)+',')
        f.write(str(msg.distance)+',')
        f.write(str(msg.time_needed)+'\n')

if __name__ == '__main__':
    init()