# Autonomous-Maze-Solver-Robot
The code that I wrote for the autonomous bot that I built for the International Robotics Challenge, Techfest 2018, IIT Bombay. It is a maze solving robot that uses the flood fill algorithm to navigate and map the maze.

## Table of Content
1. [About the Competetion](#about-the-competetion)
2. [The Autonomous Bot](#the-autonomous-bot)
3. [Explanation of the program](#explanation-of-the-program)

## About the competetion
For the competition, we were required to build two robots, a manual and autonomous bot that would
coordinate with each other to tackle various challenges set forth during the competition. The
autonomous bot had to solve a maze without any form of external help from the participants. It had to
even identify the positions of different coloured blocks and scan a QR code. The manual bot had to be
designed to move using a remote controller and to pick and place blocks. Its main objective was to clear
the way for the autonomous bot by transferring the blocks detected by the autonomous bot in the maze
to specified zones outside the maze. It had to also tackle obstacles and fire a projectile at a target. Each
team was allotted with a time limit of 8 minutes to complete all the tasks and a time limit of 5 minutes
for a pre-run of the autonomous bot for it to learn the maze.

##### The Arena
> ![WhatsApp Image 2019-01-12 at 5 14 12 PM (1)](https://user-images.githubusercontent.com/46392391/55337994-5568e280-54bd-11e9-9995-7de755a03438.jpeg)

## The Autonomous Bot
The autonomous bot that we built ran on a raspberry pi-3 board that used a python script with OpenCV.
We built the logic on the floodfill algorithm. We used 3 ultrasonic sensors to detect the right, front and
left maze walls, an RGB sensor to detect the coloured blocks and a pi-camera to scan the QR code blocks
obstructing the path of the bot. It was constructed on an aluminium sheet taken as a base. It had 4 12V 300 rpm 
DC motors connected to wheels for movement. The motors were controlled by a pair of two L298N Dual H Bridge Motor
Drivers. We used a standard 2A power bank to power the raspberry and a set of 3 Standard 18650
2200mAh 3.7V Rechargeable Li-ion batteries connected in series (To get a power supply of 2200mAh
11.1 V) to power the motors.
We first tested the program extensively on an online simulator that we had built to optimize it and fix
bugs. Then we integrated the code into the bot and ran trials on a demo arena that we had built for
testing in the college.

##### The Autonomous Bot
> ![WhatsApp Image 2019-04-01 at 8 39 29 PM](https://user-images.githubusercontent.com/46392391/55338440-5d755200-54be-11e9-993a-dcf04371aa4e.jpeg)

## Explanation of the program
The project is available in 3 different branches:
#### 1. Master Branch
Warning: This is for the final implimentation only. 
The main.py in this branch should only be run on a raspberry pi that has been connected to all the various electronic components. The code includes the specification of various Raspberry pins, kindly edit the pin numbers according to how you have connected them.
> [Final Implementation](https://github.com/Captainspockears/Autonomous-Maze-Solver-Robot/blob/master/main.py)
#### 2. Without-walls-simulation
The main.py in this branch is used for testing. It can be run on a PC without a raspberry pi. It will display a simulation of how the robot would move in a maze that has no walls.
> [Testing Without Walls](https://github.com/Captainspockears/Autonomous-Maze-Solver-Robot/blob/Without-walls-simulation/main.py)
#### 3. Random-walls-simulation
The main.py in this branch is used for testing. It can be run on a PC without a raspberry pi. It will display a simulation of how the robot would move in a maze that has walls. The walls are generated with every movement of the bot randomly. This does not work well, and a better simulator is required that constructs an entire random maze.
> [Testing With Walls](https://github.com/Captainspockears/Autonomous-Maze-Solver-Robot/blob/Random-walls-simulation/main.py)
