#!/usr/bin/env python

#Limo navigation with recovery behaviour

import tf
import time
import rospy
import actionlib
from tf.transformations import *
from std_srvs.srv import Empty
from nav_msgs.msg import Odometry
from geometry_msgs.msg import *
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionlib_msgs.msg import GoalID
import Tkinter as tk
from threading import *

rospy.init_node('limo_navigator_node')
Transmit = actionlib.SimpleActionClient('move_base',MoveBaseAction)
rospy.loginfo("Connecting to move_base...")
Transmit.wait_for_server()
rospy.loginfo("Connected to move_base!")

#Coordinates
Locations=[[0.067974713851,-0.0650388809978,0.720975515893,0.692960536742],
[1.71546372374,1.21678855105,-0.734646091504,0.678450528954],
[1.48785510148, 0.057853535204,-0.832395625637,0.554181849595], 
[1.15036511409,-1.49419650198,-0.991729772925,0.128343513641],
[0.0811615051857,-1.31634785141,0.996705343698,0.0811076928827],
[-1.71400100641,-1.24356925127,0.809531684505,0.587076189078],
[-1.43863442466,0.127779450346,0.632459158467,0.774593708257],
[-1.03745437851,1.43108833029,0.0130347026953,0.999915044654],[0.0781221002446,1.67085428298,-0.0237610190226,0.999717667132]]



def setodom(): #Localise by odom
	pub = rospy.Publisher('/initialpose', PoseWithCovarianceStamped, queue_size=2)
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

def setamcl(): #Localise by amcl
	pub = rospy.Publisher('/initialpose', PoseWithCovarianceStamped, queue_size=2)
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


#Calling a service
def setglobpose():   
    Position=rospy.ServiceProxy('/global_localization', Empty)
    resp1=Position()
    return resp1


def Rotatecar():
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=2)
    Rotate=Twist()
    Rotate.linear.x=0
    Rotate.linear.y=0
    Rotate.linear.z=0
    Rotate.angular.x=0
    Rotate.angular.y=0
    Rotate.angular.z=1
    for i in range(10):
     pub.publish(Rotate)
     time.sleep(0.1)
    
     
def Clearmap():
    Clearing=rospy.ServiceProxy('/move_base/clear_costmaps', Empty)
    resp1=Clearing()
    return resp1

ismoving=False
def Cancelmove():
    global ismoving
    ismoving=False
    global sub
    sub.unregister()
    pub = rospy.Publisher('/move_base/cancel', GoalID, queue_size=2)
    message=GoalID()
    pub.publish(message)
    status.config(text="Move stopped")



def Transmit_MoveBase(pos): 
    global status
    status.config(text=("Moving to Zone"+str(pos)))
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
        global ismoving,x
        x=0
        ismoving=True #addition       
        Transmit.send_goal(checkpoint)
        wait = Transmit.wait_for_result()
        status.config(text="Move Complete")
        ismoving=False   #addition
        sub.unregister() #addition        
        return 

    def callrecover(data): #Recovery behaviour,check if car velocity is 0 every few seconds for x
        global x       
        if data.linear.x==0 and data.linear.y==0 and data.linear.z==0 and data.angular.x==0 and data.angular.y==0 and data.angular.z==0 and ismoving:
            rospy.loginfo(str(x))
            time.sleep(2)
            x=x+1
        else:
            x=0
        if x>5:
            Clearmap()
            Rotatecar()
            rospy.loginfo("Clearmap")
            x=0
        
     
    global sub #addition
    sub=rospy.Subscriber("cmd_vel", Twist, callrecover) #addition
    t1=Thread(target=sendgoal)
    t1.start()    
    
   

#GUI
border=tk.Tk()
border.title("Move")
frame=tk.Frame(border)
frame.grid()
buttonC=tk.Button(frame,text='Clearmap',command=Clearmap)
buttonC.grid(row=0,columnspan=2,column=0,sticky="NESW")
buttonC=tk.Button(frame,text='Stop',command=Cancelmove,bg="red")
buttonC.grid(row=0,columnspan=3,column=2,sticky="NESW")
buttonO=tk.Button(frame,text='RotateCar',command=Rotatecar)
buttonO.grid(row=0,column=5,sticky="NESW")
buttonG=tk.Button(frame,text='GlobPose',command=setglobpose)
buttonG.grid(row=0,column=6,sticky="NESW")
buttonA=tk.Button(frame,text='AmclPose',command=setamcl)
buttonA.grid(row=0,column=7,sticky="NESW")
buttonO=tk.Button(frame,text='OdomPose',command=setodom)
buttonO.grid(row=0,column=8,sticky="NESW")



