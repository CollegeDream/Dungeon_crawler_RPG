import pygame
# Import the code from the other files
from sprites import *
from config import *
from rooms import *
import sys #import system

# This helps the files open correctly regardless of where the file is ran from
import os
absolute_path = os.path.dirname(__file__)
relative_path1 = "Assets/character.png"
relative_path2 = "Assets/terrain_atlas 2x.png"
relative_path3 = "Assets/intro_screen.png"
relative_path4 = "Assets/dungeoncrawlerfont.ttf"
relative_path5 = "Assets/MenuButtons.png"
relative_path6 = "Assets/enemy.png"
relative_path7 = "Assets/gameover.png"
relative_path8 = "Assets/blade_attack 2x.png"

''' GAME OBJECT '''
class Game:
    def __init__(self):
        # Function that Initializes pygame (must run whenever you make a pygame program)
        pygame.init()
        # Create our screen
        self.window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT)) # WIN_WIDTH & WIN_HEIGHT in config.py!
        self.clock = pygame.time.Clock() # Initialize the FPS of the game
        self.running = True
        self.font = pygame.font.Font(os.path.join(absolute_path, relative_path4), 175) # font name, size
        # Should a new room be made?
        self.genRoom = False
        # biome identifier
        self.biome = [0]
        self.biomeScaler = [0]
        # Load in spritesheets
        self.character_spritesheet = Spritesheet(os.path.join(absolute_path, relative_path1))
        self.enemy_spritesheet = Spritesheet(os.path.join(absolute_path, relative_path6))
        self.terrain_spritesheet = Spritesheet(os.path.join(absolute_path, relative_path2))
        self.attack_spritesheet = Spritesheet(os.path.join(absolute_path, relative_path8))
        self.menubutton_spritesheet = pygame.image.load(os.path.join(absolute_path, relative_path5))
        self.intro_background = pygame.image.load(os.path.join(absolute_path, relative_path3))
        self.gameover_background = pygame.image.load(os.path.join(absolute_path, relative_path7))


    # Function to create a player object and sprite for the game and set it to spawnpoint
    def newPlayer(self, posX, posY):
        self.player = Player(self, posY, posX)

    # Function to generate all biomes for the game
    def createBiomes(self):
        # Assign All Room Biomes
        while len(self.biome) < 9:
            biomenum = random.randrange(1,9)
            if biomenum not in self.biome:
                self.biome.append(biomenum)

    def genNewRoom(self):
        # store the new room according to the player
        newRoom = self.player.room
        print("Generating room "+str(self.player.room)+"...")

        # Destroy the current room
        for sprite in self.all_sprites:
            if sprite != self.player:
                sprite.kill()

        # Set make new room back to false
        self.genRoom = False

        # Construct the new room, b_room is fetched from the biome assigned to each room
        # Generate Room by its number
        createRoom(self, ROOM_TILEMAP[newRoom], self.biome[newRoom])
        
        self.player.CurrentRoomTiles = sqlGetInteractableTiles(self.player.room)

        # Update sprites to recenter with characters
        rectx = self.player.rect.x/TILESIZE
        recty = self.player.rect.y/TILESIZE
        self.player.rect.x = self.player.tileX*TILESIZE
        self.player.rect.y = self.player.tileY*TILESIZE
                        
        if self.player.tileX > rectx:
            for sprite in self.all_sprites:
                #if sprite != self.player:
                sprite.rect.x -= (self.player.tileX - rectx)*TILESIZE

        if self.player.tileX < rectx:
            for sprite in self.all_sprites:
                sprite.rect.x += (rectx - self.player.tileX)*TILESIZE
        
        if self.player.tileY > recty:
            for sprite in self.all_sprites:
                sprite.rect.y -= (self.player.tileY - recty)*TILESIZE

        if self.player.tileY < recty:
            for sprite in self.all_sprites:
                sprite.rect.y += (recty - self.player.tileY)*TILESIZE

    # Function to start a new game
    def startup(self):
        # a new game starts after this line is called
        self.biome.clear()
        self.biome.append(0)
        self.biomeScaler.clear()
        self.biomeScaler.append(0)
        self.createBiomes() # Generate new biomes once the game starts
        sqlDatabaseReset(self.biome, self.biomeScaler) # refresh/reset necessary database value
        self.playing = True
        # Start setting up sprite groups, or rather groups of sprites we can control
        # This function call will be what contains all of our sprites, character, and other information like that.
        self.all_sprites = pygame.sprite.LayeredUpdates() # ALL Sprites
        self.path = pygame.sprite.LayeredUpdates() # Path Sprites
        self.deco = pygame.sprite.LayeredUpdates() # Decoration / Detail sprites
        self.interactable = pygame.sprite.LayeredUpdates() # Interactables
        self.enemies = pygame.sprite.LayeredUpdates() # Enemy Sprite
        self.attacks = pygame.sprite.LayeredUpdates() # Attack Animation
        # Create Tilemap
        createRoom(self, ROOM_TILEMAP[0], self.biome[0]) # 0 == Spawn

    # Performs corrections for tile locations on the screen
    def startupCorrect(self):
        for sprite in self.all_sprites:
            sprite.rect.x -= 2*TILESIZE
            sprite.rect.y -= 6*TILESIZE

    # detect and react to keyboard presses
    def events(self):
        # game loop events
        # for loop to get every single event that happens in pygame
        for event in pygame.event.get():
            # If the event type is quit, stop the game
            if event.type == pygame.QUIT:
                self.player = False
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.player.facing == 'up':
                        #print(str(self.player.rect.x),str(self.player.rect.y))
                        Attack(self, (self.player.rect.x)/TILESIZE, (self.player.rect.y - TILESIZE)/TILESIZE)
                    if self.player.facing == 'down':
                        #print(str(self.player.rect.x),str(self.player.rect.y))
                        Attack(self, (self.player.rect.x)/TILESIZE, (self.player.rect.y + TILESIZE)/TILESIZE)
                    if self.player.facing == 'left':
                        #print(str(self.player.rect.x),str(self.player.rect.y))
                        Attack(self, (self.player.rect.x - TILESIZE)/TILESIZE, (self.player.rect.y)/TILESIZE)
                    if self.player.facing == 'right':
                        #print(str(self.player.rect.x),str(self.player.rect.y))
                        Attack(self, (self.player.rect.x + TILESIZE)/TILESIZE, (self.player.rect.y)/TILESIZE)

    # make sure our image does not stay static. Update player & creature movement, and interaction updates
    def update(self):
        # This will update the player sprites update function
        if(self.genRoom == True):  
            self.genNewRoom()
        # Update the display for all sprites
        self.all_sprites.update()

        # update hud
        self.hudPlayerHP = self.hudPlayerHPFont.render('Health: '+str(self.player.health), True, WHITE)
        self.hudPlayerHP_rect = self.hudPlayerHP.get_rect(x=10, y=0)
        self.hudPlayerFood = self.hudPlayerFoodFont.render('Food: '+str(self.player.food), True, WHITE)
        self.hudPlayerFood_rect = self.hudPlayerFood.get_rect(x=10, y=50)
        self.hudPlayerExp = self.hudPlayerExpFont.render('Exp: '+str(self.player.experience), True, WHITE)
        self.hudPlayerExp_rect = self.hudPlayerExp.get_rect(x=10, y=100)

    # displays all the sprites to our screen
    def draw(self):
        # game loop sprite displays
        # fill the screen with black
        self.window.fill(BLACK)
        self.all_sprites.draw(self.window)
        self.clock.tick(FPS) # set FPS
        
        self.window.blit(self.hudPlayerHP, self.hudPlayerHP_rect) # blit title
        self.window.blit(self.hudPlayerFood, self.hudPlayerFood_rect) # blit title
        self.window.blit(self.hudPlayerExp, self.hudPlayerExp_rect) # blit title
        pygame.display.update() # update the screen

    # What will run constantly while the game is going
    def main(self):
        # in-game music
        pygame.mixer.music.load('Blinch - Lich Is Unbreakable (Loop Hero OST).mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        
        # basic player HUD
        self.hudPlayerHPFont = pygame.font.Font('PythonGameMap/Assets/dungeoncrawlerfont.ttf', 48)
        self.hudPlayerFoodFont = pygame.font.Font('PythonGameMap/Assets/dungeoncrawlerfont.ttf', 48)
        self.hudPlayerExpFont = pygame.font.Font('PythonGameMap/Assets/dungeoncrawlerfont.ttf', 48)
        
        # game loop
        '''
        invSelOut = invSelOutFont.render((str(fetchedInv[i][0])+' is Used in Crafting'), True, WHITE)
        invSelOut_rect = invSelOut.get_rect(x=1250, y=0)
        self.game.window.blit(invSelOut, invSelOut_rect) # blit title'''
        print(self.biome)
        print(self.biomeScaler)

        while self.playing:
            self.events() # contain keypresses
            self.update() # make sure its not just a static image


            self.draw() # display all the sprites to our screen

    def intro_screen(self):
        intro = True
        title = self.font.render('Dungeon Crawler', True, WHITE)
        title_rect = title.get_rect(x=200, y=250)
        play_button  = Button(500, 700, 1080, 685, 900, 185, WHITE, 'PLAY GAME', 100)
        # menu music - play once and chill
        pygame.mixer.music.load('Blinch - Last Sabbath (Loop Hero OST).mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(1)
        # because no event loop is running yet, we must make our own for intro screen
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False
                if pygame.key.get_pressed()[pygame.K_DOWN]:
                    intro = False
                    self.running = False
            # get the pos of the mouse
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            # start game if button clicked
            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False
            # display screen
            self.window.blit(self.intro_background, (0,0)) # blit background
            self.window.blit(title, title_rect) # blit title
            self.window.blit(play_button.image, play_button.rect) # blit button
            self.clock.tick(FPS)
            pygame.display.update()
        pygame.mixer.music.fadeout(1000)   # exiting menu - stop menu music

    def game_over(self):
        # gameover has been triggered, display the gameover to the screen
        restart_button = Button(500, 700, 2950, 685, 900, 185, WHITE, 'TRY AGAIN', 100)
        # because no event loop is running yet, we must make our own for intro screen

        pygame.mixer.music.fadeout(500)   # stop normal game music
        pygame.mixer.music.load('Blinch - Last Sabbath (Loop Hero OST).mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(1)

        for sprite in self.all_sprites:
            sprite.kill() # kill all sprites, including the player

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if pygame.key.get_pressed()[pygame.K_DOWN]:
                    self.running = False
            # get the pos of the mouse
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            # start game if button clicked
            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                pygame.mixer.music.fadeout(1000)
                g.startup()
                g.newPlayer(14, 16)
                g.startupCorrect()
                break
            # display screen
            self.window.blit(self.gameover_background, (0,0)) # blit background
            self.window.blit(restart_button.image, restart_button.rect) # blit button
            self.clock.tick(FPS)
            pygame.display.update()

''' MAIN CODE'''
# Create a game object
g = Game() 
# Run the intro screen
g.intro_screen()
# Initiate the start of the game
g.startup()
g.newPlayer(14, 16)
g.startupCorrect()
# While we are playing the game:
while g.running:
    g.main() # function for the game loop events, updates, & drawing.
    g.game_over() # check for game_over
# Once the game is set to QUIT,
pygame.quit() # Quit the game
sys.exit() # Quit the python program