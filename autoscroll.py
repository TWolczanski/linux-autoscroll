from pynput.mouse import Button, Controller, Listener
from threading import Event
from time import sleep

def on_move(x, y):
    global pos, scroll_mode, direction, interval, DELAY
    if scroll_mode.is_set():
        delta = pos[1] - y
        if delta > 0:
            direction = 1
        elif delta < 0:
            direction = -1
        else:
            direction = 0
        if abs(delta) < DELAY * 2:
            interval = 0.5
        else:
            interval = DELAY / abs(delta)

def on_click(x, y, button, pressed):
    global pos, scroll_mode, direction, interval, BUTTON
    if button == BUTTON and pressed:
        if scroll_mode.is_set():
            scroll_mode.clear()
        else:
            pos = (x, y)
            direction = 0
            interval = 0
            scroll_mode.set()
        
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
BUTTON = Button.middle

listener.start()
autoscroll()
