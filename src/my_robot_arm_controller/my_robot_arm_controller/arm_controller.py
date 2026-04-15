#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from sensor_msgs.msg import JointState
from threading import Thread
import sys, termios, tty, select

class ArmKeyboardController(Node):
    def __init__(self):
        super().__init__('arm_keyboard_controller')
        
        self.trajectory_publisher = self.create_publisher(
            JointTrajectory, '/joint_trajectory_controller/joint_trajectory', 10)
        
        self.state_subscriber = self.create_subscription(
            JointState, '/joint_states', self.joint_state_callback, 10)
        
        self.current_pos = [0.0, 0.0]
        self.initialized = False
        
        self.step_l1 = 0.15
        self.step_l2 = 0.005
        
        self.limits = {'l1': [-3.14, 3.14], 'l2': [-0.025, 0.025]}

        self.print_usage()
        
        Thread(target=self.keyboard_loop, daemon=True).start()

    def print_usage(self):
        print("\n" + "="*45)
        print("="*45)
        print("  W : Xoay khớp l1 ngược chiều kim đồng hồ")
        print("  S : Xoay khớp l1 thuận chiều kim đồng hồ")
        print("  A : Day khớp l2 ra ngoaif")
        print("  D : Thu khớp l2 vao trong")
        print("  Q : Thoát chương trình")
        print("="*45)


    def joint_state_callback(self, msg):
        try:
            idx1, idx2 = msg.name.index('l1'), msg.name.index('l2')
            self.current_pos = [msg.position[idx1], msg.position[idx2]]
            self.initialized = True
        except ValueError: 
            pass

    def send_cmd(self, target_l1, target_l2):
        msg = JointTrajectory()
        msg.joint_names = ['l1', 'l2']
        point = JointTrajectoryPoint()
        
        point.positions = [
            max(self.limits['l1'][0], min(self.limits['l1'][1], target_l1)),
            max(self.limits['l2'][0], min(self.limits['l2'][1], target_l2))
        ]
        point.time_from_start.nanosec = 100000000
        msg.points.append(point)
        self.trajectory_publisher.publish(msg)

    def keyboard_loop(self):
        old_settings = termios.tcgetattr(sys.stdin)
        try:
            tty.setraw(sys.stdin.fileno())
            while rclpy.ok():
                if select.select([sys.stdin], [], [], 0.1)[0]:
                    key = sys.stdin.read(1).lower()
                    
                    if not self.initialized: 
                        continue
                    
                    t_l1, t_l2 = self.current_pos 
                    
                    if key == 'w': t_l1 += self.step_l1
                    elif key == 's': t_l1 -= self.step_l1
                    elif key == 'a': t_l2 -= self.step_l2
                    elif key == 'd': t_l2 += self.step_l2
                    elif key == 'q': 
                        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
                        rclpy.shutdown()
                        break
                    
                    self.send_cmd(t_l1, t_l2)
                    
                    while select.select([sys.stdin], [], [], 0.0)[0]: 
                        sys.stdin.read(1)
                    
                    sys.stdout.write(f"\r >> [l1: {t_l1:+.3f} rad] | [l2: {t_l2:+.3f} m]      ")
                    sys.stdout.flush()
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

def main(args=None):
    rclpy.init(args=args)
    node = ArmKeyboardController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()