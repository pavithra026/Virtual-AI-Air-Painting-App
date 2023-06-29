import numpy as np
import cv2
from collections import deque

yellowLower = np.array([22, 93, 0])
yellowUpper = np.array([45, 255, 255])

# Define a 5x5 kernel for erosion and dilation
kernel = np.ones((5, 5), np.uint8)

#default called trackbar function 
def setValues(x):
   print("")

# Creating the trackbars needed for adjusting the marker colour
cv2.namedWindow("Color detectors")
cv2.createTrackbar("Upper Hue", "Color detectors", 153, 180,setValues)
cv2.createTrackbar("Upper Saturation", "Color detectors", 255, 255,setValues)
cv2.createTrackbar("Upper Value", "Color detectors", 255, 255,setValues)
cv2.createTrackbar("Lower Hue", "Color detectors", 64, 180,setValues)
cv2.createTrackbar("Lower Saturation", "Color detectors", 72, 255,setValues)
cv2.createTrackbar("Lower Value", "Color detectors", 49, 255,setValues)

# Initialize deques to store different colors in different arrays
bpoints = [deque(maxlen=512)]
gpoints = [deque(maxlen=512)]
rpoints = [deque(maxlen=512)]
ypoints = [deque(maxlen=512)]
ppoints = [deque(maxlen=512)]
mpoints = [deque(maxlen=512)]
blpoints = [deque(maxlen=512)]
wpoints = [deque(maxlen=512)]

bindex = 0
gindex = 0
rindex = 0
yindex = 0
pindex = 0
mindex = 0
blindex = 0
windex = 0

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255),(148,0,211),(0,0,0)] 
colorIndex = 0

# Create a blank white image
paintWindow = np.zeros((550,636,3)) + 255
#Draw buttons like colored rectangles on the white image
paintWindow = cv2.rectangle(paintWindow, (20,5), (90,50), (0, 0, 255), 2)
paintWindow = cv2.rectangle(paintWindow, (105,5), (175,50), colors[0], -1)
paintWindow = cv2.rectangle(paintWindow, (190,5), (260,50), colors[1], -1)
paintWindow = cv2.rectangle(paintWindow, (275,5), (345,50), colors[2], -1)
paintWindow = cv2.rectangle(paintWindow, (360,5), (430,50), colors[3], -1)
paintWindow = cv2.rectangle(paintWindow, (445,5), (515,50), colors[4], -1)
paintWindow = cv2.rectangle(paintWindow, (530,5), (600,50), colors[5], -1)

cv2.putText(paintWindow, "C", (43, 45), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2, cv2.LINE_AA)


# Load the video
camera = cv2.VideoCapture(0)

# Keep looping
while True:
    # Grab the current paintWindow
    (grabbed, frame) = camera.read()

    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    if not grabbed:
        break    

    u_hue = cv2.getTrackbarPos("Upper Hue", "Color detectors")
    u_saturation = cv2.getTrackbarPos("Upper Saturation", "Color detectors")
    u_value = cv2.getTrackbarPos("Upper Value", "Color detectors")
    l_hue = cv2.getTrackbarPos("Lower Hue", "Color detectors")
    l_saturation = cv2.getTrackbarPos("Lower Saturation", "Color detectors")
    l_value = cv2.getTrackbarPos("Lower Value", "Color detectors")
    
    
    # Add the same paint interface to the camera feed captured through the webcam (for ease of usage)
    frame = cv2.rectangle(frame, (20,5), (90,50), (0, 0, 255), 2)
    frame = cv2.rectangle(frame, (105,5), (175,50), colors[0], -1)
    frame = cv2.rectangle(frame, (190,5), (260,50), colors[1], -1)
    frame = cv2.rectangle(frame, (275,5), (345,50), colors[2], -1)
    frame = cv2.rectangle(frame, (360,5), (430,50), colors[3], -1)
    frame = cv2.rectangle(frame, (445,5), (515,50), colors[4], -1)
    frame = cv2.rectangle(frame, (530,5), (600,50), colors[5], -1)
    
    
    cv2.putText(frame, "C", (43, 45), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2, cv2.LINE_AA)
    
    cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)
    # Determine which pixels fall within the blue boundaries and then blur the binary image
    greenMask = cv2.inRange(hsv, yellowLower, yellowUpper)
    greenMask = cv2.erode(greenMask, kernel, iterations=2)
    greenMask = cv2.morphologyEx(greenMask, cv2.MORPH_OPEN, kernel)
    greenMask = cv2.dilate(greenMask, kernel, iterations=1)

    # Find contours in the image
    (cnts, _) = cv2.findContours(greenMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    center = None

    if len(cnts) > 0:
        cnt = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
        ((x, y), radius) = cv2.minEnclosingCircle(cnt)
        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
        M = cv2.moments(cnt)
        center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
        
        if center[1] <= 65:
            if 40 <= center[0] <= 140: # Clear Button
                bpoints = [deque(maxlen=512)]
                gpoints = [deque(maxlen=512)]
                rpoints = [deque(maxlen=512)]
                ypoints = [deque(maxlen=512)]
                ppoints = [deque(maxlen=512)]
                mpoints = [deque(maxlen=512)]
                
                

                bindex = 0
                gindex = 0
                rindex = 0
                yindex = 0
                pindex = 0
                mindex = 0
                

                paintWindow[67:,:,:] = 175
            elif 105 <= center[0] <= 175:
                    colorIndex = 0 # Blue
            elif 190 <= center[0] <= 260:
                    colorIndex = 1 # Green
            elif 275 <= center[0] <= 345:
                    colorIndex = 2 # Red
            elif 360 <= center[0] <= 430:
                    colorIndex = 3 # Yellow
            elif 445 <= center[0] <= 515:
                    colorIndex = 4 # purple
            elif 530 <= center[0] <= 600:
                    colorIndex = 5 # black
            
        else :
            if colorIndex == 0:
                bpoints[bindex].appendleft(center)
            elif colorIndex == 1:
                gpoints[gindex].appendleft(center)
            elif colorIndex == 2:
                rpoints[rindex].appendleft(center)
            elif colorIndex == 3:
                ypoints[yindex].appendleft(center)
            elif colorIndex == 4:
                ppoints[pindex].appendleft(center)
            elif colorIndex == 5:
                mpoints[mindex].appendleft(center)
           
    # Append the next deques when nothing is detected to avois messing up
    else:
        bpoints.append(deque(maxlen=512))
        bindex += 1
        gpoints.append(deque(maxlen=512))
        gindex += 1
        rpoints.append(deque(maxlen=512))
        rindex += 1
        ypoints.append(deque(maxlen=512))
        yindex += 1
        ppoints.append(deque(maxlen=512))
        pindex += 1
        mpoints.append(deque(maxlen=512))
        mindex += 1
        

    # Draw lines of all the colors (Blue, Green, Red and Yellow)
    points = [bpoints, gpoints, rpoints, ypoints, ppoints, mpoints]
    for i in range(len(points)):
        for j in range(len(points[i])):
            for k in range(1, len(points[i][j])):
                if points[i][j][k - 1] is None or points[i][j][k] is None:
                    continue
                cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2)


    cv2.imshow("Tracking", frame)
    cv2.imshow("Paint", paintWindow)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
camera.release()
cv2.destroyAllWindows()
