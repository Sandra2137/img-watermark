import cv2
import numpy as np
import urllib.request 
from urllib.request import Request

### --- Creating watermark img --- ###

image = cv2.imread('pytlog.png', cv2.IMREAD_UNCHANGED)
image[np.where(np.all(image[..., :3] == 255, -1))] = 0

scale_percent = 10
width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)
dim = (width, height)
resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

bgra = cv2.cvtColor(resized, cv2.COLOR_BGR2BGRA) 
bgra[...,3] = 127

cv2.imwrite('result.png', bgra)

### --- Reading url and watermarking --- ##

req = Request(
    url = input('Paste url of the photo you want to watermark: '),
    headers={'User-Agent': 'Mozilla/5.0'}
)

url_response = urllib.request.urlopen(req)
bottom_photo = cv2.imdecode(np.array(bytearray(url_response.read()), dtype=np.uint8), -1)


logo = cv2.imread("result.png") 
h_logo, w_logo, _ = logo.shape 
h_img, w_img, _ = bottom_photo.shape 

center_x = w_img // 2
center_y = h_img // 2
top_y = center_y - h_logo // 2
bottom_y = top_y + h_logo
left_x = center_x - w_logo // 2
right_x = left_x + w_logo


waterm = bottom_photo[top_y:bottom_y, left_x:right_x] 
result = cv2.addWeighted(waterm, 1, logo, 0.5, 0) 
bottom_photo[top_y:bottom_y, left_x:right_x] = result 
cv2.imwrite("watermarked.jpg", bottom_photo) 
cv2.imshow("Watermarked Image", bottom_photo) 

cv2.waitKey(0) 
cv2.destroyAllWindows() 

