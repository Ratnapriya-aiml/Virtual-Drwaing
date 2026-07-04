import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Black canvas
canvas = np.zeros((720, 1280, 3), np.uint8)

xp, yp = 0, 0
draw_color = (255, 0, 0)  # Blue
brush_thickness = 7
eraser_thickness = 50
drawing_enabled = False

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Blue color range
    lower_blue = np.array([100, 150, 80])
    upper_blue = np.array([140, 255, 255])

    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    mask = cv2.medianBlur(mask, 7)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    x, y = 0, 0  # default pointer

    if contours:
        c = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(c)

        if area > 800:
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            x, y = int(x), int(y)

            if drawing_enabled:
                if xp == 0 and yp == 0:
                    xp, yp = x, y

                thickness = eraser_thickness if draw_color == (0, 0, 0) else brush_thickness
                cv2.line(canvas, (xp, yp), (x, y), draw_color, thickness)
                xp, yp = x, y
        else:
            xp, yp = 0, 0

    # Create black display (only drawing)
    output = canvas.copy()

    # OPTIONAL: show pointer as white dot
    if x != 0 and y != 0:
        cv2.circle(output, (x, y), 8, (255, 255, 255), -1)

    # Toolbar text (on black background)
    cv2.putText(output, "D: Draw", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    cv2.putText(output, "S: Stop", (220, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
    cv2.putText(output, "C: Clear", (390, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)
    cv2.putText(output, "Q: Quit", (580, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

    cv2.imshow("Virtual Drawing (Black Background)", output)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('d'):
        drawing_enabled = True
        xp, yp = 0, 0

    elif key == ord('s'):
        drawing_enabled = False
        xp, yp = 0, 0

    elif key == ord('c'):
        canvas = np.zeros((720, 1280, 3), np.uint8)

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
