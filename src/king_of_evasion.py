"""
 King of Evasion - Collect the Stars to gain points.
 
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
GAME_STATE_PAUSED = "GAME PAUSED"

# Game Difficulty definition
GAME_DIFFICULTY_EASY = "EASY"
GAME_DIFFICULTY_MED = "MEDIUM"
GAME_DIFFICULTY_HARD = "HARD"
GAME_DIFFICULTY_IMPOSSIBLE = "IMPOSSIBLE"

# Game modes
GAME_MODE_NORMAL = "Normal Mode"
GAME_MODE_TIMER = "Timer Mode"

# Game and screen
screen = None
game = None

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class Game(object):
    
    def __init__(self):
        # timer
        self.tick_rate = 30
        self.tick_count = 0
        self.timer_limit = 0
        
        # Highscore game mode - Used to switch views of game modes
        self.highscore_view_mode = gd.HIGHSCORE_VIEW_MODE_NORMAL
        
        # Game controller
        self.game_controller = gd.GAME_CONTROLLER_MOUSE
        
        # Game mode
        self.game_mode = GAME_MODE_NORMAL
        
        # Game difficulty
        self.game_difficulty = GAME_DIFFICULTY_EASY
        
        # Asteroid speed - Default speed is Easy mode's speed
        self.asteroid_speed = gd.ASTEROID_MOVE_SPEED_EASY
        
        # Create new asteroid list
        self.asteroid_list = pygame.sprite.Group()
        # Number of asteroids
        self.asteroid_list_size = 0
        
        self.game_state = GAME_STATE_MENU
        
        # Reward item status - if true, item is already created. If false, item isn't created
        self.reward_item_status = False
        self.score = 0
        self.old_score = 0
        
        # Countdown before the match starts
        self.countdown = 3
        
        # Fonts
        self.normal_font = pygame.font.SysFont('Calibri', 25, True, False)
        self.title_font_1 = pygame.font.SysFont('Calibri', 50, True, False)
        self.title_font_2 = pygame.font.SysFont('Calibri', 130, True, False)
        self.countdown_font = pygame.font.SysFont('Calibri', 105, True, False)
        
        # Create music list
        self.music_list = []
        self.music_list.append(gd.MUSIC_01)
        self.music_list.append(gd.MUSIC_02)
        self.music_list.append(gd.MUSIC_03)
        self.music_list.append(gd.MUSIC_04)
        
        # Highscore dict
        self.highscore_dict = {}
        
        # Create ship sprite in the center of the screen
        self.ship = ship_sprite.Ship(gd.PLAYER_IMG,[gd.SCREEN_WIDTH/2 - gd.SHIP_RADIUS, gd.SCREEN_HEIGHT/2 - gd.SHIP_RADIUS])
        
        # Create reward sprite
        self.reward_item = reward_sprite.Reward(gd.REWARD_IMG, [0, 0])
        
        # Background image
        self.background = custom_sprite.CustomSprite(resource_path(gd.BACKGROUND_IMG), [0,0])
    
    # Calculate asteroid limit based on selected difficulty and screen size
    def calculate_asteroid_limit(self):
        if self.game_difficulty == GAME_DIFFICULTY_EASY:
            self.asteroid_list_size = round(gd.ASTEROID_LIMIT_EASY * (gd.SCREEN_WIDTH - gd.SCREEN_HEIGHT))
        elif self.game_difficulty == GAME_DIFFICULTY_MED:
            self.asteroid_list_size = round(gd.ASTEROID_LIMIT_MED * (gd.SCREEN_WIDTH - gd.SCREEN_HEIGHT))
        elif self.game_difficulty == GAME_DIFFICULTY_HARD:
            self.asteroid_list_size = round(gd.ASTEROID_LIMIT_HARD * (gd.SCREEN_WIDTH - gd.SCREEN_HEIGHT))
        elif self.game_difficulty == GAME_DIFFICULTY_IMPOSSIBLE:
            self.asteroid_list_size = round(gd.ASTEROID_LIMIT_IMPOSSIBLE * (gd.SCREEN_WIDTH - gd.SCREEN_HEIGHT))
    
    def create_asteroids(self):
        self.asteroid_list.empty()
        is_collided = True
        for count in range(1,self.asteroid_list_size+1):
            asteroid = asteroid_sprite.Asteroid(gd.ASTEROID_IMG,"Ball " + str(count), [0,0], gd.ASTEROID_RADIUS, self.asteroid_speed)
            # Randomize the location of new asteroids and ensure they don't collide with each other
            while is_collided:
                # Add 1 and Minus 1 to ensure the asteroid doesn't hit the borders at the game's start
                asteroid.rect.x = random.randint(gd.ASTEROID_RADIUS + 1, gd.SCREEN_WIDTH - gd.ASTEROID_RADIUS - 1)
                asteroid.rect.y = random.randint(gd.ASTEROID_RADIUS + 1, gd.SCREEN_HEIGHT - gd.ASTEROID_RADIUS - 1)
                collision_list = pygame.sprite.spritecollide(asteroid, self.asteroid_list, False)
                if len(collision_list) == 0:
                    is_collided = False
                    
                # Don't spawn asteroid in the center of the screen
                center_x = gd.SCREEN_WIDTH/2
                center_y = gd.SCREEN_HEIGHT/2
                safe_range = 4
                if asteroid.rect.x >= (center_x - gd.ASTEROID_RADIUS * safe_range) and asteroid.rect.x <= (center_x + gd.ASTEROID_RADIUS * safe_range) \
                and asteroid.rect.y >= (center_y - gd.ASTEROID_RADIUS * safe_range) and asteroid.rect.y <= (center_y + gd.ASTEROID_RADIUS * safe_range):
                    is_collided = True
            
            self.asteroid_list.add(asteroid)
            # Reset is_collied for verifying the next new asteroid
            is_collided = True
    
    def check_collision_between_asteroids(self):
        for asteroidA in self.asteroid_list:
            for asteroidB in self.asteroid_list:
                # Ignore if same asteroid
                if asteroidA.name == asteroidB.name:
                    continue
                # Use Pythagorean theorem to detect the collision
                if (abs(asteroidA.rect.x - asteroidB.rect.x)**2 + abs(asteroidA.rect.y - asteroidB.rect.y)**2) <= (asteroidA.radius + asteroidB.radius)**2:
                    asteroidA.change_y = asteroidA.change_y * -1
                    asteroidA.change_x = asteroidA.change_x * -1
                    break
                    
    def check_collision_with_ship(self):
        for asteroid in self.asteroid_list:
            if (abs(asteroid.rect.x - self.ship.rect.x)**2 + abs(asteroid.rect.y - self.ship.rect.y)**2) <= (gd.ASTEROID_RADIUS + gd.SHIP_RADIUS)**2:
                self.game_over()
                break
    
    def check_collision_with_reward(self):
        if (abs(self.reward_item.rect.x - self.ship.rect.x)**2 + abs(self.reward_item.rect.y - self.ship.rect.y)**2) <= (gd.REWARD_RADIUS + gd.SHIP_RADIUS)**2:
            self.score += 1
            self.reward_item_status = False
            self.tick_count = 0
    
    def game_over(self):
        self.update_highscore()
        self.game_state = GAME_STATE_OVER
        pygame.mixer.music.stop()
        pygame.mixer.music.load(resource_path(gd.GAMEOVER_SOUND))
        pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
        pygame.mixer.music.play()
        fadeGameoverMenu()
            
    def reset_stat(self):
        self.score = 0
        self.reward_item_status = False
        self.old_score = 0
        self.tick_count = 0
        self.ship.rect.x = gd.SCREEN_WIDTH/2 - gd.SHIP_RADIUS
        self.ship.rect.y = gd.SCREEN_HEIGHT/2 - gd.SHIP_RADIUS
        self.countdown = 3
        self.create_asteroids()
    
    def play_background_music(self):
        pygame.mixer.music.load(resource_path(self.music_list[random.randint(0,len(self.music_list)-1)]))
        pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
        pygame.mixer.music.play()
        
    def initialize_highscore_list(self):
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
        self.highscore_dict[GAME_MODE_NORMAL] = difficulty_normal_mode
        
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
        self.highscore_dict[GAME_MODE_TIMER] = difficulty_timer_mode
        
    def update_highscore(self):
        # Add the new score, sort the list, and remove the last element that is not within the defined top size (ex: top 10)
        self.highscore_dict[self.game_mode][self.game_difficulty].append(self.score)
        self.highscore_dict[self.game_mode][self.game_difficulty].sort(reverse=True)
        self.highscore_dict[self.game_mode][self.game_difficulty].pop()
        
    def load_highscore(self):
        
        try:
            with open(gd.HIGHSCORE_FILE_NAME) as csv_file:
                csv_reader = csv.DictReader(csv_file)
                line_count = 0
                for row in csv_reader:
                    # Reset line_count for loading scores of the next difficulty
                    if line_count >= gd.HIGHSCORE_LIST_SIZE:
                        line_count = 0
                         
                    self.highscore_dict[row["GAME_MODE"]][row["DIFFICULTY"]][line_count] = int(row["SCORE"])
                    line_count += 1
        except FileNotFoundError:
            print("Highscore file does not exist!")
            
    def save_highscore(self):
        
        try:
            with open(gd.HIGHSCORE_FILE_NAME, mode='w') as csv_file:
                fieldnames = ["GAME_MODE","DIFFICULTY","SCORE"]
                    
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                for key_game_mode in self.highscore_dict.keys():
                    for key_difficulty in self.highscore_dict[key_game_mode].keys():
                        for score in self.highscore_dict[key_game_mode][key_difficulty]:
                            writer.writerow({'GAME_MODE': key_game_mode, 'DIFFICULTY': key_difficulty, 'SCORE': score})
        except Exception:
            print("Unexpected error:", sys.exc_info()[1])

# End Game class   

# This method is for drawing created game objects like ship, asteroids, star, and score
def drawGameObjects():
    global screen, game
    # Draw the asteroids
    for asteroid in game.asteroid_list:
        screen.blit(asteroid.image, [asteroid.rect.x - gd.ASTEROID_RADIUS, asteroid.rect.y - gd.ASTEROID_RADIUS])
        
    # Draw score
    text = game.normal_font.render("Score: " + str(game.score), True, WHITE)
    screen.blit(text, [gd.SCREEN_WIDTH - 100, 0])
    
    # Draw ship    
    screen.blit(game.ship.image, [game.ship.rect.x - gd.SHIP_RADIUS, game.ship.rect.y - gd.SHIP_RADIUS])
    
    # Draw reward item - Only draw when reward item status has already spwaned
    if game.reward_item_status == True:
        screen.blit(game.reward_item.image, [game.reward_item.rect.x - gd.REWARD_RADIUS, game.reward_item.rect.y - gd.REWARD_RADIUS])

# Draw Game Over Menu
def drawGameOverMenu():
    screen.fill([0,0,0])
    text = game.title_font_1.render("GAME OVER", True, WHITE)
    # Text height will be increased every time a new line of text is created
    text_y = gd.SCREEN_HEIGHT/2 - text.get_rect().height/2
    screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
    text_y += text.get_rect().height
    text = game.normal_font.render(game.game_difficulty + " - Score: " + str(game.score), True, WHITE)
    screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
    text_y += text.get_rect().height
    text = game.normal_font.render("Press BACKSPACE to retry", True, WHITE)
    screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
    text_y += text.get_rect().height
    text = game.normal_font.render("Press SPACE BAR to return to the main menu", True, WHITE)
    screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
    text_y += text.get_rect().height

# Fading effect for game over menu
def fadeGameoverMenu(): 
    fade = pygame.Surface((gd.SCREEN_WIDTH, gd.SCREEN_HEIGHT))
    fade.fill((0,0,0))
    # for alpha in range(50, 300):
    alpha = 0
    while alpha <= 400:
        fade.set_alpha(alpha)
        alpha += 5
        # screen.fill([0,0,0])
        screen.blit(game.background.image, game.background.rect)
        drawGameObjects()
        screen.blit(fade, (0,0))
        pygame.display.update()
            
def main():
    global screen, game

    pygame.init()
 
    # Set the height and width of the screen
    size = [gd.SCREEN_WIDTH, gd.SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
     
    pygame.display.set_caption("King Of Evasion")
     
    # Loop until the user clicks the close button.
    done = False
    
    # Frame rate
    frame_rate = 60
    
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
   
    # Initialize Game object
    game = Game()
   
    # Initialize highscore list
    game.initialize_highscore_list()   
       
    # Load high scores
    game.load_highscore()
     
    # Play background music randomly
    game.play_background_music()
    
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
                elif event.key == pygame.K_RETURN and game.game_state == GAME_STATE_MENU:
                    game.game_state = GAME_STATE_SELECT_CONTROLLER
                # View highscore
                elif event.key == pygame.K_F12 and game.game_state == GAME_STATE_MENU:
                    game.game_state = GAME_STATE_SELECT_HIGHSCORE_MODE
                # Pause game
                elif event.key == pygame.K_F5 and game.game_state == GAME_STATE_PLAY:
                    game.game_state = GAME_STATE_PAUSED
                # Unpause game
                elif event.key == pygame.K_F5 and game.game_state == GAME_STATE_PAUSED:
                    game.game_state = GAME_STATE_PLAY
                # Return to main menu
                elif event.key == pygame.K_SPACE:
                    game.game_state = GAME_STATE_MENU
                    # Play background music
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(resource_path(game.music_list[random.randint(0,len(game.music_list)-1)]))
                    pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
                    pygame.mixer.music.play()
                # -- Start Difficulty --
                elif (event.key == pygame.K_1 or event.key == pygame.K_KP1) and game.game_state == GAME_STATE_SELECT_DIFFICULTY:
                    game.game_difficulty = GAME_DIFFICULTY_EASY
                    game.asteroid_speed = gd.ASTEROID_MOVE_SPEED_EASY
                    game.timer_limit = gd.TIMER_LIMIT_EASY
                    game.calculate_asteroid_limit()
                    game.game_state = GAME_STATE_COUNTDOWN
                elif (event.key == pygame.K_2 or event.key == pygame.K_KP2) and game.game_state == GAME_STATE_SELECT_DIFFICULTY:
                    game.game_difficulty = GAME_DIFFICULTY_MED
                    game.asteroid_speed = gd.ASTEROID_MOVE_SPEED_MED
                    game.timer_limit = gd.TIMER_LIMIT_MED
                    game.calculate_asteroid_limit()
                    game.game_state = GAME_STATE_COUNTDOWN
                elif (event.key == pygame.K_3 or event.key == pygame.K_KP3) and game.game_state == GAME_STATE_SELECT_DIFFICULTY:
                    game.game_difficulty = GAME_DIFFICULTY_HARD
                    game.asteroid_speed = gd.ASTEROID_MOVE_SPEED_HARD
                    game.timer_limit = gd.TIMER_LIMIT_HARD
                    game.calculate_asteroid_limit()
                    game.game_state = GAME_STATE_COUNTDOWN
                elif (event.key == pygame.K_4 or event.key == pygame.K_KP4) and game.game_state == GAME_STATE_SELECT_DIFFICULTY:
                    game.game_difficulty = GAME_DIFFICULTY_IMPOSSIBLE
                    game.asteroid_speed = gd.ASTEROID_MOVE_SPEED_IMPOSSIBLE
                    game.timer_limit = gd.TIMER_LIMIT_IMPOSSIBLE
                    game.calculate_asteroid_limit()
                    game.game_state = GAME_STATE_COUNTDOWN
                # -- End Difficulty --
                # -- Game Mode --
                elif (event.key == pygame.K_1 or event.key == pygame.K_KP1) and game.game_state == GAME_STATE_SELECT_GAME_MODE:
                    game.game_mode = GAME_MODE_NORMAL
                    game.game_state = GAME_STATE_SELECT_DIFFICULTY
                elif (event.key == pygame.K_2 or event.key == pygame.K_KP2) and game.game_state == GAME_STATE_SELECT_GAME_MODE:
                    game.game_mode = GAME_MODE_TIMER
                    game.game_state = GAME_STATE_SELECT_DIFFICULTY
                # -- End Game Mode --
                # -- Game Mode --
                elif (event.key == pygame.K_1 or event.key == pygame.K_KP1) and game.game_state == GAME_STATE_SELECT_HIGHSCORE_MODE:
                    game.highscore_view_mode = GAME_MODE_NORMAL
                    game.game_state = GAME_STATE_VIEW_HIGHSCORE
                elif (event.key == pygame.K_2 or event.key == pygame.K_KP2) and game.game_state == GAME_STATE_SELECT_HIGHSCORE_MODE:
                    game.highscore_view_mode = GAME_MODE_TIMER
                    game.game_state = GAME_STATE_VIEW_HIGHSCORE
                # -- End Game Mode --
                # -- Controller Mode --
                elif (event.key == pygame.K_1 or event.key == pygame.K_KP1) and game.game_state == GAME_STATE_SELECT_CONTROLLER:
                    game.game_controller = gd.GAME_CONTROLLER_MOUSE
                    game.game_state = GAME_STATE_SELECT_GAME_MODE
                elif (event.key == pygame.K_2 or event.key == pygame.K_KP2) and game.game_state == GAME_STATE_SELECT_CONTROLLER:
                    game.game_controller = gd.GAME_CONTROLLER_KEYBOARD
                    game.game_state = GAME_STATE_SELECT_GAME_MODE
                # -- End Controller Mode --
                # -- ship_sprite controlled by Keyboard -- Set the speed based on the key pressed
                elif event.key == pygame.K_LEFT:
                    game.ship.move_ship(-gd.SHIP_SPEED, 0)
                elif event.key == pygame.K_RIGHT:
                    game.ship.move_ship(gd.SHIP_SPEED, 0)
                elif event.key == pygame.K_UP:
                    game.ship.move_ship(0, -gd.SHIP_SPEED)
                elif event.key == pygame.K_DOWN:
                    game.ship.move_ship(0, gd.SHIP_SPEED)
                # -- End ship_sprite controlled by keyboard --
                # Retry option
                elif event.key == pygame.K_BACKSPACE and game.game_state == GAME_STATE_OVER:
                    game.reset_stat()
                    game.play_background_music()
                    game.game_state = GAME_STATE_COUNTDOWN
            # -- ship_sprite controlled by Keyboard -- Reset speed when key goes up
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    game.ship.move_ship(gd.SHIP_SPEED, 0)
                elif event.key == pygame.K_RIGHT:
                    game.ship.move_ship(-gd.SHIP_SPEED, 0)
                elif event.key == pygame.K_UP:
                    game.ship.move_ship(0, gd.SHIP_SPEED)
                elif event.key == pygame.K_DOWN:
                    game.ship.move_ship(0, -gd.SHIP_SPEED)
            # -- End ship_sprite controlled by keyboard
            elif event.type == pygame.constants.USEREVENT:
                    if game.game_state != GAME_STATE_OVER:
                        game.play_background_music()

        # Set the screen background
        screen.blit(game.background.image, game.background.rect)
        
        if game.game_state == GAME_STATE_PLAY:
            # Hide the ship cursor
            pygame.mouse.set_visible(0)
            
            # -- Timer Update --
            if game.game_mode == GAME_MODE_TIMER:
                total_seconds = game.timer_limit - (game.tick_count // game.tick_rate)
                if total_seconds <= 0:
                    game.game_over()
             
                # Divide by 60 to get total minutes
                minutes = total_seconds // 60
             
                # Use modulus (remainder) to get seconds
                seconds = total_seconds % 60
             
                # Use python string formatting to format in leading zeros
                output_string = "Time left: {0:02}:{1:02}".format(minutes, seconds)
             
                # Blit to the screen
                text = game.normal_font.render(output_string, True, WHITE)
             
                screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, 0])
                game.tick_count += 1
            # --End Timer Update --
            
            # Increase asteroids' speed
            if (game.score - game.old_score) == gd.SPEED_INCREASE_POINTS:
                game.old_score = game.score
                for asteroid in game.asteroid_list:
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
            if game.game_controller == gd.GAME_CONTROLLER_MOUSE:
                game.ship_pos = pygame.mouse.get_pos()
                game.ship.rect.x = game.ship_pos[0]
                game.ship.rect.y = game.ship_pos[1]
                
            # Update ship location for keyboard players    
            if game.game_controller == gd.GAME_CONTROLLER_KEYBOARD:
                game.ship.update()
                
            # Mouse cursor should not overlap the borders
            if game.ship.rect.y >= (gd.SCREEN_HEIGHT - gd.SHIP_RADIUS):
                game.ship.rect.y = gd.SCREEN_HEIGHT - gd.SHIP_RADIUS
            elif game.ship.rect.y <= gd.SHIP_RADIUS:
                game.ship.rect.y = gd.SHIP_RADIUS
            if game.ship.rect.x >= (gd.SCREEN_WIDTH - gd.SHIP_RADIUS):
                game.ship.rect.x = gd.SCREEN_WIDTH - gd.SHIP_RADIUS
            elif game.ship.rect.x <= gd.SHIP_RADIUS:
                game.ship.rect.x = gd.SHIP_RADIUS    
                
            # Draw ship    
            screen.blit(game.ship.image, [game.ship.rect.x - gd.SHIP_RADIUS, game.ship.rect.y - gd.SHIP_RADIUS])
            # -- End Mouse Pointer Update --
            
            
            if game.game_state == GAME_STATE_PLAY:
                # Create reward item
                if game.reward_item_status == False:
                    game.reward_item.rect.x = random.randint(0,gd.SCREEN_WIDTH - gd.REWARD_RADIUS) + gd.REWARD_RADIUS
                    game.reward_item.rect.y = random.randint(0,gd.SCREEN_HEIGHT - gd.REWARD_RADIUS) + gd.REWARD_RADIUS
                    # Reward item should not overlap the borders
                    if game.reward_item.rect.y >= (gd.SCREEN_HEIGHT - gd.REWARD_RADIUS):
                        game.reward_item.rect.y = gd.SCREEN_HEIGHT - gd.REWARD_RADIUS
                    elif game.reward_item.rect.y <= gd.REWARD_RADIUS:
                        game.reward_item.rect.y = gd.REWARD_RADIUS
                    if game.reward_item.rect.x >= (gd.SCREEN_WIDTH - gd.REWARD_RADIUS):
                        game.reward_item.rect.x = gd.SCREEN_WIDTH - gd.REWARD_RADIUS
                    elif game.reward_item.rect.x <= gd.REWARD_RADIUS:
                        game.reward_item.rect.x = gd.REWARD_RADIUS
                    screen.blit(game.reward_item.image, [game.reward_item.rect.x - gd.REWARD_RADIUS, game.reward_item.rect.y - gd.REWARD_RADIUS])
                    game.reward_item_status = True
                else:
                    screen.blit(game.reward_item.image, [game.reward_item.rect.x - gd.REWARD_RADIUS, game.reward_item.rect.y - gd.REWARD_RADIUS])
                    
                # Check if the ship collides with the reward item
                game.check_collision_with_reward()
                
                # Draw score
                textSmallScore = game.normal_font.render("Score: " + str(game.score), True, WHITE)
                screen.blit(textSmallScore, [gd.SCREEN_WIDTH - 100, 0])
                
                # Check if asteroids collide each other
                game.check_collision_between_asteroids()
             
                # Move asteroids
                for asteroid in game.asteroid_list:
                    asteroid.move_asteroid()

                # Draw the asteroids
                for asteroid in game.asteroid_list:
                    screen.blit(asteroid.image, [asteroid.rect.x - gd.ASTEROID_RADIUS, asteroid.rect.y - gd.ASTEROID_RADIUS])
                    
                # Check if any asteroid collides with the ship
                game.check_collision_with_ship()
                
        elif game.game_state == GAME_STATE_OVER:
            # Show the ship cursor
            pygame.mouse.set_visible(1)
            
            drawGameOverMenu()
            
        elif game.game_state == GAME_STATE_MENU:
            # Show the ship cursor
            pygame.mouse.set_visible(1)
            game.countdown = 3
            
            text = game.title_font_2.render("King Of Evasion", True, WHITE)
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
            
            text = game.title_font_1.render("Collect the Stars to gain points and Evade asteroids", True, WHITE)
            screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
            text_y += text.get_rect().height
            
            text = game.title_font_1.render("Press F12 to view high scores", True, WHITE)
            screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
            text_y += text.get_rect().height
            
            text = game.title_font_1.render("Press ENTER to play", True, WHITE)
            screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
            text_y += text.get_rect().height
        elif game.game_state == GAME_STATE_COUNTDOWN:
            # Reset all stats and create asteroids based on selected difficulty and screen size
            if game.countdown == 3:
                game.reset_stat()
                
            text = game.normal_font.render("Press F5 to pause the game", True, WHITE)
            screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, 0])
                    
            # Show the ship cursor
            pygame.mouse.set_visible(1)
            
            if game.countdown < 0:
                game.game_state = GAME_STATE_PLAY
            else:
                # Draw the asteroids
                for asteroid in game.asteroid_list:
                    screen.blit(asteroid.image, [asteroid.rect.x - gd.ASTEROID_RADIUS, asteroid.rect.y - gd.ASTEROID_RADIUS])
                    
                if game.countdown == 0:
                    text = game.countdown_font.render("GO", True, WHITE)
                    screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, gd.SCREEN_HEIGHT/2 - text.get_rect().height/2])
                elif game.countdown > 0:    
                    text = game.countdown_font.render(str(game.countdown), True, WHITE)
                    screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, gd.SCREEN_HEIGHT/2 - text.get_rect().height/2])
                game.countdown -= 1
            pygame.time.delay(1000)
        elif game.game_state == GAME_STATE_PAUSED:
            # Show the ship cursor
            pygame.mouse.set_visible(1)
            
            # Draw game objects
            drawGameObjects()
                
            text_y = gd.SCREEN_HEIGHT/2 - text.get_rect().height/2
            text = game.countdown_font.render("GAME PAUSED", True, WHITE)
            screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
            text_y += text.get_rect().height
            
            text = game.normal_font.render("Press F5 to unpause the game", True, WHITE)
            screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
        elif game.game_state == GAME_STATE_SELECT_DIFFICULTY:
            pygame.mouse.set_visible(1)
            
            # Text height will be increased every time a new line of text is created
            text_y = gd.SCREEN_HEIGHT/2 - text.get_rect().height/2
            text = game.title_font_1.render("Select a difficulty:", True, WHITE)
            screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
            text_y += text.get_rect().height
            text = game.title_font_1.render("1 - Easy", True, WHITE)
            screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
            text_y += text.get_rect().height
            text = game.title_font_1.render("2 - Medium", True, WHITE)
            screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
            text_y += text.get_rect().height
            text = game.title_font_1.render("3 - Hard", True, WHITE)
            screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
            text_y += text.get_rect().height
            text = game.title_font_1.render("4 - Impossible", True, WHITE)
            screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
            text_y += text.get_rect().height
        elif game.game_state == GAME_STATE_SELECT_GAME_MODE:
            pygame.mouse.set_visible(1)
            
            # Text height will be increased every time a new line of text is created
            text_y = gd.SCREEN_HEIGHT/2 - text.get_rect().height/2
            text = game.title_font_1.render("Select a game mode:", True, WHITE)
            screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
            text_y += text.get_rect().height
            text = game.title_font_1.render("1 - Normal", True, WHITE)
            screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
            text_y += text.get_rect().height
            text = game.title_font_1.render("2 - Timer", True, WHITE)
            screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
            text_y += text.get_rect().height
        elif game.game_state == GAME_STATE_SELECT_CONTROLLER:
            pygame.mouse.set_visible(1)
            
            # Text height will be increased every time a new line of text is created
            text_y = gd.SCREEN_HEIGHT/2 - text.get_rect().height/2
            text = game.title_font_1.render("Select your controller type:", True, WHITE)
            screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
            text_y += text.get_rect().height
            text = game.title_font_1.render("1 - Mouse", True, WHITE)
            screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
            text_y += text.get_rect().height
            text = game.title_font_1.render("2 - Keyboard", True, WHITE)
            screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
            text_y += text.get_rect().height
        elif game.game_state == GAME_STATE_SELECT_HIGHSCORE_MODE:
            pygame.mouse.set_visible(1)
            
            # Text height will be increased every time a new line of text is created
            text_y = gd.SCREEN_HEIGHT/2 - text.get_rect().height/2
            text = game.title_font_1.render("Select a highscore view mode:", True, WHITE)
            screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
            text_y += text.get_rect().height
            text = game.title_font_1.render("1 - Normal", True, WHITE)
            screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
            text_y += text.get_rect().height
            text = game.title_font_1.render("2 - Timer", True, WHITE)
            screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
            text_y += text.get_rect().height
        elif game.game_state == GAME_STATE_VIEW_HIGHSCORE:
            pygame.mouse.set_visible(1)
            
            # Text height will be increased every time a new line of text is created
            text_y = gd.SCREEN_HEIGHT/2 * 0.25 - text.get_rect().height/2
            text = game.title_font_1.render("HIGH SCORES", True, WHITE)
            screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
            text_y += text.get_rect().height
            text = game.title_font_1.render("Mode: " + str(game.highscore_view_mode), True, WHITE)
            screen.blit(text, [gd.SCREEN_WIDTH/2 - text.get_rect().width/2, text_y])
            text_y += text.get_rect().height
            text_y += text.get_rect().height
            
            difficulty_count = 1;
            old_text_y = text_y
            for key_difficulty in game.highscore_dict[game.highscore_view_mode].keys():
                # Make all score columns at the same height
                text_y = old_text_y
                
                text = game.title_font_1.render(key_difficulty, True, WHITE)
                screen.blit(text, [gd.SCREEN_WIDTH/2 * 0.4 * difficulty_count - text.get_rect().width/2, text_y])
                text_y += text.get_rect().height
                
                for score in game.highscore_dict[game.highscore_view_mode][key_difficulty]:
                    text = game.title_font_1.render(str(score), True, WHITE)
                    screen.blit(text, [gd.SCREEN_WIDTH/2 * 0.4 * difficulty_count - text.get_rect().width/2, text_y])
                    text_y += text.get_rect().height
                    
                difficulty_count += 1
     
        # --- Wrap-up
        # Limit frames per second
        clock.tick(frame_rate)
     
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
    
    # Save highscore before quitting
    game.save_highscore()
    # Close everything down
    pygame.quit()
    
# Call the main function, start up the game
if __name__ == "__main__":
    main()