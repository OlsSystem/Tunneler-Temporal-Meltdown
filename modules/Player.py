# ---- Python Modules ---- #
import pygame
import time
from threading import Thread

from modules.utils.Spritesheet import SpriteSheet
from modules.utils.Particles import Dust, dustParticles
# ---- Misc Variables ---- #


# ---- Initialising Variables ---- # 


class Player(pygame.sprite.Sprite):
    def __init__(self, screen, sheet, scale, LG):
        super().__init__() # allows use of the pygame Sprite class
        # Initialise variables from the imports.
        self.screen = screen
        self.LG = LG
        self.MenuHandler = None
        self.spriteSheet = SpriteSheet(sheet)
        self.animationList = []
        self.animationSteps = 3
        self.x = 220
        self.y = 659
        self.x_direction = 0
        self.y_direction = 0
        
        self.yGravity = 1
        self.jumpHeight = 7
        self.playerWeight = 1
        self.jumpOnCooldown = False
        self.yVelocity = self.jumpHeight
        self.mass = self.playerWeight
        
        self.finishRect = None
        
        self.isMoving = False
        self.isJumping = False
        self.Facing = "Right"
        
        self.speed = 1
        self.scale = scale
        
        # Load animations
        self.listAnimations()
        
        self.currentFrame = 0
        self.lastUpdated = 0
        # Sets the current frame
        self.image = self.animationList[self.currentFrame]
        self.rectangle = self.image.get_rect(topleft=(self.x, self.y))

    def setMenuHandler(self, MH):
        self.MenuHandler = MH

    def listAnimations(self):
        for x in range(self.animationSteps):
            self.animationList.append(self.spriteSheet.getSprite(x, 138, 182, self.scale, (30,50,30))) # Adds each mage frame to a list.
        
    def draw(self, isInLevel):
        #pygame.draw.rect(self.screen, (255,2,200), self.rectangle)  
        if isInLevel:
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
        if event == "Left":
            self.x_direction = -2
            self.Facing = "Left"
            self.isMoving = True # sets moving to true
        elif event == "Right":
            self.x_direction = 2
            self.Facing = "Right"
            self.isMoving = True # sets moving to true
        elif event == "Jump":
            self.isJumping = True


    def keyUp(self, event): # as a key is pressed the x direction is changed to signify a stopping motion.
        if event == "Left":
            self.x_direction = 0
            self.isMoving = False # sets moving to false as they aren holding the move key down no more
        elif event == "Right":
            self.x_direction = 0
            self.isMoving = False # sets moving to false as they aren holding the move key down no more 
            
    def movePlayerToCoordinates(self, x, y):
        self.rectangle.x = x
        self.rectangle.y = y - 48
        self.y = y - 48

    def tunnelPlayer(self, x, y, tunnelColour):
        # moves the player to where the tunnel is.
        self.rectangle.x = x
        self.rectangle.y = y 
        
        # adds dust onto the player to show them coming out of tunnel
        particles = Dust(self.rectangle.center, tunnelColour, None, 12)
        dustParticles.append(particles)     
        
    # starts the level by moving the player to the correct coordinates with a y ofset of 48 and sets the finish rect.
    def levelStarted(self, startX, startY, finishX, finishY, finishW, finishH):
        self.movePlayerToCoordinates(startX, startY)
        
        self.finishRect = pygame.Rect(finishX, finishY, finishW, finishH)

    def jumpCooldown(self):
        self.jumpOnCooldown = True
        time.sleep(1)
        self.jumpOnCooldown = False
    
    def checkIfCollidingInteractable(self, objectToCheck):
        collided = False

        for interactable in self.LG.interactables: # check all interactables
            isHit = interactable.buttonMain.colliderect(objectToCheck) # if the object passing through is colliding with the interactable fire that its been clicked.
            # set is pressed to true
            interactable.isPressed = isHit

            if isHit:
                collided = True

        return collided
    
    def movePlayer(self, canCollide=None, hasMoveables=None, isInLevel=False):
        if not isInLevel: return
        
        hasCollided = False # checks for collisions
        shouldJump = False
        shouldMove = True
        jumpForce = (1/2) * self.mass * (self.yVelocity**2)
            
        isInteracting = False    
        for obj in hasMoveables:
            isInteracting = self.checkIfCollidingInteractable(obj["rect"])
          
        if not isInteracting:  
            self.checkIfCollidingInteractable(self.rectangle)
            
        if self.isJumping and not self.jumpOnCooldown:
            shouldJump = True
            self.yVelocity -= 0.4
            
            if self.yVelocity < 0:
                self.mass = -1
                
            if self.yVelocity <= -(self.jumpHeight - 1):
                self.isJumping = False
                shouldJump = False
                Thread(target=self.jumpCooldown).start()

                self.yVelocity = self.jumpHeight
                self.mass = self.playerWeight

                self.rectangle.y = self.y
        
        if canCollide: # if there are any collidable objects in the map.
            for object in canCollide: # loops through each object in the can collide list.
                
                # Checks if they are colliding and are trying to move in the opposite direction of the wall.
                if object.collidepoint(self.rectangle.topleft) and self.x_direction == 2:
                    break
                    
                if object.collidepoint(self.rectangle.topright) and self.x_direction == -2:
                    break
                
                if self.finishRect.collidepoint(self.rectangle.topright): # checks if the player has collided with the finish area
                    hasCollided = False
                    self.MenuHandler.enableMenu("DeadScreen") # sets a "win screen"
                    break
                    
                # if they have collided with the wall then stop movement
                if self.rectangle.colliderect(object):
                    hasCollided = True
                    
                    if self.x_direction != 0:
                        self.x_direction = 0
                    if self.y_direction != 0:
                        self.y_direction = 0
                    break


        if hasMoveables: # if theres moveables
            collidedWithWall = False
            for i, data in enumerate(hasMoveables): # loops through all the moveab;es
                if self.rectangle.colliderect(data["rect"]): # checks if the player has collided with a rect of the moveable.

                    # gets the x and y of the player
                    dx = self.speed * self.x_direction
                    dy = self.speed * self.y_direction

                    if canCollide: # checks if theres collidables
                        for object in canCollide:
                                                    
                            # loops through each collideable checking if the players touching it and moveing. if moving in the opposite way it ignores
                            if object.collidepoint(data["rect"].topleft) and self.x_direction == 2:
                                shouldMove = False
                                break

                            if object.collidepoint(data["rect"].bottomright) and self.x_direction == -2:
                                shouldMove = False
                                break

                            # if box isnt moving and collided the player has collided
                            if object.collidepoint(data["rect"].topleft):
                                collidedWithWall = True

                            if object.collidepoint(data["rect"].bottomright):
                                collidedWithWall = True

                            if collidedWithWall: # checks if box collided with the wall
                                hasCollided = True # sets collided to true doesnt allow player to move and box
                                shouldMove = False # sets should move to false to not move the box
                                
                                # resets the x and y
                                if self.x_direction != 0:
                                    self.x_direction = 0
                                if self.y_direction != 0:
                                    self.y_direction = 0
                                break

                    # Only push if player is actually moving
                    if (dx != 0 or dy != 0) and collidedWithWall == False and shouldMove:
                        self.LG.moveMoveable(i)


        if not hasCollided: # if there's no collisions start to move the players x and y values
            self.rectangle.x += self.speed * self.x_direction
            if shouldJump and not self.jumpOnCooldown:
                self.rectangle.y -= jumpForce
            
        self.draw(isInLevel) # draw the sprite in the new location
    