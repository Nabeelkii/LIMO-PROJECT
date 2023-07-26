#!/usr/bin/env python
import rospy
from std_msgs.msg import String

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I recorded %s", data.data)
    pub = rospy.Publisher('chatter2', String, queue_size=10) 
    pub.publish(data.data)
    
def recorder():  
    rospy.init_node('recorder')         
    sub = rospy.Subscriber("chatter", String, callback)     
    rate = rospy.Rate(10) # 10hz
    rospy.spin()

if __name__ == '__main__':
    try:
        recorder()
    except rospy.ROSInterruptException:
        pass
