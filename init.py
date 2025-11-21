# ---- Python Modules ---- #
import cv2
import time

# ---- Custom Modules ---- #
import modules.handTracking as handTracking
import modules.coreGame as Core

# -- Core Variables -- #

HT = handTracking.TrackHands()
CORE = Core.CoreGame()

#HT.start()