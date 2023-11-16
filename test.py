from PIL import ImageGrab
import numpy as np
import cv2

screen = cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_RGB2BGR)
screen = screen[226:1014,351:1547,:]
# 351 226 1547 1014
cv2.imshow('Python Window', screen)
cv2.waitKey(0)