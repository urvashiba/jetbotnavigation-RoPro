#!/usr/bin/env python

import rospy
import tf

class tf_firsttry_pub_class():
    def __init__(self):
        rospy.init_node('tf_firsttry_pub')
        now = rospy.Time.now()
        br = tf.TransformBroadcaster()
        R = rospy.Rate(250)
        while not rospy.is_shutdown():
            br.sendTransform((1, 1, 1), (0, 0, 0, 1), rospy.Time(), 'One','base_link')      
            R.sleep()


if __name__ == '__main__':
    try:
        tf_firsttry_pub_class()
    except rospy.ROSInterruptException:
        pass
