from abc import ABC, abstractclassmethod, abstractmethod

from opensbt.experiment.search_configuration import SearchConfiguration
from opensbt.model_ga.problem import SimulationProblem
from opensbt.model_ga.result import SimulationResult
from pymoo.optimize import minimize

class Optimizer(ABC):
    
    algorithm_name: str
    
    parameters: str

    @abstractmethod
    def __init__(self, problem: SimulationProblem, config: SearchConfiguration):
        ''' Create here the algorithm instance to be used in run '''
        pass

    def run(self) -> SimulationResult:
        return minimize(self.problem,
                self.algorithm,
                self.termination,
                save_history=self.save_history,
                verbose=True)