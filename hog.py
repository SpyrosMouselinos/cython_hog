import cv2
import wget
import os

if not os.path.exists('./haarcascade_frontalface_default.xml'):
    wget.download("https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml")

# Load the cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
font = cv2.FONT_HERSHEY_SIMPLEX 
# fontScale 
fontScale = 1
# To capture video from webcam. 
cap = cv2.VideoCapture(0)
# Blue color in BGR 
color = (255, 0, 0) 
  
# Line thickness of 2 px 
thickness = 2
# To use a video file as input 
# cap = cv2.VideoCapture('filename.mp4')
message = 'Start...'
prev_x = 0
prev_y = 0
while True:
    # Read the frame
    _, img = cap.read()
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect the faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    # Draw the rectangle around each face
    candidate_tuple = None
    w_max = 0
    h_max = 0
    x_cand = 0
    y_cand = 0
    for (x, y, w, h) in faces:
        if w > w_max and h > h_max:
            x_cand = x
            y_cand = y
            w_max = w
            h_max = h
    cv2.rectangle(img, (x_cand, y_cand), (x_cand+w_max, y_cand+h_max), (255, 0, 0), 2)

    if x_cand > prev_x + 10:
        message = 'Right'
    elif x_cand < prev_x - 10:
        message = 'Left'
    else:
        message=''

    prev_x = x_cand
    # Display
    img = img[y_cand:y_cand+h_max, x_cand:x_cand+w_max]
    img = cv2.putText(img, f'{message}', (50, 50), font,  
                fontScale, color, thickness, cv2.LINE_AA) 
    try:
        cv2.imshow('img', img )
    except:
        pass
    # Stop if escape key is pressed
    k = cv2.waitKey(30) & 0xff
    if k==27:
        break
# Release the VideoCapture object
cap.release()