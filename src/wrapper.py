#!/usr/bin/env python
import os
import rospkg
import roslib, rospy
from datetime import datetime
from laser_analysis.msg import Analysis4MetersMsg
from radio_services.srv import InstructionAndStringWithAnswer

robot_id = 0
logs_path = ''
hpr_sub = None
rospack = None
running = False
analysis_topic = ''

def init():
    global robot_id, logs_path, analysis_topic, hpr_sub, rospack
    rospy.init_node('hpr_wrapper')
    analysis_topic = rospy.get_param("~analysis_topic", "/laser_analysis/results4meters")
    robot_id = rospy.get_param("~robot_id", 0)
    rospy.Service('/hpr_wrapper/node_state_service', InstructionAndStringWithAnswer, nodeStateCallback)
    rospack = rospkg.RosPack()
    if running:
        hpr_sub = rospy.Subscriber(analysis_topic, Analysis4MetersMsg, analysisCallback)
    while not rospy.is_shutdown():
        rospy.spin()

def nodeStateCallback(req):
    global running, hpr_sub, logs_path
    if req.command == 0 and running:
        running = False
        hpr_sub.unregister()
        print 'Stopped hpr wrapper!'
    elif req.command == 1 and not running:
        dt = datetime.now()
        current_name = req.name
        filename = 'official_log_walk_'+current_name+'_'+datetime.today().strftime("%d-%m-%Y")+'_'+dt.strftime("%H%M%S")+'.csv'
        logs_path = rospack.get_path('hpr_wrapper') + '/logs/' + filename
        hpr_sub = rospy.Subscriber(analysis_topic, Analysis4MetersMsg, analysisCallback)
        running = True
        with open(logs_path,'ab+') as f:
            f.write("Human ID, Distance, Time for 4 meters\n")
        print 'Started hpr wrapper!'
    return running

def analysisCallback(msg):
    global logs_path, robot_id
    with open(logs_path,'ab+') as f:
        f.write(str(msg.human_id)+',')
        f.write(str(msg.distance)+',')
        f.write(str(msg.time_needed)+'\n')

if __name__ == '__main__':
    init()