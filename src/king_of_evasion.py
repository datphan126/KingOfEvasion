"""
 King of Evasion - Touch the Green Orb to gain points.
 
 There are four difficulty mode in this game:
 Easy, Medium, Hard, and Impossible
 
 After gaining a specific amount of points, the speed of balls will increase
 
 Author: Dat Phan
"""
 
import pygame
import random
import sys
import os
import game_definitions as gd
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
GAME_STATE_SELECT_MODE = "SELECT MODE"

# Game Difficulty definition
GAME_DIFFICULTY_EASY = "EASY"
GAME_DIFFICULTY_MED = "MEDIUM"
GAME_DIFFICULTY_HARD = "HARD"
GAME_DIFFICULTY_IMPOSSIBLE = "IMPOSSIBLE"

pygame.init()
 
# Set the height and width of the screen
size = [gd.SCREEN_WIDTH, gd.SCREEN_HEIGHT]
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# Window mode - Testing
screen = pygame.display.set_mode(size, pygame.FULLSCREEN | pygame)
 
pygame.display.set_caption("King Of Evasion")
 
# Loop until the user clicks the close button.
done = False

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
ball_size = 50

# Initiate Mouse position
mouse_x = 0
mouse_y = 0
mouse_size = 25

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

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# Calculate ball limit based on selected difficulty
def calculate_ball_limit():
    global ball_list_size
    if game_difficulty == GAME_DIFFICULTY_EASY:
        ball_list_size = round(gd.BALL_LIMIT_EASY * gd.SCREEN_WIDTH)
    elif game_difficulty == GAME_DIFFICULTY_MED:
        ball_list_size = round(gd.BALL_LIMIT_MED * gd.SCREEN_WIDTH)
    elif game_difficulty == GAME_DIFFICULTY_HARD:
        ball_list_size = round(gd.BALL_LIMIT_HARD * gd.SCREEN_WIDTH)
    elif game_difficulty == GAME_DIFFICULTY_IMPOSSIBLE:
        ball_list_size = round(gd.BALL_LIMIT_IMPOSSIBLE * gd.SCREEN_WIDTH)

def create_balls():
    global balls
    balls.clear()
    for count in range(1,ball_list_size+1):
        if count <= ball_list_size/2:
            ball_x_pos = round((gd.SCREEN_WIDTH/ball_list_size) + (count * ball_size * 3))
            ball_y_pos = round(0.25 * gd.SCREEN_HEIGHT)
        else:
            ball_x_pos = round((gd.SCREEN_WIDTH/ball_list_size) + ((count - ball_list_size/2) * ball_size * 3))
            ball_y_pos = round(0.75 * gd.SCREEN_HEIGHT)
        ball = Ball("Ball " + str(count), ball_x_pos,ball_y_pos,ball_size,game_speed)
        balls.append(ball)

def check_ball_collision():
    for ballA in balls:
        for ballB in balls:
            # Ignore if same ball
            if ballA.name == ballB.name:
                continue
            # Use Pythagorean theorem to determine the collision
            if (abs(ballA.x_pos - ballB.x_pos)**2 + abs(ballA.y_pos - ballB.y_pos)**2) <= (ballA.size + ballB.size)**2:
                ballA.circle_change_y = ballA.circle_change_y * -1
                ballA.circle_change_x = ballA.circle_change_x * -1
                break
                
def check_collision_with_mouse():
    for ballA in balls:
        if (abs(ballA.x_pos - mouse_x)**2 + abs(ballA.y_pos - mouse_y)**2) <= (ballA.size + mouse_size)**2:
            global game_state
            game_state = GAME_STATE_OVER
            pygame.mixer.music.stop()
            pygame.mixer.music.load(resource_path("GameOver.mp3"))
            pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
            pygame.mixer.music.play()
            break

def check_collision_with_reward():
    if (abs(reward_x_pos - mouse_x)**2 + abs(reward_y_pos - mouse_y)**2) <= (reward_item_size + mouse_size)**2:
        global score
        score += 1
        global reward_item_status
        reward_item_status = False
        
def reset_stat():
    global score
    score = 0
    global reward_item_status
    reward_item_status = False
    global reward_x_pos
    reward_x_pos = 0
    global reward_y_pos
    reward_y_pos = 0
    global mouse_x
    mouse_x = 0
    global mouse_y
    mouse_y = 0
    global old_score
    old_score = 0
    create_balls()
    
