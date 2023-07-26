#!/usr/bin/env python

import time                                                                 # python time library
import rospy                                                                # python rospy library
import actionlib                                                            # ROS actionlib library
from tf.transformations import *                                            # ROS melodic transformation library
from std_srvs.srv import Empty                                              # Empty datatype from std_msgs.msg 
from nav_msgs.msg import Odometry                                           # Odometry datatype from nav_msgs.msg           
from geometry_msgs.msg import *                                             # all datatype from geometry_msgs.msg 
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal                 # move_base action messages
from actionlib_msgs.msg import GoalID                                       # GoalID datatype from actionlib_msgs.msg 
import Tkinter as tk                                                        # Tkinter python library
from threading import *                                                     # threading python library

# Initialize the node as limo_navigator_node and start up the action server
rospy.init_node('limo_navigator_node')
Transmit = actionlib.SimpleActionClient('move_base',MoveBaseAction)
rospy.loginfo("Connecting to move_base...")
Transmit.wait_for_server()
rospy.loginfo("Connected to move_base!")

# 8 waypoints for the limo to navigate to, position x,y and orientation z,w
Locations=[[0.067974713851,-0.0650388809978,0.720975515893,0.692960536742], # center waypoint at origin
[1.71546372374,1.21678855105,-0.734646091504,0.678450528954],               # Zone 1, Fort Siloso waypoint
[1.48785510148, 0.057853535204,-0.832395625637,0.554181849595],             # Zone 2, Universal Studio Singapore waypoint
[1.15036511409,-1.49419650198,-0.991729772925,0.128343513641],              # Zone 3, Wings of Time waypoint
[0.0811615051857,-1.31634785141,0.996705343698,0.0811076928827],            # Zone 4, Sentosa Entrance waypoint (RAMP)
[-1.71400100641,-1.24356925127,0.809531684505,0.587076189078],              # Zone 5, SEA Aquarium waypoint
[-1.43863442466,0.127779450346,0.632459158467,0.774593708257],              # Zone 6, Aventure Cove waypoint
[-1.03745437851,1.43108833029,0.0130347026953,0.999915044654],              # Zone 7, IFly waypoint 
[0.0781221002446,1.67085428298,-0.0237610190226,0.999717667132]]            # Zone 8, Merlion waypoint (ROUNDABOUT)

# Localise by odometry data
# Odometry is the use of data from motion sensors to estimate change in position over time
def setodom(): 
	pub = rospy.Publisher('/initialpose', PoseWithCovarianceStamped, queue_size=2)          # To publish to ROS topic '/initialpose' to localise robot based on robotic platform
	message = rospy.wait_for_message('/odom', Odometry, timeout=1.0)                        # Read Odometry message from ROS topic '/odom' when function is being called
	x = message.pose.pose.position.x    
	y = message.pose.pose.position.y    
	z = message.pose.pose.position.z    
	roll, pitch, yaw = euler_from_quaternion([message.pose.pose.orientation.x, message.pose.pose.orientation.y, message.pose.pose.orientation.z, message.pose.pose.orientation.w]) 
        initial_pose = PoseWithCovarianceStamped()          # initialize object as ROS datatype PoseWithCovarianceStamped
        initial_pose.header.frame_id = 'map'                # set frame_id as 'map'
        initial_pose.pose.pose.position.x = x               # retrieve position.x from message
        initial_pose.pose.pose.position.y = y               # retrieve position.y from message
        initial_pose.pose.pose.position.z = z               # retrieve position.z from message
        angular = quaternion_from_euler(0, 0, yaw)
        initial_pose.pose.pose.orientation.x = angular[0]   # retrieve orientation.x from message
        initial_pose.pose.pose.orientation.y = angular[1]   # retrieve orientation.y from message
        initial_pose.pose.pose.orientation.z = angular[2]   # retrieve orientation.z from message
        initial_pose.pose.pose.orientation.w = angular[3]   # retrieve orientation.w from message
        pub.publish(initial_pose)

