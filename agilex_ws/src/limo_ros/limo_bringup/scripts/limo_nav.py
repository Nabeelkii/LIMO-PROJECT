#!/usr/bin/env python

import tf
import rospy
import actionlib
from nav_msgs.msg import Odometry
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

rospy.init_node('limo_navigator_node')
Transmit = actionlib.SimpleActionClient('move_base',MoveBaseAction)
rospy.loginfo("Connecting to move_base...")
Transmit.wait_for_server()
rospy.loginfo("Connected to move_base!")

Locations = [(0.211, 0.762, 1.513),(-0.579, 1.853 ,1.487),(-0.390, 2.929 ,1.650),(0.198, 5.044, 1.567) ]


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
        pos = (0.211, 0.762, 1.513)
        goal = Transmit_MoveBase(pos)
        if goal:
            rospy.loginfo("1st Checkpoint Reached!")

        pos = (-0.579, 1.853 ,1.487)
        goal = Transmit_MoveBase(pos)
        if goal:
            rospy.loginfo("2nd Checkpoint Reached!")

        pos = (-0.390, 2.929 ,1.650)
        goal = Transmit_MoveBase(pos)
        if goal:
            rospy.loginfo("3rd Checkpoint Reached!")

        pos = (0.198, 5.044, 1.567)
        goal = Transmit_MoveBase(pos)
        if goal:
            rospy.loginfo("4th Checkpoint Reached!")

    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation Terminated.")
