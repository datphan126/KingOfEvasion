"""
 King of Evasion - Touch the Green Orb to gain points.
 
 There are four difficulty modes in this game:
 Easy, Medium, Hard, and Impossible
 
 After gaining a specific amount of points, the speed of balls will increase
 
 Author: Dat Phan
"""
 
import pygame
import random
import sys
import os
import game_definitions as gd
import ship_sprite 
from ball import Ball
from custom_sprite import CustomSprite
 
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
GAME_STATE_SELECT_MODE = "SELECT MODE"
GAME_STATE_SELECT_CONTROLLER = "SELECT CONTROLLER"

# Game Difficulty definition
GAME_DIFFICULTY_EASY = "EASY"
GAME_DIFFICULTY_MED = "MEDIUM"
GAME_DIFFICULTY_HARD = "HARD"
GAME_DIFFICULTY_IMPOSSIBLE = "IMPOSSIBLE"

# Game modes
GAME_MODE_NORMAL = "NORMAL_MODE"
GAME_MODE_TIMER = "TIMER_MODE"

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

# Game controller
game_controller = gd.GAME_CONTROLLER_MOUSE

# Game mode
game_mode = GAME_MODE_NORMAL

# Game difficulty
game_difficulty = GAME_DIFFICULTY_EASY

# Game speed - Default speed is Easy mode's speed
game_speed = gd.BALL_MOVE_SPEED_EASY
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Create new ball list
balls = []
# Number of balls
ball_list_size = 0
ball_radius = 50

game_state = GAME_STATE_MENU

# Reward item status - if true, item is already created. If false, item isn't created
reward_item_status = False
reward_item_size = 20
reward_x_pos = 0
reward_y_pos = 0
score = 0
old_score = 0

# Countdown before the match starts
countdown = 3

# Select the font to use, size, bold, italics
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

# Create ship
ship = ship_sprite.Ship(gd.PLAYER_IMG,[gd.SHIP_RADIUS,gd.SHIP_RADIUS])

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# Calculate ball limit based on selected difficulty
def calculate_ball_limit():
    global ball_list_size
    if game_difficulty == GAME_DIFFICULTY_EASY:
        ball_list_size = round(gd.BALL_LIMIT_EASY * (gd.SCREEN_WIDTH - gd.SCREEN_HEIGHT))
    elif game_difficulty == GAME_DIFFICULTY_MED:
        ball_list_size = round(gd.BALL_LIMIT_MED * (gd.SCREEN_WIDTH - gd.SCREEN_HEIGHT))
    elif game_difficulty == GAME_DIFFICULTY_HARD:
        ball_list_size = round(gd.BALL_LIMIT_HARD * (gd.SCREEN_WIDTH - gd.SCREEN_HEIGHT))
    elif game_difficulty == GAME_DIFFICULTY_IMPOSSIBLE:
        ball_list_size = round(gd.BALL_LIMIT_IMPOSSIBLE * (gd.SCREEN_WIDTH - gd.SCREEN_HEIGHT))

def create_balls():
    global balls
    balls.clear()
    temp_ball_list = pygame.sprite.Group()
    is_collided = True
    for count in range(1,ball_list_size+1):
        ball_sprite = CustomSprite(gd.BALL_IMG,[0,0])
        # Randomize the location of new balls and ensure they don't collide with each other
        while is_collided:
            # Add 1 and Minus 1 to ensure the ball doesn't hit the borders at the game's start
            ball_sprite.rect.x = random.randint(ball_radius + 1, gd.SCREEN_WIDTH - ball_radius - 1)
            ball_sprite.rect.y = random.randint(ball_radius + 1, gd.SCREEN_HEIGHT - ball_radius - 1)
            collision_list = pygame.sprite.spritecollide(ball_sprite, temp_ball_list, False)
            if len(collision_list) == 0:
                is_collided = False
        
        temp_ball_list.add(ball_sprite)
        ball = Ball("Ball " + str(count), ball_sprite.rect.x, ball_sprite.rect.y, ball_radius, game_speed)
        balls.append(ball)
        # Reset is_collied for verifying the next new ball
        is_collided = True

def check_collision_between_balls():
    for ballA in balls:
        for ballB in balls:
            # Ignore if same ball
            if ballA.name == ballB.name:
                continue
            # Use Pythagorean theorem to determine the collision
            if (abs(ballA.x_pos - ballB.x_pos)**2 + abs(ballA.y_pos - ballB.y_pos)**2) <= (ballA.radius + ballB.radius)**2:
                ballA.circle_change_y = ballA.circle_change_y * -1
                ballA.circle_change_x = ballA.circle_change_x * -1
                break
                
def check_collision_with_ship():
    for ballA in balls:
        if (abs(ballA.x_pos - ship.rect.x)**2 + abs(ballA.y_pos - ship.rect.y)**2) <= (ballA.radius + gd.SHIP_RADIUS)**2:
            game_over()
            break

