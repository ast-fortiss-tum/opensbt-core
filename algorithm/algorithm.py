from enum import Enum

''' Define here all available algorithms to be triggered via number in -a flag.'''

class AlgorithmType(Enum):
    NSGAII = 1
    PSO = 2 
    NSGAIIDT = 3
