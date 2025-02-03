#Toumpa Georgia, 2120163
#Kalaitzidis Ioannis, 2120067

#Libraries
import pygame
import sys
import random
import math

pygame.init()

# Set display width and height
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h
size = (screen_width , screen_height) 
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

pygame.display.set_caption("Oh Mummy")

# Start the music
pygame.mixer.init()
pygame.mixer.music.set_volume(0.3) #set volume
pygame.mixer.music.load('assets\\music.mp3') #load music archive
pygame.mixer.music.play(-1) #-1 plays the music in a loop, 0 plays it just once

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 128, 255)
RED = (255, 0, 0)
BROWN = (102, 51, 0)
BERGENDY = (128, 0, 32)

#-------------------------- LOAD IMAGES ------------------------------------------------

# Load the heart image
heart_image = pygame.image.load("assets\\live.png")  
heart_image = pygame.transform.scale(heart_image, (50, 50))  # Adjust the size as needed

# Load images and scale them
intro = pygame.image.load("assets\\intro.png")
intro = pygame.transform.scale(intro, (info.current_w, info.current_h))

map_image = pygame.image.load("assets\\map.png")
map_image = pygame.transform.scale(map_image, (info.current_w, info.current_h))

logo = pygame.image.load("assets\\logo.png")
logo = pygame.transform.scale(logo, (550, 100))
logo_rect = logo.get_rect()
logo_rect.topright = (690, 20)

compass = pygame.image.load("assets\\compass.png")
compass = pygame.transform.scale(compass, (160, 160))  
compass_rect = compass.get_rect()
compass_rect.bottomleft = (10, screen_height - 20) 

#------------------------- BUTTONS --------------------------------------------

# Define button properties
button_font = pygame.font.SysFont("arialblack", 40)

play_button_text = button_font.render("Play", True, YELLOW)
play_button_rect = play_button_text.get_rect(center=(screen_width // 2, screen_height // 2))

exit_button_text = button_font.render("Exit", True, YELLOW)
exit_button_rect = exit_button_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))

restart_button_text = button_font.render("Restart", True, YELLOW)
restart_button_rect = restart_button_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
#------------------------- INITIALIZATIONS -------------------------------------

# Health bar properties
max_lives = 3
current_lives = 3
last_life_gain_time = pygame.time.get_ticks()  # Time when the last life was gained
life_gain_delay = 2000  # Delay before allowing the player to gain a life (in milliseconds)

# black rectangles properties
rectangle_width = 180
rectangle_height = 80
space_between_rectangles = 50

# rows and columns for grid 4*5
rows = 4
columns = 5

# Main game loop
clock = pygame.time.Clock()
done = False
flag = False  # variable for random choice of images to only happen once

play_button_pressed = False # Check if the user is using keyboard buttons
selected_button_index = 0 # Check for the color change in each button we select

# Distance between footprints
footprint_distance = 10
footprints = []  # List to store footprint positions

current_direction = "back"  # Variable to store the current direction of the player's footprints

# variables for player
x_speed = 0
y_speed = 0
x_coord = 755
y_coord = 237
player_width = 40
player_height = 40

# variables for mummy
mx_speed = 0.12
my_speed = 0
mx_coord = 220
my_coord = 623
mummy_width = 40
mummy_height = 40

#-------------------------- LOAD ASSETS --------------------------------------------------
key = pygame.image.load("assets\\Key.png")
key = pygame.transform.scale(key, (rectangle_width, rectangle_height))

treasure = pygame.image.load("assets\\Treasure.png")
treasure = pygame.transform.scale(treasure, (rectangle_width, rectangle_height))

empty = pygame.image.load("assets\\Empty.png")
empty = pygame.transform.scale(empty, (rectangle_width, rectangle_height))

black = pygame.image.load("assets\\Black.png")
black = pygame.transform.scale(black, (rectangle_width, rectangle_height))

sarc = pygame.image.load("assets\\Sarcophagus.png")
sarc = pygame.transform.scale(sarc, (rectangle_width, rectangle_height))

# Load mummy images
mummy1 = pygame.image.load("assets\\mummyf.png")
mummy1 = pygame.transform.scale(mummy1, (mummy_width, mummy_height))

mummy2 = pygame.image.load("assets\\mummyb.png")
mummy2 = pygame.transform.scale(mummy2, (mummy_width, mummy_height))

