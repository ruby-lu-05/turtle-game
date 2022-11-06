# game name: the hungry turtle
# game objective: move around the screen and collect food to feed a baby turtle
# only certain foods are edible (player will be shown which ones are/aren't edible)
# there are enemies moving across the screen that can kill the player
# game win: the player fed the turtle all 4 of the edible foods
# game loss: the player died from an enemy or fed the baby turtle an inedible food

import pygame,os,random                   
pygame.init()
WIN_X = 800  # screen x coordinate
WIN_Y = 600  # screen y coordinate
WIN = pygame.display.set_mode((WIN_X,WIN_Y))
pygame.display.set_caption('The Hungry Turtle')

# colour palette
WHITE = (255,255,255)
LIGHT_GRAY = (230,231,232)
DARK_GRAY = (147,149,152)
GREEN = (0,104,56)
RED = (190,30,45)

class Food():  # class for all food objects
    def __init__(self,name,file_name,x,y,obtained,fed):  # constructing different foods
        self.name = name
        self.file_name = file_name
        self.x = x
        self.y = y
        self.obtained = obtained
        self.fed = fed
        self.food = pygame.image.load(os.getcwd() + "\\" + self.file_name)
    def draw_still(self):            # draws the food on screen based on given coordinates
        if self.obtained == False and self.fed == False:
            WIN.blit(self.food,(self.x,self.y))
    def collide_box(self):           # creates a box around the food
        return pygame.Rect(self.x,self.y,self.food.get_width(),self.food.get_height())
    def relocate(self,new_x,new_y):  # redraws food on top of the player when obtained
        self.new_x = new_x
        self.new_y = new_y
        if self.obtained == True:
            WIN.blit(self.food,(self.new_x,self.new_y))
    def draw_foodscreen(self,y):     # draws food with a label beside it (for food screen)
        WIN.blit(self.food,(450,y))
        label_font = pygame.font.SysFont("ubuntu mono",25)
        label = label_font.render(self.name,1,WHITE)
        WIN.blit(label,(500,y+(self.food.get_width()-25)/2))

class Enemy():  # class for enemies
    # defining general details for enemies
    r = 10
    d = r*2
    vel = 1.5
    def __init__(self,x,y,right,up,part1):  # constructing specific enemies
        self.x = x
        self.y = y
        self.right = right
        self.up = up
        self.part1 = part1 # this variable is specifically used for enemies with rectangular animation
    def draw_enemy(self):  # drawing the enemy
        pygame.draw.circle(WIN,RED,(self.x,self.y),Enemy.r)
    def collide_box(self): # creating a box around the enemy
        return pygame.Rect(self.x-Enemy.r,self.y-Enemy.r,Enemy.d,Enemy.d)
    def horiz_animate(self,left_x,right_x):  # parameters for start and end coordinates
        # horizontal animation
        if self.right == True:
            self.x += Enemy.vel  # movement right
            if self.x >= right_x:
                self.right = False
        else:
            self.x -= Enemy.vel  # movement left
            if self.x <= left_x:
                self.right = True
    def vert_animate(self,up_y,down_y):
        # vertical animation
        if self.up == True:
            self.y -= Enemy.vel  # movement up
            if self.y < up_y:
                self.up = False
        else:
            self.y += Enemy.vel  # movement down
            if self.y > down_y:
                self.up = True
    def rect_animate(self,right_x,left_x,up_y,down_y):
        # animation in a rectangle
        if self.part1 == True:
            if self.right == True:
                self.x += Enemy.vel  # movement to the right
                if self.x >= right_x:
                    self.right = False
            else:
                self.y += Enemy.vel  # movement downwards
                if self.y >= down_y:
                    self.part1 = False
        else:
            if self.right == False:
                self.x -= Enemy.vel  # movement to the left
                if self.x <= left_x:
                    self.right = True
            else:
                self.y -= Enemy.vel  # movement upwards
                if self.y <= up_y:
                    self.right = True
                    self.part1 = True

