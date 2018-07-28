import numpy as np
import cv2
from math import atan2,sin,cos

def drawBoard():
    board = cv2.aruco.CharucoBoard_create(5, 7, 1, 0.75, cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50))
    drawing = board.draw((5*150,7*150),1,1)
    cv2.imwrite("board.png",drawing)
    
#drawBoard()
mat = np.array([[547.83678859,   0.        , 318.38894077],
       [  0.        , 548.64027301, 221.58152955],
       [  0.        ,   0.        ,   1.        ]])

dist = np.array([[-1.50870616e-01,  7.15661549e-01,  1.99754373e-03,-4.21943548e-04, -1.08743679e+00]])

def main():
    offset_transform = None
    smooth_px = 0
    smooth_py = 0
    offset_x = 0
    offset_y = 0
    angle = 0
    cap = cv2.VideoCapture(1)
    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    board = cv2.aruco.CharucoBoard_create(5, 7, 1, 0.75, dictionary)
        
    # http://answers.opencv.org/question/98447/camera-calibration-using-charuco-and-python/
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        res = cv2.aruco.detectMarkers(gray, dictionary)
        
        cv2.aruco.drawDetectedMarkers(frame,res[0],res[1])
        
        if len(res[0]) > 0:
            #res = res[0]
            #print(res)
            res2 = cv2.aruco.interpolateCornersCharuco(res[0],res[1],gray,board)
            res3,rvec,tvec = cv2.aruco.estimatePoseCharucoBoard(res2[1],res2[2],board,mat,dist)
            #print(res3)
            if res3:
                #print(tvec)
                cv2.aruco.drawAxis(frame,mat,dist,rvec,tvec, 1.5)
                if offset_transform is not None:
                    position = np.squeeze(offset_transform.dot(np.vstack((tvec.reshape((3,1)),1))))
                    print(position)
                    p_x = cos(angle)*position[0] + sin(angle)*position[1]
                    p_y = -sin(angle)*position[0] + cos(angle)*position[1]
                    
                    p_x += offset_x
                    p_y += offset_y
                    
                    smooth_px = smooth_px*0.95 + p_x*0.05
                    smooth_py = smooth_py*0.95 + p_y*0.05
                    cv2.putText(frame,"{:+.4f}".format(smooth_px),(0, 40),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),4)
                    cv2.putText(frame,"{:+.4f}".format(smooth_py),(0, 80),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),4)
                    cv2.putText(frame,"{:+.4f}".format(position[2]),(0,120),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),4)
                
        
        cv2.imshow("Frame",frame)
        k = cv2.waitKey(1)
        if k == 27:
            break
        elif k == 32:
            offset_transform = np.zeros((4,4))
            offset_transform[0:3,3] = np.squeeze(tvec)
            offset_transform[3,3] = 1
            rod = cv2.Rodrigues(rvec)[0]
            print(rod)
            offset_transform[0:3,0:3] = rod
            offset_transform = np.linalg.inv(offset_transform)
            print(offset_transform)
        elif k == ord('a'):
            angle = -atan2(position[0],position[1])
            print("ANGLE:",angle)
        elif k == ord('x'):
            offset_x = -smooth_px
        elif k == ord('y'):
            offset_y = -smooth_py
        elif k == ord('c'):
            offset_x = offset_x - smooth_px / 2
        elif k == ord('u'):
            offset_y = offset_y - smooth_py / 2
        elif k == -1:
            pass
        else:
            print(k)

if __name__ == "__main__":
    main()