mummy3 = pygame.image.load("assets\\mummyl.png")
mummy3 = pygame.transform.scale(mummy3, (mummy_width, mummy_height))

mummy4 = pygame.image.load("assets\\mummyr.png")
mummy4 = pygame.transform.scale(mummy4, (mummy_width, mummy_height))

# Load player images
player1 = pygame.image.load("assets\\playerf.png") #Front
player1 = pygame.transform.scale(player1, (player_width, player_height))

player2 = pygame.image.load("assets\\playerb.png") #Back
player2 = pygame.transform.scale(player2, (player_width, player_height))

player3 = pygame.image.load("assets\\playerl.png") #Left
player3 = pygame.transform.scale(player3, (player_width, player_height))

player4 = pygame.image.load("assets\\playerr.png") #Right
player4 = pygame.transform.scale(player4, (player_width, player_height))

player_images = [player1, player2, player3, player4]

# Load footprints images
footprints_image1 = pygame.image.load("assets\\footprints-f.png")  # Front
footprints_image1 = pygame.transform.scale(footprints_image1, (40, 40))

footprints_image2 = pygame.image.load("assets\\footprints-b.png")  # Back
footprints_image2 = pygame.transform.scale(footprints_image2, (40, 40))

footprints_image3 = pygame.image.load("assets\\footprints-l.png")  # Left
footprints_image3 = pygame.transform.scale(footprints_image3, (40, 40))

footprints_image4 = pygame.image.load("assets\\footprints-r.png")  # Right
footprints_image4 = pygame.transform.scale(footprints_image4, (40, 40))

#------------------------- CLASS FOR PLAYERS -------------------------------------
class Block(pygame.sprite.Sprite):
    
    def __init__(self, images, width, height, x, y, speed):
        super().__init__()
        self.images = images
        self.index = 1  # Direction
        self.image = self.images[self.index] 
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.speed = 2
        self.current_destination = 0 # For footprrints

    def update_image(self):
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

    def update(self, path):
        if self.rect.x == path[self.current_destination][0] and self.rect.y == path[self.current_destination][1]:
            self.current_destination += 1
            if self.current_destination >= len(path):
                self.current_destination = 0

        target_x, target_y = path[self.current_destination]
        if self.rect.x < target_x:
            self.rect.x += min(self.speed, target_x - self.rect.x)
            self.index = 3  # Update animation index for right direction
        elif self.rect.x > target_x:
            self.rect.x -= min(self.speed, self.rect.x - target_x)
            self.index = 2  # Update animation index for left direction
        elif self.rect.y < target_y:
            self.rect.y += min(self.speed, target_y - self.rect.y)
            self.index = 1  # Update animation index for up direction
        elif self.rect.y > target_y:
            self.rect.y -= min(self.speed, self.rect.y - target_y)
            self.index = 0  # Update animation index for down direction
   
#------------------------- SCENES -------------------------------------
# Main menu scene
def main_menu():
    screen.blit(intro, (0, 0))
    screen.blit(logo, logo_rect)
    screen.blit(play_button_text, play_button_rect)
    screen.blit(exit_button_text, exit_button_rect)
    restart_button_rect.topleft = (-60, -60)
    update_button_colors()
    pygame.display.flip()

def restart_game():
    global current_lives, high_score, passed_rectangles, mummy, last_life_gain_time, rect, x_coord, y_coord, mx_coord, my_coord, mx_speed, my_speed, current_direction, top, bottom, left, right, left_passed, right_passed, top_passed, bottom_passed, won, lost
    
    # Reset variables
    current_lives = 3
    high_score = 0
    last_life_gain_time = pygame.time.get_ticks()  # Time when the last life was gained

    # Reset player position
    x_coord = 755
    y_coord = 237
    player.index = 1

    # Reset mummy position
    mx_coord = 220
    my_coord = 623
    mummy.index = 3
    mx_speed = 0.12
    my_speed = 0
    mx_coord += mx_speed
    my_coord += my_speed

    # Clear footprints
    footprints.clear()

    # Clear passed rectangles
    passed_rectangles.clear()

    # Update footprints
    current_direction = "back"
    
    image_to_place.clear()
    rectangles.clear()

    # grid of rectangles with spaces between them
    for row in range(rows):
        for col in range(columns):

            x = col * (rectangle_width + space_between_rectangles) + 220
            y = row * (rectangle_height + space_between_rectangles) + 280
            rectangles.append(pygame.Rect(x, y, rectangle_width, rectangle_height))
            
    key_choice = False

    for rect in rectangles:
        # Randomly choose between empty and treasure
        if key_choice == False:
            choice = random.choice([empty, treasure, key, sarc])
            if choice == key:
                key_choice = True
        elif key_choice == True:
            choice = random.choice([empty, treasure, sarc])
        image_to_place.append(choice)

    top = False
    bottom = False
    left = False
    right = False
    passed_rectangles = set()  # Set to store passed rectangles

    # Initialize arrays for each side of the rectangles
    left_passed = [False] * len(rectangles)
    right_passed = [False] * len(rectangles)
    top_passed = [False] * len(rectangles)
    bottom_passed = [False] * len(rectangles)

    won = False
    lost = False

    # Update scene
    game_scene()

    # Update display
    pygame.display.flip()

