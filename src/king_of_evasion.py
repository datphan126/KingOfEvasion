"""
 King of Evasion - Touch the Green Orb to gain points.
 
 There are four difficulty modes in this game:
 Easy, Medium, Hard, and Impossible
 
 After gaining a specific amount of points, the speed of asteroids will increase
 
 Author: Dat Phan
"""
 
import pygame
import random
import sys
import os
import csv
import game_definitions as gd
import ship_sprite 
import asteroid_sprite
import reward_sprite
import custom_sprite
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Game State
GAME_STATE_OVER = "GAMEOVER"
GAME_STATE_MENU = "MENU"
GAME_STATE_PLAY = "PLAY"
GAME_STATE_COUNTDOWN = "COUNTDOWN"
GAME_STATE_SELECT_DIFFICULTY = "SELECT DIFFICULTY"
GAME_STATE_SELECT_GAME_MODE = "SELECT GAME MODE"
GAME_STATE_SELECT_CONTROLLER = "SELECT CONTROLLER"
GAME_STATE_VIEW_HIGHSCORE = "VIEW HIGHSCORE"
GAME_STATE_SELECT_HIGHSCORE_MODE = "SELECT HIGHSCORE MODE"

# Game Difficulty definition
GAME_DIFFICULTY_EASY = "EASY"
GAME_DIFFICULTY_MED = "MEDIUM"
GAME_DIFFICULTY_HARD = "HARD"
GAME_DIFFICULTY_IMPOSSIBLE = "IMPOSSIBLE"

# Game modes
GAME_MODE_NORMAL = "Normal Mode"
GAME_MODE_TIMER = "Timer Mode"

pygame.init()
 
# Set the height and width of the screen
size = [gd.SCREEN_WIDTH, gd.SCREEN_HEIGHT]
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
 
pygame.display.set_caption("King Of Evasion")
 
# Loop until the user clicks the close button.
done = False

# Frame rate
frame_rate = 60

# timer
tick_rate = 30
tick_count = 0
timer_limit = 0

# Highscore game mode - Used to switch views of game modes
highscore_view_mode = gd.HIGHSCORE_VIEW_MODE_NORMAL

# Game controller
game_controller = gd.GAME_CONTROLLER_MOUSE

# Game mode
game_mode = GAME_MODE_NORMAL

# Game difficulty
game_difficulty = GAME_DIFFICULTY_EASY

# Asteroid speed - Default speed is Easy mode's speed
asteroid_speed = gd.ASTEROID_MOVE_SPEED_EASY
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Create new asteroid list
asteroid_list = pygame.sprite.Group()
# Number of asteroids
asteroid_list_size = 0

game_state = GAME_STATE_MENU

# Reward item status - if true, item is already created. If false, item isn't created
reward_item_status = False
score = 0
old_score = 0

# Countdown before the match starts
countdown = 3

# Fonts
normal_font = pygame.font.SysFont('Calibri', 25, True, False)
title_font_1 = pygame.font.SysFont('Calibri', 50, True, False)
title_font_2 = pygame.font.SysFont('Calibri', 130, True, False)
countdown_font = pygame.font.SysFont('Calibri', 105, True, False)

# Create music list
music_list = []
music_list.append("TheGraveyard.mp3")
music_list.append("DevilDragonBossFight.mp3")
music_list.append("MikeTysonBattle.mp3")
music_list.append("ForestFunk.mp3")

# Highscore dict
highscore_dict = {}

# Create ship sprite
ship = ship_sprite.Ship(gd.PLAYER_IMG,[gd.SHIP_RADIUS,gd.SHIP_RADIUS])

# Create reward sprite
reward_item = reward_sprite.Reward(gd.REWARD_IMG, [0, 0])

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# Calculate asteroid limit based on selected difficulty and screen size
def calculate_asteroid_limit():
    global asteroid_list_size
    if game_difficulty == GAME_DIFFICULTY_EASY:
        asteroid_list_size = round(gd.ASTEROID_LIMIT_EASY * (gd.SCREEN_WIDTH - gd.SCREEN_HEIGHT))
    elif game_difficulty == GAME_DIFFICULTY_MED:
        asteroid_list_size = round(gd.ASTEROID_LIMIT_MED * (gd.SCREEN_WIDTH - gd.SCREEN_HEIGHT))
    elif game_difficulty == GAME_DIFFICULTY_HARD:
        asteroid_list_size = round(gd.ASTEROID_LIMIT_HARD * (gd.SCREEN_WIDTH - gd.SCREEN_HEIGHT))
    elif game_difficulty == GAME_DIFFICULTY_IMPOSSIBLE:
        asteroid_list_size = round(gd.ASTEROID_LIMIT_IMPOSSIBLE * (gd.SCREEN_WIDTH - gd.SCREEN_HEIGHT))

