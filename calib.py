import time
import cv2.aruco as A
import cv2
import numpy as np

dictionary = A.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
board = A.CharucoBoard_create(5, 7, 1, 0.75, dictionary)
#img = board.draw((200*3,200*3))

#Dump the calibration board to a file
#cv2.imwrite('charuco.png',img)


#Start capturing images for calibration
cap = cv2.VideoCapture(4)

allCorners = []
allIds = []
decimator = 0
for i in range(300):

    ret,frame = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    res = cv2.aruco.detectMarkers(gray,dictionary)

    if len(res[0])>0:
        res2 = cv2.aruco.interpolateCornersCharuco(res[0],res[1],gray,board)
        if res2[1] is not None and res2[2] is not None and len(res2[1])>3 and decimator%3==0:
            allCorners.append(res2[1])
            allIds.append(res2[2])

        cv2.aruco.drawDetectedMarkers(gray,res[0],res[1])

    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    decimator+=1

imsize = gray.shape

#Calibration fails for lots of reasons. Release the video if we do
try:
    res, mat, dist = cv2.aruco.calibrateCameraCharuco(allCorners,allIds,board,imsize,None,None)
    print(mat)
    print(dist)
except:
    cap.release()


cap.release()
cv2.destroyAllWindows()
