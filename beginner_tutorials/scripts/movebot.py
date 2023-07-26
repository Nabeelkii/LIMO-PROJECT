#!/usr/bin/env python

#rostopic  pub -1 cmd_vel geometry_msgs/Twist -- '[-2.0, 0.0, 0.0]' '[0.0, 0.0, 1.8]'

import rospy
from std_msgs.msg import String
from gazebo_msgs.msg import ModelStates
from geometry_msgs.msg import Twist

def pose_callback(robotpose):
    cmd=Twist()
    rospy.loginfo("%s",robotpose.pose[2].position.y)
    if robotpose.pose[2].position.y<-2:
        cmd.linear.x=-2
    else:
        cmd.linear.x=2
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)   
    pub.publish(cmd)


def mover():
    rospy.init_node('mover')    
    #rate = rospy.Rate(10) # 10hz
    sub=rospy.Subscriber('gazebo/model_states',ModelStates,pose_callback)
    rospy.spin()
    
    
        
        

if __name__ == '__main__':
    try:
        #pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)   
        mover()
    except rospy.ROSInterruptException:
        pass

'''
def move(dur,linX,linY,linZ,varx,vary,varz): #speed,angle,duration
    twist = Twist()  
    for i in range(2):
        twist.angular.x=varx
        twist.angular.y=vary
        twist.angular.z=varz
        twist.linear.x=linX
        twist.linear.y=linY
        twist.linear.z=linZ
        pub.publish(twist)
        time.sleep(dur)
    for i in range(1):
        twist.angular.x=0
        twist.angular.y=0
        twist.angular.z=0
        twist.linear.x=0
        twist.linear.y=0
        twist.linear.z=0
        pub.publish(twist)
        time.sleep(1)
    return 
'''