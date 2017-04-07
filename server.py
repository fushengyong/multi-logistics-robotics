import socket
import os
import sys
import rospy
import time
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, Point, Quaternion
os.system('gnome-terminal -e "bash -c \'roscore\'" &')
time.sleep(5)
os.system('gnome-terminal -e "bash -c \'roslaunch turtlebot_bringup minimal.launch\'" &')
time.sleep(5)
os.system('gnome-terminal -e "bash -c \'roslaunch turtlebot_navigation amcl_demo.launch map_file:=/home/libliuis/my_map.yaml\'" &')
time.sleep(5)
address = ('172.16.42.6', 31500)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(address)
class GoToPose():
    def __init__(self):

        self.goal_sent = False

    # What to do if shut down (e.g. Ctrl-C or failure)
        rospy.on_shutdown(self.shutdown)
    
    # Tell the action client that we want to spin a thread by default
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        rospy.loginfo("Wait for the action server to come up")

    # Allow up to 5 seconds for the action server to come up
        self.move_base.wait_for_server(rospy.Duration(5))

    def goto(self, pos, quat):

        # Send a goal
        self.goal_sent = True
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = 'map'
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose = Pose(Point(pos['x'], pos['y'], 0.000),Quaternion(quat['r1'], quat['r2'], quat['r3'], quat['r4']))
    # Start moving
        self.move_base.send_goal(goal)

    # Allow TurtleBot up to 60 seconds to complete task
        success = self.move_base.wait_for_result(rospy.Duration(60)) 

        state = self.move_base.get_state()
        result = False

        if success and state == GoalStatus.SUCCEEDED:
            # We made it!
            result = True
        else:
            self.move_base.cancel_goal()

        self.goal_sent = False
        return result

    def shutdown(self):
        if self.goal_sent:
            self.move_base.cancel_goal()
        rospy.loginfo("Stop")
        rospy.sleep(1)

if __name__ == '__main__':
    while True:
        data, addr = s.recvfrom(2048)
        if not data:
            print "client has exist"
            break
        robot_x1,robot_y1,robot_x2,robot_y2=data.split()
        try:
            rospy.init_node('nav_test', anonymous=False)
            navigator = GoToPose()
            # Customize the following values so they are appropriate for your location
            position = {}
            position['x']=float(robot_x1)
            position['y']=float(robot_y1)
            quaternion = {'r1' : 0.000, 'r2' : 0.000, 'r3' : 0.000, 'r4' : 1.000}
            rospy.loginfo("Go to (%s, %s) pose", position['x'], position['y'])
            success = navigator.goto(position, quaternion)
            if success:
                position = {}
                position['x']=float(robot_x2)
                position['y']=float(robot_y2)
                quaternion = {'r1' : 0.000, 'r2' : 0.000, 'r3' : 0.000, 'r4' : 1.000}
                rospy.loginfo("Go to (%s, %s) pose", position['x'], position['y'])
                success = navigator.goto(position, quaternion)
                if success:
                    msg='success'
                    s.sendto(msg,addr)
                    rospy.loginfo("Hooray, reached the desired pose")
                    continue
                else:
                    rospy.loginfo("The base failed to reach the desired pose")
            else:
                rospy.loginfo("The base failed to reach the desired pose")
            rospy.sleep(1)
        except rospy.ROSInterruptException:
            rospy.loginfo("Ctrl-C caught. Quitting")
    s.close()
