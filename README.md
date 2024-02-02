# OpenSBT - A Modular Framework for Search-based Testing of Automated Driving Systems


## Intro

OpenSBT provides a modular and extandable code base to facilitate search-based testing of automated driving systems. It provides interfaces to integrate search algorithms, fitness/criticality functions and simulation environments in a modular way. It allows to visualize testing results and analyse the critical behaviour of the tested system. 

An introductory video of OpenSBT can be found here: https://www.youtube.com/watch?v=qi_CTTzrk5s.


## Overview

<div align="center"><img src="https://github.com/ast-fortiss-tum/opensbt-core/blob/main/docs/figures/OpenSBT_architecture.png?raw=True" width=500 ></div>

OpenSBT builds upon [Pymoo](https://pymoo.org/) 0.6.0 and extends internal optimization related models, such as `Problem`, `Result`, to tailor heuristic search algorithms for testing ADS systems.

## Installation

OpenSBT requires Python to be installed and its compatibality has been tested with Python 3.8. OpenSBT can be run as a standalone application or can be imported as a library.

Installation instructions are available in the following [jupyter notebook](https://git.fortiss.org/opensbt/opensbt-core/-/tree/main/docs/jupyter/01_Installation.ipynb).

## Usage

You can find several tutorials as [jupyter notebooks](https://git.fortiss.org/opensbt/opensbt-core/-/tree/main/docs/jupyter) which explain step-by-step of how to use OpenSBT. In these tutorials, we have integrated:

-  A simplified SUT simulated in very simplistic simulator (linear motion planning, no GPU required) 
-  A real-world FMI-based AEB agent developed in the [fortiss Mobility lab](https://www.fortiss.org/forschung/fortiss-labs/detail/mobility-lab) which is simulated in [CARLA](https://carla.org/) using the simulator adapter [CARLA Runner Extension](https://git.fortiss.org/opensbt/carla-runner).

_Note: We have also implemented a [simulator adapter](https://git.fortiss.org/opensbt/prescan_runner) for testing Simulink-based SUTs in Prescan._


## Output

OpenSBT produces several result artefacts. All artefacts are written into the *results* folder in a folder named as the problem name. 
OpenSBT generates the following outputs:


| Type | Description | Example | 
|:--------------|:-------------|:--------------|
| Design Space Plot | Visualization of all evaluated test cases in the input space + of predicted critical regions using the decision tree algorithm, pairwise. Constraints of derived regions are stored in CSV file [bounds_regions.csv](https://git.fortiss.org/opensbt/opensbt-core/-/tree/main/docs/example/results/single/PedestrianCrossingStartWalk/NSGA2-F/ex1/classification/bounds_regions.csv) and the learned tree in [tree.pdf](https://git.fortiss.org/opensbt/opensbt-core/-/tree/main/docs/example/results/single/PedestrianCrossingStartWalk/NSGA2-F/ex1/classification/tree.pdf) | <img src="https://github.com/ast-fortiss-tum/opensbt-core/blob/main/docs/example/results/single/PedestrianCrossingStartWalk/NSGA2-F/ex1/design_space/orientation_ego_orientation_ped.png?raw=True" alt="Design Space Plot" width="400"/>  |
| Scenario 2D Visualization | Visualization of traces of the ego vehicle and adversaries in a two-dimensional GIF animation | <img src="https://github.com/ast-fortiss-tum/opensbt-core/blob/main/docs/example/results/single/PedestrianCrossingStartWalk/NSGA2-F/ex1/gif/0_trajectory.gif?raw=True" alt="Scenario Visualization" width="300"/> |
Objective Space Plot | Visualization of fitness values of evaluated test cases, pairwise.   | <img src="https://github.com/ast-fortiss-tum/opensbt-core/blob/main/docs/example/results/single/PedestrianCrossingStartWalk/NSGA2-F/ex1/objective_space/Min Adapted Distance_Velocity At Min Adapted Distance.png?raw=True" alt="Objective Space Plot" width="400"/> |
| All Testcases |  CSV file of all test inputs of all evaluated testcases | [all_testcases.csv](https://git.fortiss.org/opensbt/opensbt-core/-/tree/main/docs/example/results/single/PedestrianCrossingStartWalk/NSGA2-F/ex1/all_testcases.csv) |
| All Critical Testcases |  CSV file of all critical test inputs of all evaluated testcases | [all_critical_testcases.csv](https://git.fortiss.org/opensbt/opensbt-core/-/tree/main/docs/example/results/single/PedestrianCrossingStartWalk/NSGA2-F/ex1/all_critical_testcases.csv)|
| Calculation Properties |  CSV file of all experiment configuration parameters (e.g. algorithm parameters, such as population size, number iterations; search space, fitness function etc..).  | [calculation_properties.csv](https://git.fortiss.org/opensbt/opensbt-core/-/tree/main/docs/example/results/single/PedestrianCrossingStartWalk/NSGA2-F/ex1/calculation_properties.csv) |
| Evaluation Results |  CSV file containing performance values of the algorithm, e.g., number critical test cases found in relation to all evaluations, execution time.| [summary_results.csv](https://git.fortiss.org/opensbt/opensbt-core/-/tree/main/docs/example/results/single/PedestrianCrossingStartWalk/NSGA2-F/ex1/summary_results.csv)|



## Application Use Cases

OpenSBT has been already applied:

- For a replication experiment to replicate the results of a surrogate assisted testing technique, s. [here](https://github.com/Leviathan321/reflection_study).
- In an industrial case study to validate a systems behaviour for different operating scenarios, s. [here](https://drive.google.com/file/d/1lr5BZpLFaxotwNFju43WF1C9fUTNM-SS/view?usp=sharing) and here: [https://doi.org/10.1007/978-3-031-46002-9_15](https://doi.org/10.1007/978-3-031-46002-9_15)

## Contribution

If you like to contribute please contact one of the developers listed below or create a pull request. If you face any issue with OpenSBT feel free to create an issue or contact the developers.

## Acknowledgements

OpenSBT has been developed by [Lev Sorokin](mailto:sorokin@fortiss.org), [Tiziano Munaro](mailto:munaro@fortiss.org) and [Damir Safin](mailto:safin@fortiss.org) within the 
[FOCETA Project](https://www.foceta-project.eu/tools/). Special thanks go to [Brian Hsuan-Cheng Liao](mailto:h.liao@eu.denso.com) and Adam Molin from [DENSO AUTOMOTIVE Deutschland GmbH](https://www.denso.com/de/de/about-us/company-information/dnde/) for their valuable feedback and evaluation of OpenSBT on the AVP Case Study in the Prescan simulator.

## Reference

If you use or extend OpenSBT please cite our framework. Here is an example BibTeX entry:

```bibtex
@misc{sorokin2023opensbt,
      title={OpenSBT: A Modular Framework for Search-based Testing of Automated Driving Systems}, 
      author={Lev Sorokin and Tiziano Munaro and Damir Safin and Brian Hsuan-Cheng Liao and Adam Molin},
      year={2023},
      eprint={2306.10296},
      archivePrefix={arXiv},
      primaryClass={cs.SE}
}
```
## License

OpenSBT is licensed under the [Apache License, Version 2.0](LICENSE).
