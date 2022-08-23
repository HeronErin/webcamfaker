import time
import pyfakewebcam
import numpy as np
import cv2
  
  
# define a video capture object
vid = cv2.VideoCapture(0)
blue = np.zeros((480,640,3), dtype=np.uint8)
blue[:,:,2] = 255

red = np.zeros((480,640,3), dtype=np.uint8)
red[:,:,0] = 255

camera = pyfakewebcam.FakeWebcam('/dev/video2', 640, 480)

while True:
    ret, frame = vid.read()
    camera.schedule_frame(frame)
    time.sleep(1/30.0)