def game_scene():
    screen.fill(YELLOW)
    screen.blit(map_image, (0, 0))  
    screen.blit(compass, compass_rect)
    play_button_rect.topleft = (-60, -60)
    exit_button_rect.topleft = (-60, -60)
    restart_button_rect.topleft = (-60, -60)
           
    pygame.display.flip()

def won_scene(action):
    
    pygame.draw.rect(screen, BERGENDY, [850, 80, 330, 120], 0)
    font = pygame.font.SysFont("arialblack", 35)
    
    exit_button_rect.center = (915,160)
    screen.blit(exit_button_text, exit_button_rect)
    restart_button_rect.center = (1070,160)
    screen.blit(restart_button_text, restart_button_rect)
    update_button_colors()
    
    if action == won:
        text2 = font.render("YOU WON !!!", True, YELLOW)  # Render the text onto a surface
        screen.blit(text2, (900, 90))
    elif action == lost:
        text2 = font.render("YOU LOST !!!", True, YELLOW)  # Render the text onto a surface
        screen.blit(text2, (900, 90))

def update_button_colors():
    if selected_button_index == 0:
        play_button_text_color = WHITE
        exit_button_text_color = YELLOW
        restart_button_text_color = YELLOW
    elif selected_button_index == 1:
        play_button_text_color = YELLOW
        exit_button_text_color = WHITE
        restart_button_text_color = YELLOW
    elif selected_button_index == 2:
        play_button_text_color = YELLOW
        exit_button_text_color = YELLOW
        restart_button_text_color = WHITE
 
    screen.blit(button_font.render("Play", True, play_button_text_color), play_button_rect)
    screen.blit(button_font.render("Exit", True, exit_button_text_color), exit_button_rect) 
    screen.blit(button_font.render("Restart", True, restart_button_text_color), restart_button_rect) 
    
def update_footprints(footprints, player_rect, current_direction):
    delay = 40  # Adjust the delay as needed (in milliseconds)
    if not footprints or pygame.time.get_ticks() - footprints[-1][2] > delay:
        # Calculate distance between current player position and last footprint position
        if not footprints:
            distance_to_last_footprint = float('inf')  # Set distance to infinity if footprints is empty
        else:
            distance_to_last_footprint = math.sqrt((player_rect.x - footprints[-1][0])**2 + (player_rect.y - footprints[-1][1])**2)
        # Define threshold for footprint spacing
        footprint_distance = 50  # Adjust as needed
        if distance_to_last_footprint >= footprint_distance:
            footprints.append((player_rect.x, player_rect.y, pygame.time.get_ticks(), current_direction))  # Store the timestamp and direction

def draw_footprints(footprints):
    for footprint in footprints:
        direction = footprint[3]  # Get direction from footprints list
        image_index = {"front": 0, "back": 1, "left": 2, "right": 3}[direction]  # Map direction to index
        screen.blit(footprints_images[image_index], (footprint[0], footprint[1]))  # Draw footprint with appropriate image

# Define a function to reveal mummies
def reveal_mummies():
    # Create more mummy sprites
    mummy_2 = Block(mummy_images, mummy_width, mummy_height, 230, my_coord, mx_speed)
    mummy_3 = Block(mummy_images, mummy_width, mummy_height, mx_coord, my_coord, mx_speed)

    # Add all mummy sprites to the sprite group
    sprites_list.add(mummy_2)
    block_list.add(mummy_2)
    sprites_list.add(mummy_3)
    block_list.add(mummy_3)

    # Set index and update image after adding to sprite lists
    mummy_2.index = 0
    mummy_2.update(choice_path)
    mummy_2.update_image()
    mummy_3.index = 0
    mummy_3.update(choice_path)
    mummy_3.update_image()

    return mummy_2, mummy_3

