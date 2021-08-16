import cv2
import pygame

cam = cv2.VideoCapture(0) #this uses the first or default device camera
pygame.init()
pygame.mixer.init()
sounda = pygame.mixer.Sound("alert.wav")
while cam.isOpened():
    ret, frame1 = cam.read()
    ret, frame2 = cam.read()
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        if cv2.contourArea(c) < 5000:
            # sounda.stop()
            continue
        x, y , w, h = cv2.boundingRect(c)
        cv2.rectangle(frame1, (x,y), (x+w, y+h), (0, 255, 0), 2) #draw rectangle by first capturing the x and y position then multiply the x by width and y by height to get the full rectangle
        sounda.play()
    if cv2.waitKey(10) == ord('q'): # wait 10 nano secs if the q key is pressed then destroy frame
        break
    cv2.imshow('Street Cam', frame1)
