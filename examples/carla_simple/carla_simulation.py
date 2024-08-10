from pathlib import Path
import sys
from typing import List, Dict
from examples.carla_simple.carla_runner.src.carla_simulation import balancer
from opensbt.simulation.simulator import Simulator, SimulationOutput
import logging
import json
import os

SCENARIO_DIR = "/tmp/scenarios"

class CarlaSimulator(Simulator):

    ''' Simulates a set of scenarios and returns the output '''
    @staticmethod
    def simulate(
        list_individuals,
        variable_names,
        scenario_path: str,
        sim_time: float,
        time_step:float,
        do_visualize:bool = False
    ) -> List[SimulationOutput]:
        xosc = scenario_path
        try:
            for ind in list_individuals:
                logging.info("provided following values:")
                instance_values = [v for v in zip(variable_names,ind)]
                logging.info(instance_values)
                CarlaSimulator.create_scenario_instance_xosc(xosc, dict(instance_values), outfolder=SCENARIO_DIR)
            logging.info("++ running scenarios with carla ++ ")
            outs = balancer.run_scenarios(scenario_dir=SCENARIO_DIR, visualization_flag=do_visualize)
            results = []
            for out in outs:
                simout = SimulationOutput.from_json(json.dumps(out))
                #print(f"len(simout.collisions): {len(simout.collisions)}")
                simout.otherParams["isCollision"] = (len(simout.collisions) != 0)
                results.append(simout)
        except Exception as e:
            raise e
        finally:
            logging.info("++ removing temporary scenarios ++")
            file_list = [ f for f in os.listdir(SCENARIO_DIR) if f.endswith(".xosc") ]
            for f in file_list:
                os.remove(os.path.join(SCENARIO_DIR, f))
        return results

    ''' Replace parameter values in parameter declaration section by provided parameters '''
    @staticmethod
    def create_scenario_instance_xosc(filename: str, values_dict: Dict, outfolder=None):
    
        import xml.etree.ElementTree as ET
        xml_tree = ET.parse(filename)
    
        parameters = xml_tree.find('ParameterDeclarations')
        for name, value in values_dict.items():
            for parameter in parameters:
                if parameter.attrib.get("name") == name:
                    parameter.attrib["value"] = str(value)
            
        # # Write the file out again
        if outfolder is not None:
            Path(outfolder).mkdir(parents=True, exist_ok=True)
            filename = outfolder + os.sep + os.path.split(filename)[1]
        splitFilename =  os.path.splitext(filename)
        newPathPrefix = splitFilename[0]
        ending = splitFilename[1]

        suffix = ""
        for k,v in values_dict.items():
            suffix = suffix + "_" + str(v)
        
        newFileName  = newPathPrefix + suffix + ending
        xml_tree.write(newFileName)

        return newFileName
