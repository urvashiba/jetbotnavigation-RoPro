#!/usr/bin/env python
import rospy
import time
import math 

from Adafruit_MotorHAT import Adafruit_MotorHAT
from std_msgs.msg import String
from geometry_msgs.msg import Twist

PWM_MIN=0.5
PWM_MAX=1.0

# sets motor speed between [-1.0, 1.0]
def set_speed(motor_ID, value):
  max_pwm = 200.0
  speed = int(min(max(abs(value * max_pwm), 0), max_pwm))
  a = b = 0
  if motor_ID == 1:
    motor = motor_left
    a=1
    b=0
  elif motor_ID == 2:
    motor = motor_right
    a=2
    b=3
  else:
    rospy.logerror('set_speed(%d, %f) -> invalid motor_ID=%d', motor_ID, value, motor_ID)
    return
	
  motor.setSpeed(speed)

  if value < 0:
    motor.run(Adafruit_MotorHAT.FORWARD)
    motor.MC._pwm.setPWM(a,0,0)
    motor.MC._pwm.setPWM(b,0,speed*16)
  elif value > 0:
    motor.run(Adafruit_MotorHAT.BACKWARD)
    motor.MC._pwm.setPWM(a,0,speed*16)
    motor.MC._pwm.setPWM(b,0,0)
  else:
    motor.run(Adafruit_MotorHAT.RELEASE)
    motor.MC._pwm.setPWM(a,0,0)
    motor.MC._pwm.setPWM(b,0,0)


# stops all motors
def all_stop():
	set_speed(motor_left_ID, 0.0)
	set_speed(motor_right_ID, 0.0)

# directional commands (degree, speed)
def on_cmd_dir(msg):
	rospy.loginfo(rospy.get_caller_id() + ' cmd_dir=%s', msg.data)

# raw L/R motor commands (speed, speed)
def on_cmd_raw(msg):
	rospy.loginfo("msg cmd_raw")
	rospy.loginfo(msg)
        x=max(min(msg.linear.x,1.0),-1.0)
        z=max(min(msg.angular.z,1.0),-1.0)         
        l=(x-z)/2
        r=(x+z)/2
	#rospy.loginfo(x)
        #rospy.loginfo(z)
	#rospy.loginfo(l)
        #rospy.loginfo(r)
        
        lpwm= PWM_MIN+math.fabs(l)*(PWM_MAX-PWM_MIN)
        rpwm= PWM_MIN+math.fabs(r)*(PWM_MAX-PWM_MIN)
 	#rospy.loginfo(lpwm)
        #rospy.loginfo(rpwm)
        kl=1 if l>0 else -1
        kr=1 if r>0 else -1
        if l==0 : kl=0
        if r==0 : kr=0 
	set_speed(motor_left_ID, kl*lpwm )
	set_speed(motor_right_ID, kr*rpwm) 

# simple string commands (left/right/forward/backward/stop)
def on_cmd_str(msg):
	rospy.loginfo(rospy.get_caller_id() + ' cmd_str=%s', msg.data)

	if msg.data.lower() == "left":
		set_speed(motor_left_ID,  -1.0)
		set_speed(motor_right_ID,  1.0) 
	elif msg.data.lower() == "right":
		set_speed(motor_left_ID,   1.0)
		set_speed(motor_right_ID, -1.0) 
	elif msg.data.lower() == "forward":
		set_speed(motor_left_ID,   1.0)
		set_speed(motor_right_ID,  1.0)
	elif msg.data.lower() == "backward":
		set_speed(motor_left_ID,  -1.0)
		set_speed(motor_right_ID, -1.0)  
	elif msg.data.lower() == "stop":
		all_stop()
	else:
		rospy.logerror(rospy.get_caller_id() + ' invalid cmd_str=%s', msg.data)


# initialization
if __name__ == '__main__':

	# setup motor controller
	motor_driver = Adafruit_MotorHAT(i2c_bus=1)

	motor_left_ID = 1
	motor_right_ID = 2

	motor_left = motor_driver.getMotor(motor_left_ID)
	motor_right = motor_driver.getMotor(motor_right_ID)

	# stop the motors as precaution
	all_stop()

	# setup ros node
	rospy.init_node('jetbot_motors')
	
	rospy.Subscriber('~cmd_dir', String, on_cmd_dir)
	rospy.Subscriber('/cmd_vel', Twist, on_cmd_raw)
	rospy.Subscriber('~cmd_str', String, on_cmd_str)

	# start running
	rospy.spin()

	# stop motors before exiting
	all_stop()

