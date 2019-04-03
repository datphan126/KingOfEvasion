"""
 Bounces balls around the screen.
 
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
 
 Explanation video: http://youtu.be/-GmKoaX2iMs
 
 Edited by: Dat Phan
"""
 
import pygame
import random
import screen_for_ball_game as scr
from ball import Ball
 
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

pygame.init()
 
# Set the height and width of the screen
size = [scr.SCREEN_WIDTH, scr.SCREEN_HEIGHT]
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("Bouncing Balls")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Create new ball list
balls = []
ball01 = Ball("Ball 01", 50,50,50)
ball02 = Ball("Ball 02",350,350,50)
ball03 = Ball("Ball 03",550,350,50)
ball04 = Ball("Ball 04",750,350,50)
ball05 = Ball("Ball 05",360,150,50)
ball06 = Ball("Ball 06",560,250,50)
balls.append(ball01)
balls.append(ball02)
balls.append(ball03)
balls.append(ball04)
balls.append(ball05)
balls.append(ball06)

# Initiate Mouse position
mouse_x = 0
mouse_y = 0
mouse_size = 20

game_state = GAME_STATE_MENU

# Reward item status - if true, item is already created. If false, item isn't created
reward_item_status = False
reward_item_size = 20
reward_x_pos = 0
reward_y_pos = 0
score = 0

# Countdown before the match starts
countdown = 3

# Select the font to use, size, bold, italics
font = pygame.font.SysFont('Calibri', 25, True, False)

def check_collision():
    for ballA in balls:
        for ballB in balls:
            # Ignore if same ball
            if ballA.name == ballB.name:
                continue
            if (abs(ballA.x_pos - ballB.x_pos)**2 + abs(ballA.y_pos - ballB.y_pos)**2) <= (ballA.size + ballB.size)**2:
                ballA.circle_change_y = ballA.circle_change_y * -1
                ballA.circle_change_x = ballA.circle_change_x * -1
                
def check_collision_with_mouse():
    for ballA in balls:
        if (abs(ballA.x_pos - mouse_x)**2 + abs(ballA.y_pos - mouse_y)**2) <= (ballA.size + mouse_size)**2:
            global game_state
            game_state = GAME_STATE_OVER
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
    global countdown
    countdown = 3

# -------- Main Program Loop -----------
while not done:
    # --- Event Processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                game_state = GAME_STATE_COUNTDOWN
            elif event.key == pygame.K_ESCAPE:
                game_state = GAME_STATE_MENU
 
    # Set the screen background
    screen.fill(BLACK)
    
    if game_state == GAME_STATE_PLAY:
        # Hide the mouse cursor
        pygame.mouse.set_visible(0)
        
        # Draw mouse pointer
        mouse_pos = pygame.mouse.get_pos()
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        pygame.draw.circle(screen,RED,[mouse_x,mouse_y],mouse_size)
        
        # Check if any ball collides with the mouse
        check_collision_with_mouse()
        
        if game_state == GAME_STATE_PLAY:
            # Create reward item
            if reward_item_status == False:
                reward_x_pos = random.randint(0,scr.SCREEN_WIDTH - reward_item_size) + reward_item_size
                reward_y_pos = random.randint(0,scr.SCREEN_HEIGHT - reward_item_size) + reward_item_size
                pygame.draw.circle(screen, GREEN, [reward_x_pos, reward_y_pos], reward_item_size)
                reward_item_status = True
            else:
                pygame.draw.circle(screen, GREEN, [reward_x_pos, reward_y_pos], reward_item_size)
                
            # Check if the mouse collides with the reward item
            check_collision_with_reward()
            
            # Draw score
            textSmallScore = font.render("Score: " + str(score), True, WHITE)
            screen.blit(textSmallScore, [scr.SCREEN_WIDTH - 100, 0])
            
            # Check if balls collide each other
            check_collision()
         
            # Move balls
            for ball in balls:
                ball.move_ball()
            
            # Draw the balls
            for ball in balls:
                pygame.draw.circle(screen, WHITE, [ball.x_pos, ball.y_pos], ball.size)
                
    elif game_state == GAME_STATE_OVER:
        # Show the mouse cursor
        pygame.mouse.set_visible(1)
        text = font.render("GAME OVER", True, WHITE)
        screen.blit(text, [200, scr.SCREEN_HEIGHT/2])
        textScore = font.render("Score: " + str(score), True, WHITE)
        screen.blit(textScore, [200, scr.SCREEN_HEIGHT/2 + 25])
        textKey = font.render("Press ESC to return to main menu", True, WHITE)
        screen.blit(textKey, [200, scr.SCREEN_HEIGHT/2 + 50])
        
    elif game_state == GAME_STATE_MENU:
        # Show the mouse cursor
        pygame.mouse.set_visible(1)
        text = font.render("King Of Evasion - Touch the Green Orb to gain points", True, WHITE)
        screen.blit(text, [200, scr.SCREEN_HEIGHT/2])
        textScore = font.render("Press ENTER to play", True, WHITE)
        screen.blit(textScore, [200, scr.SCREEN_HEIGHT/2 + 25])
        reset_stat()
    elif game_state == GAME_STATE_COUNTDOWN:
        # Show the mouse cursor
        pygame.mouse.set_visible(1)
        countdown_font = pygame.font.SysFont('Calibri', 105, True, False)
        if countdown == 0:
            text = countdown_font.render("GO", True, WHITE)
            screen.blit(text, [200, scr.SCREEN_HEIGHT/2])
        elif countdown > 0:    
            text = countdown_font.render(str(countdown), True, WHITE)
            screen.blit(text, [200, scr.SCREEN_HEIGHT/2])
        elif countdown < 0:
            game_state = GAME_STATE_PLAY
        countdown -= 1
        pygame.time.delay(1000)
 
    # --- Wrap-up
    # Limit to 60 frames per second
    clock.tick(150)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Close everything down
pygame.quit()