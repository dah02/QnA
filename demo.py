from openpibo.motion import Motion

motion = Motion()

def run():
  motion.set_motion(name="breath1", cycle=100)

if __name__ == "__main__":
  run()
