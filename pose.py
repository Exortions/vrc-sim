import math

class Pose:
  def __init__(self, x, y, theta):
    # units are assumed to be inches and radians
    self.x = x
    self.y = y
    self.theta = theta

  def __eq__(self, other):
    return self.x == other.x and self.y == other.y and self.theta == other.theta

  def __add__(self, other):
    return Pose(self.x + other.x, self.y + other.y, self.theta + other.theta)
  
  def __sub__(self, other):
    return Pose(self.x - other.x, self.y - other.y, self.theta - other.theta)

  def __mul__(self, other):
    return Pose(self.x * other, self.y * other, self.theta * other)
  
  def __truediv__(self, other):
    return Pose(self.x / other, self.y / other, self.theta / other)

  def __str__(self):
    return f"Pose(x={self.x}, y={self.y}, theta={self.theta})"

  def to_string(self, simple, theta):
    string = f"{round(self.x, 3)}, {round(self.y, 3)}"
    if theta:
      string += f", {round(self.theta, 3)}"

    if not simple:
      return f"Pose({string})"

    return string

  def distance(self, other):
    return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5
  
  def angle(self, other):
    return math.atan2(other.y - self.y, other.x - self.x)
  
  def rotate(self, angle):
    return Pose(self.x * math.cos(angle) - self.y * math.sin(angle),
                self.x * math.sin(angle) + self.y * math.cos(angle),
                self.theta)
  
  def relativeTo(self, other):
    x_d = other.x
    y_d = other.y

    x_c = self.x
    y_c = self.y
    theta = self.theta

    x_e = ((x_d - x_c) * math.cos(theta)) + ((y_d - y_c) * math.sin(theta))
    y_e = ((x_d - x_c) * -math.sin(theta)) - ((y_d - y_c) * math.cos(theta))
    theta_e = other.theta - self.theta

    return Pose(x_e, y_e, theta_e)