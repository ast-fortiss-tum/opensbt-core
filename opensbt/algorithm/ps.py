

import pymoo

from opensbt.model_ga.individual import IndividualSimulated
pymoo.core.individual.Individual = IndividualSimulated

from opensbt.model_ga.population import PopulationExtended
pymoo.core.population.Population = PopulationExtended

from opensbt.model_ga.result  import SimulationResult
pymoo.core.result.Result = SimulationResult

from opensbt.model_ga.problem import SimulationProblem
pymoo.core.problem.Problem = SimulationProblem

from pymoo.core.algorithm import Algorithm
from opensbt.algorithm.optimizer import Optimizer

import os
import sys
from pathlib import Path
from typing import List

from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter
from pymoo.core.problem import Problem
from pymoo.termination import get_termination
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.population import Population
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.operators.sampling.lhs import LHS
from pymoo.optimize import minimize
from pymoo.termination import get_termination
from opensbt.algorithm.classification.classifier import ClassificationType
from opensbt.algorithm.classification.decision_tree.decision_tree import *
from opensbt.evaluation.critical import Critical
from opensbt.experiment.search_configuration import DefaultSearchConfiguration, SearchConfiguration
from opensbt.problem.pymoo_test_problem import PymooTestProblem
from opensbt.simulation.simulator import SimulationOutput
from opensbt.visualization import visualizer
import opensbt.quality_indicators.metrics.spread as qi
import logging as log
from opensbt.utils.evaluation import evaluate_individuals
from opensbt.model_ga.result import *
import time

class PureSampling(Optimizer):
    
    algorithm_name = "RS"

    def __init__(self,
                problem: Problem,
                config: SearchConfiguration,
                sampling_type = FloatRandomSampling):

        self.config = config
        self.problem = problem
        self.res = None
        self.sampling_type = sampling_type
        self.sample_size = config.population_size
        self.n_splits = 10 # divide the population by this size 
                         # to make the algorithm iterative for further analysis
        self.parameters = { 
                            "sample_size" : self.sample_size
        }
        log.info(f"Initialized algorithm with config: {config.__dict__}")

    def run(self) -> SimulationResult:

        problem = self.problem
        sample_size = self.sample_size
        sampled = self.sampling_type()(problem,sample_size)
        n_splits = self.n_splits
        start_time = time.time()

        pop = evaluate_individuals(sampled, problem)

        execution_time = time.time() - start_time

        # create result object

        self.res = PureSampling.create_result(problem, pop, execution_time, n_splits)
        
        return self.res 
    
    def create_result(problem, pop, execution_time, n_splits):
        res_holder = SimulationResult()
        res_holder.algorithm = Algorithm()
        res_holder.algorithm.pop = pop
        res_holder.algorithm.evaluator.n_eval = len(pop)
        res_holder.problem = problem
        res_holder.algorithm.problem = problem
        res_holder.exec_time = execution_time
        res_holder.opt = get_nondominated_population(pop)
        res_holder.algorithm.opt = res_holder.opt

        res_holder.history = []  # history is the same instance 
        n_bucket = len(pop) // n_splits
    
        pop_sofar = 0
        for i in range(0,n_splits):
            
            algo = Algorithm()
            algo.pop = pop[(i*n_bucket):min((i+1)*n_bucket,len(pop))]
            pop_sofar += len(algo.pop)
            algo.evaluator.n_eval = pop_sofar
            algo.opt = get_nondominated_population(algo.pop)
            res_holder.history.append(algo)
        
        return res_holder

    # def write_results(self, results_folder = RESULTS_FOLDER, params=None):
    #     algorithm_name = self.algorithm_name
    #     if self.res is None:
    #         log.info("Result object is None. Execute algorithm first, before writing results.")
    #         return
    #     log.info(f"=====[{ALGORITHM_NAME}] Writing results...")
    #     config = self.config
    #     res = self.res
    
    #     save_folder = visualizer.create_save_folder(res.problem, results_folder, algorithm_name)
        
    #     # Analysis
    #     visualizer.convergence_analysis(self, save_folder)
    #     visualizer.hypervolume_analysis(self, save_folder)
    #     visualizer.spread_analysis(self, save_folder)
        
    #     # Basis Output
    #     visualizer.write_calculation_properties(res,save_folder,algorithm_name,params)
    #     visualizer.design_space(res, save_folder)
    #     visualizer.objective_space(res, save_folder)
    #     visualizer.optimal_individuals(res, save_folder)
    #     visualizer.write_summary_results(res, save_folder)
    #     visualizer.write_simulation_output(res,save_folder)
    #     visualizer.simulations(res, save_folder)
    #     visualizer.all_critical_individuals(res, save_folder)

    #     if WRITE_ALL_INDIVIDUALS:
    #         visualizer.all_individuals(res, save_folder)

    #     #persist results object
    #     res.persist(save_folder + "backup")
