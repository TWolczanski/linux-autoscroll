from pynput.mouse import Button, Controller, Listener

# TODO
# class Autoscroll
# block the mouse pointer and change its look when the middle button is clicked
# refine delta
# overwrite middle mouse button behavior from other programs

def on_move(x, y):
    if scroll_mode:
        global pos, delta
        """
        if y < pos:
            mouse.scroll(0, 1)
        elif y > pos:
            mouse.scroll(0, -1)
        """
        d = pos - y
        if d * delta < 0:
            delta = d
        else:
            delta += d
        if abs(delta) >= 10:
            mouse.scroll(0, delta // 3)
            delta = 0
        pos = y

def on_click(x, y, button, pressed):
    if button == Button.right:
        global end
        end = True
    elif button == Button.middle and pressed:
        global scroll_mode, pos
        scroll_mode = not scroll_mode
        pos = mouse.position[1]

mouse = Controller()
listener = Listener(on_move=on_move, on_click=on_click)
listener.start()
end = False
scroll_mode = False
delta = 0
pos = mouse.position[1]

while not end:
    pass