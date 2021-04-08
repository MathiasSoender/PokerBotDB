import pyautogui as p
import pytesseract
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def handle_raw(data):
    print(data)
    if not "$" in data:
        return 0
    stop = False
    idx = 0
    real_data = ""

    if "$" in data:
        processed = data.split("$")[-1]
    elif "S" in data:
        processed = data.split("S")[-1]
    else:
        processed = data.split("$")[-1]

    while not stop:
        try:
            if processed[idx] == ".":
                real_data += "."
            else:
                int(processed[idx])
                real_data += processed[idx]
            idx += 1
        except:
            stop = True

    return float(real_data)


leftBottom = (240, 372, 130, 20)  # Working
leftTop = (252, 234, 110, 20)  # Working
top = (500, 170, 132, 20)  # working
topold = (508, 170, 140, 20)
rightTop = (575, 211, 155, 20)  # working
rightBottom = (600, 372, 160, 20)  # working


# Stack
leftBottomS = (57, 400, 90, 20)  # Working
leftTopS = (89, 197, 90, 20)  # Working
topS = (424, 134, 90, 18)  # working
rightTopS = (804, 199, 90, 20)  # working
rightBottomS = (828, 403, 90, 20)  # working
hero = (475, 520, 90, 20)

im = p.screenshot(region=top)
im.show()
data = pytesseract.image_to_string(im, lang="eng", config='--psm 11 --oem 1')
print(handle_raw(data))


# 10, 11, 12
