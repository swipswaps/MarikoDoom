import vizdoom as vzd
import cv2, os 
from time import sleep, time
import socket
import argparse

def init(scenario, map, client_res):
    # Create DoomGame instance. It will run the game and communicate with you.
    game = vzd.DoomGame()

    # Load the Doom scenario from the supplied WAD
    game.set_doom_scenario_path("scenarios/"+scenario+".wad") 

    # Sets map to start (scenario .wad files can contain many maps).
    game.set_doom_map(map)

    # Sets resolution. Default is 320X240 (16:9 - RES_256X144 RES_320X180 RES_400X225 RES_512X288
    if client_res == 1:
        res = vzd.ScreenResolution.RES_320X180
    elif client_res == 2:
        res = vzd.ScreenResolution.RES_400X225
    else:
        res = vzd.ScreenResolution.RES_256X144
    game.set_screen_resolution(res)

    # Sets the screen buffer format. Not used here but now you can change it. Default is CRCGCB.
    game.set_screen_format(vzd.ScreenFormat.BGR24)

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

    # Adds all needed variables
    game.add_available_game_variable(vzd.GameVariable.HEALTH)
    game.add_available_game_variable(vzd.GameVariable.ARMOR)
    game.add_available_game_variable(vzd.GameVariable.AMMO2)
    game.add_available_game_variable(vzd.GameVariable.AMMO3)
    game.add_available_game_variable(vzd.GameVariable.AMMO4)
    game.add_available_game_variable(vzd.GameVariable.AMMO5)
    game.add_available_game_variable(vzd.GameVariable.AMMO6)
    game.add_available_game_variable(vzd.GameVariable.AMMO7)
    game.add_available_game_variable(vzd.GameVariable.WEAPON1)
    game.add_available_game_variable(vzd.GameVariable.WEAPON2)
    game.add_available_game_variable(vzd.GameVariable.WEAPON3)
    game.add_available_game_variable(vzd.GameVariable.WEAPON4)
    game.add_available_game_variable(vzd.GameVariable.WEAPON5)
    game.add_available_game_variable(vzd.GameVariable.WEAPON6)
    game.add_available_game_variable(vzd.GameVariable.WEAPON7)

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

def get_action(data, game, action):
    if not len(action):
        action = [False, False, 0, False, False, False, False, 0, False, False, False, False]

    if data == "INIT":
        print(" * Client connected.")
        game.send_game_command("set snd_musicvolume 0.5")
        data = 0
    elif data == "left_down": #TURN_LEFT
        action[0] = True
    elif data == "right_down": #TURN_RIGHT
        action[1] = True
    elif data[0:7] == "Stick;1": #TURN_LEFT_RIGHT_DELTA + MOVE_FORWARD_BACKWARD_DELTA
        ax0 = float(data.split(";")[2])
        ax1 = -float(data.split(";")[3])
        if (ax0>0.2 or ax0<-0.2 or ax1>0.2 or ax1<-0.2):
            action[2]=ax0*10
            action[7]=ax1*30

    elif data == "sl_down": #MOVE_LEFT
        action[3] = True
    elif data == "sl_up": 
        action[3] = False
    elif data == "sr_down": #MOVE_RIGHT
        action[4] = True
    elif data == "sr_up": 
        action[4] = False
    elif data == "up_down": #MOVE_FORWARD
        action[5] = True
    elif data == "up_up": 
        action[5] = False
    elif data == "down_down": #MOVE_BACKWARD
        action[6] = True
    elif data == "down_up": 
        action[6] = False
    elif data == "a_down": #ATTACK
        action[8] = True
    elif data == "a_up": 
        action[8] = False
    elif data == "y_down": #USE
        action[9] = True
    elif data == "y_up": 
        action[9] = False
    elif data == "zl_down": #SELECT_PREV_WEAPON
        action[10] = True
    elif data == "zl_up": 
        action[10] = False
    elif data == "zr_down": #SELECT_NEXT_WEAPON
        action[11] = True
    elif data == "zr_up": 
        action[11] = False
    else:
        action=[False, False, 0, False, False, False, False, 0, False, False, False, False]

    return data, action

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

