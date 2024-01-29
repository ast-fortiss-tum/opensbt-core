
from ast import List
from pymoo.indicators.hv import *
from pymoo.indicators.igd import *
from opensbt.quality_indicators.metrics.spread import *
from dataclasses import dataclass
import dill
import os
from pathlib import Path
import logging as log 

class Quality(object):

    @staticmethod
    def calculate_hv(result):
        res = result
        problem = res.problem
        hist = res.history
        if hist is not None:
            n_evals, hist_F = res.obtain_history()
            F = res.opt.get("F")
            approx_ideal = F.min(axis=0)
            approx_nadir = F.max(axis=0)
            n_obj = problem.n_obj
            metric_hv = Hypervolume(ref_point=np.array(n_obj * [1.01]),
                                    norm_ref_point=False,
                                    zero_to_one=True,
                                    ideal=approx_ideal,
                                    nadir=approx_nadir)

            hv = [metric_hv.do(_F) for _F in hist_F]
            return EvaluationResult("hv_regional", n_evals, hv)
        else:
            return None

    @staticmethod
    def calculate_hv_hitherto(result):
        res = result
        problem = res.problem
        hist = res.history
        if hist is not None:
            n_evals, hist_F = res.obtain_history_hitherto()
            F = res.opt.get("F")
            approx_ideal = F.min(axis=0)
            approx_nadir = F.max(axis=0)
            n_obj = problem.n_obj
            metric_hv = Hypervolume(ref_point=np.array(n_obj * [1.01]),
                                    norm_ref_point=False,
                                    zero_to_one=True,
                                    ideal=approx_ideal,
                                    nadir=approx_nadir)

            hv = [metric_hv.do(_F) for _F in hist_F]
            return EvaluationResult("hv", n_evals, hv)
        else:
            return None

    @staticmethod
    def calculate_igd(result, input_pf=None):  
        res = result
        hist = res.history
        problem = res.problem
        # provide a pareto front or use a pareto front from other sources
        if input_pf is not None:
            pf = input_pf
        else:
            pf = problem.pareto_front_n_points()
        hist = res.history
        if hist is not None:
            n_evals, hist_F = res.obtain_history_hitherto()
            if pf is not None:
                metric_igd = IGD(pf, zero_to_one=True)
                igd = [metric_igd.do(_F) for _F in hist_F]
                return EvaluationResult("igd",n_evals, igd)
            else:
                log.info("No convergence analysis possible. The Pareto front is not known.")
                return None
        else:
            log.info("No convergence analysis possible. The history of the run is not given.")
            return None


    @staticmethod
    def calculate_sp(result):   
        res = result
        hist = res.history
        problem = res.problem

        if problem.n_obj > 2:
            log.info("Uniformity Delta metric is only available for a 2D objective space.")
            return 0
        if hist is not None:
            n_evals, hist_F = res.obtain_history_hitherto()
            uni = [spread(_F) for _F in hist_F]
            return EvaluationResult("spread",n_evals, uni)
        else:
            log.info("No uniformity analysis possible. The history of the run is not given.")
            return None

@dataclass 
class EvaluationResult(object):
    name: str
    steps: List(float)
    values: List(float)
          
    @staticmethod
    def load(save_folder, name):
        with open(save_folder + os.sep + name, "rb") as f:
            return dill.load(f)      
    
    def persist(self, save_folder: str):
        Path(save_folder).mkdir(parents=True, exist_ok=True)
        with open(save_folder + os.sep + self.name, "wb") as f:
            dill.dump(self, f)
            
    def to_string(self):
        return "name: "+ str(self.name) + "\nsteps: " + str(self.steps) + "\nvalues: " + str(self.values)
