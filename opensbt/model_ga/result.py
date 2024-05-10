import numpy as np
from pymoo.core.result import Result
from opensbt import config
from opensbt.model_ga.population import PopulationExtended as Population
from opensbt.model_ga.individual import IndividualSimulated as Individual
from opensbt.utils.sorting import *
import dill
import os
from pathlib import Path
from opensbt.visualization import visualizer
import logging as log

from opensbt.config import RESULTS_FOLDER, WRITE_ALL_INDIVIDUALS, EXPERIMENTAL_MODE
import numpy as np
from utils.sorting import *

class SimulationResult(Result):

    save_folder: str = None #we need to store results for each iteration, so we need to propagate

    def __init__(self) -> None:
        super().__init__()
        self._additional_data = dict()
    
    def obtain_history_design(self):
        hist = self.history
        
        if hist is not None:
            n_evals = []  # corresponding number of function evaluations
            hist_X = []  # the objective space values in each 
            pop = Population()
            for algo in hist:
                n_evals.append(algo.evaluator.n_eval)  # store the number of function evaluations                            
                pop = Population.merge(pop, algo.pop)
                feas = np.where(pop.get("feasible"))[
                    0]  # filter out only the feasible and append and objective space values
                hist_X.append(pop.get("X")[feas])
        else:
            n_evals = None
            hist_X = None
        return n_evals, hist_X
    
    # iteration of first critical solutions found + fitness values
    def get_first_critical(self):
        hist = self.history
        res = Population() 
        iter = 0
        if hist is not None:
            for algo in hist:
                iter += 1
                #n_evals.append(algo.evaluator.n_eval)  # store the number of function evaluations
                opt = algo.opt  # retrieve the optimum from the algorithm
                crit = np.where((opt.get("CB"))) [0] 
                feas = np.where((opt.get("feasible"))) [0] 
                feas = list(set(crit) & set(feas))
                res = opt[feas]
                if len(res) == 0:
                    continue
                else:
                    return iter, res
        return 0, res
    
    def obtain_history(self, critical=False):
        hist = self.history
        if hist is not None:
            n_evals = []  # corresponding number of function evaluations
            hist_F = []  # the objective space values in each generation
            for algo in hist:
                n_evals.append(algo.evaluator.n_eval)  # store the number of function evaluations
                opt = algo.opt  # retrieve the optimum from the algorithm
                if critical:
                    crit = np.where((opt.get("CB"))) [0] 
                    feas = np.where((opt.get("feasible"))) [0] 
                    feas = list(set(crit) & set(feas))
                else:
                    feas = np.where(opt.get("feasible"))[0]  # filter out only the feasible and append and objective space values
                hist_F.append(opt.get("F")[feas])
        else:
            n_evals = None
            hist_F = None
        return n_evals, hist_F

    def obtain_all_population(self):
        all_population = Population()
        hist = self.history
        if hist is not None:
            for generation in hist:
                all_population = Population.merge(all_population, generation.pop)
        return all_population

    def obtain_history_hitherto(self,critical=False, optimal=True, var = "F"):
        hist = self.history
        n_evals = []  # corresponding number of function evaluations
        hist_F = []  # the objective space values in each generation

        all = Population()
        for algo in hist:
            n_evals.append(algo.evaluator.n_eval)
            all = Population.merge(all, algo.pop)  
            if optimal:
                all = get_nondominated_population(all)
            
            if critical:
                crit = np.where((all.get("CB"))) [0] 
                feas = np.where((all.get("feasible")))[0] 
                feas = list(set(crit) & set(feas))
            else:
                feas = np.where(all.get("feasible"))[0]  # filter out only the feasible and append and objective space values
            hist_F.append(all.get(var)[feas])
        return n_evals, hist_F
    
    def persist(self, save_folder):
        Path(save_folder).mkdir(parents=True, exist_ok=True)
        with open(save_folder + os.sep + "result", "wb") as f:
            dill.dump(self, f)

    @staticmethod
    def load(save_folder, name="result"):
        with open(save_folder + os.sep + name, "rb") as f:
            return dill.load(f)
    
    @property
    def additional_data(self):
        return self._additional_data

    def write_results(self, 
                     results_folder = RESULTS_FOLDER, 
                     params=None, 
                     is_experimental=EXPERIMENTAL_MODE,
                     save_folder = None):
        algorithm = self.algorithm

        # WHen algorithm is developed without subclassing pymoos Algorithm,
        # we need to use the explicit algorithm name passed via params

        # if type(algorithm) is Algorithm:
        #     algorithm_name = params["algorithm_name"] 
        # else:
        # 
        algorithm_name = algorithm.__class__.__name__ 
          
        log.info(f"=====[{algorithm_name}] Writing results to: ")

        # we can also pass already the save folder and do not to create it
        if save_folder is None:
            save_folder = visualizer.create_save_folder(self.problem, results_folder, algorithm_name, is_experimental=is_experimental)
        log.info(save_folder)

        if config.BACKUP_PROBLEM:
            visualizer.backup_problem(self, save_folder)
            
        if config.BACKUP_RESULT:
            visualizer.backup_object(self, save_folder, name="result")
        # Mostly for algorithm evaluation relevant
        
        # visualizer.convergence_analysis(self, save_folder)
        # visualizer.hypervolume_analysis(self, save_folder)
        # visualizer.spread_analysis(self, save_folder)
        
        visualizer.write_calculation_properties(self,save_folder,algorithm_name, algorithm_parameters=params)
        visualizer.design_space(self, save_folder)
        visualizer.objective_space(self, save_folder)
        visualizer.optimal_individuals(self, save_folder)
        visualizer.all_critical_individuals(self,save_folder)
        visualizer.write_summary_results(self, save_folder)
        visualizer.write_simulation_output(self,save_folder,
                                           mode= config.MODE_WRITE_SIMOUT,
                                           write_max=config.NUM_SIMOUT_MAX)
        visualizer.plot_timeseries_basic(self,
                               save_folder,
                               mode= config.MODE_PLOT_TIME_TRACES,
                                write_max = config.NUM_PLOT_TIME_TRACES)
        
        visualizer.simulations(self, 
                    save_folder,
                    mode = config.MODE_WRITE_GIF,
                    write_max = config.NUM_GIF_MAX)
        if WRITE_ALL_INDIVIDUALS:
            visualizer.all_individuals(self, save_folder)
        