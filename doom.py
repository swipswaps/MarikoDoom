import vizdoom as vzd
import cv2, os 
from time import sleep, time
import socket, select
import sys

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

    # Enables depth buffer.
    game.set_depth_buffer_enabled(False)

    # Enables labeling of in game objects labeling.
    game.set_labels_buffer_enabled(False)

    # Enables buffer with top down map of the current episode/level.
    game.set_automap_buffer_enabled(False)

    # Enables information about all objects present in the current episode/level.
    game.set_objects_info_enabled(False)

    # Enables information about all sectors (map layout).
    game.set_sectors_info_enabled(False)

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

    # Adds game variables that will be included in state.
    game.add_available_game_variable(vzd.GameVariable.AMMO2)

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

def fpscounter(img, fps):
    font                   = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (375,15)
    fontScale              = 0.5
    fontColor              = (255,255,0)
    lineType               = 1

    cv2.putText(img, str(fps)[:2], bottomLeftCornerOfText, font, fontScale,fontColor,lineType)

    return img

def main():
    joystep = 1
    maxjoystep = 2
    frame_timeout = 0.01
    max_fps = 45
    start = time()
    i = 0
    fps = 0
    show_server_fps = False
    scenario = "doom1"
    map = 1
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(0.001)
    # Bind the socket to the port
    server_address = ('localhost', 10000)
    print(" * Doom server starting up on {} port {}".format(*server_address))
    sock.bind(server_address)
   
    while True:        
        game = init(scenario, "E1M" + str(map))
        data = 0
        while not game.is_episode_finished():        
            # Gets the state
            state = game.get_state()    

            # Gets current screen buffer and updates frame on server 
            screen_buf = state.screen_buffer
            if show_server_fps:
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
            if data:      
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
            else:
                action=[False, False, 0, False, False, False, False, 0, False, False, False, False]
            r = game.make_action(action)
            i+=1

            # dynamic fps adjustment
            if i%30==0:                
                fps = (30/(time()-start))
                if fps < max_fps:
                    frame_timeout = frame_timeout - 0.05*frame_timeout
                elif fps > max_fps:
                    frame_timeout = frame_timeout + 0.05*frame_timeout
                start = time()            
            sleep(frame_timeout)

        if game.get_last_reward() == 1:
            map += 1
            print(" * Level finished.")
        else:
            print(" * Player died. Restart level.")
        print("   Total reward:", game.get_total_reward())
        print("   ************************") 


if __name__ == "__main__":
    main()
