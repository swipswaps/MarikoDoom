# MarikoDoom
Play Doom on your Nintendo Switch without CFW!

## What is this?
This repository lets you play the levels of the original Doom (shareware) in your Nintendo Switch's hidden browser. No costum firmware needed.

Though, it won't be running on your Switch but rather on the computer you are running the server on.

Effectively this is a crude game streaming server with kind of high latency, low resolution and "some" (lol) dropped frames, so yes, worse than Stadia ;) 

To keep it simple, I used ViZDoom as my engine since it allows easy access to the frame buffer. I tried to build a screen casting application first but the delay was huge since I could not figure out a way to access the screen's frame buffer with more than 10 FPS (at least on my computer). I'm aware there are projects like [this](https://www.linux-projects.org/uv4l/tutorials/play-retropie-in-browser/) that do something pretty similar to what I did. However they use features (WebRTC) the browser does not support. In the future I might look into porting that to my engine though.

## But... why?
Because everything needs to run Doom. Even patched Switch devices (Mariko and Lite) that to this date can't use soft modding exploits to run unsigned code.
This isn't meant to be a good way of playing the game. The only reason this exists is because I wanted to push the browser to it's limits and learn JavaScript.

Also, this repository can be used to do this for basically every game. I might make a separate repository for this and link it here.
Basically, replace `doom.py` with your own game, make it handle the joycon inputs and save the frame buffer at `static/img.jpg`. Keep the resolution and jpeg quality on the lower side and you're good to go.

## How do I use this?
(This works on Linux (Manjaro). I haven't tried this on Windows or OSX but I suppose it should work there too. You will have to make yourself a `run.bat` to replace the `run.sh` for Windows.)

This guide assumes you are using `python3.x` under the alias `python` and `pip3` under the alias `pip` (i.e. Arch/Manjaro). 

If you use python3/pip3 (i.e. Ubuntu/Raspbian) change those accordingly in the guide and `run.sh`.

1. Clone this repository
   ```bash
   git clone https://github.com/z80z80z80/MarikoDoom.git
   cd MarikoDoom
   ```
2. Install the dependencies (On raspbian python-opencv does not exist for pip. For installation instructions see [here](https://raspberrypi.stackexchange.com/questions/95982/how-to-install-opencv-on-raspbian-stretch))
   
   First, make sure you have all [ViZDoom dependencies](https://github.com/mwydmuch/ViZDoom/blob/master/doc/Building.md#linux_deps) installed.
   
   After that, install the python dependencies:
   
   `pip install flask cython vizdoom python-opencv --user`
   
3. Download doom1.wad

   ```bash
   wget http://distro.ibiblio.org/pub/linux/distributions/slitaz/sources/packages/d/doom1.wad
   mv doom1.wad scenarios/.
   ```
4. Make run.sh and stop.sh executable

   ```bash
   chmod +x run.sh
   chmod +x stop.sh
   ```
5. Run the server

   `./run.sh`
6. Connect your Nintendo Switch to the same network as your server using the SwitchBru DNS 

   For more informations see: [switchbru.com](https://www.switchbru.com/dns/)
7. Find out your computers IP address and enter this as URL on the SwitchBru portal. Add it as costum link for convenience.

   `<YOUR_IP>:8080`
8. Tap the image to go fullscreen, click the left joystick and you are playing Doom.

9. To shut down the server:
   `./stop.sh`

## Controls
The usable buttons are a bit limited since the browser uses B to go back and X to close the browser.

Button | Action
-------| ------
Left joystick | Move around
A | Attack
Y | Use
ZR | Next weapon
ZL | Previous weapon
-------| ------
DPad left | Turn left
DPad right | Turn right
DPad up | Move forward
DPad down | Move backward
Shoulder L | Move left
Shoulder R | Move right
