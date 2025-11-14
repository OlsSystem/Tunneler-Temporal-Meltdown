# ---- Python Modules ---- #
import cv2
import mediapipe 

cameraUiEnabled = False # used to turn off the camera when its not needed.

def startHandTracking():
    camera = cv2.VideoCapture(0) # Used to fetch the camera feed.
    #camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920) # Allows me to test out the camera in a bigger size
    #camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080) 

    cameraUiEnabled = True
    mpHandsSolution = mediapipe.solutions.hands # Imports the hands solution from Mediapipe
    mpDrawingSolution = mediapipe.solutions.drawing_utils # Imports the drawing utilities from Mediapipe

    hand = mpHandsSolution.Hands() # Initialises the Hands moduel from the hands solution

    if not camera.isOpened(): # Checking if the user has got the camera opened.
        print('Camera cant be opened.. Exiting.')
        cameraUiEnabled = False
        return "Camera Not Found." # Return an Error to the core of the game.

    while cameraUiEnabled: # Keeping the camera on when its in use.

        foundCamera, cameraImage = camera.read() # Reading the image of the camera
        cameraImage = cv2.flip(cameraImage, 1) # Flips the video image so that you move the hand in the same direction on the camera as you are in real life.

        if not foundCamera: # Checks if the camera is found if not itll stop the function.
            print('Camera not found.. Exiting.')
            cameraUiEnabled = False
            return "Couldn't use camera feed." # Returns it couldnt find the camera.

        colourConvert = cv2.cvtColor(cameraImage, cv2.COLOR_BGR2RGB) # Converts the image into RGB from BGR.

        handsInView = hand.process(colourConvert) # Finds the hands that are in view of the camera.

        if handsInView.multi_hand_landmarks: # Runs if it finds hands.
            for handPos in handsInView.multi_hand_landmarks: # Runs for each hand in view of the camera.
                for id, landMark in enumerate(handPos.landmark): # Runs for each point on a hand.
                    h, w, c = cameraImage.shape # Provides height and width of the camera ui
                    x, y = int(landMark.x * w), int(landMark.y * h) # converts the height and width into x and y coordinates to draw on the hand
                    if id == 8: # 8 is the ID for the tip of the index finger.
                        cv2.circle(cameraImage, (x, y), 15, (255, 0, 255), cv2.FILLED) # Creates a circle around the point on the index finger.
        
        cv2.imshow('image', cameraImage) # Displaying the cameras image in a window
        cv2.waitKey(1) # Wait for a key to be used

def stopHandTracking(): # Used to disable the camera when its not needed.
    cameraUiEnabled = False