# import cv2, time
#
#
# def video_cam_play(imageroot):
#
#     cap = cv2.VideoCapture(0)
#
#     # Check if the webcam is opened correctly
#     if not cap.isOpened():
#         raise IOError("Cannot open webcam")
#     cv2.startWindowThread()
#     while True:
#         ret, frame = cap.read()
#         frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
#         cv2.imshow('Input', frame)
#
#         c = cv2.waitKey(1)
#         if cv2.getWindowProperty('Input',cv2.WND_PROP_VISIBLE) < 1:
#             break
#         if c == 27:
#             break
#         if c == ord('s'):
#            cv2.imwrite(imageroot+"saved_images/classroom_images/"+str(round(time.time()))+".png",frame)
#
#     cap.release()
#     cv2.destroyAllWindows()

