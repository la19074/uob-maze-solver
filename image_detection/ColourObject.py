import cv2
import numpy as np

cap = cv2.VideoCapture(0)
#cap.set(cv2.CAP_PROP_FPS, 10)

while True:
    _, frame1 = cap.read()
    frame = frame1[6:480, 62: 606]
    Gauss_frame = cv2.GaussianBlur(frame, (5, 5), 0)
    hsv_frame = cv2.cvtColor(Gauss_frame, cv2.COLOR_BGR2HSV)
    """
    # Red color
    low_red = np.array([161, 155, 84])
    high_red = np.array([179, 255, 255])
    red_mask = cv2.inRange(hsv_frame, low_red, high_red)
    red = cv2.bitwise_and(frame, frame, mask=red_mask)
    """
    # Blue color
    low_blue = np.array([94, 80, 2])
    high_blue = np.array([126, 255, 255])
    blue_mask = cv2.inRange(hsv_frame, low_blue, high_blue)
    blue = cv2.bitwise_and(frame, frame, mask=blue_mask)
    """
    # Green color
    low_green = np.array([25, 52, 72])
    high_green = np.array([102, 255, 255])
    green_mask = cv2.inRange(hsv_frame, low_green, high_green)
    green = cv2.bitwise_and(frame, frame, mask=green_mask)
    """
    contours, _ = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 0:
        #np.array([])
        Active = False

    # ((x, y), radius) = cv2.minEnclosingCircle(c)
    #centers = np.zeros((len(contours), 2), dtype=np.int32)
    for i, c in enumerate(contours):
        area = cv2.contourArea(c)
        M = cv2.moments(c)  # Moment calculation required to get centre
        if M["m00"] != 0 and area > 100:
            Active = True
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))   # Equation to get centre of contour
            NewCenter = np.array(((center[0] / 1.6265), (center[1] / 1.608)), dtype=np.int32)
            #print(NewCenter)
        else:
            center = (0, 0)
            Active = False
        #centers[i] = center

    cv2.drawContours(frame, contours, -1, (0, 0, 255), 3)
    print(Active)

    # print(contours)

    cv2.imshow("Frame", frame)
    #cv2.imshow("Red", red)
    cv2.imshow("Blue", blue)
    #cv2.imshow("Green", green)
    # cv2.imshow("Result", result)

    key = cv2.waitKey(1)
    if key == 27:
        break