# Function to calculate distance between the player and each rectangular
def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Function to calculate angle between the player and each rectangular
def angle(x1, y1, x2, y2):
    return math.atan2(y2 - y1, x2 - x1)
         
def instructions():
    # Render and display the messages
    font1 = pygame.font.SysFont("arial", 25)

    # Draw the message box
    message_box_rect = pygame.Rect(1400, 250, 410, 380)
    pygame.draw.rect(screen, BROWN, message_box_rect)  # Brown message box background

    # Define the lines of text
    lines = [
        "Use your keyboard arrows to change",
        "the position of your player.",
        "Circle the rooms to unlock their contents.",
        "Find the key to win.",
        " ",
        "But be careful,",
        "because you are not alone in the pyramid...",
        "Try to avoid the mummy.",
        "You have three lives!",
        " ",
        "Have fun!",
    ]

    # Render and display each line of text inside the message box
    line_height = font1.get_height()
    x_position = message_box_rect.left + 10  # Adjust x-position to leave some padding
    y_position = message_box_rect.top + 10  # Adjust y-position to leave some padding

    for line in lines:
        message_line = font1.render(line, True, YELLOW)
        screen.blit(message_line, (x_position, y_position))
        y_position += line_height  # Move to the next line


    
#----------------------------- MAKE PLAYERS -------------------------------------
block_list = pygame.sprite.Group()  #to check for a colition
sprites_list = pygame.sprite.Group()    #for all sprites  

#MUMMY
mummy_images = [mummy1, mummy2, mummy3, mummy4]
mummy = Block(mummy_images, mummy_width, mummy_height, mx_coord, my_coord, mx_speed)
mummy.index = 3
sprites_list.add(mummy)
block_list.add(mummy)

# mummy_2 = None
# mummy_3 = None

# Create a path for the mummy to follow
path1 = [(405, 625), (405, 365), (635, 365), (635, 237), (865, 237), (865, 365), (1095, 365), (1095, 495), (1321, 495), (1321, 755), (1095, 755), (1095, 625), (865, 625), (865, 495), (635, 495), (635, 755), (180, 625)]
path2 = [(635,625), (635,495), (865, 495), (865, 365), (635,365), (635, 237), (1095, 237), (1095, 625), (1321, 625), (1321, 495), (865, 495), (865, 755), (180, 755), (180, 625)]
path3 = [(180, 495), (405, 495), (405, 237), (180, 237), (180, 365), (635, 365), (635, 237), (635, 495), (865, 495), (865, 625), (635, 625), (635, 495), (405, 495), (405, 755), (1095, 755), (1095, 625), (1321, 625), (1321,365), (1095, 365), (1095, 237), (865, 237), (865, 755), (180, 755), (180, 625)]

choice_path = random.choice([path1, path2, path3])

#PLAYER
footprints_images = [footprints_image1, footprints_image2, footprints_image3, footprints_image4]
player = Block(player_images, player_width, player_height, x_coord, y_coord, x_speed)
sprites_list.add(player)

#------------------------- SCORE -------------------------------------
score_x = 160
score_y = 130
high_score = 0
font = pygame.font.SysFont("arialblack", 40)
text = font.render(f"Hight score: {high_score}", True, YELLOW)  # Render the text into the screen

#------------------------- MAKE GRID 5*4 -------------------------------------
passed_rectangles = set()  # Set to store passed rectangles
# List to store rectangle positions
rectangles = []
image_to_place = [] # list so we can keep the choices and re-draw them inside the game loop

# grid of rectangles with spaces between them
for row in range(rows):
    for col in range(columns):

        x = col * (rectangle_width + space_between_rectangles) + 220
        y = row * (rectangle_height + space_between_rectangles) + 280
        rectangles.append(pygame.Rect(x, y, rectangle_width, rectangle_height))
        
key_choice = False

for rect in rectangles:
    # Randomly choose between empty and treasure
    if key_choice == False:
        choice = random.choice([empty, treasure, key, sarc])
        if choice == key:
            key_choice = True
    elif key_choice == True:
        choice = random.choice([empty, treasure, sarc])
    image_to_place.append(choice)

