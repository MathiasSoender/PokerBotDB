import time
import pyautogui as py

from Bot.Readers.misc import change_dir


class waitLoops:
    def __init__(self, ID, clicker):
        self.start_time_im_back = time.time()
        self.start_time_session = time.time()
        self.clicker = clicker

        self.hand = None
        self.conf1 = None
        self.conf2 = None

        if ID == 0:
            self.callBtnRegion = (680, 625, 250, 50)
            self.checkBtnRegion = (650, 625, 130, 50)

            self.leftNumRegion = (433, 456, 25, 30)
            self.rightNumRegion = (486, 456, 28, 30)

            self.blankFlopRegion = (330, 255, 100, 70)
            self.blankTurnRegion = (510, 255, 60, 65)
            self.blankRiverRegion = (570, 250, 70, 75)

        elif ID == 1:
            pass

    def setHand(self, hand, conf1, conf2):
        self.hand = hand
        self.conf1 = conf1
        self.conf2 = conf2

    def beforePreFlop(self):
        print("inside beforePreFlop loop")
        while True:
            self._Im_back()
            change_dir("gameplay")

            Call, Check = self._find_call_check()
            if Call or Check is not None:
                return
            time.sleep(0.25)

    def beforeFlop(self):
        print("inside flop loop")
        time.sleep(0.5)
        while True:
            fold = self._find_hand()

            if fold:
                return "folded"

            else:
                call, check = self._find_call_check()

                if check is not None:
                    return "flop"

                if call is not None:
                    change_dir("gameplay")
                    flop_card = py.locateOnScreen("noFlop.png", confidence=0.9, region=self.blankFlopRegion)
                    if flop_card is None:
                        return "flop"
                    else:
                        return "preflop"

            time.sleep(0.5)




    def beforeTurn(self):
        print("in turn loop")

        while True:
            fold = self._find_hand()

            if fold:
                return "folded"

            else:
                call, check = self._find_call_check()

                if check is not None:
                    return "turn"

                if call is not None:
                    change_dir("gameplay")
                    turn_card = py.locateOnScreen("noTurn.png", confidence=0.9, region=self.blankTurnRegion)

                    if turn_card is None:
                        return "turn"
                    else:
                        return "flop"

            time.sleep(0.5)

    def beforeRiver(self):
        print("in river loop")
        while True:
            fold = self._find_hand()

            if fold:
                return "folded"

            else:
                call, check = self._find_call_check()

                if check is not None:
                    return "river"

                if call is not None:
                    change_dir("gameplay")
                    river_card = py.locateOnScreen("noRiver.png", confidence=0.9, region=self.blankRiverRegion)

                    if river_card is None:
                        return "river"
                    else:
                        return "turn"

            time.sleep(0.5)

    def afterRiver(self):
        print("in river after loop")

        while True:
            fold = self._find_hand()

            if fold:
                return "folded"
            else:
                call, _ = self._find_call_check()

                if call is not None:
                    return "river"

            time.sleep(0.5)



    def _Im_back(self):
        change_dir("lobby")
        if time.time() - self.start_time_im_back > 10:
            im_back = py.locateCenterOnScreen("back.png", confidence=0.95, grayscale=True, region=(0, 0, 960, 1000))
            if im_back is not None:
                self.clicker.im_back()
            self.start_time_im_back = time.time()

    def _find_hand(self):
        change_dir("cards")
        T1 = py.locateOnScreen(str(self.hand[0].value) + ".png", confidence=self.conf1-0.02,
                               region=self.leftNumRegion, grayscale=True)

        T2 = py.locateOnScreen(str(self.hand[1].value) + ".png", confidence=self.conf2-0.02,
                               region=self.rightNumRegion, grayscale=True)

        return T1 is None or T2 is None

    def _find_call_check(self):
        change_dir("gameplay")
        call = py.locateOnScreen("call.png", confidence=0.80, region=self.callBtnRegion, grayscale=True)
        check = py.locateOnScreen("check.png", confidence=0.80, region=self.checkBtnRegion, grayscale=True)

        return call, check

if __name__ == "__main__":
    W = waitLoops(0,None)
    time.sleep(1)
    print(W._find_call_check())
    print(py.locateOnScreen("noRiver.png", confidence=0.9, region=W.blankRiverRegion))

