import pint
units = pint.UnitRegistry()

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

  def distance(self, other):
    return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5
  
  def angle(self, other):
    return atan2(other.y - self.y, other.x - self.x)
  
  def rotate(self, angle):
    return Pose(self.x * cos(angle) - self.y * sin(angle),
                self.x * sin(angle) + self.y * cos(angle),
                self.theta)
  
  def relativeTo(self, other):
    x_d = other.x
    y_d = other.y

    x_c = self.x
    y_c = self.y
    theta = self.theta

    x_e = ((x_d - x_c) * cos(theta)) + ((y_d - y_c) * sin(theta))
    y_e = ((x_d - x_c) * -sin(theta)) - ((y_d - y_c) * cos(theta))
    theta_e = other.theta - self.theta

    return Pose(x_e, y_e, theta_e)