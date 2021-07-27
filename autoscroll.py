from pynput.mouse import Button, Controller, Listener

# TODO
# block the mouse pointer and change its look when the middle button is clicked
# refine delta
# overwrite middle mouse button behavior from other programs

class Mouse:
    def __init__(self):
        self.controller = Controller()
        self.pos = self.controller.position
        self.scroll_pos = self.controller.position
        self.scroll_mode = False
        self.delta = 0
        self.px_to_scr = 10
    
    def on_move(self, x, y):
        if self.scroll_mode:
            self.delta = self.delta + self.pos[1] - y
            px_to_scr = self.px_to_scr - (0.1 * abs(self.scroll_pos[1] - y)) // 1
            if px_to_scr < 2:
                px_to_scr = 2
                
            if self.delta > 0:
                self.controller.scroll(0, self.delta // px_to_scr)
                self.delta %= px_to_scr
            elif self.delta < 0:
                self.controller.scroll(0, -(-self.delta // px_to_scr))
                self.delta = -(-self.delta % px_to_scr)
                
            """
            while abs(self.delta) >= 10:
                if self.delta < 0:
                    self.controller.scroll(0, -1)
                    self.delta += 10
                elif self.delta > 0:
                    self.controller.scroll(0, 1)
                    self.delta -= 10
            """
            
            self.pos = (x, y)
            
    def on_click(self, x, y, button, pressed):
        if button == Button.right:
            return False
        elif button == Button.middle and pressed:
            self.scroll_mode = not self.scroll_mode
            self.pos = (x, y)
            self.scroll_pos = (x, y)
            self.delta = 0

mouse = Mouse()

with Listener(on_move = mouse.on_move, on_click = mouse.on_click) as listener:
    listener.join()