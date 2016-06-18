#!/usr/bin/env python
import roslib, rospy
from laser_analysis.msg import Analysis4MetersMsg
from datetime import datetime
import rospkg

analysis_topic = ''
start_time = 0
logs_path = ''
robot_id = 0

def init():
    global robot_id, logs_path, analysis_topic
    dt = datetime.now()
    start_time = dt.minute*60000000 + dt.second*1000000 + dt.microsecond
    print "start_time = ", start_time
    rospy.init_node('hpr_wrapper')
    analysis_topic = rospy.get_param("~analysis_topic", "/laser_analysis/results4meters")
    robot_id = rospy.get_param("~robot_id", 0)
    rospy.Subscriber(analysis_topic, Analysis4MetersMsg, analysisCallback)
    rospack = rospkg.RosPack()
    logs_path = rospack.get_path('hpr_wrapper')+'/logs/'
    while not rospy.is_shutdown():
        rospy.spin()

def analysisCallback(msg):
    global start_time, logs_path, robot_id
    dt = datetime.now()
    start_time = dt.minute*60000000 + dt.second*1000000 + dt.microsecond
    with open(logs_path+'official_log_'+datetime.today().strftime("%d-%m-%Y")+'.log','ab+') as f:
        f.write('## Robot ID ##\n')
        f.write(str(robot_id)+'\n')
        f.write('## HUMAN ID ##\n')
        f.write(str(msg.human_id)+'\n')
        f.write('## INFO ##\n')
        f.write(str(datetime.now().strftime("[%d-%m-%Y %H:%M:%S] ")) + str(msg.distance) + ' meters in ' + str(msg.time_needed) + ' seconds\n')
        f.write('---\n')

if __name__ == '__main__':
    init()