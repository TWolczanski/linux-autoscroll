import pyautogui
from pynput.mouse import Button, Controller, Listener

# TODO
# block the mouse pointer and change its look when the middle button is clicked
# refine delta
# overwrite middle mouse button behavior from other programs

SCREEN_HEIGHT = pyautogui.size()[1]

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
            d = self.pos[1] - y
            
            if self.delta * d < 0:
                self.delta = d
                self.scroll_pos = (x, y)
            else:
                self.delta += d
                
            if self.delta > 0:
                self.controller.scroll(0, self.delta // self.px_to_scr)
                self.delta %= self.px_to_scr
            else:
                self.controller.scroll(0, -(-self.delta // self.px_to_scr))
                self.delta = -(-self.delta % self.px_to_scr)
                
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
            
            global SCREEN_HEIGHT
            if self.pos[1] in [0, SCREEN_HEIGHT]:
                self.controller.position = self.scroll_pos
                self.pos = self.scroll_pos

    def on_click(self, x, y, button, pressed):
        if button == Button.right:
            return False
        elif button == Button.middle and pressed:
            self.scroll_mode = not self.scroll_mode
            self.pos = (x, y)
            self.scroll_pos = (x, y)

mouse = Mouse()
# mouse.controller.position = (mouse.controller.position[0], 5000)
# mouse.pos = mouse.controller.position

with Listener(on_move = mouse.on_move, on_click = mouse.on_click) as listener:
    listener.join()