button0=tk.Button(frame,text='Center',command= lambda:Transmit_MoveBase(0) )
button0.grid(row=1,column=0,sticky="NESW")
button1=tk.Button(frame,text='Zone1',command= lambda:Transmit_MoveBase(1) )
button1.grid(row=1,column=1,sticky="NESW")
button2=tk.Button(frame,text='Zone2',command= lambda:Transmit_MoveBase(2) )
button2.grid(row=1,column=2,sticky="NESW")
button3=tk.Button(frame,text='Zone3',command= lambda:Transmit_MoveBase(3) )
button3.grid(row=1,column=3,sticky="NESW")
button4=tk.Button(frame,text='Zone4',command= lambda:Transmit_MoveBase(4) )
button4.grid(row=1,column=4,sticky="NESW")
button5=tk.Button(frame,text='Zone5',command= lambda:Transmit_MoveBase(5) )
button5.grid(row=1,column=5,sticky="NESW")
button6=tk.Button(frame,text='Zone6',command= lambda:Transmit_MoveBase(6) )
button6.grid(row=1,column=6,sticky="NESW")
button7=tk.Button(frame,text='Zone7',command= lambda:Transmit_MoveBase(7) )
button7.grid(row=1,column=7,sticky="NESW")
button8=tk.Button(frame,text='Zone8',command= lambda:Transmit_MoveBase(8) )
button8.grid(row=1,column=8,sticky="NESW")
exit_button=tk.Button(frame,text='Quit',command=quit)
exit_button.grid(row=2,columnspan=9,sticky="NESW")
status =tk.Label(frame,text="No button pressed")
status.grid(row=3)
border.mainloop()
'''
buttonC=tk.Button(topframe,text='Clearmap',command=Clearmap)
buttonC.pack(side=tk.LEFT)
buttonG=tk.Button(topframe,text='SetGlobalPose',command=setglobpose)
buttonG.pack(side=tk.LEFT)
buttonA=tk.Button(topframe,text='SetamclPose',command=setamcl)
buttonA.pack(side=tk.LEFT)
buttonO=tk.Button(topframe,text='SetodomPose',command=setodom)
buttonO.pack(side=tk.LEFT)
buttonu1=tk.Button(topframe,text='unstuck1',command=unstuckf)
buttonu1.pack(side=tk.LEFT)
buttonu2=tk.Button(topframe,text='unstuck2',command=unstuckb)
buttonu2.pack(side=tk.LEFT)


button0=tk.Button(botframe,text='Center',command= lambda:Transmit_MoveBase(Locations[0]) )
button0.pack(side=tk.LEFT)
button1=tk.Button(botframe,text='Zone1',command= lambda:Transmit_MoveBase(Locations[1]) )
button1.pack(side=tk.LEFT)
button2=tk.Button(botframe,text='Zone2',command= lambda:Transmit_MoveBase(Locations[2]) )
button2.pack(side=tk.LEFT)
button3=tk.Button(botframe,text='Zone3',command= lambda:Transmit_MoveBase(Locations[3]) )
button3.pack(side=tk.LEFT)
button4=tk.Button(botframe,text='Zone4',command= lambda:Transmit_MoveBase(Locations[4]) )
button4.pack(side=tk.LEFT)
button5=tk.Button(botframe,text='Zone5',command= lambda:Transmit_MoveBase(Locations[5]) )
button5.pack(side=tk.LEFT)
button6=tk.Button(botframe,text='Zone6',command= lambda:Transmit_MoveBase(Locations[6]) )
button6.pack(side=tk.LEFT)
button7=tk.Button(botframe,text='Zone7',command= lambda:Transmit_MoveBase(Locations[7]) )
button7.pack(side=tk.LEFT)
button8=tk.Button(botframe,text='Zone8',command= lambda:Transmit_MoveBase(Locations[8]) )
button8.pack(side=tk.LEFT)
exit_button=tk.Button(frame,text='Quit',command=quit)
exit_button.pack()
'''






    
