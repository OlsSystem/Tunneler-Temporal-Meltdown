# ---- Python Modules ---- #
import cv2
from threading import Thread
import mediapipe
import math

# ---- Misc Variables ---- #

Pink = (255, 0, 255)
Blue = (255, 0, 0)
Green = (0, 255, 0)
Red = (0, 0, 255)

# ---- Initialising Variables ---- # 

coordinates = [ # Coordinate points for the grid 640x480 and applies colour
    
    # -- Central Cross -- #
    [(320,55), (320,425), Pink],
    [(60,240), (580,240), Pink],

    # -- Dead Zone Box -- #
    [(380,200), (380,280), Red],
    [(260,200), (260,280), Red],
    [(380,200), (260,200), Red],
    [(380,280), (260,280), Red],

    # -- Extra Moves Boxes -- #
    [(580,480), (580,0), Green],
    [(60,480), (60,0), Green],
    [(0,425), (640,425), Green],
    [(0,55), (640,55), Green]
] 

class TrackHands():
    def __init__(self):
        self.camera = None # Initialising Variable
        #camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920) # Allows me to test out the camera in a bigger size
        #camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        self.cameraUiEnabled = True # used to turn off the camera when its not needed.
        self.mpHandsSolution = mediapipe.solutions.hands # Imports the hands solution from Mediapipe

        self.hand = self.mpHandsSolution.Hands() # Initialises the Hands moduel from the hands solution
        
        self.handLocation = "Unknown"
        self.menuTracked = False
        self.x, self.y = 100, 100

    
    def start(self):
        self.camera = cv2.VideoCapture(0) # Used to fetch the camera feed.
        
        if not self.camera.isOpened(): # Checking if the user has got the camera opened.
            print('Camera cant be opened.. Exiting.')
            self.cameraUiEnabled = False
            return "Camera Not Found." # Return an Error to the core of the game.

        self.cameraUiEnabled = True
        Thread(target=self.startCameraFeedThread).start() # Starts the camera feed as a Thread so that other code is able to run while still having the camera enabled since it requires a loop


    def stop(self): # Disables the camera feed and thread.
        print("Stopping camera...")
        self.cameraUiEnabled = False # Sets the for loop within the thread to false so it stops.

        if self.camera: # If theres still and camera it will
            self.camera.release() # Shuts off the camera Feed. 
            self.camera = None # Sets the camera to None to allow for boot up again.
            cv2.destroyWindow("image") # Closes out the window that shows the camera.

    def enableMenuTracking(self, cursor):
        self.menuTracked = True # Enables the menu tracking to be used.
        self.cursor = cursor # Brings the cursor over from the core file to be used and changed with mediapipe and cv2.
        
    def disableMenuTracking(self):
        self.menuTracked = False # Disables the menu tracking.
        self.cursor.setImage("Idle")
        
    def setXandY(self, x, y):
        self.x = x # Sets the hands x
        self.y = y # Sets the hands y

    def menuTracking(self):
        if self.menuTracked: # If the menus enabled and hand tracking is on.
            self.cursor.moveCursor(self.x, self.y) # Moves the cursor based on the set values.
            
    def applyGrid(self):
        for coord_set in coordinates: # Loops through the dictionary 
            cv2.line(self.cameraImage, coord_set[0], coord_set[1], coord_set[2], 6) # Sets the line using the camera image and points from the dictionary.
                
    # To be deleted after testing ----- ----- -----
    def showCoords(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            print(f'X: {x} // Y: {y}')
            self.checkHand(x,y)
            print(self.handLocation)
    # ----- ----- ----- ----- ----- ----- ----- ----- 

    def checkHand(self, x, y):
        # -- Dead Zone Check -- #
        if x > 260 and x < 380 and y < 280 and y > 200:
            self.handLocation = "Dead Zone"
            return

        # -- Top Right -- #
        if x > 320 and x < 580 and y < 240 and y > 55:
            self.handLocation = "Top Right"
            return
        
        # -- Top Left -- #
        if x > 60 and x < 320 and y < 240 and y > 55:
            self.handLocation = "Top Left"
            return

        # -- Bottom Left -- #
        if x > 60 and x < 320 and y < 420 and y > 240:
            self.handLocation = "Bottom Left"
            return

        # -- Bottom Right -- #
        if x > 320 and x < 580 and y < 420 and y > 240:
            self.handLocation = "Bottom Right"
            return
            
        # -- Left Side Green -- #
        if x > 0 and x < 60 and y < 425 and y > 55:
            self.handLocation = "Left Side Green"
            return
        
        # -- Right Side Green -- #
        if x > 580 and x < 640 and y < 425 and y > 55:
            self.handLocation = "Right Side Green"
            return
        
        # -- Top Green -- #
        if x > 60 and x < 580 and y < 55 and y > 0:
            self.handLocation = "Top Green"
            return
        
        # -- Bottom Green -- #
        if x > 60 and x < 580 and y < 480 and y > 425:
            self.handLocation = "Bottom Green"
            return
        
        self.handLocation = "Unknown"
        
    def isPinching(self, p1, p2, threashold=30):
        return math.hypot(p2[0] - p1[0], p2[1] - p1[1]) < threashold
        
    def startCameraFeedThread(self):
        while self.cameraUiEnabled: # Keeping the camera on when its in use.
            indexLandmark = None
            thumbLandmark = None
            foundCamera, self.cameraImage = self.camera.read() # Reading the image of the camera
            self.cameraImage = cv2.flip(self.cameraImage, 1) # Flips the video image so that you move the hand in the same direction on the camera as you are in real life.

            if not foundCamera: # Checks if the camera is found if not itll stop the function.
                print('Camera not found.. Exiting.')
                self.cameraUiEnabled = False
                return "Couldn't use camera feed." # Returns it couldnt find the camera.

            colourConvert = cv2.cvtColor(self.cameraImage, cv2.COLOR_BGR2RGB) # Converts the image into RGB from BGR.

            handsInView = self.hand.process(colourConvert) # Finds the hands that are in view of the camera.

            self.applyGrid() # Applys the grid to the

            if handsInView.multi_hand_landmarks: # Runs if it finds hands.
                for handPos in handsInView.multi_hand_landmarks: # Runs for each hand in view of the camera.
                    for id, landMark in enumerate(handPos.landmark): # Runs for each point on a hand.
                        h, w, c = self.cameraImage.shape # Provides height and width of the camera ui
                        x, y = int(landMark.x * w), int(landMark.y * h) # converts the height and width into x and y coordinates to draw on the hand
                        if id == 8: # 8 is the ID for the tip of the index finger.
                            cv2.circle(self.cameraImage, (x, y), 15, (255, 0, 255), cv2.FILLED) # Creates a circle around the point on the index finger.
                            self.setXandY(x,y)
                            indexLandmark = (x,y)
                            
                        if id == 4 and self.menuTracked:
                            cv2.circle(self.cameraImage, (x, y), 15, (255, 0, 255), cv2.FILLED) 
                            thumbLandmark = (x,y)
                            
                        
            if indexLandmark and thumbLandmark:
                if self.isPinching(indexLandmark, thumbLandmark, 20):   
                    self.cursor.setImage("Select")
                else:
                    self.cursor.setImage("Idle")
            else:
                self.cursor.setImage("Idle")


            cv2.imshow('image', self.cameraImage) # Displaying the cameras image in a window
            cv2.setMouseCallback('image', self.showCoords) # Displays the mouse coords after clicking
            cv2.waitKey(1) # Wait for a key to be used

            if cv2.waitKey(1) & 0xFF == ord('q'): # Temp for when q is clicked the window closes for testing.
                self.cameraUiEnabled = False