For some Linux users, especially those coming from Windows, scrolling through long PDFs or webpages is a real nightmare. On Windows you just click the middle mouse button to start scrolling and move your mouse to adjust the direction and speed.

This is exactly what this simple Python script does. It gives you a Windows-like autoscroll feature on Linux. It works system-wide on every distribution with Xorg.

## Installation

1. Clone the repository:
```
git clone https://github.com/TWolczanski/linux-autoscroll.git
```
2. Create a Python virtual environment and activate it:
```
cd linux-autoscroll/
python3 -m venv .venv
source .venv/bin/activate
```
3. Install pynput:
```
python3 -m pip install pynput
```
4. Add the following shebang to the script (substitute `/path/to/linux-autoscroll` with the actual path to your virtual environment):
```
#!/path/to/linux-autoscroll/.venv/bin/python3
```
5. Make the script executable:
```
chmod u+x autoscroll.py
```
6. Add the script to the list of autostart commands.

## Configuration

You can adjust the `DELAY` and `BUTTON` constants for better experience.

By changing `DELAY` you can adjust the speed of scrolling. By default its value is 3 but you may find it either too fast or too slow. You can decrease the value to make scrolling faster or increase it to make scrolling slower.

Modifying `BUTTON` is going to change the button used for entering the scroll mode. The default is the middle mouse button but if your mouse has additional side buttons it might be a good idea to use one of them instead, as the middle button is often used for different purposes (for example to open a link in a new tab in most web browsers or to copy and paste text system-wide). As the script is using the pynput library, you can hopefully find the name of the side button with the following piece of code:
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
Then just replace `BUTTON = Button.middle` with `BUTTON = Button.name` where `name` is the name of the side button.
