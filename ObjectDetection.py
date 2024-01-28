import cv2
import numpy as np

cap = cv2.VideoCapture(r"C:\Users\shiva\Downloads\video.mp4")
min_width_react = 80
min_height_react = 80
algo = cv2.createBackgroundSubtractorMOG2()

def center_handle(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx, cy

detect_left = []
detect_right = []
offset = 6
counter_left = 0
counter_right = 0

# Define the left and right side rectangles
left_rectangle = (50, 300, 600, 700)  # Adjust these coordinates as needed
right_rectangle = (700, 300, 1100, 700)  # Adjust these coordinates as needed
large_rectangle = (0, 0, 1850, 1080)  # Adjust these coordinates as needed

while True:
    ret, frame = cap.read()
    if not ret:
        break

    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(grey, (3, 3), 5)
    img_sub = algo.apply(blur)
    dilat = cv2.dilate(img_sub, np.ones((5, 5)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilatada = cv2.morphologyEx(dilat, cv2.MORPH_CLOSE, kernel)
    dilatada = cv2.morphologyEx(dilatada, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(dilatada, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Default values in case no contours are found
    x, y, w, h = 0, 0, 0, 0

    for (i, c) in enumerate(contours):
        x, y, w, h = cv2.boundingRect(c)
        validate_counter = (w >= min_width_react) and (h >= min_height_react)
        if not validate_counter:
            continue

        # Reduce the width and height of the bounding rectangle
        w = int(w * 0.8)  # Adjust the factor (0.8) as needed
        h = int(h * 0.8)

        center = center_handle(x, y, w, h)

        # Check if the center is within the left and right rectangles
        if (left_rectangle[0] < center[0] < left_rectangle[2] and
                left_rectangle[1] < center[1] < left_rectangle[3] and
                large_rectangle[0] < center[0] < large_rectangle[2] and
                large_rectangle[1] < center[1] < large_rectangle[3]):
            # Check if the vehicle is already in the detect_left list
            vehicle_detected = False
            for (cx, cy) in detect_left:
                if abs(cx - center[0]) < offset and abs(cy - center[1]) < offset:
                    vehicle_detected = True
                    break
            if not vehicle_detected:
                detect_left.append(center)
                counter_left += 1
                cv2.putText(frame, "Left Vehicle Counter: " + str(counter_left), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                print("Left Vehicle Counter: " + str(counter_left))

        elif (right_rectangle[0] < center[0] < right_rectangle[2] and
                right_rectangle[1] < center[1] < right_rectangle[3] and
                large_rectangle[0] < center[0] < large_rectangle[2] and
                large_rectangle[1] < center[1] < large_rectangle[3]):
            # Check if the vehicle is already in the detect_right list
            vehicle_detected = False
            for (cx, cy) in detect_right:
                if abs(cx - center[0]) < offset and abs(cy - center[1]) < offset:
                    vehicle_detected = True
                    break
            if not vehicle_detected:
                detect_right.append(center)
                counter_right += 1
                cv2.putText(frame, "Right Vehicle Counter: " + str(counter_right), (700, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                print("Right Vehicle Counter: " + str(counter_right))

    # Draw the left, right, and large rectangles
    cv2.rectangle(frame, (left_rectangle[0], left_rectangle[1]), (left_rectangle[2], left_rectangle[3]), (0, 255, 0), 2)
    cv2.rectangle(frame, (right_rectangle[0], right_rectangle[1]), (right_rectangle[2], right_rectangle[3]), (0, 0, 255), 2)
    cv2.rectangle(frame, (large_rectangle[0], large_rectangle[1]), (large_rectangle[2], large_rectangle[3]), (255, 0, 0), 2)

    cv2.imshow("Detector", frame)
    if cv2.waitKey(1) == 13:
        break

cv2.destroyAllWindows()
cap.release()
