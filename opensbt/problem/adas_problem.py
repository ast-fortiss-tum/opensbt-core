from dataclasses import dataclass
from typing import Dict
from pymoo.core.problem import Problem
import numpy as np
from opensbt.evaluation.critical import Critical
from opensbt.evaluation.fitness import *
import logging as log

@dataclass
class ADASProblem(Problem):

    def __init__(self,
                 xl: List[float],
                 xu: List[float],
                 scenario_path: str,
                 fitness_function: Fitness,
                 simulate_function,
                 critical_function: Critical,
                 simulation_variables: List[float],
                  simulation_time: float = 10,
                 sampling_time: float = 100,
                 design_names: List[str] = None,
                 objective_names: List[str] = None,
                 problem_name: str = None,
                 other_parameters: Dict = None,
                 approx_eval_time: float = None,
                 do_visualize: bool = False):

        super().__init__(n_var=len(xl),
                         n_obj=len(fitness_function.name),
                         xl=xl,
                         xu=xu)

        assert xl is not None
        assert xu is not None
        assert scenario_path is not None
        assert fitness_function is not None
        assert simulate_function is not None
        assert simulation_time is not None
        assert sampling_time is not None
        assert np.equal(len(xl), len(xu))
        assert np.less_equal(xl, xu).all()
        assert len(fitness_function.min_or_max) == len(fitness_function.name)

        self.fitness_function = fitness_function
        self.simulate_function = simulate_function
        self.critical_function = critical_function
        self.simulation_time = simulation_time
        self.sampling_time = sampling_time
        self.simulation_variables = simulation_variables
        self.do_visualize = do_visualize
  
        if design_names is not None:
            self.design_names = design_names
        else:
            self.design_names = simulation_variables

        if objective_names is not None:
            self.objective_names = objective_names
        else:
            self.objective_names = fitness_function.name

        self.scenario_path = scenario_path
        self.problem_name = problem_name

        if other_parameters is not None:
            self.other_parameters = other_parameters

        if approx_eval_time is not None:
            self.approx_eval_time = approx_eval_time

        self.signs = []
        for value in self.fitness_function.min_or_max:
            if value == 'max':
                self.signs.append(-1)
            elif value == 'min':
                self.signs.append(1)
            else:
                raise ValueError(
                    "Error: The optimization property " + str(value) + " is not supported.")

        self.counter = 0

    def _evaluate(self, x, out, *args, **kwargs):
        self.counter = self.counter + 1
        log.info(f"Running evaluation number {self.counter}")
        try:
            simout_list = self.simulate_function(x, self.simulation_variables, self.scenario_path, sim_time=self.simulation_time,
                                                 time_step=self.sampling_time, do_visualize=self.do_visualize)
        except Exception as e:
            log.info("Exception during simulation ocurred: ")
            # TODO handle exception, terminate, so that results are stored
            raise e
        out["SO"] = []
        vector_list = []
        label_list = []

        for simout in simout_list:
            out["SO"].append(simout)
            vector_fitness = np.asarray(
                self.signs) * np.array(self.fitness_function.eval(simout))
            vector_list.append(np.array(vector_fitness))
            label_list.append(self.critical_function.eval(vector_fitness))

        out["F"] = np.vstack(vector_list)
        out["CB"] = label_list
    # self.counter = self.counter + 1
    # log.info(f"++ Evaluations executed {self.counter*100/(population_size*num_gen)}% ++")

    def is_simulation(self):
        return True