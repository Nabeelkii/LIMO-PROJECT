#!/usr/bin/env python

import tf
import rospy
import actionlib
from tf.transformations import *
from std_srvs.srv import Empty
from nav_msgs.msg import Odometry
from geometry_msgs.msg import *
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionlib_msgs.msg import GoalID
from threading import *

rospy.init_node('limo_navigator_node')
Transmit = actionlib.SimpleActionClient('move_base',MoveBaseAction)
rospy.loginfo("Connecting to move_base...")
Transmit.wait_for_server()
rospy.loginfo("Connected to move_base!")

Locations=[[0.00118075589623,-0.0398973047257, 0.00338845157115,0.999994259181], #Center[0]
[-1.20054027758,1.75484936808,0.330264185501,0.943888535673],	#Fort Siloso[1]
[0.079300001398,1.44235297321,-0.119827715265,0.992794701162], #USS[2]
[1.13045238755,1.13657079761,-0.636382312471,0.771373808458],  #Wings of Time[3]
[1.18543553772,0.0656192645706,-0.633586216209,0.773672092446],   #Entrance[4]
[1.01032632416,-1.44291227146,-0.890632529673,0.454723759098], #Aquarium[5]
[-0.544453788484,-1.2554029761,0.994663230146,0.103174893245], #Adventure Cove[6]
[-1.62296689727,-0.797907988253,0.760548856966,0.649280706757],  #iFly[7]
[-1.60073027418,0.552269191547,0.652811545718,0.757520353375]]#Merlion[8]


	

def unstuckf(): 
	pub = rospy.Publisher('/initalpose', PoseWithCovarianceStamped, queue_size=2)
	message = rospy.wait_for_message('/odom', Odometry, timeout=1.0)
	x = message.pose.pose.position.x
	y = message.pose.pose.position.y
	z = message.pose.pose.position.z
	roll, pitch, yaw = euler_from_quaternion([message.pose.pose.orientation.x, message.pose.pose.orientation.y, message.pose.pose.orientation.z, message.pose.pose.orientation.w])
    	initial_pose = PoseWithCovarianceStamped()
    	initial_pose.header.frame_id = 'map'
    	initial_pose.pose.pose.position.x = x + 10
    	initial_pose.pose.pose.position.y = y + 0.1
    	initial_pose.pose.pose.position.z = z
    	angular = quaternion_from_euler(0, 0, yaw)
    	initial_pose.pose.pose.orientation.x = angular[0]
    	initial_pose.pose.pose.orientation.y = angular[1]
    	initial_pose.pose.pose.orientation.z = angular[2]
    	initial_pose.pose.pose.orientation.w = angular[3]
    	pub.publish(initial_pose)




def unstuckb():
	pub = rospy.Publisher('/initalpose', PoseWithCovarianceStamped, queue_size=2)
	message = rospy.wait_for_message('/odom', Odometry, timeout=1.0)
	x = message.pose.pose.position.x
	y = message.pose.pose.position.y
	z = message.pose.pose.position.z
	roll, pitch, yaw = euler_from_quaternion([message.pose.pose.orientation.x, message.pose.pose.orientation.y, message.pose.pose.orientation.z, message.pose.pose.orientation.w])
    	initial_pose = PoseWithCovarianceStamped()
    	initial_pose.header.frame_id = 'map'
    	initial_pose.pose.pose.position.x = x - 0.1
    	initial_pose.pose.pose.position.y = y - 0.1
    	initial_pose.pose.pose.position.z = z
    	angular = quaternion_from_euler(0, 0, yaw)
    	initial_pose.pose.pose.orientation.x = angular[0]
    	initial_pose.pose.pose.orientation.y = angular[1]
    	initial_pose.pose.pose.orientation.z = angular[2]
    	initial_pose.pose.pose.orientation.w = angular[3]
    	pub.publish(initial_pose)
	

def unstuckl(): 
	pub = rospy.Publisher('/initalpose', PoseWithCovarianceStamped, queue_size=2)
	message = rospy.wait_for_message('/odom', Odometry, timeout=1.0)
	x = message.pose.pose.position.x
	y = message.pose.pose.position.y
	z = message.pose.pose.position.z
	roll, pitch, yaw = euler_from_quaternion([message.pose.pose.orientation.x, message.pose.pose.orientation.y, message.pose.pose.orientation.z, message.pose.pose.orientation.w])
    	initial_pose = PoseWithCovarianceStamped()
    	initial_pose.header.frame_id = 'map'
    	initial_pose.pose.pose.position.x = x + 0.1
    	initial_pose.pose.pose.position.y = y - 0.1
    	initial_pose.pose.pose.position.z = z
    	angular = quaternion_from_euler(0, 0, yaw)
    	initial_pose.pose.pose.orientation.x = angular[0]
    	initial_pose.pose.pose.orientation.y = angular[1]
    	initial_pose.pose.pose.orientation.z = angular[2]
    	initial_pose.pose.pose.orientation.w = angular[3]
    	pub.publish(initial_pose)


def unstuckr():
	pub = rospy.Publisher('/initalpose', PoseWithCovarianceStamped, queue_size=2)
	message = rospy.wait_for_message('/odom', Odometry, timeout=1.0)
	x = message.pose.pose.position.x
	y = message.pose.pose.position.y
	z = message.pose.pose.position.z
	roll, pitch, yaw = euler_from_quaternion([message.pose.pose.orientation.x, message.pose.pose.orientation.y, message.pose.pose.orientation.z, message.pose.pose.orientation.w])
    	initial_pose = PoseWithCovarianceStamped()
    	initial_pose.header.frame_id = 'map'
    	initial_pose.pose.pose.position.x = x - 0.1
    	initial_pose.pose.pose.position.y = y + 0.1
    	initial_pose.pose.pose.position.z = z
    	angular = quaternion_from_euler(0, 0, yaw)
    	initial_pose.pose.pose.orientation.x = angular[0]
    	initial_pose.pose.pose.orientation.y = angular[1]
    	initial_pose.pose.pose.orientation.z = angular[2]
    	initial_pose.pose.pose.orientation.w = angular[3]
    	pub.publish(initial_pose)

