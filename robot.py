from threading import Thread, Lock
import math
import time

class Robot:
  def __init__(self, track_width, wheel_radius, gear_ratio, motor_rpm):
    self.track_width = track_width
    self.wheel_radius = wheel_radius
    self.gear_ratio = gear_ratio
    self.motor_rpm = motor_rpm

    self.max_speed = ((motor_rpm * gear_ratio) / 60) * (Math.pi * wheel_radius * 2) # in/s

    self.pose = Pose(0, 0, Math.pi / 2)

    # (-127 to 127)
    self.left_power = 0
    self.right_power = 0

    self.is_running = False
    self.is_queued = False

    self.distance_travelled = 0
    self.angle_travelled = 0

    self.mutex = Lock()

    self.task = None
    self.task_running = False

  def initialize(self):
    # create a loop to run update every 10ms
    if (self.task == None):
      self.task_running = True
      self.task = Thread(target=self.update_loop)
      self.task.start()

  def stop(self):
    self.task_running = False
    self.task.join()

  def update_loop(self):
    while self.task_running:
      self.update(0.01)
      time.sleep(0.01)

  def update(self, dt):
    # TODO: account for noise and wheel slippage + drift
    left_velocity = (self.left_power / 127) * self.max_speed
    right_velocity = (self.right_power / 127) * self.max_speed

    x_delta = ((left_velocity + right_velocity) / 2) * Math.cos(self.pose.theta) * dt
    y_delta = ((left_velocity + right_velocity) / 2) * Math.sin(self.pose.theta) * dt
    theta_delta = ((right_velocity - left_velocity) / self.track_width) * dt

    self.pose = self.pose + Pose(x_delta, y_delta, theta_delta)

  def move(self, left_power, right_power):
    self.left_power = left_power
    self.right_power = right_power

  def get_pose(self):
    return self.pose

  def set_pose(self):
    self.pose = pose
  
  def set_pose(self, x, y, theta):
    self.pose = Pose(x, y, theta)
  
  def wait_until(self, distance):
    while self.distance_travelled < distance:
      time.sleep(0.01)

  def wait_until(self, angle):
    while self.angle_travelled < angle:
      time.sleep(0.01)

  def wait_until_done(self):
    while self.distance_travelled != -9999 and self.angle_travelled != -9999:
      time.sleep(0.01)
  
  def request_motion_start(self):
    if self.is_in_motion():
      self.is_queued = True
    else:
      self.is_running = True

    self.mutex.acquire()

  def end_motion():
    self.is_running = self.is_queued
    self.is_queued = False

    self.mutex.release()

  def cancel_motion(self):
    self.is_running = False
    time.sleep(0.01)

  def cancel_all_motions(self):
    self.is_running = False
    self.is_queued = False
    time.sleep(0.01)

  def is_in_motion(self):
    return self.is_running