import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from nav_msgs.msg import Odometry
import math
from std_msgs.msg import Float32
from std_srvs.srv import SetBool

# Global variable to store turtle's position
robot_x = 0.0
distance_in_feet=0.0
state=True

# Callback function to update turtle's position
def pose_callback(msg):
    global robot_x
    global distance_in_feet
    robot_x = msg.pose.pose.position.x
    robot_y = msg.pose.pose.position.y
    distance_in_feet = ((robot_x**2 +robot_y**2)**0.5)*3.28084
    

def toggle_state(self, request, response):    
    global state
    
    state = request.data
    response.success = True
    response.message = 'State changed to: ' + str(state)
    return response

class TurtlePatternNode(Node):
    def __init__(self):
        super().__init__('moving_robot_node')
        self.pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.sub = self.create_subscription(Odometry, '/odom', pose_callback, 10)
        self.timer = self.create_timer(0.1, self.move_robot)
        self.pub_feet = self.create_publisher(Float32, 'distance_in_feet', 10)
        self.srv = self.create_service(SetBool, 'stop_restart',toggle_state)

        self.vel_msg = Twist()
        self.forward_speed = 1.0
        self.turn_speed = 1.0
        self.max_x = 8
        self.min_x = 2
        self.moving_up = True

    def move_robot(self):
        global state
        global robot_x
        # Move forward horizontally
        
        self.vel_msg.angular.z = 0.0
        
        if state==0:
            self.vel_msg.linear.x = 0.0
            self.vel_msg.angular.z = 0.0
        else:
            self.vel_msg.linear.x = self.forward_speed

        # Check if the turtle has reached the edge
        if  robot_x >= self.max_x:
            self.moving_up = False
            self.vel_msg.angular.z = self.turn_speed
        elif robot_x <= self.min_x:
            self.moving_up = True
            self.vel_msg.angular.z = -1.0*self.turn_speed
        else:
            self.vel_msg.angular.z = 0.0

        if state==0:
            self.vel_msg.linear.x = 0.0
            self.vel_msg.angular.z = 0.0



        self.pub.publish(self.vel_msg)

    def pub_distance(self):
        self.pub_feet.publish(distance_in_feet)




def main(args=None):
    rclpy.init(args=args)
    node = TurtlePatternNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

