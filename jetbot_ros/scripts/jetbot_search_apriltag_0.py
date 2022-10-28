#!/usr/bin/env python
import rospy
import time
import serial

from std_msgs.msg import String, Int16


rospy.set_param("/jetbot_apriltag/goal",0)
rospy.set_param("/jetbot_apriltag/sub_goal",0)
serial_openmv=serial.Serial("/dev/ttyUSB0", 9600, timeout=1)

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
	sub_goal= rospy.get_param("/jetbot_apriltag/sub_goal") 
	for i in range(int(dd[0])):
		if goal==0:
			go=0
		elif tags[i][j%5]==goal:
			go=2
		elif tags[i][j%5]==sub_goal:
			go=3
		#elif tags[i][j%5]==sub_goal:
		#	go=3
		else:   # 
			go=4
	rospy.loginfo('go=%s',go)  
	
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
