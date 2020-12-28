import cv2
print(cv2.__version__)
import numpy as np

def nothing(x):
    pass

cv2.namedWindow('Trackbars')
cv2.moveWindow('Trackbars', 1320, 0)

cv2.createTrackbar('hueLower', 'Trackbars',0,179,nothing)
cv2.createTrackbar('hueHigher', 'Trackbars', 18, 179, nothing)
cv2.createTrackbar('hueLower2', 'Trackbars',150,179,nothing)
cv2.createTrackbar('hueHigher2', 'Trackbars', 179, 179, nothing)
cv2.createTrackbar('satLower', 'Trackbars', 120, 255, nothing)
cv2.createTrackbar('satHigher', 'Trackbars', 255, 255, nothing)
cv2.createTrackbar('valLower', 'Trackbars', 60, 255, nothing)
cv2.createTrackbar('valHigher', 'Trackbars', 255, 255, nothing)

dispW = 640
dispH = 480
flip = 0
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam=cv2.VideoCapture(camSet)
while True:
    ret, frame=cam.read()
    cv2.imshow('nanoCam',frame)
    cv2.moveWindow('nanoCam', 0, 0)

    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    hueLow=cv2.getTrackbarPos('hueLower', 'Trackbars')
    hueHigh=cv2.getTrackbarPos('hueHigher', 'Trackbars')
    hue2Low=cv2.getTrackbarPos('hueLower2', 'Trackbars')
    hue2High=cv2.getTrackbarPos('hueHigher2', 'Trackbars')
    satLow=cv2.getTrackbarPos('satLower', 'Trackbars')
    satHigh=cv2.getTrackbarPos('satHigher', 'Trackbars')
    valLow=cv2.getTrackbarPos('valLower', 'Trackbars')
    valHigh=cv2.getTrackbarPos('valHigher', 'Trackbars')

    l_b=np.array([hueLow,satLow,valLow])
    u_b=np.array([hueHigh,satHigh,valHigh])

    l_b2=np.array([hue2Low,satLow,valLow])
    u_b2=np.array([hue2High,satHigh,valHigh])

    FGmask=cv2.inRange(hsv,l_b,u_b)
    FGmask2=cv2.inRange(hsv,l_b2,u_b2)
    FGmaskcomp=cv2.add(FGmask,FGmask2)
    cv2.imshow('FGmaskcomp',FGmaskcomp)
    cv2.moveWindow('FGmaskcomp', 0, 500)

    FG=cv2.bitwise_and(frame, frame, mask=FGmaskcomp)
    cv2.imshow('FG', FG)
    cv2.moveWindow('FG', 700, 0)

    bgMask=cv2.bitwise_not(FGmaskcomp)
    cv2.imshow('bgMask', bgMask)
    cv2.moveWindow('bgMask',700,500)

    BG=cv2.cvtColor(bgMask,cv2.COLOR_GRAY2BGR)

    final=cv2.add(FG,BG)
    cv2.imshow('final', final)
    cv2.moveWindow('final',1400,1000)

    if cv2.waitKey(1) == ord('q'):
        break
cam.release()
cv2.destroyALLWindows()