import multiprocessing as mp
from Misc.Simulator_package import tree_package
from Services.OddsPrecomputedService import pre_computed_service
from Misc.Simulator_package import pre_computed_package
from Tree.Tree import Tree


class LoopController:
    def __init__(self, cores, target_func, new_tree, path,human_vs_bot = False):
        self.data_comms = []
        self.pre_computed_Q = mp.Queue()
        self.result_Q = mp.Queue()
        self.end_Q = mp.Queue()

        self.new_tree = new_tree
        self.path = path


        self.jobs = []
        self.cores = cores
        self.MAIN = target_func

        self.pre_computed_service = None

        self.human_vs_bot = human_vs_bot



    """ Initial start. """
    def start(self):

        for i in range(0, self.cores):
            Queue = mp.Queue()
            self.data_comms.append(Queue)
            if not self.human_vs_bot:
                self.jobs.append(self.start_proc(i))

        self.pre_computed_service = mp.Process(target = pre_computed_service,
                                               args = (self.pre_computed_Q, self.data_comms))
        self.pre_computed_service.start()


    """ Spins up a process. """
    def start_proc(self, ID):
        p = mp.Process(target=self.MAIN, args=(self.data_comms[ID], self.pre_computed_Q, self.new_tree, self.path,
                                               self.result_Q, self.end_Q, ID))
        p.start()
        return p



    def close_processes(self):
        print("Shutting down processes")
        for _ in range(0, 10):
            self.end_Q.put("stop")

        for j in self.jobs:
            j.join()
        self.pre_computed_Q.put((pre_computed_package(None, None, None, "stop", None)))
        self.pre_computed_service.join()





