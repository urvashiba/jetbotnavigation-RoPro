# Jetbot_navigation with google-cartographer

# project

 Flash your jetson nano's SD card from the official NVIDIA Jetbot website
 Minimum 32 GB card is required.




# Install ROS Melodic

 enable all Ubuntu packages:
 ```bash
1. sudo apt-add-repository universe
2. sudo apt-add-repository multiverse
3. sudo apt-add-repository restricted
```
# add ROS repository to apt sources

```bash
 sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
 sudo apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654
```
# install ROS Base
```bash
 sudo apt-get update
 sudo apt-get install ros-melodic-ros-base
```
# add ROS paths to environment

```bash
sudo sh -c 'echo "source /opt/ros/melodic/setup.bash" >> ~/.bashrc'
```
Close and restart the terminal.


### Install Adafruit Libraries

These Python libraries from Adafruit support the TB6612/PCA9685 motor drivers and the SSD1306 debug OLED:

###pip should be installed
```bash
 sudo apt-get install python-pip
```
# install Adafruit libraries
```bash
 pip install Adafruit-MotorHAT
 pip install Adafruit-SSD1306
```

Grant your user access to the i2c bus:

```bash
 sudo usermod -aG i2c $USER
   
```
Reboot the system for the changes to take effect.

### Create catkin workspace

Create a ROS Catkin workspace to contain our ROS packages:

```bash
# create the catkin workspace
$ mkdir -p ~/workspace/catkin_ws/src
$ cd ~/workspace/catkin_ws
$ catkin_make

# add catkin_ws path to bashrc
$ sudo sh -c 'echo "source ~/workspace/catkin_ws/devel/setup.bash" >> ~/.bashrc'

```