def create_asteroids():
    global asteroid_list
    asteroid_list.empty()
    is_collided = True
    for count in range(1,asteroid_list_size+1):
        asteroid = asteroid_sprite.Asteroid(gd.ASTEROID_IMG,"Ball " + str(count), [0,0], gd.ASTEROID_RADIUS, asteroid_speed)
        # Randomize the location of new asteroids and ensure they don't collide with each other
        while is_collided:
            # Add 1 and Minus 1 to ensure the asteroid doesn't hit the borders at the game's start
            asteroid.rect.x = random.randint(gd.ASTEROID_RADIUS + 1, gd.SCREEN_WIDTH - gd.ASTEROID_RADIUS - 1)
            asteroid.rect.y = random.randint(gd.ASTEROID_RADIUS + 1, gd.SCREEN_HEIGHT - gd.ASTEROID_RADIUS - 1)
            collision_list = pygame.sprite.spritecollide(asteroid, asteroid_list, False)
            if len(collision_list) == 0:
                is_collided = False
        
        asteroid_list.add(asteroid)
        # Reset is_collied for verifying the next new asteroid
        is_collided = True

def check_collision_between_asteroids():
    for asteroidA in asteroid_list:
        for asteroidB in asteroid_list:
            # Ignore if same asteroid
            if asteroidA.name == asteroidB.name:
                continue
            # Use Pythagorean theorem to detect the collision
            if (abs(asteroidA.rect.x - asteroidB.rect.x)**2 + abs(asteroidA.rect.y - asteroidB.rect.y)**2) <= (asteroidA.radius + asteroidB.radius)**2:
                asteroidA.change_y = asteroidA.change_y * -1
                asteroidA.change_x = asteroidA.change_x * -1
                break
                
def check_collision_with_ship():
    for asteroid in asteroid_list:
        if (abs(asteroid.rect.x - ship.rect.x)**2 + abs(asteroid.rect.y - ship.rect.y)**2) <= (gd.ASTEROID_RADIUS + gd.SHIP_RADIUS)**2:
            game_over()
            break

def check_collision_with_reward():
    if (abs(reward_item.rect.x - ship.rect.x)**2 + abs(reward_item.rect.y - ship.rect.y)**2) <= (gd.REWARD_RADIUS + gd.SHIP_RADIUS)**2:
        global score
        score += 1
        global reward_item_status
        reward_item_status = False
        global tick_count
        tick_count = 0

def game_over():
    update_highscore(score)
    global game_state
    game_state = GAME_STATE_OVER
    pygame.mixer.music.stop()
    pygame.mixer.music.load(resource_path("GameOver.mp3"))
    pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
    pygame.mixer.music.play()
        
def reset_stat():
    global score
    score = 0
    global reward_item_status
    reward_item_status = False
    global old_score
    old_score = 0
    global tick_count
    tick_count = 0
    global ship
    ship.rect.x = gd.SHIP_RADIUS
    ship.rect.y = gd.SHIP_RADIUS
    global countdown
    countdown = 3
    create_asteroids()

def play_background_music():
    pygame.mixer.music.load(resource_path(music_list[random.randint(0,len(music_list)-1)]))
    pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
    pygame.mixer.music.play()
    