top = False
bottom = False
left = False
right = False
passed_rectangles = set()  # Set to store passed rectangles

# Initialize arrays for each side of the rectangles
left_passed = [False] * len(rectangles)
right_passed = [False] * len(rectangles)
top_passed = [False] * len(rectangles)
bottom_passed = [False] * len(rectangles)

won = False
lost = False
#------------------------ MAIN LOOP ------------------------------------------
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:  # Check for mouse events
            
            mouse_pos = pygame.mouse.get_pos()
            if play_button_rect.collidepoint(mouse_pos):
                play_button_pressed = True
                game_scene()
            elif exit_button_rect.collidepoint(mouse_pos):
                done = True
            elif compass_rect.collidepoint(mouse_pos):
                done = True
            elif restart_button_rect.collidepoint(mouse_pos):
                restart_game()
                
        elif event.type == pygame.KEYDOWN: #pressed key
            
            if event.key == pygame.K_LEFT:
                if lost == True or won == True:
                    x_speed = 0
                    y_speed = 0
                else:
                    x_speed = -3
                    y_speed = 0
                player.index = 2  # Left
                current_direction = "left"
                footprints_image = footprints_image3
                    
            elif event.key == pygame.K_RIGHT:
                if lost == True or won == True:
                    x_speed = 0
                    y_speed = 0
                else:
                    x_speed = 3
                    y_speed = 0
                player.index = 3  # Right
                current_direction = "right"
                footprints_image = footprints_image4
                    
            elif event.key == pygame.K_UP:
                if lost == True or won == True:
                    x_speed = 0
                    y_speed = 0
                else:
                    y_speed = -3
                    x_speed = 0
                player.index = 0  # Front
                current_direction = "front"
                footprints_image = footprints_image1
                    
            elif event.key == pygame.K_DOWN:
                if lost == True or won == True:
                    x_speed = 0
                    y_speed = 0
                else:
                    y_speed = 3
                    x_speed = 0
                player.index = 1  # Back
                current_direction = "back"
                footprints_image = footprints_image2
                    
            elif event.key == pygame.K_ESCAPE:
                done = True
               
        elif event.type == pygame.KEYUP: #released key
            
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                x_speed = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                y_speed = 0
                
    # Handle player movement
    x_coord += x_speed
    y_coord += y_speed
    keys = pygame.key.get_pressed()
    player.rect.x = x_coord
    player.rect.y = y_coord
    player.update_image()
           
#------------------------- PLACE SPRITES -------------------------------------
    # place the player inside the big rect and keep him here
    x_coord = max(180, min(x_coord, 180 + 1180 - player_width))
    y_coord = max(235, min(y_coord, 235 + 565 - player_height))
    
#------------------------- DRAW GRID -------------------------------------    
    # Clear the screen
    screen.fill(YELLOW)
    screen.blit(map_image, (0, 0))  
    screen.blit(compass, compass_rect)
    screen.blit(logo, logo_rect)
    
    instructions()

    if high_score == 0:
        screen.blit(text, (score_x, score_y))

    # big rectangle 
    pygame.draw.rect(screen, BROWN, [180, 237, 1185, 570], 0)

    # Check player position relative to rectangles and update passed arrays
    for i, rect in enumerate(rectangles):
        # Calculate angle between player and rectangle
        angle_to_rect = angle(x_coord + player_height / 2, y_coord + player_height / 2, rect.x + rectangle_width / 2, rect.y + rectangle_height / 2)
        angle_to_rect = (angle_to_rect + 2 * math.pi) % (2 * math.pi)

        # Check if player is close to this rectangle
        distance_to_rect = distance(x_coord + player_height / 2, y_coord + player_height / 2, rect.x + rectangle_width / 2, rect.y + rectangle_height / 2)
        if distance_to_rect < 100:
            # Determine which side of the rectangle the player has reached
            if 0 <= angle_to_rect < math.pi / 4 or 7 * math.pi / 4 <= angle_to_rect < 2 * math.pi:
                print("Left side")
                left_passed[i] = True
            elif math.pi / 4 <= angle_to_rect < 3 * math.pi / 4:
                print("Top side")
                top_passed[i] = True
            elif 3 * math.pi / 4 <= angle_to_rect < 5 * math.pi / 4:
                print("Right side")
                right_passed[i] = True
            else:
                print("Bottom side")
                bottom_passed[i] = True

        # Draw rectangles in black if not passed, else reveal the images
        if left_passed[i] and right_passed[i] and top_passed[i] and bottom_passed[i]:
            screen.blit(image_to_place[i], rect)
            
            if i not in passed_rectangles:
                passed_rectangles.add(i)
                
                if image_to_place[i] == treasure: # increase
                    high_score = high_score + 500
                elif image_to_place[i] == sarc: # dicrease 
                    # mummy_2 = reveal_mummies()
                    
                    if high_score > 0:
                        high_score = high_score - 100
                    else: continue
                
            if image_to_place[i] == key:  # bonus
                high_score = high_score + 1000
                won = True

        else:
            screen.blit(black, rect)
            
    if won == False:
        text = font.render(f"Score: {high_score}", True, YELLOW)
        screen.blit(text, (score_x, score_y))
    
    player_rect = pygame.Rect(x_coord, y_coord, player_width, player_height)
    
    # Update footprints
    current_direction = "front" 

    if keys[pygame.K_UP]:
        current_direction = "front"
    elif keys[pygame.K_DOWN]:
        current_direction = "back"
    elif keys[pygame.K_LEFT]:
        current_direction = "left"
    elif keys[pygame.K_RIGHT]:
        current_direction = "right"
