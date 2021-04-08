from threading import Thread

from Bot.Readers.misc import change_dir
import time
import pyautogui as py

class MiscActions(Thread):
    def __init__(self, Clicker, Q = None):
        super(MiscActions, self).__init__()

        self.Clicker = Clicker
        self.Q = Q
        self.start_time_session = time.time()


    def run(self):
        while True:
            if time.time() - self.start_time_session > 1:
                change_dir("lobby")
                senssion_summary = py.locateCenterOnScreen("keepPlay.png", confidence=0.85, grayscale=True)

                if senssion_summary is not None:
                    self.Clicker.session_summary()

                self.start_time_session = time.time()

            if not self.Q.empty():
                return

            time.sleep(1)









