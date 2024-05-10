import os

from abc import ABC, abstractclassmethod, abstractmethod

from opensbt.experiment.search_configuration import SearchConfiguration
from opensbt.model_ga.problem import SimulationProblem
from opensbt.model_ga.result import SimulationResult
from pymoo.optimize import minimize

import dill
from opensbt.config import RESULTS_FOLDER, EXPERIMENTAL_MODE, BACKUP_ITERATIONS
from opensbt.visualization.visualizer import create_save_folder, backup_object

class Optimizer(ABC):
    
    algorithm_name: str
    
    parameters: str

    save_folder: str
    
    @abstractmethod
    def __init__(self, problem: SimulationProblem, config: SearchConfiguration):
        ''' Create here the algorithm instance to be used in run '''
        pass

    def run(self) -> SimulationResult:
        # create a backup during the search for each generation
        algorithm = self.algorithm
        algorithm.setup(problem = self.problem, 
                        termination = self.termination,
                        save_history = self.save_history)
        save_folder = create_save_folder(self.problem, 
                                RESULTS_FOLDER,
                                algorithm_name=self.algorithm_name,
                                is_experimental=EXPERIMENTAL_MODE)

        while(algorithm.termination.do_continue()):
            algorithm.next()
            if BACKUP_ITERATIONS:
                n_iter = algorithm.n_iter - 1
                backup_object(algorithm, 
                              save_folder, 
                              name = f"algorithm_iteration_{n_iter}")

        res = algorithm.result()
        self.save_folder = save_folder
        return res