import cv2
import time

image = cv2.imread('map.jpg')

while(True):
    a = time.time()
    cv2.imshow('image',image)
    #cv2.circle(image,(int(image.shape[1]/2),int(image.shape[0]/2)) , 50, (0,0,255), 4)
    #cv2.line(image,(int(image.shape[1]/2),int(image.shape[0]/2)),(int(image.shape[1]/2 + 100),int(image.shape[0]/2)),(255,255,255), 10)
    k = cv2.waitKey(1) & 0xFF
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    print(time.time()-a)
cv2.destroyAllWindows()        
