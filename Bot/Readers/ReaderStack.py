import pyautogui as py
import pytesseract
import time

class StackReader:
    def __init__(self, ID):
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        self.stack = 0

        if ID == 0:
            self.position = (475, 520, 90, 20)


    def Read(self):
        im = py.screenshot(region=self.position)
        self.stack = self.handle_raw(im)

    def handle_raw(self, image):
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

        data = pytesseract.image_to_string(image, lang="eng", config='--psm 11 --oem 1')

        if "$" not in data:
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

if __name__ == "__main__":
    R = StackReader(ID=0)
    R.Read()
    print(R.stack)