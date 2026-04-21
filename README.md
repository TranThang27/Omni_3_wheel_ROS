# My Robot ROS 2 - Omni 3 Wheel Robot with Arm


```bash
git clone https://github.com/TranThang27/Omni_3_wheel_ROS.git
```

```bash
cd Omni_3_wheel_ROS
colcon build
source install/setup.bash 
```
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



