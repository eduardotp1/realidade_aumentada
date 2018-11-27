# Imports
import numpy as np
from cv2 import cv2
import sys

# Item 3
def find_homography(orig, dest):
    return cv2.findHomography(np.array(orig), np.array(dest))

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
last_frame = np.zeros_like(frame)
INCEPTION = False

if len(sys.argv) == 2:
    if (sys.argv[1] == 'inception'):
        print('INCEPTION MODE')
        INCEPTION = True
        overlay = last_frame
    else:
        print('Using image', sys.argv[1])    
        overlay = cv2.imread(sys.argv[1])
else:
    print('Using default Neymar image')
    overlay = cv2.imread('./neymar.jpg')

while(True):
    ret, frame = cap.read()
    adict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)

    c,i,r = cv2.aruco.detectMarkers(frame,dictionary=adict)
    # frame = cv2.aruco.drawDetectedMarkers(frame, c)
    
    board = cv2.imread("./board_aruco_fix.png")
    board_h, board_x = board.shape[:2]


    img = cv2.resize(overlay if INCEPTION == False else last_frame, (board_x, board_h)) 
    c2,i2,r2 = cv2.aruco.detectMarkers(board,dictionary=adict)
    
    orig = []
    dest = []
    
    original_frame = frame

    if(len(c) > 0):
        for iterator in range(0,len(i)):
            index = np.where(i2 == i[iterator])
            for j in range(0,len(c[iterator][0])):
                dest.append(c[iterator][0][j])
                orig.append(c2[index[0][0]][0][j])
        homography = find_homography(orig,dest)[0]  
        w, h, rr = frame.shape

        #transformar 0,0,0 em 1,1,1
        frame = cv2.warpPerspective(img, homography, (h,w))
        # frame = cv2.add(frame, original_frame)
        mask = frame > [0,0,0]
        frame = np.uint8(np.clip(np.where(mask, frame, original_frame), 0, 255))

    cv2.imshow('frame', frame)
    last_frame = frame
            
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

