import tkinter as tk
from tkinter import ttk
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from threading import Thread

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('move_robot')
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        self.msg = Twist()  # Initialize the Twist message

    def publish_twist(self):
        try:
            while rclpy.ok():
                self.publisher_.publish(self.msg)
                self.get_logger().info(f'Publishing: linear.x={self.msg.linear.x}, angular.z={self.msg.angular.z}')
                rclpy.spin_once(self, timeout_sec=0.1)
        except KeyboardInterrupt:
            self.get_logger().info("Node stopped by user.")

class GUIApplication:
    def __init__(self, master, publisher):
        self.master = master
        self.publisher = publisher

        self.master.title("Twist Message Publisher")

        self.linear_label = ttk.Label(master, text="Linear Velocity x:")
        self.linear_label.grid(row=0, column=0)
        
        self.linear_entry = ttk.Entry(master)
        self.linear_entry.grid(row=0, column=1)

        self.angular_label = ttk.Label(master, text="Angular Velocity z:")
        self.angular_label.grid(row=1, column=0)

        self.angular_entry = ttk.Entry(master)
        self.angular_entry.grid(row=1, column=1)

        self.publish_button = ttk.Button(master, text="Publish", command=self.start_publishing)
        self.publish_button.grid(row=2, column=0, columnspan=2)

    def start_publishing(self):
        try:
            linear_x = float(self.linear_entry.get())
            angular_z = float(self.angular_entry.get())
        except ValueError:
            print("Invalid input. Please enter numeric values.")
            return

        self.publisher.msg.linear.x = linear_x
        self.publisher.msg.angular.z = angular_z

        # Start publishing in a separate thread
        thread = Thread(target=self.publisher.publish_twist)
        thread.start()

def main(args=None):
    rclpy.init(args=args)
    publisher = MinimalPublisher()

    root = tk.Tk()
    app = GUIApplication(root, publisher)
    root.protocol("WM_DELETE_WINDOW", lambda: graceful_shutdown(root, publisher))
    root.mainloop()

    publisher.destroy_node()
    rclpy.shutdown()

def graceful_shutdown(root, publisher):
    publisher.destroy_node()
    rclpy.shutdown()
    root.destroy()

if __name__ == '__main__':
    main()

