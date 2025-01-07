import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from nav_msgs.msg import Odometry
import math

# Global variable to store turtle's position
robot_x = 0.0

# Callback function to update turtle's position
def pose_callback(msg):
    global robot_x
    robot_x = msg.pose.pose.position.x
    print(robot_x)

class TurtlePatternNode(Node):
    def __init__(self):
        super().__init__('moving_robot_node')
        self.pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.sub = self.create_subscription(Odometry, '/odom', pose_callback, 10)
        self.timer = self.create_timer(0.1, self.move_turtle)
        self.vel_msg = Twist()
        self.forward_speed = 1.0
        self.turn_speed = 1.0
        self.max_x = 8
        self.min_x = 2
        self.moving_up = True

    def move_turtle(self):
        # Move forward horizontally
        self.vel_msg.linear.x = self.forward_speed
        self.vel_msg.angular.z = 0.0
        self.pub.publish(self.vel_msg)

        # Check if the turtle has reached the edge
        if  robot_x >= self.max_x:
            self.moving_up = False
            self.vel_msg.angular.z = self.turn_speed
        elif robot_x <= self.min_x:
            self.moving_up = True
            self.vel_msg.angular.z = -1.0*self.turn_speed
        else:
            self.vel_msg.angular.z = 0.0

        self.pub.publish(self.vel_msg)


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