def initialize_highscore_list():
    global highscore_dict
    game_difficulty_count = 1
    
    # Normal mode
    difficulty_normal_mode = {}
    while(game_difficulty_count <= gd.NUM_OF_DIFFICULTIES):
        scores = []
        # Create empty highscore list
        for score_count in range(0, gd.HIGHSCORE_LIST_SIZE):
            scores.append(0)
        # Create difficulty dictionary
        if game_difficulty_count == 1:
            difficulty_normal_mode[GAME_DIFFICULTY_EASY] = scores
        elif game_difficulty_count == 2:
            difficulty_normal_mode[GAME_DIFFICULTY_MED] = scores
        elif game_difficulty_count == 3:
            difficulty_normal_mode[GAME_DIFFICULTY_HARD] = scores
        elif game_difficulty_count == 4:
            difficulty_normal_mode[GAME_DIFFICULTY_IMPOSSIBLE] = scores
        game_difficulty_count += 1
    
    # Add difficulty dictionary to the highscore dictionary
    highscore_dict[GAME_MODE_NORMAL] = difficulty_normal_mode
    
    game_difficulty_count = 1
    
    # Timer mode
    difficulty_timer_mode = {}
    while(game_difficulty_count <= gd.NUM_OF_DIFFICULTIES):
        scores = []
        # Create empty highscore list
        for score_count in range(0, gd.HIGHSCORE_LIST_SIZE):
            scores.append(0)
        # Create difficulty dictionary
        if game_difficulty_count == 1:
            difficulty_timer_mode[GAME_DIFFICULTY_EASY] = scores
        elif game_difficulty_count == 2:
            difficulty_timer_mode[GAME_DIFFICULTY_MED] = scores
        elif game_difficulty_count == 3:
            difficulty_timer_mode[GAME_DIFFICULTY_HARD] = scores
        elif game_difficulty_count == 4:
            difficulty_timer_mode[GAME_DIFFICULTY_IMPOSSIBLE] = scores
        game_difficulty_count += 1
        
    # Add difficulty dictionary to the highscore dictionary
    highscore_dict[GAME_MODE_TIMER] = difficulty_timer_mode
    
def update_highscore(score):
    global highscore_dict
    # Add the new score, sort the list, and remove the last element that is not within the defined top size (ex: top 10)
    highscore_dict[game_mode][game_difficulty].append(score)
    highscore_dict[game_mode][game_difficulty].sort(reverse=True)
    highscore_dict[game_mode][game_difficulty].pop()
    
def load_highscore():
    global highscore_dict
    
    try:
        with open(gd.HIGHSCORE_FILE_NAME) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for row in csv_reader:
                # Ignore the header
#                 if line_count == 0:
#                     line_count += 1
#                     continue 
                
                # Reset line_count for loading scores of the next difficulty
                if line_count >= gd.HIGHSCORE_LIST_SIZE:
                    line_count = 0
                     
                highscore_dict[row["GAME_MODE"]][row["DIFFICULTY"]][line_count] = int(row["SCORE"])
                line_count += 1
    except FileNotFoundError:
        print("Highscore file does not exist!")
        
def save_highscore():
    
    try:
        with open(gd.HIGHSCORE_FILE_NAME, mode='w') as csv_file:
            fieldnames = ["GAME_MODE","DIFFICULTY","SCORE"]
                
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for key_game_mode in highscore_dict.keys():
                for key_difficulty in highscore_dict[key_game_mode].keys():
                    for score in highscore_dict[key_game_mode][key_difficulty]:
                        writer.writerow({'GAME_MODE': key_game_mode, 'DIFFICULTY': key_difficulty, 'SCORE': score})
    except Exception as e:
        print("Unexpected error:", sys.exc_info()[1])
   
# Initialize highscore list
initialize_highscore_list()   
   
# Load high scores
load_highscore()
 
# Play background music randomly
play_background_music()

# Background image
background = custom_sprite.CustomSprite(resource_path(gd.BACKGROUND_IMG), [0,0])

