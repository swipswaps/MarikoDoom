import vizdoom as vzd
import cv2, os 
from time import sleep, time
import socket
import argparse

def init(scenario, map):
    # Create DoomGame instance. It will run the game and communicate with you.
    game = vzd.DoomGame()

    # Load the Doom scenario from the supplied WAD
    game.set_doom_scenario_path("scenarios/"+scenario+".wad") 

    # Sets map to start (scenario .wad files can contain many maps).
    game.set_doom_map(map)

    # Sets resolution. Default is 320X240
    game.set_screen_resolution(vzd.ScreenResolution.RES_400X225)

    # Sets the screen buffer format. Not used here but now you can change it. Default is CRCGCB.
    game.set_screen_format(vzd.ScreenFormat.RGB24)

    # Sets other rendering options (all of these options except crosshair are enabled (set to True) by default)
    game.set_render_hud(True)
    game.set_render_minimal_hud(False)  # If hud is enabled
    game.set_render_crosshair(False)
    game.set_render_weapon(True)
    game.set_render_decals(True)  # Bullet holes and blood on the walls
    game.set_render_particles(True)
    game.set_render_effects_sprites(True)  # Smoke and blood
    game.set_render_messages(True)  # In-game messages
    game.set_render_corpses(True)
    game.set_render_screen_flashes(True)  # Effect upon taking damage or picking up items

    # Adds buttons that will be allowed.
    game.add_available_button(vzd.Button.TURN_LEFT)
    game.add_available_button(vzd.Button.TURN_RIGHT)
    game.add_available_button(vzd.Button.TURN_LEFT_RIGHT_DELTA)
    game.add_available_button(vzd.Button.MOVE_LEFT)
    game.add_available_button(vzd.Button.MOVE_RIGHT)
    game.add_available_button(vzd.Button.MOVE_FORWARD)
    game.add_available_button(vzd.Button.MOVE_BACKWARD)    
    game.add_available_button(vzd.Button.MOVE_FORWARD_BACKWARD_DELTA)
    game.add_available_button(vzd.Button.ATTACK)
    game.add_available_button(vzd.Button.USE)
    game.add_available_button(vzd.Button.SELECT_PREV_WEAPON)  
    game.add_available_button(vzd.Button.SELECT_NEXT_WEAPON)  

    # Causes episodes to finish after 200 tics (actions)
    game.set_episode_timeout(0)

    # Makes episodes start after 10 tics (~after raising the weapon)
    game.set_episode_start_time(10)

    # Enable sound from host
    game.set_sound_enabled(True)

    # Makes the window appear (turned on by default)
    game.set_window_visible(False)

    # Sets ViZDoom mode (PLAYER, ASYNC_PLAYER, SPECTATOR, ASYNC_SPECTATOR, PLAYER mode is default)
    game.set_mode(vzd.Mode.PLAYER)

    # Sets rewards/penalty for surviving/death
    game.set_living_reward(1)
    game.set_death_penalty(-1)

    # Initialize the game. Further configuration won't take any effect from now on.
    game.init()

    return game

def gen_actions(data):
    if data == "INIT":
        print(" * Client connected.")
    elif data == "left_down": #TURN_LEFT
        action=[True, False, 0, False, False, False, False, 0, False, False, False, False]
    elif data == "right_down": #TURN_RIGHT
        action=[False, True, 0, False, False, False, False, 0, False, False, False, False]
    elif data[0:7] == "Stick;1": #TURN_LEFT_RIGHT_DELTA + MOVE_FORWARD_BACKWARD_DELTA
        if joystep < maxjoystep:
            joystep+=1
            ax0 = ((float(data.split(";")[2])*10)/maxjoystep)*joystep
            ax1 = ((-float(data.split(";")[3])*30)/maxjoystep)*joystep
            action=[False, False, 0, False, False, False, False, 0, False, False, False, False]
            if ax0 < -1.5:
                action[0]=True
            elif ax0 > 1.5:
                action[1]=True
            if ax1 < -15:
                action[6]=True
            elif ax1 > 15:
                action[5]=True
        else:
            data = 0 
            joystep = 0
    elif data == "sl_down": #MOVE_LEFT
        action=[False, False, 0, True, False, False, False, 0, False, False, False, False]  
    elif data == "sr_down": #MOVE_RIGHT
        action=[False, False, 0, False, True, False, False, 0, False, False, False, False]                   
    elif data == "up_down": #MOVE_FORWARD
        action=[False, False, 0, False, False, True, False, 0, False, False, False, False]
    elif data == "down_down": #MOVE_BACKWARD
        action=[False, False, 0, False, False, False, True, 0, False, False, False, False]
    elif data == "a_down": #ATTACK
        action=[False, False, 0, False, False, False, False, 0, True, False, False, False]
    elif data == "y_down": #USE
        action=[False, False, 0, False, False, False, False, 0, False, True, False, False]
    elif data == "zl_down": #SELECT_PREV_WEAPON
        action=[False, False, 0, False, False, False, False, 0, False, False, True, False]
    elif data == "zr_down": #SELECT_NEXT_WEAPON
        action=[False, False, 0, False, False, False, False, 0, False, False, False, True]                   
    else:
        action=[False, False, 0, False, False, False, False, 0, False, False, False, False]

    return data, joystep, action