def display_text(words,x,y,colour):
    # displays text in game with the same font style but different coordinates and colours
    font = pygame.font.SysFont("ubuntu mono",25)
    text = font.render(words,1,colour)
    WIN.blit(text,(x,y))

def centered_text(words,x,y,colour):
    # displays lines of text on the title screen
    font = pygame.font.SysFont("ubuntu mono",25)
    text = font.render(words,1,colour)
    # makes it easier to make text horizontally centered
    text_box = text.get_rect(center=(x,y))
    WIN.blit(text,(text_box))

def popup_text(text,x,y):  # draws the text inside the popup box
    font = pygame.font.SysFont("ubuntu mono",20)
    popup_text = font.render(text,1,WHITE)
    WIN.blit(popup_text,(x,y))

# defining title font style and rendering title
title_font = pygame.font.SysFont("shrikhand",45)
title = title_font.render("The Hungry Turtle",1,GREEN)

# loading player images with relative paths (one facing each direction)
player_right = pygame.image.load(os.getcwd() + "\\turtle_right.png")
player_left = pygame.image.load(os.getcwd() + "\\turtle_left.png")
player_up = pygame.image.load(os.getcwd() + "\\turtle_up.png")
player_down = pygame.image.load(os.getcwd() + "\\turtle_down.png")

# defining two white bars at the top and bottom of the screen
bar_height = WIN_Y/10
bar_y = WIN_Y - bar_height

# loading an image for the title screen
turtle_eating = pygame.image.load(os.getcwd() + "\\turtle_eating.png")
turtle_eating = pygame.transform.scale(turtle_eating,(225,150))

# details for the walls
wall_thick = 20
wall_length = 340
wall1_x = WIN_X/3 - wall_thick/2
wall1_y = WIN_Y - bar_height - wall_length
wall2_x = WIN_X*(2/3) - wall_thick/2
wall2_y = bar_height

