from pynput.mouse import Button, Controller, Listener
from threading import Event
from time import sleep

def on_move(x, y):
    global pos, scroll_mode, direction, interval, DELAY, DEAD_AREA
    if scroll_mode.is_set():
        delta = pos[1] - y
        if abs(delta) <= DEAD_AREA:
            direction = 0
        elif delta > 0:
            direction = 1
        elif delta < 0:
            direction = -1
        if abs(delta) <= DEAD_AREA + DELAY * 2:
            interval = 0.5
        else:
            interval = DELAY / (abs(delta) - DEAD_AREA)

def on_click(x, y, button, pressed):
    global pos, scroll_mode, direction, interval, BUTTON_START, BUTTON_STOP
    if button == BUTTON_START and pressed and not scroll_mode.is_set():
        pos = (x, y)
        direction = 0
        interval = 0
        scroll_mode.set()
    elif button == BUTTON_STOP and pressed and scroll_mode.is_set():
        scroll_mode.clear()
        
def autoscroll():
    global mouse, scroll_mode, direction, interval
    while True:
        scroll_mode.wait()
        sleep(interval)
        mouse.scroll(0, direction)

mouse = Controller()
listener = Listener(on_move = on_move, on_click = on_click)
scroll_mode = Event()
pos = mouse.position
direction = 0
interval = 0

# modify this to adjust the speed of scrolling
DELAY = 5
# modify this to change the button used for entering the scroll mode
BUTTON_START = Button.middle
# modify this to change the button used for exiting the scroll mode
BUTTON_STOP = Button.middle
# modify this to change the size (in px) of the area below and above the starting point where the scrolling is paused
DEAD_AREA = 30

listener.start()
autoscroll()