# function to call '/global_localization' service to try and localize the ROS platform
def setglobpose():   
    Position=rospy.ServiceProxy('/global_localization', Empty)
    resp1=Position()
    return resp1

# Localise by AMCL data
# AMCL is a probabilistic localization system for a robot moving in 2D
# It implements the adaptive (or KLD-sampling) Monte Carlo localization approach, which uses a particle filter to track the pose of a robot against a known map.
def setamcl():
	pub = rospy.Publisher('/initialpose', PoseWithCovarianceStamped, queue_size=2)               # To publish to ROS topic '/initialpose' to localise robot based on robotic platform
	message = rospy.wait_for_message('/amcl_pose', PoseWithCovarianceStamped, timeout=1.0)       # Read AMCL message from ROS topic '/amcl_pose' when function is being called
	x = message.pose.pose.position.x
	y = message.pose.pose.position.y
	z = message.pose.pose.position.z
	roll, pitch, yaw = euler_from_quaternion([message.pose.pose.orientation.x, message.pose.pose.orientation.y, message.pose.pose.orientation.z, message.pose.pose.orientation.w])
        initial_pose = PoseWithCovarianceStamped()          # initialize object as ROS datatype PoseWithCovarianceStamped
    	initial_pose.header.frame_id = 'map'                # set frame_id as 'map'
    	initial_pose.pose.pose.position.x = x               # retrieve position.x from message
    	initial_pose.pose.pose.position.y = y               # retrieve position.y from message
    	initial_pose.pose.pose.position.z = z               # retrieve position.z from message
    	angular = quaternion_from_euler(0, 0, yaw)
    	initial_pose.pose.pose.orientation.x = angular[0]   # retrieve orientation.x from message
    	initial_pose.pose.pose.orientation.y = angular[1]   # retrieve orientation.y from message
    	initial_pose.pose.pose.orientation.z = angular[2]   # retrieve orientation.z from message
    	initial_pose.pose.pose.orientation.w = angular[3]   # retrieve orientation.w from message
    	pub.publish(initial_pose)
    
# function to call '/move_base/clear_costmaps' service to clear the dynamic local map generated by the ROS platform
def Clearmap():
    Clearing=rospy.ServiceProxy('/move_base/clear_costmaps', Empty)
    resp1=Clearing()
    return resp1

ismoving=False # cleck flag if robot is moving or not

# function to stop the ROS robotic platform
def Cancelmove():
    global ismoving
    ismoving=False
    global sub
    sub.unregister()
    pub = rospy.Publisher('/move_base/cancel', GoalID, queue_size=2) # publish to ROS topic '/move_base/cancel' to stop ROS platform
    message=GoalID()
    pub.publish(message)
    status.config(text="Move stopped")

# Function to use actionlib to make ROS platform move to intended waypoints
def Transmit_MoveBase(pos): 
    global status
    status.config(text=("Moving to Zone"+str(pos)))
    global Locations
    pos=Locations[pos]                                      # check for waypoints
    Clearmap()                                              # clear maps
    global checkpoint
    checkpoint = MoveBaseGoal()                             # create MoveBaseGoal object
    checkpoint.target_pose.header.frame_id = "map"          # set frame_id to 'map'
    checkpoint.target_pose.header.stamp = rospy.Time.now()  # timestamped
    checkpoint.target_pose.pose.position.x = pos[0]         # set x positon coordinate to pos[0] value
    checkpoint.target_pose.pose.position.y = pos[1]         # set y positon coordinate to pos[1] value
    checkpoint.target_pose.pose.position.z = 0.0            # set z positon coordinate to 0.0
    checkpoint.target_pose.pose.orientation.x = 0.0         # set x orientation coordinate to 0.0
    checkpoint.target_pose.pose.orientation.y = 0.0         # set x orientation coordinate to 0.0
    checkpoint.target_pose.pose.orientation.z = pos[2]      # set x orientation coordinate to pos[2] value
    checkpoint.target_pose.pose.orientation.w = pos[3]      # set x orientation coordinate to pos[3] value
    
    # Sub-function is called under function Transmit_MoveBase to use actionlib to send the robotic platform to the selected waypint
    def sendgoal():
        global ismoving,x
        x=0
        ismoving=True #addition       
        Transmit.send_goal(checkpoint) # Move to selected waypoint
        wait = Transmit.wait_for_result() # Wait for the motion to finish
        status.config(text="Move Complete")
        ismoving=False   #addition
        sub.unregister() #addition        
        return 
    
    # Callback function is called when certain conditions are met to make the ROS platform to force its recovery
    def callrecover(data):
        global x       
        if data.linear.x==0 and data.linear.y==0 and data.linear.z==0 and data.angular.x==0 and data.angular.y==0 and data.angular.z==0 and ismoving:
            rospy.loginfo(str(x))
            time.sleep(2)
            x=x+1
        else:
            x=0
        if x>5:
            Clearmap()  # clearmap
            rospy.loginfo("Clearmap")
            x=0
        
     
    global sub 
    sub=rospy.Subscriber("cmd_vel", Twist, callrecover) # recovery action
    t1=Thread(target=sendgoal) # navigation action
    t1.start()    