def SetOdom(): #Localise by odom
	global pub
	message = rospy.wait_for_message('/odom', Odometry, timeout=1.0)
	x = message.pose.pose.position.x
	y = message.pose.pose.position.y
	z = message.pose.pose.position.z
	roll, pitch, yaw = euler_from_quaternion([message.pose.pose.orientation.x, message.pose.pose.orientation.y, message.pose.pose.orientation.z, message.pose.pose.orientation.w])
    	initial_pose = PoseWithCovarianceStamped()
    	initial_pose.header.frame_id = 'map'
    	initial_pose.pose.pose.position.x = x
    	initial_pose.pose.pose.position.y = y
    	initial_pose.pose.pose.position.z = z
    	angular = quaternion_from_euler(0, 0, yaw)
    	initial_pose.pose.pose.orientation.x = angular[0]
    	initial_pose.pose.pose.orientation.y = angular[1]
    	initial_pose.pose.pose.orientation.z = angular[2]
    	initial_pose.pose.pose.orientation.w = angular[3]
    	pub.publish(initial_pose)

def setamcl():
	global pub
	message = rospy.wait_for_message('/amcl_pose', PoseWithCovarianceStamped, timeout=1.0)
	x = message.pose.pose.position.x
	y = message.pose.pose.position.y
	z = message.pose.pose.position.z
	roll, pitch, yaw = euler_from_quaternion([message.pose.pose.orientation.x, message.pose.pose.orientation.y, message.pose.pose.orientation.z, message.pose.pose.orientation.w])
    	initial_pose = PoseWithCovarianceStamped()
    	initial_pose.header.frame_id = 'map'
    	initial_pose.pose.pose.position.x = x
    	initial_pose.pose.pose.position.y = y
    	initial_pose.pose.pose.position.z = z
    	angular = quaternion_from_euler(0, 0, yaw)
    	initial_pose.pose.pose.orientation.x = angular[0]
    	initial_pose.pose.pose.orientation.y = angular[1]
    	initial_pose.pose.pose.orientation.z = angular[2]
    	initial_pose.pose.pose.orientation.w = angular[3]
    	pub.publish(initial_pose)


	
def Setpose():   
    Position=rospy.ServiceProxy('/global_localization', Empty)
    resp1=Position()
    return resp1

def Clearmap():
    Clearing=rospy.ServiceProxy('/move_base/clear_costmaps', Empty)
    resp1=Clearing()
    return resp1

def Cancelmove():
    pub = rospy.Publisher('/move_base/cancel', GoalID, queue_size=2)
    message=GoalID()
    pub.publish(message)


def Transmit_MoveBase(pos): 
    global Locations
    pos=Locations[pos]
    Clearmap()
    global checkpoint
    checkpoint = MoveBaseGoal()
    checkpoint.target_pose.header.frame_id = "map"
    checkpoint.target_pose.header.stamp = rospy.Time.now()   
    checkpoint.target_pose.pose.position.x = pos[0]
    checkpoint.target_pose.pose.position.y = pos[1]
    checkpoint.target_pose.pose.position.z = 0.0
    #quaternion = tf.transformations.quaternion_from_euler(0.0, 0.0, pos[2])
    checkpoint.target_pose.pose.orientation.x = 0.0
    checkpoint.target_pose.pose.orientation.y = 0.0
    checkpoint.target_pose.pose.orientation.z = pos[2]
    checkpoint.target_pose.pose.orientation.w = pos[3]
    def sendgoal():
    	Transmit.send_goal(checkpoint)
    	wait = Transmit.wait_for_result()
        if not wait:
        	rospy.logerr("Action server not available!")
        	rospy.signal_shutdown("Action server not available!")
        else:
        	return Transmit.get_result()
    t1=Thread(target=sendgoal)
    t1.start()



if __name__ == '__main__':
    try:	
	pub = rospy.Publisher('/initialpose', PoseWithCovarianceStamped, queue_size=2)
	SetOdom()	
	var = raw_input("Enter Location: ") 
	goal=False
	while var!="stop":
		if (len(var)==1 and var.isdigit() and int(var)<9):
			print "Location Registered"
			goal = Transmit_MoveBase(int(var))	
		elif(var=="unstuckf"):
			goal=True
			unstuckf()
		elif(var=="unstuckb"):
			goal=True
			unstuckb()
		elif(var=="unstuckl"):
			goal=True
			unstuckl()
		elif(var=="unstuckr"):
			goal=True
			unstuckr()
		elif(var=="A"):
			goal=True
			setamcl()
		elif(var=="G"):
			goal=True
			Setpose()
        	elif(var=="O"):
			goal=True
			SetOdom()
		elif(var=="C"):
			goal=True
			Clearmap()
		elif(var=="S"):
			goal=True
			Cancelmove()
		else:
			print "Failed to Identify Location"
			goal=True		
        	if goal:
        		rospy.loginfo("Checkpoint Reached!")
			goal=True
		var = raw_input("Enter Location: ") 
	
		                   
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation Terminated.")