# Play background music randomly
pygame.mixer.music.load(resource_path(music_list[random.randint(0,len(music_list)-1)]))
pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
pygame.mixer.music.play()

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
            elif event.key == pygame.K_RETURN and game_state == GAME_STATE_MENU:
                game_state = GAME_STATE_SELECT_MODE
            elif event.key == pygame.K_SPACE:
                game_state = GAME_STATE_MENU
                # Play background music
                pygame.mixer.music.stop()
                pygame.mixer.music.load(resource_path(music_list[random.randint(0,len(music_list)-1)]))
                pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
                pygame.mixer.music.play()
            elif (event.key == pygame.K_1 or event.key == pygame.K_KP1) and game_state == GAME_STATE_SELECT_MODE:
                game_difficulty = GAME_DIFFICULTY_EASY
                game_speed = gd.BALL_MOVE_SPEED_EASY
                calculate_ball_limit()
                game_state = GAME_STATE_COUNTDOWN
            elif (event.key == pygame.K_2 or event.key == pygame.K_KP2) and game_state == GAME_STATE_SELECT_MODE:
                game_difficulty = GAME_DIFFICULTY_MED
                game_speed = gd.BALL_MOVE_SPEED_MED
                calculate_ball_limit()
                game_state = GAME_STATE_COUNTDOWN
            elif (event.key == pygame.K_3 or event.key == pygame.K_KP3) and game_state == GAME_STATE_SELECT_MODE:
                game_difficulty = GAME_DIFFICULTY_HARD
                game_speed = gd.BALL_MOVE_SPEED_HARD
                calculate_ball_limit()
                game_state = GAME_STATE_COUNTDOWN
            elif (event.key == pygame.K_4 or event.key == pygame.K_KP4) and game_state == GAME_STATE_SELECT_MODE:
                game_difficulty = GAME_DIFFICULTY_IMPOSSIBLE
                game_speed = gd.BALL_MOVE_SPEED_IMPOSSIBLE
                calculate_ball_limit()
                game_state = GAME_STATE_COUNTDOWN
        elif event.type == pygame.constants.USEREVENT:
                if game_state != GAME_STATE_OVER:
                    pygame.mixer.music.load(resource_path(music_list[random.randint(0,len(music_list)-1)]))
                    pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
                    pygame.mixer.music.play()
 
    # Set the screen background
    screen.fill([255, 255, 255])
    screen.blit(background.image, background.rect)
    
    if game_state == GAME_STATE_PLAY:
        # Hide the mouse cursor
        pygame.mouse.set_visible(0)
        
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
        
        # Draw mouse pointer
        mouse_pos = pygame.mouse.get_pos()
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        # Mouse cursor should not overlap the borders
        if mouse_y >= (gd.SCREEN_HEIGHT - mouse_size):
            mouse_y = gd.SCREEN_HEIGHT - mouse_size
        elif mouse_y <= mouse_size:
            mouse_y = mouse_size
        if mouse_x >= (gd.SCREEN_WIDTH - mouse_size):
            mouse_x = gd.SCREEN_WIDTH - mouse_size
        elif mouse_x <= mouse_size:
            mouse_x = mouse_size
#         pygame.draw.circle(screen,RED,[mouse_x,mouse_y],mouse_size)
        player_sprite = CustomSprite(gd.PLAYER_IMG, [mouse_x - mouse_size, mouse_y - mouse_size])
        screen.blit(player_sprite.image, player_sprite.rect)
        
        # Check if any ball collides with the mouse
        check_collision_with_mouse()
        
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
#                 pygame.draw.circle(screen, GREEN, [reward_x_pos, reward_y_pos], reward_item_size)
                reward_item_sprite = CustomSprite(gd.REWARD_IMG, [reward_x_pos - reward_item_size, reward_y_pos - reward_item_size])
                screen.blit(reward_item_sprite.image, reward_item_sprite.rect)
                reward_item_status = True
            else:
#                 pygame.draw.circle(screen, GREEN, [reward_x_pos, reward_y_pos], reward_item_size)
                reward_item_sprite = CustomSprite(gd.REWARD_IMG, [reward_x_pos - reward_item_size, reward_y_pos - reward_item_size])
                screen.blit(reward_item_sprite.image, reward_item_sprite.rect)
                
            # Check if the mouse collides with the reward item
            check_collision_with_reward()
            
            # Draw score
            textSmallScore = normal_font.render("Score: " + str(score), True, WHITE)
            screen.blit(textSmallScore, [gd.SCREEN_WIDTH - 100, 0])
            
            # Check if balls collide each other
            check_ball_collision()
         
            # Move balls
            for ball in balls:
                ball.move_ball()
            
            # Draw the balls
            for ball in balls:
#                 pygame.draw.circle(screen, WHITE, [ball.x_pos, ball.y_pos], ball.size)
                ball_sprite = CustomSprite(gd.BALL_IMG, [ball.x_pos - ball.size, ball.y_pos - ball.size])
                screen.blit(ball_sprite.image, ball_sprite.rect)
            
    elif game_state == GAME_STATE_OVER:
        # Show the mouse cursor
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
        # Show the mouse cursor
        pygame.mouse.set_visible(1)
        countdown = 3
        
        text = title_font_2.render("King Of Evasion", True, WHITE)
        # Text height will be increased every time a new line of text is created
        text_y = gd.SCREEN_HEIGHT/2 - text.get_rect().height/2
        screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
        
        # Draw the player sprite on the main menu
        try:
            player_sprite = CustomSprite(gd.PLAYER_IMG, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2 - mouse_size*2, text_y - mouse_size])
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
        reset_stat()
        # Show the mouse cursor
        pygame.mouse.set_visible(1)
        if countdown < 0:
            game_state = GAME_STATE_PLAY
        else:
            if countdown == 0:
                text = countdown_font.render("GO", True, WHITE)
                screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, gd.SCREEN_HEIGHT/2 - text.get_rect().height/2])
            elif countdown > 0:    
                text = countdown_font.render(str(countdown), True, WHITE)
                screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, gd.SCREEN_HEIGHT/2 - text.get_rect().height/2])
            # Draw the balls
            for ball in balls:
#                 pygame.draw.circle(screen, WHITE, [ball.x_pos, ball.y_pos], ball.size)
                ball_sprite = CustomSprite(gd.BALL_IMG, [ball.x_pos - ball.size, ball.y_pos - ball.size])
                screen.blit(ball_sprite.image, ball_sprite.rect)
            countdown -= 1
        pygame.time.delay(1000)
    elif game_state == GAME_STATE_SELECT_MODE:
        pygame.mouse.set_visible(1)
        
        # Text height will be increased every time a new line of text is created
        text_y = gd.SCREEN_HEIGHT/2 - text.get_rect().height/2
        text = title_font_1.render("Select difficulty:", True, WHITE)
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
 
    # --- Wrap-up
    # Limit frames per second
    clock.tick(60)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Close everything down
pygame.quit()