def save(game):
    player_state = {
        "HEALTH": game.get_game_variable(vzd.GameVariable.HEALTH),
        "ARMOR": game.get_game_variable(vzd.GameVariable.ARMOR),

        "AMMO2": game.get_game_variable(vzd.GameVariable.AMMO2),
        "AMMO3": game.get_game_variable(vzd.GameVariable.AMMO3),
        "AMMO4": game.get_game_variable(vzd.GameVariable.AMMO4),
        "AMMO5": game.get_game_variable(vzd.GameVariable.AMMO5),
        "AMMO6": game.get_game_variable(vzd.GameVariable.AMMO6),
        "AMMO7": game.get_game_variable(vzd.GameVariable.AMMO7),

        "WEAPON1": game.get_game_variable(vzd.GameVariable.WEAPON1),
        "WEAPON2": game.get_game_variable(vzd.GameVariable.WEAPON2),
        "WEAPON3": game.get_game_variable(vzd.GameVariable.WEAPON3),
        "WEAPON4": game.get_game_variable(vzd.GameVariable.WEAPON4),
        "WEAPON5": game.get_game_variable(vzd.GameVariable.WEAPON5),
        "WEAPON6": game.get_game_variable(vzd.GameVariable.WEAPON6),
        "WEAPON7": game.get_game_variable(vzd.GameVariable.WEAPON7)
        }

    return player_state

def restore_save(game, player_state):
    if player_state["HEALTH"] < 100:
        game.send_game_command("take health %s" % str(100-player_state["HEALTH"]))
    else:
        game.send_game_command("give health %s" % str(100-player_state["HEALTH"]))
    if player_state["ARMOR"]:
        game.send_game_command("give ARMOR %s" % str(100-player_state["ARMOR"]))

    if player_state["WEAPON1"] == 2.0:
        game.send_game_command("give Chainsaw")   
    if player_state["WEAPON3"] == 1.0:        
        game.send_game_command("give Shotgun")        
    elif player_state["WEAPON3"] == 2.0:        
        game.send_game_command("give SuperShotgun")  
    if player_state["WEAPON4"] == 1.0:
        game.send_game_command("give Chaingun")      
    if player_state["WEAPON5"] == 1.0:
        game.send_game_command("give RocketLauncher")      
    if player_state["WEAPON6"] == 1.0:
        game.send_game_command("give PlasmaRifle")    
    if player_state["WEAPON7"] == 1.0:
        game.send_game_command("give BFG9000")          

    if player_state["AMMO2"] < 50:
        game.send_game_command("take Clip %s" % str(50 - player_state["AMMO2"]))     
    else:
        game.send_game_command("give Clip %s" % str(50 - player_state["AMMO2"]))     
    if player_state["AMMO3"]:
        game.send_game_command("give Shell %s" % str(player_state["AMMO3"]))     
    if player_state["AMMO5"]:
        game.send_game_command("give RockeAmmo %s" % str(player_state["AMMO5"]))     
    if player_state["AMMO6"] or player_state["AMMO7"]:
        game.send_game_command("give Cell %s" % str(player_state["AMMO6"]))       

def parse_arg():
    parser = argparse.ArgumentParser(description='ViZDoom based Doom server.', usage='python %(prog)s [options]')
    parser.add_argument('--nosound', dest='sound', default=True, help='decativate sound on the host')
    parser.add_argument('--http', dest='http_port', default=8080, metavar='PORT', help='port of the http server')
    parser.add_argument('--ap', dest='ap', metavar='INT', default=False, help='start ap with interface INT (see "ip address" to find your wifi interface, i.e. wlan0 or wlp2s0)')    
    parser.add_argument('--serverfps', dest='server_fps', default=False, help='show the server side fps in the top left corner')
    parser.add_argument('--maxfps', dest='max_fps', metavar='N', default=35, help='goal fps of dynamic fps adjustment (default: 35)')
    parser.add_argument('--fps', dest='fps', metavar='N', default=2, help='client fps (1 = 15FPS, 2 = 20FPS, default: 2)')    
    parser.add_argument('--res', dest='res', metavar='N', default=1, help='resolution (1 = low, 2 = mid, default: 1)')

    args = parser.parse_args()

    return args