# assigning background music
pygame.mixer.music.load(os.getcwd() + "\\background_music.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

# making sound effects for certain actions
pickup = pygame.mixer.Sound(os.getcwd() + "\\pickup.mp3")              # for picking up food
pickup.set_volume(0.4)
chomp = pygame.mixer.Sound(os.getcwd() + "\\chomp.mp3")                # for feeding the turtle
game_over_sound = pygame.mixer.Sound(os.getcwd() + "\\game_over.wav")  # for player loss
game_won = pygame.mixer.Sound(os.getcwd() + "\\game_won.wav")          # for player win

# boolean variables used to track the screen the user should be on
beginning_screen = True
titlescreen = True
instructions = False
instructions1 = True
food_screen = False
gameplay = False

#---------------------------------------------------------------------------------------------------------------#
# PART 1: TITLE SCREEN AND INSTRUCTIONS
#---------------------------------------------------------------------------------------------------------------#
# player will get to choose between instructions and starting gameplay

while beginning_screen == True and food_screen == False:  # loop for the screen
    pygame.time.delay(10)
    keys = pygame.key.get_pressed()

    # TITLE SCREEN
    # -----------------------------------------------------------------------------------------------------------
    # making a screen to welcome the player
    if titlescreen == True:
        WIN.fill(LIGHT_GRAY)
        pygame.time.delay(10)
        keys = pygame.key.get_pressed()
        title_box = title.get_rect(center=(WIN_X/2,WIN_Y/2-120))
        WIN.blit(title,(title_box))  # displaying title of game
        WIN.blit(turtle_eating,(WIN_X/2-112,WIN_Y/2-60))  # displaying image of turtle

        # making each line horizontally centered
        centered_text("WELCOME TO",WIN_X/2,WIN_Y/2-170,DARK_GRAY)
        centered_text("press SPACE for instructions",WIN_X/2,WIN_Y/2+135,DARK_GRAY)
        centered_text("press ENTER to start game",WIN_X/2,WIN_Y/2+160,DARK_GRAY)

        if keys[pygame.K_SPACE]:   # will take player to the instructions
            titlescreen = False
            instructions = True
        if keys[pygame.K_RETURN]:  # will take player directly to food screen
            titlescreen = False
            food_screen = True
            
    # INSTRUCTIONS (2 pages)
    # -----------------------------------------------------------------------------------------------------------
    if instructions == True:
        WIN.fill(GREEN)
        pygame.time.delay(10)
        keys = pygame.key.get_pressed()
        instructions_title = title_font.render("Instructions",1,LIGHT_GRAY)
        instructions_box = instructions_title.get_rect(center = (WIN_X/2,WIN_Y/5))
        WIN.blit(instructions_title,(instructions_box))  # displaying header
        if instructions1 == True:  # first page of instructions
            display_text("You are a turtle, and your objective is to feed your",50,WIN_Y/5+50,WHITE)
            display_text("baby turtle. Use the ARROW KEYS to move across the",50,WIN_Y/5+80,WHITE)
            display_text("screen. When you are within reach, press SPACE to pick",50,WIN_Y/5+110,WHITE)
            display_text("up the food. Make your way back to your baby turtle",50,WIN_Y/5+140,WHITE)
            display_text("and press F to feed it. You may only hold one object",50,WIN_Y/5+170,WHITE)
            display_text("at a time. There will also be enemies (red circles)",50,WIN_Y/5+200,WHITE)
            display_text("moving around the screen. Make sure to avoid them!",50,WIN_Y/5+230,WHITE)
            display_text("Coming into contact with one will kill you.",50,WIN_Y/5+260,WHITE)
            if right_pressed == True:
                instructions1 = False   # allowing users to go to the next screen
            elif left_pressed == True:
                instructions = False    # allowing users to go to back to title screen
                titlescreen = True
        else:  # second page of instructions
            display_text("Your baby turtle happens to have severe allergies",50,WIN_Y/5+50,WHITE)
            display_text("and can only eat 4/8 of the foods available. You",50,WIN_Y/5+80,WHITE)
            display_text("will be shown which foods it can or cannot eat.",50,WIN_Y/5+110,WHITE)
            display_text("Be sure to only feed your turtle the foods that",50,WIN_Y/5+140,WHITE)
            display_text("it can eat! You win when you have fed your turtle",50,WIN_Y/5+170,WHITE)
            display_text("all 4 of the foods it can eat. You lose if you",50,WIN_Y/5+200,WHITE)
            display_text("come into contact with an enemy or feed your",50,WIN_Y/5+230,WHITE)
            display_text("turtle a food that it cannot eat.",50,WIN_Y/5+260,WHITE)
            if left_pressed == True:
                instructions1 = True   # allowing user to go to the previous page
            elif right_pressed == True:
                instructions = False
                beginning_screen = False
                food_screen = True     # allowing users to go to the food screen
        display_text("press RIGHT to continue, LEFT to go back",50,WIN_Y/5+325,WHITE)

        player_up = pygame.transform.scale(player_up,(125,125))
        WIN.blit(player_up,(WIN_X*(4/5)-20,WIN_Y*(2/3)))  # displaying an image of a turtle

    # changing keyboard press variables back to false
    right_pressed = False
    left_pressed = False
    
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:     # detecting keyboard input
            if event.key == pygame.K_RIGHT:  # checking which key was pressed
                right_pressed = True         # assigning keyboard press variable
            if event.key == pygame.K_LEFT:
                left_pressed = True
        if event.type == quit:
            pygame.quit()
            sys.exit

#---------------------------------------------------------------------------------------------------------------#
# PART 2: FOOD SCREEN
#---------------------------------------------------------------------------------------------------------------#
# this section informs the user which foods can and cannot be eaten

# creating a list of the foods and initializing food objects
food_list = [Food("AVOCADO","avocado.png",0,bar_height,False,False),
             Food("PINE CONE","pine_cone.png",wall2_x-30,bar_height,False,False),
             Food("PINEAPPLE","pineapple.png",wall1_x-40,WIN_Y*(2/3),False,False),
             Food("DONUT","donut.png",WIN_X/2-15,WIN_Y/2-15,False,False),
             Food("ROCK","rock.png",wall1_x+wall_thick+10,WIN_Y-bar_height-40,False,False),
             Food("GUMMY BEAR","gummy_bear.png",wall2_x,WIN_Y-bar_height-40,False,False),
             Food("FLOWER","flower.png",wall2_x+wall_thick,bar_height,False,False),
             Food("CANDY CANE","candy_cane.png",WIN_X-40,WIN_Y*(2/3)-15,False,False)]

# choosing a random 4 items to be the edible items and making edible/inedible lists
# will be different each game
random.shuffle(food_list)
edible_list = food_list[:4]
inedible_list = food_list[4:]

while food_screen == True:  # loop for the food screen
    WIN.fill(RED)
    pygame.time.delay(10)
    
    pygame.draw.rect(WIN,GREEN,(0,0,WIN_X,WIN_Y/2))
    keys = pygame.key.get_pressed()
    space_pressed = False  # pre-defining a space pressed variable

    # large headings for edible and inedible foods
    can_eat = title_font.render("CAN eat:",1,WHITE)
    WIN.blit(can_eat,(100,WIN_Y/4-23))
    cant_eat = title_font.render("CAN'T eat:",1,WHITE)
    WIN.blit(cant_eat,(100,WIN_Y*(3/4)-23))
    centered_text("press SPACE to start the game when you are ready",WIN_X/2,WIN_Y/2,WHITE)

    # using foodscreen draw function to display edible foods with a label
    edible_list[0].draw_foodscreen(WIN_Y*(2/22))
    edible_list[1].draw_foodscreen(WIN_Y*(4/22))
    edible_list[2].draw_foodscreen(WIN_Y*(6/22))
    edible_list[3].draw_foodscreen(WIN_Y*(8/22))
    # displaying inedible foods (with labels) in a different group
    inedible_list[0].draw_foodscreen(WIN_Y*(13/22))
    inedible_list[1].draw_foodscreen(WIN_Y*(15/22))
    inedible_list[2].draw_foodscreen(WIN_Y*(17/22))
    inedible_list[3].draw_foodscreen(WIN_Y*(19/22))

    if keys[pygame.K_SPACE]:  # detecting keyboard input from user
        space_pressed = True  # updating space pressed variable
    if space_pressed == True:
        food_screen = False
        gameplay = True       # allowing user to start the game
        space_pressed = False

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == quit:
            pygame.quit()
            sys.exit

#---------------------------------------------------------------------------------------------------------------#
# PART 3: GAMEPLAY
#---------------------------------------------------------------------------------------------------------------#

# defining the dimensions of a rectangle that will pop up under a certain condition
popup_rect_length = 315
popup_rect_width = 200
popup_rect_x = WIN_X/2-popup_rect_length/2
popup_rect_y = WIN_Y/2-popup_rect_width/2
popup = False

# creating variables for various player details
player_direction = "right"  # this variable will update based on which arrow key is pressed
player_size = 70
player_x = 0
player_y = bar_y-player_size-50
player_vel = 3

# making the baby turtle
baby_turtle = pygame.image.load(os.getcwd() + "\\turtle_right.png")
baby_turtle = pygame.transform.scale(baby_turtle,(45,45))

# initializing the enemies
enemy1 = Enemy(Enemy.r,WIN_Y/2,True,False,False)
enemy2 = Enemy(WIN_X-Enemy.r,WIN_Y/2,False,False,False)
enemy3 = Enemy(wall1_x/2,bar_height+Enemy.r,False,False,False)
enemy4 = Enemy(wall2_x+wall_thick+wall1_x/2,bar_y-Enemy.r,False,True,False)
enemy5 = Enemy(WIN_X/2-90,WIN_Y/2-70,True,False,True)
enemy6 = Enemy(WIN_X/2+90,WIN_Y/2+70,False,False,False)
enemy_list = [enemy1,enemy2,enemy3,enemy4,enemy5,enemy6]  # list of enemies

# variables for the status of the player
holding_food = False
obtained_food = ""
space_count = 0
player_win = False
player_lose = False
player_die = False
baby_die = False
fed_edible = 0

while gameplay == True:  # loop for the game
    WIN.fill(LIGHT_GRAY)
    pygame.time.delay(10)
    keys = pygame.key.get_pressed()

    # drawing the white bars at the top and bottom
    pygame.draw.rect(WIN,WHITE,(0,0,WIN_X,bar_height))
    pygame.draw.rect(WIN,WHITE,(0,bar_y,WIN_X,bar_height))

    WIN.blit(title,(20,0))  # drawing the title
    display_text(str(4-fed_edible) + "/4 left",WIN_X*(5/6),20,GREEN)  # scoring system

    # making collide boxes for the walls and drawing them
    wall1 = pygame.Rect(wall1_x,wall1_y,wall_thick,wall_length)
    wall2 = pygame.Rect(wall2_x,wall2_y,wall_thick,wall_length)
    pygame.draw.rect(WIN,DARK_GRAY,(wall1))
    pygame.draw.rect(WIN,DARK_GRAY,(wall2))

    # displaying the baby turtle and making a collide box for it
    baby_box = pygame.Rect(0,WIN_Y-bar_height-45,45,45)
    WIN.blit(baby_turtle,(0,WIN_Y-bar_height-45))

    for i in food_list:
        i.draw_still()  # drawing each food from the list

    player_box = pygame.Rect(player_x,player_y,player_size,player_size)  # collide box for player

    # PLAYER MOVEMENT (WITH WALL COLLISIONS)
    # -----------------------------------------------------------------------------------------------------------
    if popup == False:
        # allowing for player movement
        if keys[pygame.K_LEFT]:         # movement left
            player_direction = "left"
            # making sure the player box and wall boxes don't touch
            if 0 < player_x and wall1.colliderect(player_box) == 0\
               and wall2.colliderect(player_box) == 0 and baby_box.colliderect(player_box) == 0:
                player_x -= player_vel
        elif keys[pygame.K_RIGHT]:      # movement right
            player_direction = "right"
            if player_x < WIN_X-70 and wall1.colliderect(player_box) == 0 and wall2.colliderect(player_box) == 0:
                player_x += player_vel
        elif keys[pygame.K_UP]:         # movement up
            player_direction = "up"
            if bar_height+2 < player_y and wall2.colliderect(player_box) == 0:
                player_y -= player_vel
        elif keys[pygame.K_DOWN]:       # movement down
            player_direction = "down"
            # making sure player can't run over their baby turtle as well
            if player_y < WIN_Y-bar_height-player_size and wall1.colliderect(player_box) == 0\
               and baby_box.colliderect(player_box) == 0:
                player_y += player_vel

    # making sure the player doesn't get stuck on a wall
    # slightly changing variables so that they can still move other directions when touching a wall
    if wall1.collidepoint(player_x+player_size,player_y) == 1:
        player_x = wall1_x-player_size-1
    elif wall1.collidepoint(player_x,player_y) == 1:
        player_x = wall1_x+wall_thick+1
    elif wall2.collidepoint(player_x+player_size,player_y) == 1:
        player_x = wall2_x-player_size-1
    elif wall2.collidepoint(player_x,player_y) == 1:
        player_x = wall2_x+wall_thick+1
    elif player_box.collidepoint(wall1_x,wall1_y) or\
         player_box.collidepoint(wall1_x+wall_thick,wall1_y):
        player_y = wall1_y-player_size
    elif player_box.collidepoint(wall2_x,wall2_y+wall_length) or\
         player_box.collidepoint(wall2_x+wall_thick,wall2_y+wall_length):
        player_y = wall2_y+wall_length+1

    # updating player direction variable based on input
    if player_direction == "right":
        player = player_right
    elif player_direction == "left":
        player = player_left
    elif player_direction == "up":
        player = player_up
    elif player_direction == "down":
        player = player_down
    player = pygame.transform.scale(player,(player_size,player_size))
    WIN.blit(player,(player_x,player_y))  # redrawing player

    # COLLECTING FOOD
    # -----------------------------------------------------------------------------------------------------------
    for i in food_list:       # iterating over the food list
        if keys[pygame.K_SPACE] and holding_food == False:
            space_count += 1
        if space_count >= 1 and player_box.colliderect(Food.collide_box(i)):
            holding_food = True
            i.obtained = True
            obtained_food = i # creating a variable for the food that was obtained
            pickup.play()     # sound effect for food pickup
        if i.obtained == True:
            # redrawing the food on top of the player (so it looks like it is on the turtle's back)
            Food.relocate(obtained_food,player_x+player_size/2-15,player_y+player_size/2-15)
            if player_box.colliderect(baby_box) and keys[pygame.K_f]:
                # allowing player to feed baby turtle
                food_list.remove(i)
                i.obtained = False
                i.fed = True
                if i in edible_list:
                    popup = True     # allowing a popup to pop up
                    chomp.play()     # sound effect for baby turtle eating
                    fed_edible += 1  # adding to the counter for edible foods fed
                else:
                    # updating booleans
                    player_lose = True
                    baby_die = True
                    gameplay = False
                    inedible_food = i       # making a variable for the inedible food
                    game_over_sound.play()  # playing the game over sound effect
                holding_food = False
                space_count = 0             # setting the space press counter back to 0

        if holding_food == False and player_box.colliderect(Food.collide_box(i)):
            # displaying specific in-game text
            centered_text("press SPACE if you want to pick up the " + i.name,WIN_X/2,580,GREEN)
        space_count = 0
    if holding_food == True:
        # notifying the player when they have obtained an object
        centered_text("you have obtained a " + obtained_food.name,WIN_X/2,555,GREEN)
        if player_box.colliderect(baby_box):
            # text to pop up when player is in range to feed their baby turtle
            centered_text("press F to feed your turtle",WIN_X/2,580,GREEN)
        else:
            centered_text("go back to your turtle to feed it!",WIN_X/2,580,GREEN)
    else:   # telling the player whether or not they have obtained anything
        centered_text("you have not picked anything up",WIN_X/2,555,GREEN)

    # ANIMATING ENEMIES
    # -----------------------------------------------------------------------------------------------------------
    for i in enemy_list:  # iterating over the enemy list to draw each enemy
        i.draw_enemy()
        
    if popup == False:
        # using various animation functions from the Enemy class
        enemy1.horiz_animate(Enemy.r,wall1_x-Enemy.r)
        enemy2.horiz_animate(wall2_x+wall_thick+Enemy.r,WIN_X-Enemy.r)
        enemy3.vert_animate(bar_height+Enemy.r,bar_y-Enemy.r)
        enemy4.vert_animate(bar_height+Enemy.r,bar_y-Enemy.r)
        enemy5.rect_animate(WIN_X/2+90,WIN_X/2-90,WIN_Y/2-70,WIN_Y/2+70)
        enemy6.rect_animate(WIN_X/2+90,WIN_X/2-90,WIN_Y/2-70,WIN_Y/2+70)
        
    # POPUP BOX
    # -----------------------------------------------------------------------------------------------------------
    else:
        # displaying the popup box
        pygame.draw.rect(WIN,GREEN,(popup_rect_x,popup_rect_y,popup_rect_length,popup_rect_width))
        yum = title_font.render("Yum!",1,LIGHT_GRAY)
        WIN.blit(yum,(WIN_X/2-75,WIN_Y/2-85))  # heading for popup box
        # using the popup text function to display multi-line text
        popup_text("You have just fed",WIN_X/2-115,WIN_Y/2-25)
        popup_text("your baby turtle a",WIN_X/2-115,WIN_Y/2-5)
        popup_text("delicious " + obtained_food.name,WIN_X/2-115,WIN_Y/2+15)
        popup_text("press SPACE to continue",WIN_X/2-115,WIN_Y/2+60)

        if keys[pygame.K_SPACE]: # detecting space presses
            popup = False        # allowing users to exit the box

    # CHECKING GAME STATUS
    # -----------------------------------------------------------------------------------------------------------
    for i in enemy_list:  # iterating over the enemy list to get the collide boxes
        if player_box.colliderect(i.collide_box()):  # checking if a player collided with any enemies
            player_lose = True
            player_die = True
            game_over_sound.play() # playing the game over sound effect

    if popup == False:
        if fed_edible == 4:    # checking if the player reached the required amount of food
            player_win = True
            game_won.play()    # playing the win sound effect

    if player_lose == True or player_win == True:
        gameplay = False   # updating gameplay/gameover variables
        gameover = True

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == quit:
            pygame.quit()
            sys.exit

#---------------------------------------------------------------------------------------------------------------#
# SECTION 4: GAME OVER
#---------------------------------------------------------------------------------------------------------------#
# specific screen based on whether they won or the way they lost

# defining new images for the game over screen and scaling them down
dead_turtle = pygame.image.load(os.getcwd() + "\\dead_turtle.png")
dead_baby = pygame.transform.scale(dead_turtle,(120,120))
dead_player = pygame.transform.scale(dead_turtle,(175,175))
happy_turtles = pygame.image.load(os.getcwd() + "\\happy_turtles.png")
happy_turtles = pygame.transform.scale(happy_turtles,(273,200))

while gameover == True:      # loop for the game over screen
    pygame.time.delay(10)
    pygame.mixer.music.stop()

    # PLAYER WIN
    # -----------------------------------------------------------------------------------------------------------
    if player_win == True:
        WIN.fill(GREEN)
        you_win = title_font.render("You Win",1,LIGHT_GRAY)
        you_win_rect = you_win.get_rect(center = (WIN_X/2,125))
        WIN.blit(you_win,(you_win_rect))  # displaying title and telling them they won
        display_text("Your baby turtle is no longer hungry.",120,180,WHITE)
        display_text("Congratulations!",120,210,WHITE)
        WIN.blit(happy_turtles,(WIN_X/2-136,300))  # displaying happy turtle image :)

    # PLAYER LOSE (2 possibilities)
    # -----------------------------------------------------------------------------------------------------------
    if player_lose == True:
        WIN.fill(RED)
        game_over = title_font.render("Game Over",1,LIGHT_GRAY)
        game_over_rect = game_over.get_rect(center = (WIN_X/2,125))
        WIN.blit(game_over,(game_over_rect)) # displaying title telling them they lost
        if baby_die == True: # checking if the player lost by killing their baby
            display_text("Your turtle can’t eat " + inedible_food.name + "S and has",90,180,WHITE)
            display_text("unfortunately died. Better luck next time!",90,210,WHITE)
            food_rect = inedible_food.food.get_rect(center=(WIN_X/2,WIN_Y/2))
            WIN.blit(inedible_food.food,food_rect)  # displaying the food that killed the baby
        else:                # checking if the player lost by dying
            display_text("You have come into contact with an enemy",90,180,WHITE)
            display_text("and died. With no one to feed it, your",90,210,WHITE)
            display_text("baby turtle died shortly afterwards.",90,240,WHITE)
            display_text("How unfortunate!",90,270,WHITE) 
            WIN.blit(dead_player,(500,300))  # displaying the dead player
        WIN.blit(dead_baby,(WIN_X/2-60,355)) # displaying the dead baby
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == quit:
            pygame.quit()
            sys.exit
