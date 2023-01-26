import cv2
import time
import easyocr
import pyautogui
import numpy as np
import keyboard as key
from googletrans import Translator

translator = Translator()
login = 0

def get_screen():
    frame = pyautogui.screenshot()
    frame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
    return frame

def resim_smaller(img):
    scale_percent = 60  # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    img = cv2.resize(img, (width, height))
    return img

def konum_detect(frame,results):
    yazilar = []
    secilen = []
    for res in results:
        top_left = tuple(res[0][0]) # top left coordinates as tuple
        bottom_right = tuple(res[0][2]) # bottom right coordinates as tuple
        # draw rectangle on image
        #cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2) 
        # write recognized text on image (top_left) minus 10 pixel on y
        yazilar.append([res[1],top_left,bottom_right])
    for i in yazilar:
        if(i[0] != "1" and i[0] != "2" and i[0] != "3" and i[0] != "4"):
            secilen.append([i[0],i[1],i[2]])
    g = translator.translate(secilen[0][0], src='tr', dest='en')
    g = g.text.lower().split(' ')
    del secilen[0]
    print(g)
    print(secilen)
    sira = 0
    for i in secilen:
        sira += 1
        for x in g:
            if x == i[0].lower():
                print(sira)
                pyautogui.press(str(sira))


    return frame

def resim_kirmpa(img,y,h,x,w):
    img = img[y:h, x:w]
    return img

reader = easyocr.Reader(['tr','en'])

while True:
     frame = resim_kirmpa(get_screen(),531,1015,683,1974)
     
     if key.is_pressed('s'):
        result = reader.readtext(frame)
        if result != []:
         cv2.imwrite("result.jpg",konum_detect(frame,result))
         time.sleep(0.6)

     
     cv2.imshow('frame', frame)
     if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