def main(args):

    frame_timeout = 0.01          # initial frame_timeout
    max_fps = int(args.max_fps)   # the goal of the server side dynamic frame rate adjustment   
    client_fps = int(args.fps)    # the refresh rate the user wishes to play at
    client_res = int(args.res)    # the quality the user wishes to play at
    start = time()                # to calculate the fps
    i = 1                         # frame counter
    fps = 0              
    scenario = "doom1"            # load doom1 shareware
    map = 1                       # initial map id

    survived = False
    running = False # indication if doom was already started

    # Create an UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(0.001) # don't wait for replys

    # Bind the socket to the port
    server_address = ('localhost', 1312)
    http_ip = find_ip() # retrieve the local IP of the http server (this machine)

    print(" * Doom starting up...")   
    sock.bind(server_address)
    
    action = action=[False, False, 0, False, False, False, False, 0, False, False, False, False]

    while True:        
        game = init(scenario, "E1M%s" % str(map), client_res) # load map

        if not running:
            game.send_game_command("set snd_musicvolume 0.0")
            game.send_game_command("set snd_mididevice -2") # using timidity++
            running = True
            print(" * Doom ready.")
            if not args.ap:
                if int(args.http_port) == 80:       
                    print("\033[1;32m * Please enter %s as manual DNS \033[0;32m" % (http_ip))
                    print("   (in the network settings of your Nintendo Switch)\033[0;39m")
                else:
                    print("\033[1;32m * Please connect your console to this url: %s:%s \033[0;32m" % (http_ip, args.http_port))
                    print("   (using i.e. https://www.switchbru.com/dns/)\033[0;39m")
            else:
                 print('\033[1;32m * Please connect to the "MarikoDoom" wifi access point with your Nintendo Switch.\033[0;39m')
        else:
            game.send_game_command("set snd_musicvolume 0.5")
        game.send_game_command("changemus d_e1m%s" % str(map))

        if survived:
            restore_save(game, player_state)

        data = 0

        while not game.is_episode_finished():        
            # Gets the state
            state = game.get_state()    
            
            # Gets current screen buffer and updates frame on server 
            screen_buf = state.screen_buffer

            if args.server_fps: # based on fps and resolution use the best combination (performance/quality/playability)
                screen_buf = fpscounter(screen_buf, fps)
            if client_fps == 1:
               if client_res == 1:
                  compression = 77
               elif client_res == 2:
                  compression = 60
            elif client_fps == 2:
               if client_res == 1:
                  compression = 60
               elif client_res == 2:
                  compression = 40
            else:
               compression = 40

            cv2.imwrite("static/tmp.jpg", screen_buf, [int(cv2.IMWRITE_JPEG_QUALITY), compression])

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
                data, action = get_action(data, game, action)
                if (action[2]!=0 or action[7]!=0):
                    data = 0

            r = game.make_action(action)

            # reset the joystick
            action[2] = 0 # reset ax0
            action[7] = 0 # reset ax1

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
            survived = True
            player_state = save(game)            
            print(" * Player survived the level. Starting next level.")
        else:
            survived = False
            print(" * Player died. Restart level.")
        print("   ************************") 

if __name__ == "__main__":

    args = parse_arg() # parse the arguments supplied by the user or script    

    try:
        main(args)
    except:
        os.system("rm -rf _vizdoom _vizdoom.ini vizdoom-crash.log") # don't @ me, I know it's dirty...
        print("\n *\033[1;31m Server stopped.\033[0;36m")
