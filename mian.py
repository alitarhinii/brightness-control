import cv2 as cv
import numpy as np
import math
from cvzone.HandTrackingModule import HandDetector
import wmi

# Initialize hand detector
detector = HandDetector(detectionCon=0.7)

# Initialize webcam to the size you want in my case i  put it to be a fullscreen display later
wCam, hCam = 1366, 768
cap = cv.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# Create a WMI object to control display brightness
wmi_obj = wmi.WMI(namespace='wmi')

while True:
    success, img = cap.read()

    # Detect hands
    hands, img = detector.findHands(img)

    if hands:
        for hand in hands:
            lmList = hand["lmList"]

            # Get landmarks of thumb tip and index finger tip
            thumb_x, thumb_y = lmList[4][1], lmList[4][2]
            index_x, index_y = lmList[8][1], lmList[8][2]

            # Calculate distance between thumb tip and index finger tip
            length = math.hypot(index_x - thumb_x, index_y - thumb_y)

            # Calculate brightness based on length
            brightness = np.interp(length, [50, 440], [0, 100])

            # Set brightness using WMI
            wmi_method = wmi_obj.WmiMonitorBrightnessMethods()[0]
            # The [0] index is used to access the first monitor in the system. 
            wmi_method.WmiSetBrightness(int(brightness), 0)
            # passing 0 as the second parameter implies that there are no additional flags or options specified for 
            # the brightness adjustment operation.
            

            # Display brightness percentage and hand landmarks
            cv.putText(img, f'Brightness: {int(brightness)}%', (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv.circle(img, (thumb_x, thumb_y), 10, (0, 255, 0), cv.FILLED)
            cv.circle(img, (index_x, index_y), 10, (0, 255, 0), cv.FILLED)
            cv.line(img, (thumb_x, thumb_y), (index_x, index_y), (255, 0, 255), 3)

    cv.imshow("Image", img)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
