# ---- Python Modules ---- #
import cv2
from threading import Thread
import mediapipe

# ---- Misc Variables ---- #

Pink = (255, 0, 255)
Blue = (255, 0, 0)
Green = (0, 255, 0)
Red = (0, 0, 255)

# ---- Initialising Variables ---- # 

coordinates = [ # Coordinate points for the grid 640x480 and applies colour
    
    # -- Central Cross -- #
    [(320,0), (320,480), Pink],
    [(0,240), (640,240), Pink],

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
        self.cameraUiEnabled = False

        if self.camera:
            self.camera.release()
            self.camera = None
            cv2.destroyWindow("image")

    def applyGrid(self):
        for coord_set in coordinates: # Loops through the dictionary 
            cv2.line(self.cameraImage, coord_set[0], coord_set[1], coord_set[2], 6) # Sets the line using the camera image and points from the dictionary.
                
    def showCoords(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            print(f'X: {x} // Y: {y}')
            self.checkHand(x,y)

    def checkHand(self, x, y):

        # -- Dead Zone Check -- #
        if x > 260 and x < 380 and y < 280 and y > 200:
            print('DEAD')
            return

        # -- Top Right -- #
        if x > 320 and x < 580 and y < 240 and y > 55:
            print('Top Right')

        # -- Top Left -- #
        if x > 60 and x < 320 and y < 240 and y > 55:
            print('Top Left')

        # -- Bottom Left -- #
        if x > 60 and x < 320 and y < 420 and y > 240:
            print('Bottom Left')

        # -- Bottom Right -- #
        if x > 320 and x < 580 and y < 420 and y > 240:
            print('Bottom Right')

    def startCameraFeedThread(self):
        while self.cameraUiEnabled: # Keeping the camera on when its in use.
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
                            self.checkHand(x,y)

            cv2.imshow('image', self.cameraImage) # Displaying the cameras image in a window
            cv2.setMouseCallback('image', self.showCoords) # Displays the mouse coords after clicking
            cv2.waitKey(1) # Wait for a key to be used

            if cv2.waitKey(1) & 0xFF == ord('q'): # Temp for when q is clicked the window closes for testing.
                self.cameraUiEnabled = False