# If none of the arrow keys are pressed, keep the current direction unchanged

    update_footprints(footprints, player_rect, current_direction)

    # Draw footprints
    draw_footprints(footprints)
       
#------------------------- DETECT COLLISION WITH MUMMY -------------------------------------
    sprites_list.draw(screen)
    block_list_hit = pygame.sprite.spritecollide(player, block_list, False)
    
#------------------------- DAMAGE -------------------------------------
    for life in range(current_lives):
        heart_x = screen_width - 200 - life * 60
        heart_y = 70
        # we use blit for drawing images and draw for shapes directly
        screen.blit(heart_image, (heart_x, heart_y))
        
    for hit in block_list_hit:
        if pygame.time.get_ticks() - last_life_gain_time >= life_gain_delay:
            current_lives -= 1
            last_life_gain_time = pygame.time.get_ticks()  # Update last life gain time
            
    if current_lives == 0:
        lost = True
       
#------------------------- DETECT COLLISION WITH RECTANGLES -------------------------------------

    for rect in rectangles:
        if player_rect.colliderect(rect): # checking the player
            if x_speed > 0:  # moving right
                x_coord = min(x_coord, rect.left - player_width)
            elif x_speed < 0:  # moving left
                x_coord = max(x_coord, rect.right)
            elif y_speed > 0:  # moving down
                y_coord = min(y_coord, rect.top - player_height)
            elif y_speed < 0:  # moving up
                y_coord = max(y_coord, rect.bottom)
                           
    # Draw player based on direction
    if current_direction == "front":
        screen.blit(player.image, (player.rect.x, player.rect.y))  # Front
    elif current_direction == "left":
        screen.blit(player.image, (player.rect.x, player.rect.y))  # Left
    elif current_direction == "right":
        screen.blit(player.image, (player.rect.x, player.rect.y))  # Right
    elif current_direction == "back":
        screen.blit(player.image, (player.rect.x, player.rect.y))  # Back

#------------------------- MUMMY MOVEMENT -------------------------------------
   
    mummy.update_image()
    mummy.update(choice_path)
    
    # Update mummies
    # if mummy_2 is not None:
    #     mummy_2.update(choice_path)
    #     mummy_2.update_image()
    # if mummy_3 is not None:
    #     mummy_3.update(choice_path)
    #     mummy_3.update_image()

#------------------------- END -------------------------------------
    if not play_button_pressed:
        main_menu()
    mouse_pos = pygame.mouse.get_pos()
    
    if play_button_rect.collidepoint(mouse_pos):
        selected_button_index = 0
    elif exit_button_rect.collidepoint(mouse_pos):
        selected_button_index = 1
    elif restart_button_rect.collidepoint(mouse_pos):
        selected_button_index = 2
        
    if won == True:
        mx_speed = 0
        my_speed = 0
        won_scene(won)
    elif lost == True:
        mx_speed = 0
        my_speed = 0
        won_scene(lost)

    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()
sys.exit()