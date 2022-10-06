#!/usr/bin/env python
import rospy
import time
import math 

from sensor_msgs.msg import Joy
from std_msgs.msg import String
from geometry_msgs.msg import Twist

pub=rospy.Publisher("/jetbot_motors/cmd_vel",Twist)

def controller(data):
    rospy.loginfo(str(data.axes[0])+" "+str(data.axes[1]))
    msg=Twist()
    msg.linear.x=data.axes[0];
    msg.linear.y=0.0;
    msg.linear.z=0.0;
    msg.angular.x=0.0;
    msg.angular.y=0.0;
    msg.angular.z=data.axes[1];
    pub.publish(msg)

    
def listener():
     rospy.init_node('jetbot_joy')
     rospy.sleep(1.0)
    
     sub = rospy.Subscriber("joy",Joy,controller)
     rospy.spin()
  
if __name__ == '__main__':
   listener()