def fpscounter(img, fps): # shows server side fps counter
    font                   = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (375,15)
    fontScale              = 0.5
    fontColor              = (255,255,0)
    lineType               = 1

    cv2.putText(img, str(fps)[:2], bottomLeftCornerOfText, font, fontScale,fontColor,lineType)

    return img

def find_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("duckduckgo.com", 80))
    ip = s.getsockname()[0]
    s.close()
    
    return ip

def parse_arg():
    parser = argparse.ArgumentParser(description='ViZDoom based Doom server.', usage='python %(prog)s [options]')
    parser.add_argument('--nosound', dest='sound', default=True, help='decativate sound on the host')
    parser.add_argument('--http', dest='http_port', default=8080, metavar='PORT', help='port of the http server')
    parser.add_argument('--fps', dest='server_fps', default=False, help='show the server side fps in the top left corner')
    parser.add_argument('--maxfps', dest='max_fps', metavar='N', default=45, help='goal fps of dynamic fps adjustment (default: 45)')
    parser.add_argument('--joystep', dest='joystep', metavar='N', default=2, help='sensitivy of the joystick (default: 2)')

    args = parser.parse_args()

    return args

def main(args):
    joystep = 1
    maxjoystep = args.joystep    # drops joystick inputs to adjust sensitivity 
    frame_timeout = 0.01     # initial frame_timeout
    max_fps = args.max_fps   # the goal of the server side dynamic frame rate adjustment      
    start = time()           # to calculate the fps
    i = 1                    # frame counter
    fps = 0              
    scenario = "doom1"       # load doom1 shareware
    map = 1                  # initial map id

    running = False # indication if doom was already started

    # Create an UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(0.001) # don't wait for replys

    # Bind the socket to the port
    server_address = ('localhost', 1312)
    http_ip = find_ip() # retrieve the local IP of the http server (this machine)

    print(" * Doom starting up...")   
    sock.bind(server_address)

    while True:        
        game = init(scenario, "E1M" + str(map)) # load map

        if not running:
           running = True
           print(" * Doom ready.")
           if int(args.http_port) == 80:       
               print("\033[1;32m * Please enter %s as manual DNS \033[0;32m" % (http_ip))
               print("   (in the network settings of your Nintendo Switch)\033[0;39m")
           else:
               print("\033[1;32m * Please connect your console to this url: %s:%s \033[0;32m" % (http_ip, args.http_port))
               print("   (using i.e. https://www.switchbru.com/dns/)\033[0;39m")

        data = 0

        while not game.is_episode_finished():        
            # Gets the state
            state = game.get_state()    

            # Gets current screen buffer and updates frame on server 
            screen_buf = state.screen_buffer
            if args.server_fps:
                screen_buf = fpscounter(screen_buf, fps)
            screen_buf = cv2.cvtColor(screen_buf, cv2.COLOR_BGR2RGB)            
            cv2.imwrite("static/tmp.jpg", screen_buf, [int(cv2.IMWRITE_JPEG_QUALITY), 75])

            # prevent flickering from incomplete images    
            os.system("mv static/tmp.jpg static/img.jpg") 

            # Gets player input
            try:
                data, address = sock.recvfrom(4096)
                data = data.decode()
            except socket.timeout:
                pass

            # if there is any input execute it
            if data:      
                data, joystep, action = get_action(data, joystep, maxjoystep)
            else:
                action=[False, False, 0, False, False, False, False, 0, False, False, False, False]

            r = game.make_action(action)
            i+=1

            # dynamic fps adjustment
            if i%30==0:
                i = 1                
                fps = (30/(time()-start))
                if fps < max_fps:
                    frame_timeout = frame_timeout - 0.05*frame_timeout
                elif fps > max_fps:
                    frame_timeout = frame_timeout + 0.05*frame_timeout
                start = time()
            
            sleep(frame_timeout) # Doom is has tic-based logic so we need to stop for a while after every frame to get a reasonable refresh rate

        if game.get_last_reward() == 1: # find out if the player died or found the exit
            map += 1
            print(" * Play survived the level. Starting next level.")
        else:
            print(" * Player died. Restart level.")
        print("   ************************") 

if __name__ == "__main__":

    args = parse_arg() # parse the arguments supplied by the user or script

    try:
        main(args)

    except:
#        os.system("rm static/img.jpg")
        print("\n *\033[1;31m Server stopped.\033[0;36m")
        
