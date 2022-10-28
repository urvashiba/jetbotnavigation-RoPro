#!/usr/bin/env python
import rospy
import time
import serial

from std_msgs.msg import String, Int16
<<<<<<< HEAD
from geometry_msgs.msg import Twist
=======

>>>>>>> 621ef2d8fe07abe3f6e1f6fe9ce24d0756d6385e

rospy.set_param("/jetbot_apriltag/goal",0)
rospy.set_param("/jetbot_apriltag/sub_goal",0)
serial_openmv=serial.Serial("/dev/ttyUSB0", 9600, timeout=1)

<<<<<<< HEAD
pub=rospy.Publisher("/jetbot_motors/cmd_raw",Twist)

=======
>>>>>>> 621ef2d8fe07abe3f6e1f6fe9ce24d0756d6385e
def parsestring(data):
	go=0
	rospy.loginfo("data_serial = %s",data)  
	# get tags
	tags=[[0]*5 for i in range(6)]
	dd=data.replace("#","").split(";")
	#rospy.loginfo(dd)  
	for i in range(int(dd[0])):
		for j in range(5):
			tags[i][j%5]=int(dd[i*5+j+1])
	#rospy.loginfo(tags)  
	#
	goal= rospy.get_param("/jetbot_apriltag/goal") 
<<<<<<< HEAD
	for i in range(int(dd[0])):
		rospy.loginfo('goal=%s',goal)
		if goal==0:
			go=0
		elif tags[i][0]==goal:
			go=2
			r=tags[i][1]+tags[i][3]/2
			rospy.loginfo('r=%s',r)			
			if r<280 or r>380 :
				go=4
			elif tags[i][3]>200 :
				go=0
				rospy.set_param("/jetbot_apriltag/goal",0)
			i=int(dd[0])
=======
	sub_goal= rospy.get_param("/jetbot_apriltag/sub_goal") 
	for i in range(int(dd[0])):
		if goal==0:
			go=0
		elif tags[i][j%5]==goal:
			go=2
		elif tags[i][j%5]==sub_goal:
			go=3
>>>>>>> 621ef2d8fe07abe3f6e1f6fe9ce24d0756d6385e
		#elif tags[i][j%5]==sub_goal:
		#	go=3
		else:   # 
			go=4
	rospy.loginfo('go=%s',go)  
<<<<<<< HEAD
	######
	if go==4:
		msg=Twist()
		msg.linear.x=0.0;
		msg.linear.y=0.0;
		msg.linear.z=0.0;
		msg.angular.x=0.0;
		msg.angular.y=0.0;
		msg.angular.z=0.5;
		pub.publish(msg)
	elif go==2:
		msg=Twist()
		msg.linear.x=0.5;
		msg.linear.y=0.0;
		msg.linear.z=0.0;
		msg.angular.x=0.0;
		msg.angular.y=0.0;
		msg.angular.z=0.0;
		pub.publish(msg)
	elif go==0:
		msg=Twist()
		msg.linear.x=0.0;
		msg.linear.y=0.0;
		msg.linear.z=0.0;
		msg.angular.x=0.0;
		msg.angular.y=0.0;
		msg.angular.z=0.0;
		pub.publish(msg)
=======
>>>>>>> 621ef2d8fe07abe3f6e1f6fe9ce24d0756d6385e
	
	pass


def set_apriltag_purpose(msg):
	rospy.set_param("/jetbot_apriltag/goal",msg.data)
	rospy.loginfo(' apriltag_purpose=%d', msg.data)


# initialization
if __name__ == '__main__':
	data_serial=""
	data_complete=False
	# setup ros node
	rospy.init_node('jetbot_search_apriltag')
	rospy.Subscriber('set_apriltag_goal', Int16, set_apriltag_purpose)
	# start running
	while not rospy.core.is_shutdown():
		while serial_openmv.inWaiting()>0:
            		c=serial_openmv.read()
			#rospy.loginfo(c)
			if c=='$':
				data_complete=True
				break
			else:
				data_serial=data_serial+c
		if data_complete == True:
			parsestring(data_serial)
			data_serial=""
			data_complete=False	
		# Update ROS
		rospy.rostime.wallsleep(0.1)
