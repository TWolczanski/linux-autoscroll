This simple Python script gives you a Windows-like autoscroll feature on Linux. It works system-wide on every distribution with Xorg.

## Installation

1. Clone the repository:
```
git clone https://github.com/adeliktas/linux-autoscroll.git
```
2. Create a Python virtual environment and activate it:
```
python3 -m venv .autoscroll
source .autoscroll/bin/activate
```
3. Install pynput:
```
pip3 install --user pynput
(python3 -m pip install pynput)
```
4. Add the following shebang to the script (substitute `/path/to` with the actual path to your virtual environment):
```
#!/path/to/.autoscroll/bin/python3
```
5. Make the script executable:
```
chmod u+x autoscroll.py
```
6. Add the script to the list of autostart commands.

## Configuration

You can adjust the `DELAY`, `BUTTON_START`, `BUTTON_STOP` and `DEAD_AREA` constants for better experience.

By changing `DELAY` you can adjust the speed of scrolling. By default its value is 5 but you may find it either too fast or too slow. You can decrease the value to make scrolling faster or increase it to make scrolling slower.

Modifying `BUTTON_START` and `BUTTON_STOP` is going to change the button used for entering and exiting the scroll mode. The default for both is the middle mouse button but if your mouse has additional side buttons it might be a good idea to use them instead, as the middle button is often used for different purposes (for example to open a link in a new tab in most web browsers or to copy and paste text system-wide). As the script is using the pynput library, you can hopefully find names of all of your mouse buttons with the following piece of code:
```python
from pynput.mouse import Button, Listener

def on_click(x, y, button, pressed):
    print(button)
    # click the middle button to exit
    if button == Button.middle:
        return False
    
with Listener(on_click = on_click) as listener:
    listener.join()
```
\
By default the scrolling begins when the mouse pointer is 30 px below or above the point where `BUTTON_START` was pressed. In order to change that you can modify `DEAD_AREA`. If you set it to 0 (which is the minimum value), the scrolling will be paused only when the vertical position of the cursor is exactly the same as the position in which the scroll mode was activated.

## Usage

Click the middle mouse button (or the button you assigned to `BUTTON_START`) and move your mouse to start scrolling. The further you move the mouse (vertically) from the point where you have clicked the button, the faster the scrolling becomes. To leave the scroll mode, simply press the middle mouse button again (or press the button you assigned to `BUTTON_STOP`).

Note that at slow speed the scrolling is not smooth and (probably) there is no way to make it smooth. However, one can easily get used to it.

## Todo

-improve scroll smoothness
-fix losing window title bar control handle
