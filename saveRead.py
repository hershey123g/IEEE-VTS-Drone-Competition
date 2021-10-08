import cv2
print(cv2.__version__)
dispW=640
dispH=480
flip=2

camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam= cv2.VideoCapture(camSet)


#Enter path to video output here 
#This can later also be set to an argument to make our lives easier
#Video is written at 21 fps, same as video input
outVid = cv2.VideoWriter('videos/testVid.avi', cv2.VideoWriter_fourcc(*'XVID'), 21,(dispW,dispH))

while True:
    ret, frame = cam.read()

    #Comment out imshow and moveWindow when actually implementing code(Its only for test visualization)
    cv2.imshow('nanoCam',frame)
    cv2.moveWindow('nanoCam',0,0)

    outVid.write(frame)

    #Key q is used to end the recording but this loop can be broken a different way later 
    if cv2.waitKey(1)==ord('q'):
        break
cam.release()
outVid.release()
cv2.destroyAllWindows()

#In order to read videos use the file path as a parameter for the VideoCapture function
#Example: cam = cv2.VideoCapture('videos/testVid.avi')
#The rest of the code to display the video should be the same as if it was being pulled from a camera