#! /usr/bin/env python

import rospy
import actionlib
from tf.transformations import *
from move_base_msgs.msg import MoveBaseGoal, MoveBaseAction
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseWithCovarianceStamped
import Tkinter as tk


class Controller:
	def __init__(self):
		rospy.init_node("LIMO_Controller")
		rospy.loginfo("LIMO controller booting up ...")
		self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
		rospy.loginfo("move_base client starting up ...")
		self.client.wait_for_server()
		self.pos =[[0.0651344915017,-0.0133403160225, -0.00816222094885,0.99996668852], #Center[0]
		[1.61837289788,1.23199670596,-0.583510755675,0.812105410653],	#Fort Siloso[1]
		[1.48288601918,0.00517570756873,-0.792584507936,0.60976208293], #USS[2]
		[1.12778313766,-1.24645975567,-0.916538530527,0.399946398983],  #Wings of Time[3]
		[-0.132610580053,-1.25746317146,0.997508119638,0.0705517629505],   #Entrance[4]
		[-1.65347043849,-1.24254259271,0.725588306756,0.688129064274], #Aquarium[5]
		[-1.38411079799,0.0593315230826,0.642864813097,0.765979655135], #Adventure Cove[6]
		[-1.22812245955,1.14741622896,0.492143834655,0.870513897655],  #iFly[7]
		[0.149719823001,1.53048865858,-0.0894002471666,0.995995781018]]#Merlion[8]
		self.Pub = rospy.Publisher('/initialpose', PoseWithCovarianceStamped, queue_size=1)
		window = tk.Tk()
		button0 = tk.Button(window, text='Origin', command=self.Origin_callback)
		button0.pack()
		button1 = tk.Button(window, text='Zone1', command=self.Zone1_callback)
		button1.pack()
		button2 = tk.Button(window, text='Zone2', command=self.Zone2_callback)
		button2.pack()
		button3 = tk.Button(window, text='Zone3', command=self.Zone3_callback)
		button3.pack()
		button4 = tk.Button(window, text='Zone4', command=self.Zone4_callback)
		button4.pack()
		button5 = tk.Button(window, text='Zone5', command=self.Zone5_callback)
		button5.pack()
		button6 = tk.Button(window, text='Zone6', command=self.Zone6_callback)
		button6.pack()
		button7 = tk.Button(window, text='Zone7', command=self.Zone7_callback)
		button7.pack()
		button8 = tk.Button(window, text='Zone8', command=self.Zone8_callback)
		button8.pack()
		window.mainloop()
		rospy.spin()


	def 

	def set_initial_pose(self):
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
    		self.Pub.publish(initial_pose)

	def transmission(self, pos):
		goal = MoveBaseGoal()
		goal.target_pose.header.frame_id='map'
		goal.target_pose.pose.position.x=pos[0]
		goal.target_pose.pose.position.y=pos[1]
		goal.target_pose.pose.position.z=0.0
		goal.target_pose.pose.orientation.x=0.0
		goal.target_pose.pose.orientation.y=0.0
		goal.target_pose.pose.orientation.z=pos[2]
		goal.target_pose.pose.orientation.w=pos[3]
		self.client.send_goal(goal)
		self.client.wait_for_result()
		if self.client.get_sate() == actionlib.GoalStatus.SUCCEEDED:
			rospy.loginfo('reached waypoint')
		else:
			rospy.loginfo('fail to reach waypoint')

	def Origin_callback(self):
		rospy.loginfo("setting initial pose of LIMO robot")
		self.set_initial_pose()
		rospy.loginfo("moving to goal point")
		self.transmission(self.pos[0])

	def Zone1_callback(self):
		rospy.loginfo("setting initial pose of LIMO robot")
		self.set_initial_pose()
		rospy.loginfo("moving to goal point")
		self.transmission(self.pos[1])

	def Zone2_callback(self):
		rospy.loginfo("setting initial pose of LIMO robot")
		self.set_initial_pose()
		rospy.loginfo("moving to goal point")
		self.transmission(self.pos[2])

	def Zone3_callback(self):
		rospy.loginfo("setting initial pose of LIMO robot")
		self.set_initial_pose()
		rospy.loginfo("moving to goal point")
		self.transmission(self.pos[3])

	def Zone4_callback(self):
		rospy.loginfo("setting initial pose of LIMO robot")
		self.set_initial_pose()
		rospy.loginfo("moving to goal point")
		self.transmission(self.pos[4])

	def Zone5_callback(self):
		rospy.loginfo("setting initial pose of LIMO robot")
		self.set_initial_pose()
		rospy.loginfo("moving to goal point")
		self.transmission(self.pos[5])

	def Zone6_callback(self):
		rospy.loginfo("setting initial pose of LIMO robot")
		self.set_initial_pose()
		rospy.loginfo("moving to goal point")
		self.transmission(self.pos[6])

	def Zone7_callback(self):
		rospy.loginfo("setting initial pose of LIMO robot")
		self.set_initial_pose()
		rospy.loginfo("moving to goal point")
		self.transmission(self.pos[7])

	def Zone8_callback(self):
		rospy.loginfo("setting initial pose of LIMO robot")
		self.set_initial_pose()
		rospy.loginfo("moving to goal point")
		self.transmission(self.pos[8])

if __name__ == '__main__':
	try:
		Controller()
	except rospy.ROSInterruptException:
		pass























