import cv2
import numpy as np
import time

#laptop camera
cap = cv2.VideoCapture(0)
time.sleep(2)

#currentFrame: id to save file
currentFrame = 0
#zoom in value
zin = 0

def Zoom(cv2Object, zoomSize, dx, dy):
    #original dimensions, notice that "x" is at 1 position and "y" is at 0 position, 
    originalx = cv2Object.shape[1]
    originaly = cv2Object.shape[0]
    
    #first resize the image with zoomSize value, this will give us a larger image
    cv2Object = cv2.resize(cv2Object, None, fx= zoomSize, fy= zoomSize, interpolation= cv2.INTER_LINEAR)
    
    #then, we'll crop the image to the original viewport (original dimensions) to make the zoom effect,
    #in this step we also add dx and dy to move the viewport
    
    #coordinates from upper-left corner to crop the zoom, notice that the tuple startpoint is defined by (x, y)
    startpoint = ((cv2Object.shape[1] - originalx)/2 + dx,(cv2Object.shape[0] - originaly)/2 + dy)
    
    #coordinates from bottom-right corner to crop the zoom, 
    #here, endpoint uses position 0 from startpoint where "x" is saved and position 1 where "y" is saved
    endpoint = (startpoint[0] + originalx, startpoint[1] + originaly)

    #crop with cv2 uses the format obj = obj[start_y:end_y, start_x:end_x] so we use the tuples positions
    cv2Object = cv2Object[int(startpoint[1]): int(endpoint[1]), int(startpoint[0]):int(endpoint[0])]
    return cv2Object

#scale factor
scaleX = 0.5
scaleY = 0.5

#initial pan deltas
dx = 0
dy = 0

#initial pan limits
maxx = 0
maxy = 0

while(True):
    #read frame by frame
    ret, frame = cap.read()
    if not ret:
        print "camera error"
        break
    
    if zin > 0:
        #recalculate pan limits when zooming
        maxx = (frame.shape[0]*zin-frame.shape[0])/2
        maxy = (frame.shape[1]*zin-frame.shape[1])/2
    else:
        #recalculate pan limits to original dimensions
        maxx = frame.shape[0]
        maxy = frame.shape[1]
    
    k = cv2.waitKey(1) 
    if  k == ord('q'):
        #quits
        break
    elif k == ord('g'):
        #save image
        cv2.imwrite('frame'+str(currentFrame)+'.jpg',frame)
    elif k == ord('o') and zin > 0:
        #zoom out, scale factor decreases in 2 and recenter viewport
        zin -= 2
        dx = 0
        dy = 0
    elif k == ord('i'):
        #zoom in
        zin += 2
    elif k == ord('a'):
        #pan left
        if zin > 0:
            dx = dx - 120
    elif k == ord('d'):
        #pan right
        if zin > 0:
            dx = dx + 120
    elif k == ord('w'):
        #pan up
        if zin > 0:
            dy = dy - 120
    elif k == ord('s'):
        #pan down
        if zin > 0:
            dy = dy + 120
    if zin > 0:
        #check if pan values pass the limits, if so, update deltas
        if dx > maxy:
            dx = maxy
        elif dx < (-1*maxy):
            dx = -1*maxy
        if dy > maxx:
            dy = maxx
        elif dy < (-1*maxx):
            dy = -1*maxx
        #call to the Zoom function
        frame = Zoom(frame,zin,dx,dy)
    #shows the image with zoom and pan
    cv2.imshow('Video', frame)

    currentFrame += 1

# release and destroy
cap.release()
cv2.destroyAllWindows()
