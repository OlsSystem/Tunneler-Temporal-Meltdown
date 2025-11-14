def applyGrid(self):
    print('APPLYING GRID')
    cv2.line(self.cameraImage, (0,0), (250,250), (255, 0, 255), 9)