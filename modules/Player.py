# ---- Python Modules ---- #
import pygame
import time
from threading import Thread

from modules.utils.Spritesheet import SpriteSheet
from modules.utils.Particles import Dust, dustParticles
# ---- Misc Variables ---- #

GROUND_BUFFER = 6

# ---- Initialising Variables ---- # 


class Player(pygame.sprite.Sprite):
    def __init__(self, screen, sheet, scale, LG, disableGravity=False):
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
        self.gravityDisabled = disableGravity
        
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
            if not self.jumpOnCooldown and self.isOnGround(self.LG.canCollide, self.LG.canMove):
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
        self.rectangle.y = y - 54
        self.y = y - 54

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
    
    def checkIfCollidingInteractable(self, objectToCheck, objectToSkip=None):
        skipArray = objectToSkip or [] # arry of items to skip from the previous itteration of this so we check for both players and moveable objects

        for interactable in self.LG.interactables: # check all interactables
            isHit = interactable.buttonMain.colliderect(objectToCheck) # if the object passing through is colliding with the interactable fire that its been clicked.
            if isHit: # if the buttons been hit then set to true
                interactable.setPressed(True)
                skipArray.append(interactable) # add to the skip array to be returned later
                
            if interactable not in skipArray: # if the interacton is in the skip array dont set to false
                interactable.setPressed(False)

        return skipArray
    
    def fetchGround(self, canCollide, hasMoveables=None): # fetches the position of the object the players currently on top
        feet_y = self.rectangle.bottom

        if canCollide:
            for obj in canCollide:
                if abs(feet_y - obj.top) <= 6:
                    if self.rectangle.right > obj.left and self.rectangle.left < obj.right:
                        return obj.top

        if hasMoveables:
            for data in hasMoveables:
                rect = data["rect"]
                if abs(feet_y - rect.top) <= 6:
                    if self.rectangle.right > rect.left and self.rectangle.left < rect.right:
                        return rect.top
                    
        # returns none if it hasnt returned already
        return None

    def isOnGround(self, canCollide, hasMoveables=None): # check if the player is on the ground or ontop of a moveable
        feet_y = self.rectangle.bottom

        if canCollide:
            for obj in canCollide:
                if abs(feet_y - obj.top) <= GROUND_BUFFER: # ground buffer used to make sure player doesnt fall into the floor and prevent themself from moving
                    if self.rectangle.right > obj.left and self.rectangle.left < obj.right:
                        return True

        if hasMoveables:
            for data in hasMoveables:
                rect = data["rect"]
                if abs(feet_y - rect.top) <= GROUND_BUFFER:
                    if self.rectangle.right > rect.left and self.rectangle.left < rect.right:
                        return True

        return False

    def fetchSideCollided(self, playerRect, objectRect): # fetch the side that they player is interacting with
        dx = (playerRect.centerx - objectRect.centerx)
        dy = (playerRect.centery - objectRect.centery)

        width = (playerRect.width + objectRect.width) / 2
        height = (playerRect.height + objectRect.height) / 2

        crossWidth = width * dy
        crossHeight = height * dx

        if abs(dx) <= width and abs(dy) <= height: # checks absolute values of dx and dy with width and height
            # compares the product of width and dy with height and dx
            if crossWidth > crossHeight:
                if crossWidth > -crossHeight:
                    return "bottom" 
                else:
                    return "left"   
            else:
                if crossWidth > -crossHeight:
                    return "right"   
                else:
                    return "top"     

        return None
    
    def movePlayer(self, canCollide=None, hasMoveables=None, isInLevel=False):
        if not isInLevel: return
        
        hasCollided = False # checks for collisions
        shouldMove = True
        jumpForce = (1/2) * self.mass * (self.yVelocity**2)
        onGround = self.isOnGround(canCollide, hasMoveables)

        skipArray = []  
        if hasMoveables:  
            for obj in hasMoveables:
                result = self.checkIfCollidingInteractable(obj["rect"])
                skipArray.extend(result)
          
        # now check for the player colliding and pass through the skip array  
        self.checkIfCollidingInteractable(self.rectangle, skipArray)
            
        if self.isJumping and not self.jumpOnCooldown: # check for if the person isnt on cooldown and is currently jumping
            self.yVelocity -= 0.4 # change the velocity by 0.4
            
            if self.yVelocity < 0: # once the velocity is less then 0 reverse the mass
                self.mass = -1
                
            if self.yVelocity <= -(self.jumpHeight - 1): # check if the velocity less or equal to -(jumpheight minus 1) 
                self.isJumping = False # change jumping and should jump to false
                Thread(target=self.jumpCooldown).start() # start the cooldown

                # reset all values
                self.yVelocity = self.jumpHeight
                self.mass = self.playerWeight


        if (isInLevel and not self.isJumping and not onGround) and not self.gravityDisabled: # change players yvelocity if they are not onthe grund
            self.yVelocity += self.yGravity
        
        if canCollide: # if there are any collidable objects in the map.
            for object in canCollide: # loops through each object in the can collide list.
                
                # Checks if they are colliding and are trying to move in the opposite direction of the wall.
                if object.collidepoint(self.rectangle.topleft) and self.x_direction == 2:
                    break
                    
                if object.collidepoint(self.rectangle.topright) and self.x_direction == -2:
                    break
                
                if self.finishRect.collidepoint(self.rectangle.topright): # checks if the player has collided with the finish area
                    hasCollided = False
                    self.MenuHandler.enableMenu("WinScreen") # sets a "win screen"
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
            for i, data in enumerate(hasMoveables): # loops through all the moveab;es
                if self.rectangle.colliderect(data["rect"]): # checks if the player has collided with a rect of the moveable.
                    side = self.fetchSideCollided(self.rectangle, data["rect"])

                    # if the player is ontop of the box then make the game keep them their untill they walk off
                    if side == "top":
                        onGround = True
                        self.rectangle.bottom = data["rect"].top
                        self.yVelocity = self.jumpHeight
                        self.mass = self.playerWeight
                        continue

                    # if players below the box then stop them jumping
                    if side == "bottom":
                        self.isJumping = False
                        self.yVelocity = self.jumpHeight
                        continue

                    # if players attempting to push the box then move it left n right
                    if side in ("left", "right"):
                        if shouldMove:
                            self.LG.moveMoveable(i)
                        hasCollided = True
                        self.x_direction = 0
                        continue


        if not hasCollided: # if there's no collisions start to move the players x and y values
            self.rectangle.x += self.speed * self.x_direction
            
            if self.isJumping and not self.jumpOnCooldown: # make player jump
                self.rectangle.y -= jumpForce
            elif (isInLevel and not onGround) and not self.gravityDisabled: # enforce gravity
                self.rectangle.y += self.yVelocity
            elif onGround and not self.gravityDisabled: # if the players on the ground fetch the ground y of where the player is and make sure the value is the same for the rectangle of the player
                groundY = self.fetchGround(canCollide, hasMoveables)
                if groundY is not None:
                    self.rectangle.bottom = groundY 

                # reset jump values
                self.yVelocity = self.jumpHeight
                self.mass = self.playerWeight
            
        self.draw(isInLevel) # draw the sprite in the new location
    