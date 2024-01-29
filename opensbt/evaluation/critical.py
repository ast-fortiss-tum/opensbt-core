from opensbt.simulation.simulator import SimulationOutput
from typing import Tuple
import numpy as np
import math
from typing import List

class Critical():
    @property
    def name(self):
        return self.__class__.__name__

    def eval(self, vector_fitness: np.ndarray, simout: SimulationOutput) -> bool:
        pass


class CriticalAdasExplicitRearCollision(Critical):

    ''' ADAS problems '''
    def eval(self, vector_fitness: List[float], simout: SimulationOutput = None):
        safety_distance = 0.50 # all dimensions, radial, in m

        if simout is not None:
            isCollision = simout.otherParams['isCollision']
        else:
            isCollision = None
        # a) collision occurred (not from the rear) and velocity of ego > 0
        # b) safety distance to pedestrian violated
        if isCollision:
            loc_ego = simout.location["ego"]
            loc_ped = simout.location["other"]
            diff = [np.subtract(pos_e,pos_p) for pos_e, pos_p in zip(loc_ego, loc_ped)]
            distance = np.linalg.norm(diff)
            ind_col= np.argmin(distance)
            dist_x = abs(simout.location["ego"][ind_col][0] - simout.location["other"][ind_col][0])
            raw_dist_y = simout.location["ego"][ind_col][1] - simout.location["other"][ind_col][1]
            if dist_x < simout.otherParams["height"]/2 and raw_dist_y > 0 and vector_fitness[1] < 0:
                return True
            return False
        elif (vector_fitness[0]  - safety_distance <= 0 and vector_fitness[1] < 0):
            return True
        else:
            return False

class CriticalAdasFrontCollisions(Critical):
    def eval(self, vector_fitness, simout: SimulationOutput = None):
        if simout is not None:
            isCollision = simout.otherParams['isCollision']
        else:
            isCollision = None

        if (isCollision == True) or (vector_fitness[0] < 0.5) and (vector_fitness[1] < 0):
            return True
        else:
            return False

class CriticalAdasTTCVelocity(Critical):
    def eval(self, vector_fitness, simout: SimulationOutput = None):
        if simout is not None:
            isCollision = simout.otherParams['isCollision']
        else:
            isCollision = None

        if(isCollision == True) or (vector_fitness[0] < 5) and (vector_fitness[1] < -1):
            return True
        else:
            return False


    '''
        f[0] - min distance ego <-> pedestrian
        f[1] - velocity at time of minimal distance

        # Scenario critical <->

        # a) collision ocurred
        # b) minimal distance between ego and other vehicle < 0.3m
        # c) velcoty at time of minimal distance is > 1 m/s
    '''
class CriticalAdasDistanceVelocity(Critical):
    def eval(self, vector_fitness, simout: SimulationOutput = None):
        if simout is not None:
            isCollision = simout.otherParams['isCollision']
        else:
            isCollision = None

        if(isCollision == True) or (vector_fitness[0] < 0.3) and (vector_fitness[1] < -1):
            return True
        else:
            return False

class CriticalAdasBox(Critical):
    def eval(self, vector_fitness, simout):
        return (vector_fitness[0] < -0.6) and (vector_fitness[1] < -1.5)

class CriticalAdasBoxCollision(Critical):
    def eval(self, vector_fitness, simout: SimulationOutput = None):
        if simout is not None:
            isCollision = simout.otherParams['isCollision']
        else:
            isCollision = False  # if "or"
            # isCollision = True  # if "and"
        # works as a standard critical box function if isCollision not available
        return CriticalAdasBox().eval(vector_fitness) or isCollision
        # "or" or "and"?

''' Test problems '''
class CriticalBnhDivided(Critical):
    def eval(self, vector_fitness: np.ndarray, simout=None):
        return  (vector_fitness[0] < 10 ) and \
                (vector_fitness[1] < 50) and  (vector_fitness[1] > 20) or \
                (vector_fitness[0] < 140 ) and (vector_fitness[0] > 40 )  and \
                (vector_fitness[1] < 7) and  (vector_fitness[1] > 0)  or \
                (vector_fitness[0] < 40 ) and (vector_fitness[0] > 20 )  and \
                (vector_fitness[1] < 20) and  (vector_fitness[1] > 15)

class CriticalBnh(Critical):
    def eval(self, vector_fitness):
        return (vector_fitness[0] < 60) and (vector_fitness[1] < 20)

class CriticalRastrigin(Critical):
    def eval(self, fitness):
        return fitness < 2 and fitness > -2
