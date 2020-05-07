import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar


def decode(im):
    decodedobjects = pyzbar.decode(im)
    for obj in decodedobjects:
        print('type: ',obj.type)
        print("data: ",obj.data,"\n")
    return decodedobjects


def display(im, decodedObjects):
    # Loop over all decoded objects
    found = False
    for decodedObject in decodedObjects:
        points = decodedObject.polygon

        # If the points do not form a quad, find convex hull
        if len(points) > 4:
            hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
            hull = list(map(tuple, np.squeeze(hull)))
        else:
            hull = points;

        # Number of points in the convex hull
        n = len(hull)

        # Draw the convext hull
        for j in range(0, n):
            cv2.line(im, hull[j], hull[(j + 1) % n], (255, 0, 0), 3)
            found = True

    # Display results
    return im, found
   # cv2.imshow("Results", im);
    #cv2.waitKey(0);
# Main
if __name__ == '__main__':
    # Read image
    im = cv2.imread('../images/qrcodesample.jpeg')
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError("Cannot open webcam")
    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        cv2.imshow('Input', frame)
        decodedObjects = decode(frame)
        frame, found = display(frame, decodedObjects)
        cv2.imshow('Input', frame)
        if found == True:
            cv2.waitKey(0)
            print("Should I save the image?")
        c = cv2.waitKey(1)
        if cv2.getWindowProperty('Input', cv2.WND_PROP_VISIBLE) < 1:
            break
        #if c == 27:
         #   break

    cap.release()
    cv2.destroyAllWindows()

    decodedObjects = decode(im)
    display(im, decodedObjects)