# ---- Python Modules ---- #
import cv2
import time

# ---- Custom Modules ---- #
import modules.handTracking as handTracking


HT = handTracking.TrackHands()

HT.start()

time.sleep(3)

print('STOPPING')
HT.stop()