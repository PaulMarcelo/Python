import cv2
import numpy as np

img = cv2.imread("D:/Python/blur-detection/2.jpg", cv2.COLOR_BGR2GRAY)

laplacian_var = cv2.Laplacian(img, cv2.CV_64F).var()

if laplacian_var < 12:
    print("Image blurry")

print("Value: ",laplacian_var)

#cv2.imshow("Img", img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
