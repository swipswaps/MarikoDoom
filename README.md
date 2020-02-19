# MarikoDoom
Play Doom on your Nintendo Switch without CFW!

## What is this?
This repository lets you play the original Doom (shareware) in your Nintendo Switch's hidden browser. No costum firmware needed.

Though, it won't be running on your Switch but rather on the computer you are running the server on.

Effectively this is a crude game streaming server with kind of high latency, low resolution and "some" (lol) dropped frames, so yes, even worse than Stadia ;)

## But... why?
Because everything needs to run Doom. Even patched Switch devices (Mariko and Lite) that to this date can't use soft modding exploits to run unsigned code.
This isn't meant to be a good way of playing the game. The only reason this exists is because I wanted to push the browser to it's limits and learn JavaScript.

Also, this repository can be used to do this for basically every game. I might make a separate repository for this and link it here.
Basically, replace `doom.py` with your own game, make it handle the joycon inputs and save the frame buffer at `static/img.jpg`. Keep the resolution and jpeg quality on the lower side and you're good to go.

## How do I use this?
(This works on Linux. I haven't tried this on Windows or OSX but I suppose it should work. You will have to make yourself a run.bat to replace the run.sh for Windows.)

1. Clone this repository
2. Install the dependencies

   `pip install flask vizdoom python-opencv --user`
3. Download doom1.wad

   `wget http://distro.ibiblio.org/pub/linux/distributions/slitaz/sources/packages/d/doom1.wad && mv doom1.wad scenarios/.`
4. Make run.sh executable

   `chmod +X run.sh`
5. Run the server

   `./run.sh`
6. Connect your Nintendo Switch to the same network as your server using the SwitchBru DNS 

   For more informations see: [switchbru.com](https://www.switchbru.com/dns/)
7. Find out your computers IP address and enter this as URL on the SwitchBru portal. Add it as costum link for convenience.

   `<YOUR_IP>:8080`
8. Tap the image to go fullscreen, click the left joystick and you are playing Doom.

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
