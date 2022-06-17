This simple Python script gives you a Windows-like autoscroll feature on Linux. It works system-wide on every distribution using Xorg.

## Installation
There are two versions of the script. One of them (`autoscroll.py`) displays an icon indicating the place where the scroll mode has been entered and the other (`autoscroll_no_icon.py`) does not.
1. Clone the repository:
```
git clone https://github.com/TWolczanski/linux-autoscroll.git
cd linux-autoscroll/
```
2. Create a Python virtual environment and activate it:
```
python3 -m venv .autoscroll
source .autoscroll/bin/activate
```
3. Install necessary Python libraries (for `autoscroll_no_icon.py` you don't need the last one):
```
python3 -m pip install wheel
python3 -m pip install pynput
python3 -m pip install PyQt5
```
4. Add the following shebang to the script (substitute `/path/to` with the actual path):
```
#!/path/to/linux-autoscroll/.autoscroll/bin/python3
```
5. Make the script executable:
```
chmod u+x autoscroll.py
```
or
```
chmod u+x autoscroll_no_icon.py
```
6. Add the script to the list of autostart commands.

## Configuration

You can adjust the `DELAY`, `BUTTON_START`, `BUTTON_STOP`, `DEAD_AREA`, `TRIGGER_DELAY`, `CLEAR_CLIPBOARD` and `HOLD_MODE` constants for better experience.

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

`TRIGGER_DELAY` is the time `BUTTON_START` has to be held down for in order to enter the scroll mode. The default value of this constant is 0, meaning that the scroll mode is entered immediately after pressing `BUTTON_START`. Modifying `TRIGGER_DELAY` is a good idea if you have the middle mouse button assigned to `BUTTON_START`. For instance, if you set `TRIGGER_DELAY` to 0.5, you will be able to click the middle mouse button as usual, but after holding it for 0.5 sec you will enter the scroll mode. I would not recommend setting this constant to a value less than 0.5 (except for 0) - the timer is not that precise and might interpret clicks as holds.

If your `BUTTON_START` or `BUTTON_STOP` is the middle mouse button, consider setting `CLEAR_CLIPBOARD` to `True` so as not to paste anything accidentally from your clipboard when entering or exiting the scroll mode. Note that you have to have `xsel` installed before letting `CLEAR_CLIPBOARD = True`:
```
sudo apt install xsel
```

If you want to autoscroll only while `BUTTON_START` is held down, set `HOLD_MODE` to `True`.

In `autoscroll.py` you can also modify the `ICON_PATH` and `ICON_SIZE` constants. If you don't like the default icon displayed in the scroll mode, in `ICON_PATH` you can specify the absolute path to the image you want to be used instead. `ICON_SIZE` is the size (maximum of width and height) you want your image to be scaled to.

## Usage

Click (or hold for `TRIGGER_DELAY` seconds) the middle mouse button (or the button you assigned to `BUTTON_START`) and move your mouse to start scrolling. The further you move the mouse (vertically) from the point where you have clicked the button, the faster the scrolling becomes. To leave the scroll mode, simply press the middle mouse button again (or press the button you assigned to `BUTTON_STOP`).

Note that at slow speed the scrolling is not smooth and (probably) there is no way to make it smooth. The smoothness depends on the distance your mouse scrolls per one wheel click. There are some programs in which this distance is very small (e.g. Chrome, Teams and Discord) and in these programs the autoscroll is smoother than in others.
