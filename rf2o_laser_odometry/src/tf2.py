#!/usr/bin/env python

import rospy
import tf


class tf_firsttry_listen_class():
    def __init__(self):
        rospy.init_node('tf_firsttry_listen')
        listener = tf.TransformListener()
        now = rospy.Time.now()
        while not rospy.is_shutdown():
            listener.waitForTransform('/base_link','/One',rospy.Time(), rospy.Duration(10.0))
            (trans, rot) = listener.lookupTransform('/base_link', '/One', rospy.Time(0))
            print trans


if __name__ == '__main__':
    try:
        tf_firsttry_listen_class()
    except rospy.ROSInterruptException:
        pass
