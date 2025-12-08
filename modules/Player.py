# ---- Python Modules ---- #
import pygame

from modules.utils.Spritesheet import SpriteSheet
# ---- Misc Variables ---- #


# ---- Initialising Variables ---- # 


class Player(pygame.sprite.Sprite):
    def __init__(self, screen, sheet, scale):
        super().__init__() # allows use of the pygame Sprite class
        # Initialise variables from the imports.
        self.screen = screen
        self.spriteSheet = SpriteSheet(sheet)
        self.animationList = []
        self.animationSteps = 3
        self.x = 220
        self.y = 318
        self.x_direction = 0
        self.y_direction = 0
        
        self.isMoving = False
        self.Facing = None
        
        self.speed = 1
        self.scale = scale
        
        # Load animations
        self.listAnimations()
        
        self.currentFrame = 0
        self.lastUpdated = 0
        # Sets the current frame
        self.image = self.animationList[self.currentFrame]
        self.rectangle = self.image.get_rect(topleft=(self.x, self.y))
        
    def listAnimations(self):
        for x in range(self.animationSteps):
            self.animationList.append(self.spriteSheet.getSprite(x, 138, 182, self.scale, (30,50,30))) # Adds each mage frame to a list.
        
    def draw(self):
        #pygame.draw.rect(self.screen, (255,2,200), self.rectangle)  
        if self.isMoving: # if the player is moving
            currentTime = pygame.time.get_ticks() # gets the current time
            if currentTime - self.lastUpdated >= 100: # checks if its been less then 200 ticks
                self.currentFrame += 1 # updates the frame
                self.lastUpdated = currentTime
            if self.currentFrame == 3: # checks if the frame went above 3
                self.currentFrame = 1 # sets it back to the start of the walking animation
                
            self.screen.blit(self.animationList[self.currentFrame], self.rectangle.topleft) # On call draws on the sprite.
        else:
            self.screen.blit(self.animationList[0], self.rectangle.topleft) # On call draws on the idle sprite.
    
    def keyDown(self, event): # as a key is pressed the x direction is changed to signify a left or right movement.
        if event.key == pygame.K_LEFT:
            self.x_direction = -2
            self.Facing = "Left"
            self.isMoving = True # sets moving to true
        elif event.key == pygame.K_RIGHT:
            self.x_direction = 2
            self.Facing = "Right"
            self.isMoving = True # sets moving to true


    def keyUp(self, event): # as a key is pressed the x direction is changed to signify a stopping motion.
        if event.key == pygame.K_LEFT:
            self.x_direction = 0
            self.isMoving = False # sets moving to false as they aren holding the move key down no more
        elif event.key == pygame.K_RIGHT:
            self.x_direction = 0
            self.isMoving = False # sets moving to false as they aren holding the move key down no more      
            
    def tunnelPlayer(self, x, y):
        self.rectangle.x = x
        self.rectangle.y = y              
                
    def movePlayer(self, canCollide=None):
        hasCollided = False # checks for collisions
        if canCollide: # if there are any collidable objects in the map.
            for object in canCollide: # loops through each object in the can collide list.
                
                # Checks if they are colliding and are trying to move in the opposite direction of the wall.
                if object.collidepoint(self.rectangle.topleft) and self.x_direction == 2:
                    break
                    
                if object.collidepoint(self.rectangle.topright) and self.x_direction == -2:
                    break
                    
                # if they have collided with the wall then stop movement
                if self.rectangle.colliderect(object):
                    hasCollided = True
                    
                    if self.x_direction != 0:
                        self.x_direction = 0
                    if self.y_direction != 0:
                        self.y_direction = 0
                    break
        
        if not hasCollided: # if theres no collisions start to move the players x and y values
            self.rectangle.x += self.speed * self.x_direction
            self.rectangle.y += self.speed * self.y_direction
            
            
        self.draw() # draw the sprite in the new location
    