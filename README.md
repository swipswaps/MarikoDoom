# MarikoDoom
Play Doom on your Nintendo Switch without CFW.

## What is this?
This repository lets you play the levels of the original Doom (shareware) in your Nintendo Switch's hidden browser. No costum firmware needed.

Though, it won't be running on your Switch but rather on the computer you are running the server on.

Effectively this is a crude game streaming server with very low resolution and a low framerate. Even after optimizing the engine to minimize stuttering it still randomly happens. In this case close the browser, go to the home screen, reconnect and repeat if it still stutters. I'm not sure what is causing this but I suspect it's from filling the memory with a lot of cached frames (which to my knowledge is not a solveable issue...)

To keep it simple, I used ViZDoom as my engine since it allows easy access to the frame buffer.

## But... why?
Because everything needs to run Doom. Even patched Switch devices (Mariko and Lite) that to this date can't use soft modding exploits to run unsigned code.
This isn't meant to be a good way of playing the game. The only reason this exists is because I wanted to push the browser to it's limits and learn more about web development.

Also, this code can be used to do this for basically every game. I might eventually make a separate repository for this and link it here.
Basically, replace `doom.py` with your own game, make it handle the joycon inputs and save the graphical output frame by frame at `static/img.jpg`. Keep the resolution and jpeg quality on the lower side (< 12kB per frame) and you're good to go.

## How do I use this?
(This works on Linux (Manjaro). I haven't tried it on Windows or OSX.

Once I get it to run on a Raspberry Pi, instructions will be added. Or rather a working disk image so no one else has to go through the hells of compiling Doom on a RPi Zero. The goal would be to have a stand alone device to which you connect via wifi.)

1. Clone this repository
   ```bash
   git clone https://github.com/z80z80z80/MarikoDoom.git
   cd MarikoDoom
   ```
2. Install the dependencies
   
   First, make sure you have all [ViZDoom dependencies](https://github.com/mwydmuch/ViZDoom/blob/master/doc/Building.md#linux_deps) installed.      
 
   After this, install [create_ap](https://github.com/oblique/create_ap):
 
   - Ubuntu:    
      `sudo apt-get install hostapd`
   
      `git clone https://www.github.com/oblique/create_ap && cd create_ap && make install`  

   - Arch/Manjaro:
      `sudo pacman -S create_ap`

   Finally, install the python dependencies:
   
   `sudo pip install flask cython vizdoom python-opencv`

   Optional: If you want music in the game (played by the host of course) you will need to install [Timidity](https://wiki.archlinux.org/index.php/Timidity) and a [soundfont](http://www.arachnosoft.com/main/soundfont.php?music-packs). 
   
3. Download doom1.wad

   ```bash
   wget http://distro.ibiblio.org/pub/linux/distributions/slitaz/sources/packages/d/doom1.wad
   mv doom1.wad scenarios/.
   ```
4. Run the server

   ```bash
   sudo python run.py
   ```
   optional arguments:
   ```bash
   -h, --help   show this help message and exit
   --port PORT  port of the http server (default = 80). If you don't want to run this with sudo, use --port 8080
   --fps N      client fps (1 = 15FPS, 2 = 20FPS, default: 2)
   --res N      resolution (1 = low, 2 = mid, default: 1)
   ```
   
5. Connect your Nintendo Switch to the same network as your server and use the given IP address as manual DNS server in your network settings. Don't know how? [Here you go.](https://en-americas-support.nintendo.com/app/answers/detail/a_id/22411/~/how-to-manually-enter-dns-settings)

6. Tap the image to go fullscreen, click the left joystick and you are playing Doom.

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

