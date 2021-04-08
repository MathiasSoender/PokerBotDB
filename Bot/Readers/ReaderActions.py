import pyautogui as py
import pytesseract
import time


class ReaderActions:
    def __init__(self, ID):
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

        self.bets = [0] * 5
        if ID == 0:
            self.leftBottom = (240, 372, 130, 20)
            self.leftTop = (252, 234, 110, 20)
            self.top = (500, 170, 132, 20)
            self.rightTop = (575, 211, 155, 20)
            self.rightBottom = (600, 372, 150, 20)


        elif ID == 1:
            self.leftBottom = (422 + 954, 427, 36, 40)
            self.leftTop = (483 + 954, 427, 36, 40)
            self.top = (448 + 954, 428, 70, 50)
            self.rightTop = (510 + 954, 428, 70, 50)
            self.rightBottom = (510 + 954, 428, 70, 50)

    def Read(self, player_order, player_folded):
        self.bets = [0] * 5
        all_positions = [self.leftBottom, self.leftTop, self.top, self.rightTop, self.rightBottom]

        for p in range(0, len(player_order)):
            bet = 0
            if not player_folded[p][1]:
                time.sleep(0.1)
                im = py.screenshot(region=all_positions[p])
                bet = self.handle_raw(im)

            self.bets[p] = (player_order[p], bet)

        print("bets are: " + str(self.bets))
        print("returned")
        return

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

            if idx > 100:
                print("reader actions stuck")

        return float(real_data)


if __name__ == "__main__":
    R = ReaderActions(ID=0)
    R.Read(["MP", "CO", "BTN", "SB", "BB"], [False] * 5)
    print(R.bets)