# -------- Main Program Loop -----------
while not done:
    # --- Event Processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            # Select controller
            elif event.key == pygame.K_RETURN and game_state == GAME_STATE_MENU:
                game_state = GAME_STATE_SELECT_CONTROLLER
            elif event.key == pygame.K_F12 and game_state == GAME_STATE_MENU:
                highscore_game_mode_count = 0
                game_state = GAME_STATE_SELECT_HIGHSCORE_MODE
            # Return to main menu
            elif event.key == pygame.K_SPACE:
                game_state = GAME_STATE_MENU
                # Play background music
                pygame.mixer.music.stop()
                pygame.mixer.music.load(resource_path(music_list[random.randint(0,len(music_list)-1)]))
                pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
                pygame.mixer.music.play()
            # -- Start Difficulty --
            elif (event.key == pygame.K_1 or event.key == pygame.K_KP1) and game_state == GAME_STATE_SELECT_DIFFICULTY:
                game_difficulty = GAME_DIFFICULTY_EASY
                asteroid_speed = gd.ASTEROID_MOVE_SPEED_EASY
                timer_limit = gd.TIMER_LIMIT_EASY
                calculate_asteroid_limit()
                game_state = GAME_STATE_COUNTDOWN
            elif (event.key == pygame.K_2 or event.key == pygame.K_KP2) and game_state == GAME_STATE_SELECT_DIFFICULTY:
                game_difficulty = GAME_DIFFICULTY_MED
                asteroid_speed = gd.ASTEROID_MOVE_SPEED_MED
                timer_limit = gd.TIMER_LIMIT_MED
                calculate_asteroid_limit()
                game_state = GAME_STATE_COUNTDOWN
            elif (event.key == pygame.K_3 or event.key == pygame.K_KP3) and game_state == GAME_STATE_SELECT_DIFFICULTY:
                game_difficulty = GAME_DIFFICULTY_HARD
                asteroid_speed = gd.ASTEROID_MOVE_SPEED_HARD
                timer_limit = gd.TIMER_LIMIT_HARD
                calculate_asteroid_limit()
                game_state = GAME_STATE_COUNTDOWN
            elif (event.key == pygame.K_4 or event.key == pygame.K_KP4) and game_state == GAME_STATE_SELECT_DIFFICULTY:
                game_difficulty = GAME_DIFFICULTY_IMPOSSIBLE
                asteroid_speed = gd.ASTEROID_MOVE_SPEED_IMPOSSIBLE
                timer_limit = gd.TIMER_LIMIT_IMPOSSIBLE
                calculate_asteroid_limit()
                game_state = GAME_STATE_COUNTDOWN
            # -- Difficulty --
            # -- Game Mode --
            elif (event.key == pygame.K_1 or event.key == pygame.K_KP1) and game_state == GAME_STATE_SELECT_GAME_MODE:
                game_mode = GAME_MODE_NORMAL
                game_state = GAME_STATE_SELECT_DIFFICULTY
            elif (event.key == pygame.K_2 or event.key == pygame.K_KP2) and game_state == GAME_STATE_SELECT_GAME_MODE:
                game_mode = GAME_MODE_TIMER
                game_state = GAME_STATE_SELECT_DIFFICULTY
            # -- End Game Mode --
            # -- Game Mode --
            elif (event.key == pygame.K_1 or event.key == pygame.K_KP1) and game_state == GAME_STATE_SELECT_HIGHSCORE_MODE:
                highscore_view_mode = GAME_MODE_NORMAL
                game_state = GAME_STATE_VIEW_HIGHSCORE
            elif (event.key == pygame.K_2 or event.key == pygame.K_KP2) and game_state == GAME_STATE_SELECT_HIGHSCORE_MODE:
                highscore_view_mode = GAME_MODE_TIMER
                game_state = GAME_STATE_VIEW_HIGHSCORE
            # -- End Game Mode --
            # -- Controller Mode --
            elif (event.key == pygame.K_1 or event.key == pygame.K_KP1) and game_state == GAME_STATE_SELECT_CONTROLLER:
                game_controller = gd.GAME_CONTROLLER_MOUSE
                game_state = GAME_STATE_SELECT_GAME_MODE
            elif (event.key == pygame.K_2 or event.key == pygame.K_KP2) and game_state == GAME_STATE_SELECT_CONTROLLER:
                game_controller = gd.GAME_CONTROLLER_KEYBOARD
                game_state = GAME_STATE_SELECT_GAME_MODE
            # -- End Controller Mode --
            # -- ship_sprite controlled by Keyboard -- Set the speed based on the key pressed
            elif event.key == pygame.K_LEFT:
                ship.move_ship(-gd.SHIP_SPEED, 0)
            elif event.key == pygame.K_RIGHT:
                ship.move_ship(gd.SHIP_SPEED, 0)
            elif event.key == pygame.K_UP:
                ship.move_ship(0, -gd.SHIP_SPEED)
            elif event.key == pygame.K_DOWN:
                ship.move_ship(0, gd.SHIP_SPEED)
            # -- End ship_sprite controlled by keyboard --
            # Retry option
            elif event.key == pygame.K_BACKSPACE and game_state == GAME_STATE_OVER:
                reset_stat()
                play_background_music()
                game_state = GAME_STATE_COUNTDOWN
        # -- ship_sprite controlled by Keyboard -- Reset speed when key goes up
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                ship.move_ship(gd.SHIP_SPEED, 0)
            elif event.key == pygame.K_RIGHT:
                ship.move_ship(-gd.SHIP_SPEED, 0)
            elif event.key == pygame.K_UP:
                ship.move_ship(0, gd.SHIP_SPEED)
            elif event.key == pygame.K_DOWN:
                ship.move_ship(0, -gd.SHIP_SPEED)
        # -- End ship_sprite controlled by keyboard
        elif event.type == pygame.constants.USEREVENT:
                if game_state != GAME_STATE_OVER:
                    play_background_music()
 
    # Set the screen background
    screen.fill([255, 255, 255])
    screen.blit(background.image, background.rect)
    
    if game_state == GAME_STATE_PLAY:
        # Hide the ship cursor
        pygame.mouse.set_visible(0)
        
        # -- Timer Update --
        if game_mode == GAME_MODE_TIMER:
            total_seconds = timer_limit - (tick_count // tick_rate)
            if total_seconds <= 0:
                game_over()
         
            # Divide by 60 to get total minutes
            minutes = total_seconds // 60
         
            # Use modulus (remainder) to get seconds
            seconds = total_seconds % 60
         
            # Use python string formatting to format in leading zeros
            output_string = "Time left: {0:02}:{1:02}".format(minutes, seconds)
         
            # Blit to the screen
            text = normal_font.render(output_string, True, WHITE)
         
            screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, 0])
            tick_count += 1
        # --End Timer Update --
        
        # Increase asteroids' speed
        if (score - old_score) == gd.SPEED_INCREASE_POINTS:
            old_score = score
            for asteroid in asteroid_list:
                #Need to check direction of asteroids in order to increase speed correctly
                if asteroid.change_x > 0:
                    asteroid.change_x += 1
                else:
                    asteroid.change_x -= 1
                if asteroid.change_y > 0:
                    asteroid.change_y += 1
                else:
                    asteroid.change_y -= 1
        
        # -- Mouse pointer update --
        # Update ship location for keyboard players  
        if game_controller == gd.GAME_CONTROLLER_MOUSE:
            ship_pos = pygame.mouse.get_pos()
            ship.rect.x = ship_pos[0]
            ship.rect.y = ship_pos[1]
            
        # Update ship location for keyboard players    
        if game_controller == gd.GAME_CONTROLLER_KEYBOARD:
            ship.update()
            
        # Mouse cursor should not overlap the borders
        if ship.rect.y >= (gd.SCREEN_HEIGHT - gd.SHIP_RADIUS):
            ship.rect.y = gd.SCREEN_HEIGHT - gd.SHIP_RADIUS
        elif ship.rect.y <= gd.SHIP_RADIUS:
            ship.rect.y = gd.SHIP_RADIUS
        if ship.rect.x >= (gd.SCREEN_WIDTH - gd.SHIP_RADIUS):
            ship.rect.x = gd.SCREEN_WIDTH - gd.SHIP_RADIUS
        elif ship.rect.x <= gd.SHIP_RADIUS:
            ship.rect.x = gd.SHIP_RADIUS    
            
        # Draw ship    
        screen.blit(ship.image, [ship.rect.x - gd.SHIP_RADIUS, ship.rect.y - gd.SHIP_RADIUS])
        # -- End Mouse Pointer Update --
        
        
        if game_state == GAME_STATE_PLAY:
            # Create reward item
            if reward_item_status == False:
                reward_item.rect.x = random.randint(0,gd.SCREEN_WIDTH - gd.REWARD_RADIUS) + gd.REWARD_RADIUS
                reward_item.rect.y = random.randint(0,gd.SCREEN_HEIGHT - gd.REWARD_RADIUS) + gd.REWARD_RADIUS
                # Reward item should not overlap the borders
                if reward_item.rect.y >= (gd.SCREEN_HEIGHT - gd.REWARD_RADIUS):
                    reward_item.rect.y = gd.SCREEN_HEIGHT - gd.REWARD_RADIUS
                elif reward_item.rect.y <= gd.REWARD_RADIUS:
                    reward_item.rect.y = gd.REWARD_RADIUS
                if reward_item.rect.x >= (gd.SCREEN_WIDTH - gd.REWARD_RADIUS):
                    reward_item.rect.x = gd.SCREEN_WIDTH - gd.REWARD_RADIUS
                elif reward_item.rect.x <= gd.REWARD_RADIUS:
                    reward_item.rect.x = gd.REWARD_RADIUS
                screen.blit(reward_item.image, [reward_item.rect.x - gd.REWARD_RADIUS, reward_item.rect.y - gd.REWARD_RADIUS])
                reward_item_status = True
            else:
                screen.blit(reward_item.image, [reward_item.rect.x - gd.REWARD_RADIUS, reward_item.rect.y - gd.REWARD_RADIUS])
                
            # Check if the ship collides with the reward item
            check_collision_with_reward()
            
            # Draw score
            textSmallScore = normal_font.render("Score: " + str(score), True, WHITE)
            screen.blit(textSmallScore, [gd.SCREEN_WIDTH - 100, 0])
            
            # Check if asteroids collide each other
            check_collision_between_asteroids()
         
            # Move asteroids
            for asteroid in asteroid_list:
                asteroid.move_asteroid()
                
            # Check if any asteroid collides with the ship
            check_collision_with_ship()
            
            # Draw the asteroids
            for asteroid in asteroid_list:
                screen.blit(asteroid.image, [asteroid.rect.x - gd.ASTEROID_RADIUS, asteroid.rect.y - gd.ASTEROID_RADIUS])
            
    elif game_state == GAME_STATE_OVER:
        # Show the ship cursor
        pygame.mouse.set_visible(1)
        
        text = title_font_1.render("GAME OVER", True, WHITE)
        # Text height will be increased every time a new line of text is created
        text_y = gd.SCREEN_HEIGHT/2 - text.get_rect().height/2
        screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
        text_y += text.get_rect().height
        text = normal_font.render(game_difficulty + " - Score: " + str(score), True, WHITE)
        screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
        text_y += text.get_rect().height
        text = normal_font.render("Press BACKSPACE to retry", True, WHITE)
        screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
        text_y += text.get_rect().height
        text = normal_font.render("Press SPACE BAR to return to main menu", True, WHITE)
        screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
        text_y += text.get_rect().height
        
    elif game_state == GAME_STATE_MENU:
        # Show the ship cursor
        pygame.mouse.set_visible(1)
        countdown = 3
        
        text = title_font_2.render("King Of Evasion", True, WHITE)
        # Text height will be increased every time a new line of text is created
        text_y = gd.SCREEN_HEIGHT/2 - text.get_rect().height/2
        screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
        
        # Draw the player sprite on the main menu
        try:
            icon_sprite = custom_sprite.CustomSprite(gd.PLAYER_IMG, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2 - gd.SHIP_RADIUS*2, text_y - gd.SHIP_RADIUS])
            screen.blit(icon_sprite.image, icon_sprite.rect)
        except Exception as e:
            print(e,type(e))    
                    
        text_y += text.get_rect().height
        
        text = title_font_1.render("Touch the Star to gain points and Evade all asteroids", True, WHITE)
        screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
        text_y += text.get_rect().height
        
        text = title_font_1.render("Press F12 to view high scores", True, WHITE)
        screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
        text_y += text.get_rect().height
        
        text = title_font_1.render("Press ENTER to play", True, WHITE)
        screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
        text_y += text.get_rect().height
    elif game_state == GAME_STATE_COUNTDOWN:
        # Reset all stats and create asteroids based on selected difficulty and screen size
        if countdown == 3:
            reset_stat()
        # Show the ship cursor
        pygame.mouse.set_visible(1)
        if countdown < 0:
            game_state = GAME_STATE_PLAY
        else:
            # Draw the asteroids
            for asteroid in asteroid_list:
                screen.blit(asteroid.image, [asteroid.rect.x - gd.ASTEROID_RADIUS, asteroid.rect.y - gd.ASTEROID_RADIUS])
            if countdown == 0:
                text = countdown_font.render("GO", True, WHITE)
                screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, gd.SCREEN_HEIGHT/2 - text.get_rect().height/2])
            elif countdown > 0:    
                text = countdown_font.render(str(countdown), True, WHITE)
                screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, gd.SCREEN_HEIGHT/2 - text.get_rect().height/2])
            countdown -= 1
        pygame.time.delay(1000)
    elif game_state == GAME_STATE_SELECT_DIFFICULTY:
        pygame.mouse.set_visible(1)
        
        # Text height will be increased every time a new line of text is created
        text_y = gd.SCREEN_HEIGHT/2 - text.get_rect().height/2
        text = title_font_1.render("Select a difficulty:", True, WHITE)
        screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
        text_y += text.get_rect().height
        text = title_font_1.render("1 - Easy", True, WHITE)
        screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
        text_y += text.get_rect().height
        text = title_font_1.render("2 - Medium", True, WHITE)
        screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
        text_y += text.get_rect().height
        text = title_font_1.render("3 - Hard", True, WHITE)
        screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
        text_y += text.get_rect().height
        text = title_font_1.render("4 - Impossible", True, WHITE)
        screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
        text_y += text.get_rect().height
    elif game_state == GAME_STATE_SELECT_GAME_MODE:
        pygame.mouse.set_visible(1)
        
        # Text height will be increased every time a new line of text is created
        text_y = gd.SCREEN_HEIGHT/2 - text.get_rect().height/2
        text = title_font_1.render("Select a game mode:", True, WHITE)
        screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
        text_y += text.get_rect().height
        text = title_font_1.render("1 - Normal", True, WHITE)
        screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
        text_y += text.get_rect().height
        text = title_font_1.render("2 - Timer", True, WHITE)
        screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
        text_y += text.get_rect().height
    elif game_state == GAME_STATE_SELECT_CONTROLLER:
        pygame.mouse.set_visible(1)
        
        # Text height will be increased every time a new line of text is created
        text_y = gd.SCREEN_HEIGHT/2 - text.get_rect().height/2
        text = title_font_1.render("Select your controller type:", True, WHITE)
        screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
        text_y += text.get_rect().height
        text = title_font_1.render("1 - Mouse", True, WHITE)
        screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
        text_y += text.get_rect().height
        text = title_font_1.render("2 - Keyboard", True, WHITE)
        screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
        text_y += text.get_rect().height
    elif game_state == GAME_STATE_SELECT_HIGHSCORE_MODE:
        pygame.mouse.set_visible(1)
        
        # Text height will be increased every time a new line of text is created
        text_y = gd.SCREEN_HEIGHT/2 - text.get_rect().height/2
        text = title_font_1.render("Select a highscore view mode:", True, WHITE)
        screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
        text_y += text.get_rect().height
        text = title_font_1.render("1 - Normal", True, WHITE)
        screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
        text_y += text.get_rect().height
        text = title_font_1.render("2 - Timer", True, WHITE)
        screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
        text_y += text.get_rect().height
    elif game_state == GAME_STATE_VIEW_HIGHSCORE:
        pygame.mouse.set_visible(1)
        
        # Text height will be increased every time a new line of text is created
        text_y = gd.SCREEN_HEIGHT/2 * 0.25 - text.get_rect().height/2
        text = title_font_1.render("HIGH SCORES", True, WHITE)
        screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
        text_y += text.get_rect().height
        text = title_font_1.render("Mode: " + str(highscore_view_mode), True, WHITE)
        screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
        text_y += text.get_rect().height
        text_y += text.get_rect().height
        
        difficulty_count = 1;
        old_text_y = text_y
        for key_difficulty in highscore_dict[highscore_view_mode].keys():
            # Make all score columns at the same height
            text_y = old_text_y
            
            text = title_font_1.render(key_difficulty, True, WHITE)
            screen.blit(text, [gd.SCREEN_WIDTH/2 * 0.4 * difficulty_count - text.get_rect().width/2, text_y])
            text_y += text.get_rect().height
            
            for score in highscore_dict[highscore_view_mode][key_difficulty]:
                text = title_font_1.render(str(score), True, WHITE)
                screen.blit(text, [gd.SCREEN_WIDTH/2 * 0.4 * difficulty_count - text.get_rect().width/2, text_y])
                text_y += text.get_rect().height
                
            difficulty_count += 1
 
    # --- Wrap-up
    # Limit frames per second
    clock.tick(frame_rate)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Save highscore before quitting
save_highscore()
# Close everything down
pygame.quit()