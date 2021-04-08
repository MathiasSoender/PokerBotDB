import multiprocessing as mp
from Bot.Misc.Clickers import Clicker, ClickMaster
from Bot.Main.Loop import loop
from Bot.Misc.MiscActions import MiscActions
from Services.OddsPrecomputedService import pre_computed_service
from Misc.Simulator_package import tree_package, pre_computed_package, click_package

from Simulator_main.training_loop import main_loop


class mainController:
    def __init__(self, num_tables, testing=False):

        self.testing = testing
        self.num_tables = num_tables

        # Processes #
        self.click_service = None
        self.odds_service = None
        self.trainer_service = None
        self.main_jobs = []

        # Queues #
        self.master_click_queue = mp.Queue()
        self.master_loop_queue = mp.Queue()
        self.odds_queue = mp.Queue()
        self.tree_odds_queues = []
        self.click_queues = []
        self.MA_Q = mp.Queue()

        for _ in range(0, num_tables):
            self.tree_odds_queues.append(mp.Queue())
            self.click_queues.append(mp.Queue())

        # Add a final queue for the training service
        self.tree_odds_queues.append((mp.Queue()))
        self.trainer_end_Q = mp.Queue()

    def start_processes(self):
        # Make processes ready:
        self._start_click_service()
        self._start_odds_service()

        if not self.testing:
            self._start_trainer()
        self._start_loops()

    def _start_trainer(self):
        self.trainer_service = mp.Process(target=main_loop, args=(self.tree_odds_queues[-1],
                                                                  self.odds_queue, False, "model_db", None,
                                                                  self.trainer_end_Q,
                                                                  self.num_tables))
        self.trainer_service.start()


    def _start_click_service(self):

        self.click_service = mp.Process(target=ClickMaster, args=(self.click_queues, self.master_click_queue))
        self.click_service.start()

    def _start_odds_service(self):
        self.odds_service = mp.Process(target=pre_computed_service,
                                       args=(self.odds_queue, self.tree_odds_queues, True, "pre_odds"))
        self.odds_service.start()

    def _start_loops(self):
        for ID in range(0, self.num_tables):
            clicker = Clicker(ID, self.click_queues[ID], self.master_click_queue)
            # ...

            if ID == 0:
                MA = MiscActions(clicker, self.MA_Q)
                MA.start()
            self.main_jobs.append(mp.Process(target=loop, args=(clicker, ID, self.master_loop_queue, self.odds_queue,
                                                                self.tree_odds_queues[ID])))
            self.main_jobs[ID].start()

    def stop_processes(self):
        for _ in range(0, self.num_tables * 2):
            self.master_loop_queue.put("stop")

        for job in self.main_jobs:
            job.join()

        self.trainer_end_Q.put("stop")

        if not self.testing:
            self.trainer_service.join()

        self.master_click_queue.put(click_package("stop", 0))
        self.odds_queue.put((pre_computed_package(None, None, None, "stop", None)))
        self.MA_Q.put("stop")

        self.click_service.join()
        self.odds_service.join()

    def pause(self):
        for _ in range(0, self.num_tables):
            self.master_loop_queue.put("pause")