# create a navigation controller using Tkinter GUI
border=tk.Tk()
border.title("Move")
frame=tk.Frame(border)
frame.grid()
buttonC=tk.Button(frame,text='Clearmap',command=Clearmap)                       # clearmap button
buttonC.grid(row=0,columnspan=2,column=0,sticky="NESW")
buttonC=tk.Button(frame,text='Stop',command=Cancelmove,bg="red")                # estop button
buttonC.grid(row=0,columnspan=3,column=2,sticky="NESW")
buttonO=tk.Button(frame,text='RotateCar',command=Rotatecar)                     # rotation button
buttonO.grid(row=0,column=5,sticky="NESW")
buttonG=tk.Button(frame,text='GlobPose',command=setglobpose)                    # global localisation button
buttonG.grid(row=0,column=6,sticky="NESW")
buttonA=tk.Button(frame,text='AmclPose',command=setamcl)                        # amcl localisation button
buttonA.grid(row=0,column=7,sticky="NESW")
buttonO=tk.Button(frame,text='OdomPose',command=setodom)                        # odom localisation button
buttonO.grid(row=0,column=8,sticky="NESW")



button0=tk.Button(frame,text='Center',command= lambda:Transmit_MoveBase(0) )    # origin waypoint button
button0.grid(row=1,column=0,sticky="NESW")
button1=tk.Button(frame,text='Zone1',command= lambda:Transmit_MoveBase(1) )     # Fort Siloso button
button1.grid(row=1,column=1,sticky="NESW")
button2=tk.Button(frame,text='Zone2',command= lambda:Transmit_MoveBase(2) )     # Universal Studio Singapore button
button2.grid(row=1,column=2,sticky="NESW")
button3=tk.Button(frame,text='Zone3',command= lambda:Transmit_MoveBase(3) )     # Wing of Time button
button3.grid(row=1,column=3,sticky="NESW")
button4=tk.Button(frame,text='Zone4',command= lambda:Transmit_MoveBase(4) )     # Sentosa Entrance button
button4.grid(row=1,column=4,sticky="NESW")
button5=tk.Button(frame,text='Zone5',command= lambda:Transmit_MoveBase(5) )     # SEA Aquarium button
button5.grid(row=1,column=5,sticky="NESW")
button6=tk.Button(frame,text='Zone6',command= lambda:Transmit_MoveBase(6) )     # Adventure Cove button
button6.grid(row=1,column=6,sticky="NESW")
button7=tk.Button(frame,text='Zone7',command= lambda:Transmit_MoveBase(7) )     # IFly button
button7.grid(row=1,column=7,sticky="NESW")
button8=tk.Button(frame,text='Zone8',command= lambda:Transmit_MoveBase(8) )     # Merlion button
button8.grid(row=1,column=8,sticky="NESW")
exit_button=tk.Button(frame,text='Quit',command=quit)                           # exit controller button
exit_button.grid(row=2,columnspan=9,sticky="NESW")
status =tk.Label(frame,text="No button pressed")
status.grid(row=3)
border.mainloop()






    