def check_collision_with_reward():
    if (abs(reward_x_pos - ship.rect.x)**2 + abs(reward_y_pos - ship.rect.y)**2) <= (reward_item_size + gd.SHIP_RADIUS)**2:
        global score
        score += 1
        global reward_item_status
        reward_item_status = False
        global tick_count
        tick_count = 0

def game_over():
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
    global reward_x_pos
    reward_x_pos = 0
    global reward_y_pos
    reward_y_pos = 0
    global old_score
    old_score = 0
    global tick_count
    tick_count = 0
    global ship
    ship.rect.x = gd.SHIP_RADIUS
    ship.rect.y = gd.SHIP_RADIUS
    create_balls()

def play_background_music():
    pygame.mixer.music.load(resource_path(music_list[random.randint(0,len(music_list)-1)]))
    pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
    pygame.mixer.music.play()
    
# Play background music randomly
play_background_music()

# Background image
background = CustomSprite(resource_path(gd.BACKGROUND_IMG), [0,0])

# -------- Main Program Loop -----------
while not done:
    # --- Event Processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            # Select difficulty
            elif event.key == pygame.K_RETURN and game_state == GAME_STATE_MENU:
                game_state = GAME_STATE_SELECT_CONTROLLER
            # Return to main menu
            elif event.key == pygame.K_SPACE:
                game_state = GAME_STATE_MENU
                # Play background music
                pygame.mixer.music.stop()
                pygame.mixer.music.load(resource_path(music_list[random.randint(0,len(music_list)-1)]))
                pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
                pygame.mixer.music.play()
            # --  Difficulty --
            elif (event.key == pygame.K_1 or event.key == pygame.K_KP1) and game_state == GAME_STATE_SELECT_DIFFICULTY:
                game_difficulty = GAME_DIFFICULTY_EASY
                game_speed = gd.BALL_MOVE_SPEED_EASY
                timer_limit = gd.TIMER_LIMIT_EASY
                calculate_ball_limit()
                game_state = GAME_STATE_COUNTDOWN
            elif (event.key == pygame.K_2 or event.key == pygame.K_KP2) and game_state == GAME_STATE_SELECT_DIFFICULTY:
                game_difficulty = GAME_DIFFICULTY_MED
                game_speed = gd.BALL_MOVE_SPEED_MED
                timer_limit = gd.TIMER_LIMIT_MED
                calculate_ball_limit()
                game_state = GAME_STATE_COUNTDOWN
            elif (event.key == pygame.K_3 or event.key == pygame.K_KP3) and game_state == GAME_STATE_SELECT_DIFFICULTY:
                game_difficulty = GAME_DIFFICULTY_HARD
                game_speed = gd.BALL_MOVE_SPEED_HARD
                timer_limit = gd.TIMER_LIMIT_HARD
                calculate_ball_limit()
                game_state = GAME_STATE_COUNTDOWN
            elif (event.key == pygame.K_4 or event.key == pygame.K_KP4) and game_state == GAME_STATE_SELECT_DIFFICULTY:
                game_difficulty = GAME_DIFFICULTY_IMPOSSIBLE
                game_speed = gd.BALL_MOVE_SPEED_IMPOSSIBLE
                timer_limit = gd.TIMER_LIMIT_IMPOSSIBLE
                calculate_ball_limit()
                game_state = GAME_STATE_COUNTDOWN
            # -- End Difficulty --
            # -- Game Mode --
            elif (event.key == pygame.K_1 or event.key == pygame.K_KP1) and game_state == GAME_STATE_SELECT_MODE:
                game_mode = GAME_MODE_NORMAL
                game_state = GAME_STATE_SELECT_DIFFICULTY
            elif (event.key == pygame.K_2 or event.key == pygame.K_KP2) and game_state == GAME_STATE_SELECT_MODE:
                game_mode = GAME_MODE_TIMER
                game_state = GAME_STATE_SELECT_DIFFICULTY
            # -- End Game Mode --
            # -- Controller Mode --
            elif (event.key == pygame.K_1 or event.key == pygame.K_KP1) and game_state == GAME_STATE_SELECT_CONTROLLER:
                game_controller = gd.GAME_CONTROLLER_MOUSE
                game_state = GAME_STATE_SELECT_MODE
            elif (event.key == pygame.K_2 or event.key == pygame.K_KP2) and game_state == GAME_STATE_SELECT_CONTROLLER:
                game_controller = gd.GAME_CONTROLLER_KEYBOARD
                game_state = GAME_STATE_SELECT_MODE
            # -- End Controller Mode --
            # -- ship_sprite controlled by Keyboard -- Set the speed based on the key pressed
            elif event.key == pygame.K_LEFT:
                ship.change_ship_direction(-gd.SHIP_SPEED, 0)
            elif event.key == pygame.K_RIGHT:
                ship.change_ship_direction(gd.SHIP_SPEED, 0)
            elif event.key == pygame.K_UP:
                ship.change_ship_direction(0, -gd.SHIP_SPEED)
            elif event.key == pygame.K_DOWN:
                ship.change_ship_direction(0, gd.SHIP_SPEED)
            # -- End ship_sprite controlled by keyboard --
        # -- ship_sprite controlled by Keyboard -- Reset speed when key goes up
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                ship.change_ship_direction(gd.SHIP_SPEED, 0)
            elif event.key == pygame.K_RIGHT:
                ship.change_ship_direction(-gd.SHIP_SPEED, 0)
            elif event.key == pygame.K_UP:
                ship.change_ship_direction(0, gd.SHIP_SPEED)
            elif event.key == pygame.K_DOWN:
                ship.change_ship_direction(0, -gd.SHIP_SPEED)
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
        
        # Increase balls' speed
        if (score - old_score) == gd.SPEED_INCREASE_POINTS:
            old_score = score
            for ball in balls:
                #Need to check direction of balls in order to increase speed correctly
                if ball.circle_change_x > 0:
                    ball.circle_change_x += 1
                else:
                    ball.circle_change_x -= 1
                if ball.circle_change_y > 0:
                    ball.circle_change_y += 1
                else:
                    ball.circle_change_y -= 1
        
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
        
        # Check if any ball collides with the ship
        check_collision_with_ship()
        
        if game_state == GAME_STATE_PLAY:
            # Create reward item
            if reward_item_status == False:
                reward_x_pos = random.randint(0,gd.SCREEN_WIDTH - reward_item_size) + reward_item_size
                reward_y_pos = random.randint(0,gd.SCREEN_HEIGHT - reward_item_size) + reward_item_size
                # Reward item should not overlap the borders
                if reward_y_pos >= (gd.SCREEN_HEIGHT - reward_item_size):
                    reward_y_pos = gd.SCREEN_HEIGHT - reward_item_size
                elif reward_y_pos <= reward_item_size:
                    reward_y_pos = reward_item_size
                if reward_x_pos >= (gd.SCREEN_WIDTH - reward_item_size):
                    reward_x_pos = gd.SCREEN_WIDTH - reward_item_size
                elif reward_x_pos <= reward_item_size:
                    reward_x_pos = reward_item_size
                reward_item_sprite = CustomSprite(gd.REWARD_IMG, [reward_x_pos - reward_item_size, reward_y_pos - reward_item_size])
                screen.blit(reward_item_sprite.image, reward_item_sprite.rect)
                reward_item_status = True
            else:
                reward_item_sprite = CustomSprite(gd.REWARD_IMG, [reward_x_pos - reward_item_size, reward_y_pos - reward_item_size])
                screen.blit(reward_item_sprite.image, reward_item_sprite.rect)
                
            # Check if the ship collides with the reward item
            check_collision_with_reward()
            
            # Draw score
            textSmallScore = normal_font.render("Score: " + str(score), True, WHITE)
            screen.blit(textSmallScore, [gd.SCREEN_WIDTH - 100, 0])
            
            # Check if balls collide each other
            check_collision_between_balls()
         
            # Move balls
            for ball in balls:
                ball.move_ball()
            
            # Draw the balls
            for ball in balls:
                ball_sprite = CustomSprite(gd.BALL_IMG, [ball.x_pos - ball.radius, ball.y_pos - ball.radius])
                screen.blit(ball_sprite.image, ball_sprite.rect)
            
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
            player_sprite = CustomSprite(gd.PLAYER_IMG, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2 - gd.SHIP_RADIUS*2, text_y - gd.SHIP_RADIUS])
            screen.blit(player_sprite.image, player_sprite.rect)
        except Exception as e:
            print(e,type(e))    
                    
        text_y += text.get_rect().height
        
        text = title_font_1.render("Touch the Star to gain points and Evade all asteroids", True, WHITE)
        screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
        text_y += text.get_rect().height
        
        text = title_font_1.render("Press ENTER to play", True, WHITE)
        screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
        text_y += text.get_rect().height
    elif game_state == GAME_STATE_COUNTDOWN:
        # Reset all stats and create balls based on selected difficulty
        if countdown == 3:
            reset_stat()
        # Show the ship cursor
        pygame.mouse.set_visible(1)
        if countdown < 0:
            game_state = GAME_STATE_PLAY
        else:
            # Draw the balls
            for ball in balls:
                ball_sprite = CustomSprite(gd.BALL_IMG, [ball.x_pos - ball.radius, ball.y_pos - ball.radius])
                screen.blit(ball_sprite.image, ball_sprite.rect)
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
    elif game_state == GAME_STATE_SELECT_MODE:
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
 
    # --- Wrap-up
    # Limit frames per second
    clock.tick(frame_rate)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Close everything down
pygame.quit()