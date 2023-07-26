#!/usr/bin/env python

import tf
import rospy
import actionlib
import time
from nav_msgs.msg import Odometry
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

rospy.init_node('limo_navigator_node')
Transmit = actionlib.SimpleActionClient('move_base',MoveBaseAction)
rospy.loginfo("Connecting to move_base...")
Transmit.wait_for_server()
rospy.loginfo("Connected to move_base!")

def Transmit_MoveBase(pos):

    checkpoint = MoveBaseGoal()
    checkpoint.target_pose.header.frame_id = "map"
    checkpoint.target_pose.header.stamp = rospy.Time.now()
    
    checkpoint.target_pose.pose.position.x = pos[0]
    checkpoint.target_pose.pose.position.y = pos[1]
    quaternion = tf.transformations.quaternion_from_euler(0.0, 0.0, pos[2])
    checkpoint.target_pose.pose.orientation.x = quaternion[0]
    checkpoint.target_pose.pose.orientation.y = quaternion[1]
    checkpoint.target_pose.pose.orientation.z = quaternion[2]
    checkpoint.target_pose.pose.orientation.w = quaternion[3]

    Transmit.send_goal(checkpoint)
    wait = Transmit.wait_for_result()
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
        return Transmit.get_result()

if __name__ == '__main__':
    try:
        pos = (-0.4, -1.7, -0.2)#T4
        goal = Transmit_MoveBase(pos)
	time.sleep(1)
        pos = (0.85, -1.9, -3.2)
        goal = Transmit_MoveBase(pos)
	time.sleep(1)
        # REACH 7

        pos = (-2.3, -1.4, 1.4)
        goal = Transmit_MoveBase(pos)
	time.sleep(1)
        pos = (-1.8, 0.3, 1.7)#T2
        goal = Transmit_MoveBase(pos)
	time.sleep(1)
        pos = (-1.65, 1.9, -2)
        goal = Transmit_MoveBase(pos)
	time.sleep(1)
        #REACH 3

        pos = (-1.85, 0.1, -2)#T2
        goal = Transmit_MoveBase(pos)
	time.sleep(1)
        pos = (-2.25, -1.5, -0.2)
        goal = Transmit_MoveBase(pos)
	time.sleep(1)
        #REACH 1

        pos = (-0.2, -1.72, 1.4)#T4
        goal = Transmit_MoveBase(pos)
	time.sleep(1)
        pos = (0, 0, -0.2)
        goal = Transmit_MoveBase(pos)
	time.sleep(1)
        pos = (1.85, -0.6, 1.4)#CS
        goal = Transmit_MoveBase(pos)
	time.sleep(1)
        pos = (1.9, 0.48, 1.4)
        goal = Transmit_MoveBase(pos)
	time.sleep(1)
        #REACH 9   

        pos = (2, 1.35, 0.4)
        goal = Transmit_MoveBase(pos)
	time.sleep(1)
        pos = (2.4, 1.9, 0)
        goal = Transmit_MoveBase(pos)
	time.sleep(1)         
        #REACH TRACK

    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation Terminated.")

