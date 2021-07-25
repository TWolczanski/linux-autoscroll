import mouse
from pynput.mouse import Button, Controller, Listener
from subprocess import call

class Mice:
    def __init__(self):
        self.controller = Controller()
        self.scroll_mode = False
        self.scroll_direction = 'down'
        self.delta = 0
        self.mv_to_scr = 10
    
    def on_move(self, event):
        if self.scroll_mode:
            self.delta += 1
            if self.delta == self.mv_to_scr:
                if self.scroll_direction == 'down':
                    self.controller.scroll(0, -1)
                elif self.scroll_direction == 'up':
                    self.controller.scroll(0, 1)
                self.delta = 0

    def on_click(self, x, y, button, pressed):
        if button == Button.left and pressed and self.scroll_mode:
            self.delta = 0
            self.mv_to_scr = 15
            if self.scroll_direction == 'down':
                self.scroll_direction = 'up'
            elif self.scroll_direction == 'up':
                self.scroll_direction = 'down'
        if button == Button.right:
            call("xinput set-prop '2.4G Mouse' 'Coordinate Transformation Matrix' 1 0 0 0 1 0 0 0 1", shell = True)
            return False
        elif button == Button.middle and pressed:
            if self.scroll_mode == False:
                call("xinput set-prop '2.4G Mouse' 'Coordinate Transformation Matrix' 0 0 0 0 0 0 0 0 1", shell = True)
                self.delta = 0
                self.scroll_mode = True
                self.mv_to_scr = 15
            else:
                call("xinput set-prop '2.4G Mouse' 'Coordinate Transformation Matrix' 1 0 0 0 1 0 0 0 1", shell = True)
                self.scroll_mode = False

mice = Mice()
mouse.hook(mice.on_move)
with Listener(on_click = mice.on_click) as listener:
    listener.join()