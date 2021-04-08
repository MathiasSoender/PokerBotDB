# Clicker function, must work with multiple processes.
# ID 0 = Left, ID 1 = Right
import time
from Bot.Misc.MouseMover import HumanMovementCreator as HMC
import pyautogui as p

import random

from Bot.Readers.misc import change_dir
from Misc.Simulator_package import click_package


class Clicker:
    def __init__(self, ID, own_queue, click_Q):
        self.ID = ID
        self.click_Q = click_Q
        self.own_queue = own_queue

        if ID == 0:
            self.speed = 1
            self.X = 0
        else:
            self.speed = 2
            # Change to correct!
            self.X = 0

    def request_lock(self):
        self.click_Q.put(click_package("get", self.ID))
        self.own_queue.get()

    def return_lock(self):
        self.own_queue.put(201)

    def get_uniform(self, uniform):
        if self.ID == 1:
            return random.uniform(1 - uniform / 2, 1 + uniform / 2)
        else:
            return random.uniform(1 - uniform, 1 + uniform)

    def bet1(self, open=True):

        if open:
            self.press_key("a")
        else:
            self.request_lock()

            HMC((673 + self.X) * self.get_uniform(0.01), 567 * self.get_uniform(0.01),
                random.randint(6, 9) * self.speed)
            time.sleep(random.uniform(0.05, 0.4))
            p.click()
            time.sleep(random.uniform(0.1, 0.3))
            self._raise()
            self.return_lock()

    def bet2(self, open=True):
        if open:
            self.press_key("s")
        else:
            self.request_lock()

            HMC((753 + self.X) * self.get_uniform(0.01), 565 * self.get_uniform(0.01),
                random.randint(6, 9) * self.speed)
            time.sleep(random.uniform(0.05, 0.4))
            p.click()
            time.sleep(random.uniform(0.1, 0.3))
            self._raise()
            self.return_lock()

    def _raise(self):
        # Assume lock is already acquired
        HMC((872 + self.X) * self.get_uniform(0.05), 654 * self.get_uniform(0.03),
            random.randint(6, 9) * self.speed)
        time.sleep(random.uniform(0.1, 0.3))
        p.click()

    def fold(self):
        self.request_lock()
        HMC((558 + self.X) * self.get_uniform(0.05), 656 * self.get_uniform(0.03),
            random.randint(6, 9) * self.speed)
        time.sleep(random.uniform(0.05, 0.4))
        p.click()
        self.return_lock()

    def max(self):
        self.request_lock()
        change_dir("gameplay")
        self.press_image("max.png", 0.001, 0.001)
        time.sleep(random.uniform(0.1, 0.3))
        self._raise()
        self.return_lock()

    def call(self):
        self.request_lock()
        change_dir("gameplay")
        self.press_image("call.png", 0.015, 0.015)
        self.return_lock()

    def check(self):
        self.request_lock()
        HMC((718 + self.X) * self.get_uniform(0.05), 659 * self.get_uniform(0.03),
            random.randint(6, 9) * self.speed)
        time.sleep(random.uniform(0.05, 0.4))
        p.click()
        self.return_lock()

    def session_summary(self):
        self.request_lock()
        change_dir("lobby")
        self.press_image("keepPlay.png", 0.01, 0.01)
        self.return_lock()

    def im_back(self):
        self.request_lock()
        change_dir("lobby")
        self.press_image("back.png", 0.01, 0.01)
        self.return_lock()

    def press_key(self, key):
        self.request_lock()

        if self.ID == 0:
            if p.position()[0] > 900 or p.position()[1] >= 700:
                HMC(490 * random.uniform(0.5, 1.5), 280 * random.uniform(0.8, 1.2), random.randint(8, 12))
                time.sleep(random.uniform(0.1, 0.25))
        else:
            if p.position()[0] < 900 or p.position()[1] >= 700:
                HMC(1400 * random.uniform(0.8, 1.2), 280 * random.uniform(0.8, 1.2), random.randint(8, 12))
                time.sleep(random.uniform(0.1, 0.25))

        p.keyDown(key)
        time.sleep(random.uniform(0.05, 0.1))
        p.keyUp(key)

        self.return_lock()

    def start_game(self):
        self.request_lock()
        change_dir("lobby")
        self.press_image("play.png", 0.01, 0.01)
        self.return_lock()

    def pause(self):
        self.request_lock()
        # Press exit
        HMC((925 + self.X) * self.get_uniform(0.01), 19 * self.get_uniform(0.01), random.randint(6, 9) * self.speed)
        time.sleep(random.uniform(0.05, 0.4))
        p.click()
        change_dir("lobby")
        time.sleep(random.uniform(1, 2))

        self.press_image("leaveNow.png", 0.01, 0.01)
        self.return_lock()

    def press_image(self, image, uniform_x, uniform_y, Grayscale=True, Conf=0.85):

        if self.ID == 0:
            im_location = p.locateCenterOnScreen(image, confidence=Conf, grayscale=Grayscale, region=(0, 0, 960, 1079))
        else:
            uniform_x /= 2
            im_location = p.locateCenterOnScreen(image, confidence=Conf, grayscale=Grayscale,
                                                 region=(955, 0, 960, 1079))

        if im_location is not None:
            HMC(im_location[0] * random.uniform(1 - uniform_x, 1 + uniform_x),
                im_location[1] * random.uniform(1 - uniform_y, 1 + uniform_y),
                random.randint(6, 9) * self.speed)
            time.sleep(random.uniform(0.1, 0.3))
            p.click()
            return True

        return False


def ClickMaster(Click_channels, Click_queue):
    # Grab the first request for lock
    while True:
        res = Click_queue.get()
        if res.request == "get":
            Click_channels[res.ID].put(200)
            time.sleep(1)
            Click_channels[res.ID].get()

        elif res.request == "stop":
            return


if __name__ == "__main__":
    import multiprocessing as mp

    click_queues = []
    click_queues.append(mp.Queue())
    master_click_queue = mp.Queue()

    click_service = mp.Process(target=ClickMaster, args=(click_queues, master_click_queue))
    click_service.start()

    clicker = Clicker(0, click_queues[0], master_click_queue)
    clicker.pause()
    master_click_queue.put(click_package("stop", None))
