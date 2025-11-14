# ---- Python Modules ---- #
import cv2
from threading import Thread
import mediapipe 

class TrackHands():
    def __init__(self):
        self.camera = cv2.VideoCapture(0) # Used to fetch the camera feed.
        #camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920) # Allows me to test out the camera in a bigger size
        #camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080) 

        self.cameraUiEnabled = True # used to turn off the camera when its not needed.
        self.mpHandsSolution = mediapipe.solutions.hands # Imports the hands solution from Mediapipe

        self.hand = self.mpHandsSolution.Hands() # Initialises the Hands moduel from the hands solution

    def startCameraFeedThread(self):
        while self.cameraUiEnabled: # Keeping the camera on when its in use.
            # print(self.cameraUiEnabled)
            foundCamera, cameraImage = self.camera.read() # Reading the image of the camera
            cameraImage = cv2.flip(cameraImage, 1) # Flips the video image so that you move the hand in the same direction on the camera as you are in real life.

            if not foundCamera: # Checks if the camera is found if not itll stop the function.
                print('Camera not found.. Exiting.')
                self.cameraUiEnabled = False
                return "Couldn't use camera feed." # Returns it couldnt find the camera.

            colourConvert = cv2.cvtColor(cameraImage, cv2.COLOR_BGR2RGB) # Converts the image into RGB from BGR.

            handsInView = self.hand.process(colourConvert) # Finds the hands that are in view of the camera.

            if handsInView.multi_hand_landmarks: # Runs if it finds hands.
                for handPos in handsInView.multi_hand_landmarks: # Runs for each hand in view of the camera.
                    for id, landMark in enumerate(handPos.landmark): # Runs for each point on a hand.
                        h, w, c = cameraImage.shape # Provides height and width of the camera ui
                        x, y = int(landMark.x * w), int(landMark.y * h) # converts the height and width into x and y coordinates to draw on the hand
                        if id == 8: # 8 is the ID for the tip of the index finger.
                            cv2.circle(cameraImage, (x, y), 15, (255, 0, 255), cv2.FILLED) # Creates a circle around the point on the index finger.
        
            cv2.imshow('image', cameraImage) # Displaying the cameras image in a window
            cv2.waitKey(1) # Wait for a key to be used


    def start(self):
        if not self.camera.isOpened(): # Checking if the user has got the camera opened.
            print('Camera cant be opened.. Exiting.')
            self.cameraUiEnabled = False
            return "Camera Not Found." # Return an Error to the core of the game.
        
        Thread(target=self.startCameraFeedThread).start() # Starts the camera feed as a Thread so that other code is able to run while still having the camera enabled since it requires a loop


    def stop(self): # Disables the camera feed and thread.
        self.cameraUiEnabled = False # Stops the loop
