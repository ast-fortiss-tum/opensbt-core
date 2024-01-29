import os
import sys
from pathlib import Path

from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter
from pymoo.core.problem import Problem
from pymoo.termination import get_termination
from pymoo.algorithms.soo.nonconvex.pso import PSO
from pymoo.core.population import Population
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.optimize import minimize
from pymoo.termination import get_termination
from opensbt.algorithm.classification.classifier import ClassificationType
from opensbt.algorithm.classification.decision_tree.decision_tree import *
from opensbt.algorithm.optimizer import Optimizer
from opensbt.experiment.search_configuration import SearchConfiguration
import opensbt.quality_indicators.metrics.spread as qi
from opensbt.model_ga.result import *
import logging as log

class PSOOptimizer(Optimizer):

    algorithm_name = "PSO"

    def __init__(self,
                problem: Problem,
                config: SearchConfiguration):

        log.info("Initialized PSO Optimizer")
        
        self.config = config
        self.problem = problem
        self.res = None

        # TODO set other PSO parameters by user
        self.parameters = {
            "Population size" : str(config.population_size),
            "Max number of generations" : str(config.n_generations),
        }

        # initialize algorithm
        self.algorithm = PSO(
            pop_size=config.population_size,
        )

        ''' Prioritize max search time over set maximal number of generations'''
        if config.maximal_execution_time is not None:
            self.termination = get_termination("time", config.maximal_execution_time)
        else:
            self.termination = get_termination("n_gen", config.n_generations)

        self.save_history = True