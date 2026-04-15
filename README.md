# My Robot ROS 2 - Omni 3 Wheel Robot with Arm




### ** Hiển thị Model trên RViz**

```bash
ros2 launch my_robot_description display.launch.py
```

### **Chạy tren Gazebo**

```bash
ros2 launch my_robot_description sim.launch.py
```

### ** Điều Khiển Robot Omni (xe 3 Bánh)**

Điều khiển chuyển động của robot base (3 bánh omni).

```bash
ros2 run my_robot_teleop omni_teleop
```


### **Điều Khiển Tay Robot (2 Khớp)**

Điều khiển tay máy bằng bàn phím.

```bash
cd src/my_robot_arm_controller/my_robot_arm_controller
python arm_controller.py
```



