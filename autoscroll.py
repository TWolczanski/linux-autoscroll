from pynput.mouse import Button, Controller, Listener

# TODO
# block the mouse pointer and change its look when the middle button is clicked
# refine delta
# overwrite middle mouse button behavior from other programs

class Mouse:
    def __init__(self):
        self.controller = Controller()
        self.pos = self.controller.position[1]
        self.scroll_mode = False
    
    def on_move(self, x, y):
        if self.scroll_mode:
            if y < self.pos:
                self.controller.scroll(0, 1)
            elif y > self.pos:
                self.controller.scroll(0, -1)
            """
            d = pos - y
            if d * delta < 0:
                delta = d
            else:
                delta += d
            if abs(delta) >= 10:
                mouse.scroll(0, delta // 3)
                delta = 0
            """
            self.pos = y

    def on_click(self, x, y, button, pressed):
        if button == Button.middle and pressed:
            self.scroll_mode = not self.scroll_mode
            self.pos = self.controller.position[1]

# delta = 0
mouse = Mouse()

with Listener(on_move = mouse.on_move, on_click = mouse.on_click) as listener:
    listener.join()