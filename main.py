import robot
import pose

import math
import time

if __name__ == '__main__':
  bot = robot.Robot(11.75, 3.25, 36.0/48.0, 600)

  bot.set_pose(0, 0, math.pi / 2)
  bot.initialize()

  bot.move(127, 90)

  bot.start_logging()
  time.sleep(1)
  bot.stop_logging()
  bot.stop()
  bot.display_log()