import mouse
import time

while not mouse.is_pressed(button='left'):
    time.sleep(2)
    print("Waiting for left click...")
print("End of the program.")