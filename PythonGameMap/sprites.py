'''
    This purpose of this file is to store the classes
    for our developed sprites
'''
import pygame
from config import *
from embeddedSQL import *
import math
import random

# Spritesheet class
class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()
    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width,height])
        sprite.blit(self.sheet, (0,0), (x,y,width,height))
        sprite.set_colorkey(BLACK)
        return sprite
    def get_tile(self, x, y):
        sprite = pygame.Surface([TILESIZE,TILESIZE])
        sprite.blit(self.sheet, (0,0), (x,y,TILESIZE,TILESIZE))
        sprite.set_colorkey(BLACK)
        return sprite

# Player Class
class Player(pygame.sprite.Sprite): #Makes it a lot easier to make sprites
    def __init__(self, game, x, y):
        self.health = 100
        self.food = 10
        self.experience = 0
        # update health, food, exp whenever entering new room [TO-DO LATER]

        self.key_timer = 0 # Key Timer
        self.collide_timer = 0
        # Define time since last action
        self.game = game
        # Telling pygame which layer we want the sprinte to appear in
        self._layer = PLAYER_LAYER # Defined in config.py!
        # adding the player to the all_sprites group
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        # Sets each movement to move the player by a set number of pixels
        self.room = 0 # Default Room
        self.tileX = x
        self.tileY = y
        self.width = TILESIZE # width of player
        self.height = TILESIZE # height of player
        # Player Movement
        self.x_change = 0
        self.y_change = 0

        self.CurrentRoomTiles = sqlGetInteractableTiles(self.room)
        # for animation
        self.facing = 'down'
        self.animation_loop = 1

        #referring to main.py
        self.image = self.game.character_spritesheet.get_sprite(0, 0, self.width, self.height) 
        self.rect = self.image.get_rect() # Ensure the size of the player & image are same
        self.rect.x = x *TILESIZE # The 'hitbox'
        self.rect.y = y *TILESIZE# The 'hitbox'

    # Function to update player
    def update(self):
        # Collision detector for Camera
        self.collided = False
        # determine movement
        self.movement()
        self.animate()
        self.collide_enemy()
        if self.key_timer > HOLD_DELAY:
            self.key_timer = 0 # reset timer
        if self.collide_timer > HOLD_DELAY*2.5:
            self.collide_timer = 0 # reset timer
        # set x shift & detect collision
        self.rect.x += self.x_change
        self.collision_detection('x')
        self.rect.y += self.y_change
        self.collision_detection('y')

        # Fix Camera Movement if colliding
        if(self.collided == False):
            if self.x_change>0:
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= TILESIZE
                self.tileX += 1
            if self.x_change<0:
                for sprite in self.game.all_sprites:
                    sprite.rect.x += TILESIZE
                self.tileX -= 1
            if self.y_change<0:
                for sprite in self.game.all_sprites:
                    sprite.rect.y += TILESIZE
                self.tileY -= 1
            if self.y_change>0:
                for sprite in self.game.all_sprites:
                    sprite.rect.y -= TILESIZE
                self.tileY += 1

        # Check for interactables.
        if(self.x_change != 0 or self.y_change != 0):
            # Use line below for debugging
            #print(str(self.room)+'||'+str(self.tileX)+'||'+str(self.tileY)+'||'+str(self.rect.x/TILESIZE)+'||'+str(self.rect.y/TILESIZE)+"||"+str(self.game.biome[self.room]))

            # Check the contents of the new tile if we have moved
            for i in range(len(self.CurrentRoomTiles)):
                tmplist=self.CurrentRoomTiles[i][:3]
                tmplist2=[self.room, int(self.tileX), int(self.tileY)]
                if(tmplist == tmplist2):
                    sqlCheckTileContents(self, self.CurrentRoomTiles[i])
                    
        # then reset movement updates
        self.x_change = 0
        self.y_change = 0

    # Function to update player movement
    def movement(self):
        # A list of every key pressed on your keyboard
        self.key_timer += 1
        keys = pygame.key.get_pressed()
        ### (2-4) If any of these keys if sqlCheck functions return true, then it is a walkable tile
        if keys[pygame.K_a] and self.key_timer > HOLD_DELAY: # LEFT for WASD
            #update all tiles
            self.x_change -= TILESIZE
            self.facing = 'left' # change player sprite to look left
            return
            #self.key_timer = 0 # reset timer
        if keys[pygame.K_d] and self.key_timer > HOLD_DELAY: # RIGHT for WASD\
            self.x_change += TILESIZE
            self.facing = 'right' # change player sprite to look right
            return
            #self.key_timer = 0 # reset timer
        if keys[pygame.K_w] and self.key_timer > HOLD_DELAY: # UP for WASD
            self.y_change -= TILESIZE
            self.facing = 'up' # change player sprite to look up
            return
            #self.key_timer = 0 # reset timer
        if keys[pygame.K_s] and self.key_timer > HOLD_DELAY: # DOWN for WASD
            self.y_change += TILESIZE
            self.facing = 'down' # change player sprite to look down
            return
            #self.key_timer = 0 # reset timer
        if keys[pygame.K_DOWN]:
            self.game.playing = False
            self.game.running = False # test for instant exit

        # DISPLAY INVENTORY PANEL
        if keys[pygame.K_e]:
            # Display inventory main
            invDisplay = pygame.Surface([750,1000])
            invDisplay.blit(pygame.image.load('PythonGameMap/Assets/MenuButtons.png').convert_alpha(), (0,0), (2000,0,750,1000))
            invDisplay.set_colorkey(BLACK)
            invDisplay_rect = invDisplay.get_rect(x=1150, y=40)
            # create a list to get the data from the inventory
            fetchedInv = [[]]
            fetchedInv = sqlCheckInventory()
            # create inventory slot interactable buttons
            buttonPosX = 1250 # inventory starting button x pos
            buttonPosY = 140 # inventory starting button y pos
            invSlots = [] # invetory button list
            for i in range(len(fetchedInv)):
                invSlots.append(Button(buttonPosX, buttonPosY, 0,0, 600,35, WHITE, (str(fetchedInv[i][0])+'[Uses:'+str(fetchedInv[i][1])+']'+'     ('+str(fetchedInv[i][2])+'['+str(fetchedInv[i][3])+'])'),24))
                buttonPosY += 40

            # inventory interaction
            invOpen = True
            invSelOutFont = pygame.font.Font('PythonGameMap/Assets/dungeoncrawlerfont.ttf', 24)
            invSelOut = invSelOutFont.render('', True, WHITE)
            flagClicked = False
            while invOpen:
                # check all events each frame
                for event in pygame.event.get():
                    # if its escape exit the inventory
                    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                        invOpen = False
                    if event.type == pygame.MOUSEBUTTONUP:
                        flagClicked = False
                # next, get the mouse position and detect for clicks
                mouse_pos = pygame.mouse.get_pos()
                mouse_pressed = pygame.mouse.get_pressed()
                # Blit the inventory background
                self.game.window.blit(invDisplay, invDisplay_rect)
                # Blit the inv slots                
                for i in range(len(fetchedInv)):
                    if i > 18:
                        break # break at more than 19 displayed items
                    self.game.window.blit(invSlots[i].image, invSlots[i].rect)
                    # if this button was pressed by the mouse
                
                for i in range(len(fetchedInv)):
                    if invSlots[i].is_pressed(mouse_pos, mouse_pressed):
                        
                        # do what it should based on the item type...
                        if (fetchedInv[i][2] == 'Material') and flagClicked == False:
                                invSelOut = invSelOutFont.render((str(fetchedInv[i][0])+' is Used in Crafting'), True, WHITE)
                                flagClicked = True
                        if (fetchedInv[i][2] == 'Food') and flagClicked == False:
                                invSelOut = invSelOutFont.render(('Restored '+str(fetchedInv[i][3])+' Food Points'), True, WHITE)
                                flagClicked = True
                        if (fetchedInv[i][2] == 'Health') and flagClicked == False:
                                invSelOut = invSelOutFont.render(('Restored '+str(fetchedInv[i][3])+' Health Points'), True, WHITE)
                                self.game.player.health += fetchedInv[i][3]
                                if self.game.player.health > 100:
                                    self.game.player.health = 100
                                flagClicked = True
                        if (fetchedInv[i][2] == 'Damage') and flagClicked == False:
                                invSelOut = invSelOutFont.render(('Switched Weapon to '+str(fetchedInv[i][0])+'['+str(fetchedInv[i][3])+' Dmg]'), True, WHITE)
                                flagClicked = True
                #print it
                invSelOut_rect = invSelOut.get_rect(x=1250, y=925)
                self.game.window.blit(invSelOut, invSelOut_rect) # blit title
                pygame.display.update()
            #sqlCheckInventory()
        
    def collision_detection(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.deco, False)
            if hits:
                if self.x_change > 0:
                    pass
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    pass
                    self.rect.x = hits[0].rect.right
                self.collided = True
        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.deco, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                self.collided = True
    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self,self.game.enemies, False)
        if hits:
            self.collide_timer += 1
            #print(self.collide_timer)
            if self.collide_timer > HOLD_DELAY*2.5:
                baseDamMult = random.randrange(3,7)
                hitMarkFont = pygame.font.Font('PythonGameMap/Assets/dungeoncrawlerfont.ttf', 72)
                hitMark = hitMarkFont.render('-'+str(baseDamMult), True, RED)
                hitMark_rect = hitMark.get_rect(x=880, y=440)
                self.game.window.blit(hitMark, hitMark_rect) # blit title
                self.health -= baseDamMult * self.game.biomeScaler[self.room]
                pygame.display.update()
                print(self.health)
        if self.health < 0:
            self.kill() # kill the player, show gameover
            self.game.playing = False

    def animate(self):
        down_animations = [self.game.character_spritesheet.get_sprite(6, 4, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(70, 4, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(134, 4, self.width, self.height)]

        up_animations = [self.game.character_spritesheet.get_sprite(6, 68, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(70, 68, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(134, 68, self.width, self.height)]

        left_animations = [self.game.character_spritesheet.get_sprite(6, 196, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(70, 196, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(134, 196, self.width, self.height)]

        right_animations = [self.game.character_spritesheet.get_sprite(6, 132, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(70, 132, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(134, 132, self.width, self.height)]

        if self.facing == "down" and self.key_timer > HOLD_DELAY:
            if self.y_change != 0:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
            else:
                self.image = self.game.character_spritesheet.get_sprite(6, 4, self.width, self.height)
        if self.facing == "up" and self.key_timer > HOLD_DELAY:
            if self.y_change != 0:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
            else:
                self.image = self.game.character_spritesheet.get_sprite(6, 68, self.width, self.height)

        if self.facing == "left" and self.key_timer > HOLD_DELAY:
            if self.x_change != 0:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
            else:
                self.image = self.game.character_spritesheet.get_sprite(6, 196, self.width, self.height)
        if self.facing == "right" and self.key_timer > HOLD_DELAY:
            if self.x_change != 0:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
            else:
                self.image = self.game.character_spritesheet.get_sprite(6, 132, self.width, self.height)
    
class Enemy(pygame.sprite.Sprite):
    def __init__(self,game,x,y, zLayer):
        self.key_timer = 0
        self.game = game
        self._layer = zLayer # Defined in config.py!
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.tileX = x
        self.tileY = y
        self.width = TILESIZE # width of player
        self.height = TILESIZE # height of player
        self.x_change = 0
        self.y_change = 0
        self.facing = random.choice(['left','right'])
        self.animation_loop = 1
        self.movement_loopx = 0
        self.movement_loopy = 0
        self.max_travelx = 2
        self.max_travely = 2
        self.image = self.game.enemy_spritesheet.get_sprite(6, 4, self.width, self.height)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = self.tileX * TILESIZE
        self.rect.y = self.tileY * TILESIZE
    def update(self):
        self.movement()
        self.animate()
        if self.key_timer > HOLD_DELAY:
            self.key_timer = 0 # reset timer
        self.rect.x += self.x_change
        self.rect.y += self.y_change
        self.x_change = 0
        self.y_change = 0

    def movement(self):
        self.key_timer += 1
        if self.facing == 'left' and self.key_timer > HOLD_DELAY:
            self.x_change -= TILESIZE/2
            self.movement_loopx -= 1
            if self.movement_loopx <= -self.max_travelx:
                self.facing = 'up'
        if self.facing == 'up' and self.key_timer > HOLD_DELAY:
            self.y_change -= TILESIZE/2
            self.movement_loopy -= 1
            if self.movement_loopy <= -self.max_travely:
                self.facing = 'right'
        if self.facing == 'right' and self.key_timer > HOLD_DELAY:
            self.x_change += TILESIZE/2
            self.movement_loopx += 1
            if self.movement_loopx >= self.max_travelx:
                self.facing = 'down'
        if self.facing == 'down' and self.key_timer > HOLD_DELAY:
            self.y_change += TILESIZE/2
            self.movement_loopy += 1
            if self.movement_loopy >= self.max_travely:
                self.facing = 'left'

    def animate(self):
        down_animations = [self.game.enemy_spritesheet.get_sprite(6, 4, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(70, 4, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(134, 4, self.width, self.height)]

        up_animations = [self.game.enemy_spritesheet.get_sprite(6, 68, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(70, 68, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(134, 68, self.width, self.height)]

        left_animations = [self.game.enemy_spritesheet.get_sprite(6, 196, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(70, 196, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(134, 196, self.width, self.height)]

        right_animations = [self.game.enemy_spritesheet.get_sprite(6, 132, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(70, 132, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(134, 132, self.width, self.height)]

        if self.facing == "down" and self.key_timer > HOLD_DELAY:
            if self.y_change != 0:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
            else:
                self.image = self.game.enemy_spritesheet.get_sprite(6, 4, self.width, self.height)
        if self.facing == "up" and self.key_timer > HOLD_DELAY:
            if self.y_change != 0:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
            else:
                self.image = self.game.enemy_spritesheet.get_sprite(6, 68, self.width, self.height)

        if self.facing == "left" and self.key_timer > HOLD_DELAY:
            if self.x_change != 0:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
            else:
                self.image = self.game.enemy_spritesheet.get_sprite(6, 196, self.width, self.height)
        if self.facing == "right" and self.key_timer > HOLD_DELAY:
            if self.x_change != 0:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
            else:
                self.image = self.game.enemy_spritesheet.get_sprite(6, 132, self.width, self.height)

# Attack Class
class Attack(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.x=x
        self.y=y
        self.width=TILESIZE
        self.height=TILESIZE
        self.animation_loop=1
        self.image = self.game.attack_spritesheet.get_sprite(0,0,self.width,self.height)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
        # THE ERROR IS FROM THE PLAYER.RECT ASSIGNMENT!
    def update(self):
        self.animate()
        self.collide()
    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, True)
        if hits:
            self.game.player.experience += 100
    def animate(self):
        direction = self.game.player.facing
        up_animations   =  [self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 0, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 0, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(192, 0, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(256, 0, self.width, self.height)]

        down_animations = [self.game.attack_spritesheet.get_sprite(0, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(192, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(256, 64, self.width, self.height)]

        right_animations = [self.game.attack_spritesheet.get_sprite(0, 128, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 128, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 128, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(192, 128, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(256, 128, self.width, self.height)]

        left_animations = [self.game.attack_spritesheet.get_sprite(0, 192, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 192, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 192, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(192, 192, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(256, 192, self.width, self.height)]

        if direction == 'up':
            #print(str(self.animation_loop))
            self.image = up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()
        if direction == 'down':
            #print(str(self.animation_loop))
            self.image = down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()
        if direction == 'left':
            #print(str(self.animation_loop))
            self.image = left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5    :
                self.kill()
        if direction == 'right':
            #print(str(self.animation_loop))
            self.image = right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()


# Decoration Tiles (unwalkable tiles) Class
class DecoTile(pygame.sprite.Sprite):
    def __init__(self,game, x, y, tile, zLayer):
        self.game = game # declare it part of the game
        self._layer = zLayer # Assign the Z-layer
        self.groups = self.game.all_sprites, self.game.deco # sprite groups it's assigned to
        pygame.sprite.Sprite.__init__(self, self.groups)
        # If confused on this, refer to players similar assignment comments
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE 
        self.image = self.game.terrain_spritesheet.get_sprite(tile[0], tile[1], self.width, self.height) 
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    
# Path Tiles (Walkables)
class PathTile(pygame.sprite.Sprite): # [ Walkable ]
    def __init__(self,game, x, y, tile, zLayer):
        self.game = game # declare it part of the game
        self._layer = zLayer # Assign the Z-layer
        self.groups = self.game.all_sprites, self.game.path # sprite groups it's assigned to
        pygame.sprite.Sprite.__init__(self, self.groups)
        # If confused on this, refer to players similar assignment comments
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE 
        self.image = self.game.terrain_spritesheet.get_sprite(tile[0], tile[1], self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

# Loot / Material / Door  --> Tile Class 
class InteractableTile(pygame.sprite.Sprite): # [ Walkable ]
    def __init__(self,game, x, y, tile, zLayer):
        self.game = game # declare it part of the game
        self._layer = zLayer # Assign the Z-layer
        self.groups = self.game.all_sprites, self.game.interactable # sprite groups it's assigned to
        pygame.sprite.Sprite.__init__(self, self.groups)
        # If confused on this, refer to players similar assignment comments
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE 
        self.image = self.game.terrain_spritesheet.get_sprite(tile[0], tile[1], self.width, self.height) 
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

# button class for title screen
class Button:
    def __init__(self, x, y, imgx, imgy, width, height, fg, content, fontsize):
        self.font = pygame.font.Font('PythonGameMap/Assets/dungeoncrawlerfont.ttf', fontsize)
        self.content = content
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fg = fg

        # grab image
        #imgahh = pygame.image.load('Assets/MenuButtons.png')
        self.image = pygame.Surface([self.width,self.height])
        self.image.blit(pygame.image.load('PythonGameMap/Assets/MenuButtons.png').convert_alpha(), (0,0), (imgx,imgy,self.width,self.height))
        self.image.set_colorkey(BLACK)


        #self.image = pygame.Surface((self.width, self.height))
        #self.image = pygame.image.load('Assets/MenuButtons.png')
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False


