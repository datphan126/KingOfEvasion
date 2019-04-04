"""
 King of Evasion - Touch the Green Orb to gain points.
 
 Author: Dat Phan
"""
 
import pygame
import random
import game_definitions as gd
from ball import Ball
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

ball_size = 50

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
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("King Of Evasion")
 
# Loop until the user clicks the close button.
done = False

# Game difficulty
game_difficulty = GAME_DIFFICULTY_EASY

# Game speed - Default speed is Easy mode's speed
game_speed = gd.GAME_SPEED_EASY
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Create new ball list
balls = []
# Number of balls
ball_list_size = gd.BALL_LIMIT_EASY

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
        ball = Ball("Ball " + str(count), ball_x_pos,ball_y_pos,ball_size)
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
    create_balls()

# -------- Main Program Loop -----------
while not done:
    # --- Event Processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and game_state == GAME_STATE_MENU:
                game_state = GAME_STATE_SELECT_MODE
            elif event.key == pygame.K_ESCAPE:
                game_state = GAME_STATE_MENU
            elif event.key == pygame.K_1 and game_state == GAME_STATE_SELECT_MODE:
                game_difficulty = GAME_DIFFICULTY_EASY
                game_speed = gd.GAME_SPEED_EASY
                ball_list_size = gd.BALL_LIMIT_EASY
                game_state = GAME_STATE_COUNTDOWN
            elif event.key == pygame.K_2 and game_state == GAME_STATE_SELECT_MODE:
                game_difficulty = GAME_DIFFICULTY_MED
                game_speed = gd.GAME_SPEED_MED
                ball_list_size = gd.BALL_LIMIT_MED
                game_state = GAME_STATE_COUNTDOWN
            elif event.key == pygame.K_3 and game_state == GAME_STATE_SELECT_MODE:
                game_difficulty = GAME_DIFFICULTY_HARD
                game_speed = gd.GAME_SPEED_HARD
                ball_list_size = gd.BALL_LIMIT_HARD
                game_state = GAME_STATE_COUNTDOWN
            elif event.key == pygame.K_4 and game_state == GAME_STATE_SELECT_MODE:
                game_difficulty = GAME_DIFFICULTY_IMPOSSIBLE
                game_speed = gd.GAME_SPEED_IMPOSSIBLE
                ball_list_size = gd.BALL_LIMIT_IMPOSSIBLE
                game_state = GAME_STATE_COUNTDOWN   
 
    # Set the screen background
    screen.fill(BLACK)
    
    if game_state == GAME_STATE_PLAY:
        # Hide the mouse cursor
        pygame.mouse.set_visible(0)
        
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
        pygame.draw.circle(screen,RED,[mouse_x,mouse_y],mouse_size)
        
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
                pygame.draw.circle(screen, GREEN, [reward_x_pos, reward_y_pos], reward_item_size)
                reward_item_status = True
            else:
                pygame.draw.circle(screen, GREEN, [reward_x_pos, reward_y_pos], reward_item_size)
                
            # Check if the mouse collides with the reward item
            check_collision_with_reward()
            
            # Draw score
            textSmallScore = font.render("Score: " + str(score), True, WHITE)
            screen.blit(textSmallScore, [gd.SCREEN_WIDTH - 100, 0])
            
            # Check if balls collide each other
            check_ball_collision()
         
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
        screen.blit(text, [200, gd.SCREEN_HEIGHT/2])
        textScore = font.render(game_difficulty + " - Score: " + str(score), True, WHITE)
        screen.blit(textScore, [200, gd.SCREEN_HEIGHT/2 + 25])
        textKey = font.render("Press ESC to return to main menu", True, WHITE)
        screen.blit(textKey, [200, gd.SCREEN_HEIGHT/2 + 50])
        
    elif game_state == GAME_STATE_MENU:
        # Show the mouse cursor
        pygame.mouse.set_visible(1)
        countdown = 3
        text = font.render("BEP Game - King Of Evasion - Touch the Green Orb to gain points", True, WHITE)
        screen.blit(text, [200, gd.SCREEN_HEIGHT/2])
        textScore = font.render("Press ENTER to play", True, WHITE)
        screen.blit(textScore, [200, gd.SCREEN_HEIGHT/2 + 25])
    elif game_state == GAME_STATE_COUNTDOWN:
        # Reset all stats and create balls based on selected difficulty
        reset_stat()
        # Show the mouse cursor
        pygame.mouse.set_visible(1)
        if countdown < 0:
            game_state = GAME_STATE_PLAY
        else:
            countdown_font = pygame.font.SysFont('Calibri', 105, True, False)
            if countdown == 0:
                text = countdown_font.render("GO", True, WHITE)
                screen.blit(text, [200, gd.SCREEN_HEIGHT/2])
            elif countdown > 0:    
                text = countdown_font.render(str(countdown), True, WHITE)
                screen.blit(text, [200, gd.SCREEN_HEIGHT/2])
            # Draw the balls
            for ball in balls:
                pygame.draw.circle(screen, WHITE, [ball.x_pos, ball.y_pos], ball.size)
            countdown -= 1
        pygame.time.delay(1000)
    elif game_state == GAME_STATE_SELECT_MODE:
        pygame.mouse.set_visible(1)
        text = font.render("Select difficulty:", True, WHITE)
        screen.blit(text, [200, gd.SCREEN_HEIGHT/2])
        textScore = font.render("1 - Easy", True, WHITE)
        screen.blit(textScore, [200, gd.SCREEN_HEIGHT/2 + 25])
        textScore = font.render("2 - Medium", True, WHITE)
        screen.blit(textScore, [200, gd.SCREEN_HEIGHT/2 + 50])
        textScore = font.render("3 - Hard", True, WHITE)
        screen.blit(textScore, [200, gd.SCREEN_HEIGHT/2 + 75])
        textScore = font.render("4 - Impossible", True, WHITE)
        screen.blit(textScore, [200, gd.SCREEN_HEIGHT/2 + 100])
 
    # --- Wrap-up
    # Limit frames per second
    clock.tick(game_speed)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Close everything down
pygame.quit()