#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy

class CmdVelPublisher(Node):

    def __init__(self):
        super().__init__('cmd_node')
        # pub cmd_vel
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        # sub joy signal
        self.subscription = self.create_subscription(Joy, 'joy', self.vel_callback, 10)
        # timer
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.linear_x = 0.0
        self.linear_y = 0.0
        self.angular_z = 0.0
        
    def vel_callback(self, msg):
        self.linear_x = float(msg.axes[1])
        self.linear_y = float(msg.axes[0])
        self.angular_z = float(msg.axes[3])
    def timer_callback(self):
        msg = Twist()
        msg.linear.x = self.linear_x
        msg.linear.y = self.linear_y
        msg.angular.z = self.angular_z
        self.publisher_.publish(msg)
        self.get_logger().info(
        'cmd_vel:\n'
        '  linear:\n'
        '   x:"%s"\n'
        '   y:"%s"\n'
        '  angular:\n'
        '   z: "%s"' % (msg.linear.x, msg.linear.y, msg.angular.z)
    )
def main(args=None):
    rclpy.init(args=args)
    cmd_node = CmdVelPublisher()  
    rclpy.spin(cmd_node)
    cmd_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
