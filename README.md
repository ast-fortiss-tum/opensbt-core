<div align="center" style="background: rgb(44,46,57);">
  <img src="./docs/figures/fortiss-openSBT-Logo-RGB-neg-back.png" height="150" style="background-color: rgb(44,46,57);"/>
</div>

# OpenSBT - A Modular Framework for Search-based Testing of Automated Driving Systems


## About

OpenSBT is a modular and extensible codebase designed to facilitate search-based testing of automated driving systems, whether for research, in education or in an industrial context. It provides well-defined interfaces for the integration of search algorithms, fitness functions, testing oracles, and simulation environments in a modular and flexible manner. In addition, OpenSBT supports the visualization of testing results and analysis of the failing behaviour of automated driving systems. 

## Overview

<div align="center"><img src="https://github.com/ast-fortiss-tum/opensbt-core/blob/main/docs/figures/OpenSBT_architecture.png?raw=True" width=500 ></div>

OpenSBT builds upon [Pymoo](https://pymoo.org/) 0.6.0.1 and extends internal optimization related models to tailor heuristic search algorithms for testing automated driving systems. An introductory video of OpenSBT can be found here: https://www.youtube.com/watch?v=qi_CTTzrk5s. Slides to get an overview of search-based software testing are available here: https://linktoslides

## Installation

OpenSBT requires Python to be installed and its compatibility has been tested with Python 3.8. OpenSBT can be run as a standalone application or can be imported as a library.

You can install OpenSBT via pypi:

```bash
pip install opensbt
```

If using as a standalone appplication install the dependencies after downloading OpenSBT files:

```bash
pip install -r requirements.txt
```

A complete installation example is available as a [jupyter notebook](https://git.fortiss.org/opensbt/opensbt-core/-/tree/main/docs/jupyter/01_Installation.ipynb).

## Getting Started

In the core implementation of OpenSBT a simplified dummy simulator is integrated (linear motion planning, no GPU required). To run an example test generation for this example run (flag -e holds the experiment number):

```bash
python run.py -e 5
```

Several result artefacts are generated after the generation has finished. All artefacts are written into the *results* folder in a folder named DummySimulator (problem name). 

You can find several tutorials as [jupyter notebooks](https://git.fortiss.org/opensbt/opensbt-core/-/tree/main/docs/jupyter) which explain step-by-step of how integrate custom simulators and define testing components and objectives in OpenSBT.

The tutorials include as an example the integration of a real-world FMI-based AEB agent developed in the [fortiss Mobility lab](https://www.fortiss.org/forschung/fortiss-labs/detail/mobility-lab) simulated in [CARLA](https://carla.org/) using the simulator adapter [CARLA Runner Extension](https://git.fortiss.org/opensbt/carla-runner).

As another example we have integrated Simulink-based systems simulated in Prescan [simulator adapter](https://git.fortiss.org/opensbt/prescan_runner) into OpenSBT.


## Output

OpenSBT generates a variety of outputs to support the analysis of the system:

### Visualization Outputs
These outputs provide graphical representations of the generated test cases, allowing for intuitive analysis of design and objective spaces.

- **Design Space Plot:** Visualizes all evaluated test cases within the input space, highlighting critical regions predicted by the decision tree algorithm. This plot helps identify input conditions that lead to critical situations. For example, constraints of these regions are saved in [bounds_regions.csv](https://git.fortiss.org/opensbt/opensbt-core/-/tree/main/docs/example/results/single/PedestrianCrossingStartWalk/NSGA2-F/ex1/classification/bounds_regions.csv), and the decision tree can be reviewed in [tree.pdf](https://git.fortiss.org/opensbt/opensbt-core/-/tree/main/docs/example/results/single/PedestrianCrossingStartWalk/NSGA2-F/ex1/classification/tree.pdf).  
  <img src="https://github.com/ast-fortiss-tum/opensbt-core/blob/main/docs/example/results/single/PedestrianCrossingStartWalk/NSGA2-F/ex1/design_space/orientation_ego_orientation_ped.png?raw=True" alt="Design Space Plot" width="400"/> 

- **Scenario 2D Visualization:** Displays the movement of the ego vehicle and adversaries in a 2D space using a GIF animation. This visualization provides insights into the interaction dynamics and can help identify unexpected or unsafe behaviors.
  <img src="https://github.com/ast-fortiss-tum/opensbt-core/blob/main/docs/example/results/single/PedestrianCrossingStartWalk/NSGA2-F/ex1/gif/0_trajectory.gif?raw=True" alt="Scenario Visualization" width="300"/>

- **Objective Space Plot:** Illustrates fitness values of evaluated test cases, allowing a pairwise view of objectives. This plot is useful for understanding how different objectives, such as distance and velocity, interact in the optimization process.
  <img src="https://github.com/ast-fortiss-tum/opensbt-core/blob/main/docs/example/results/single/PedestrianCrossingStartWalk/NSGA2-F/ex1/objective_space/Min%20Adapted%20Distance_Velocity%20At%20Min%20Adapted%20Distance.png?raw=True" alt="Objective Space Plot" width="400"/>


### Data Outputs
These outputs provide structured data for post-processing or detailed analysis.

- **All Test Cases** (`all_testcases.csv`): Lists all input parameters for each evaluated test case. Useful for tracking each scenario generated during testing. [View example](https://git.fortiss.org/opensbt/opensbt-core/-/tree/main/docs/example/results/single/PedestrianCrossingStartWalk/NSGA2-F/ex1/all_testcases.csv).

- **All Critical Test Cases** (`all_critical_testcases.csv`): Stores only critical test cases, focusing on scenarios where the system under test displayed critical behavior. [View example](https://git.fortiss.org/opensbt/opensbt-core/-/tree/main/docs/example/results/single/PedestrianCrossingStartWalk/NSGA2-F/ex1/all_critical_testcases.csv).

### Configuration and Summary Files
These files contain metadata about the test runs and can assist in reproducing or analyzing tests.

- **Calculation Properties** (`calculation_properties.csv`): Provides details on the configuration of each experiment, such as algorithm parameters (population size, iterations), search space, and fitness function. This file is essential for replicating test conditions. [View example](https://git.fortiss.org/opensbt/opensbt-core/-/tree/main/docs/example/results/single/PedestrianCrossingStartWalk/NSGA2-F/ex1/calculation_properties.csv).

- **Evaluation Results** (`summary_results.csv`): Summarizes algorithm performance, including the number of critical cases identified and overall execution time. This file can aid in comparing algorithm efficiency across different configurations. [View example](https://git.fortiss.org/opensbt/opensbt-core/-/tree/main/docs/example/results/single/PedestrianCrossingStartWalk/NSGA2-F/ex1/summary_results.csv).

## Application

Following Simulators have been integrated already into OpenSBT:

- [Prescan]() - [Example]()
- [CARLA](https://carla.org/) - [Example]()
- [Donkey]() - [Example]()
- [Udacity]() - [Example]()
- [BeamNG](https://www.beamng.com/game/) - [Example]()

OpenSBT has been applied in research:

- Replication Study: [Paper](https://dl.acm.org/doi/10.1016/j.infsof.2023.107286), [Code](https://github.com/Leviathan321/reflection_study) 
- Autonomous Driving Testing: [Paper](https://doi.org/10.1007/978-3-031-46002-9_15), [Video](https://drive.google.com/file/d/1lr5BZpLFaxotwNFju43WF1C9fUTNM-SS/view?usp=sharing) 
- Algorithm Benchmarking: [Paper](https://dl.acm.org/doi/10.1145/3643786.3648023), [Code](https://github.com/ast-fortiss-tum/svm-paper-deeptest-24) 
- Failure Coverage Study: [Paper](https://arxiv.org/html/2410.11769v1), [Code](https://github.com/ast-fortiss-tum/coverage-emse-24) 

## Contribution

If you like to contribute please contact one of the developers listed below or create a pull request. If you face any issues with OpenSBT feel free to create an issue or contact the developers.

## Acknowledgements

OpenSBT has been developed by [Lev Sorokin](mailto:lev.sorokin@tum.de), [Tiziano Munaro](mailto:munaro@fortiss.org) and [Damir Safin](mailto:safin@fortiss.org) within the 
[FOCETA Project](https://www.foceta-project.eu/tools/). Special thanks go to [Brian Hsuan-Cheng Liao](mailto:h.liao@eu.denso.com) and Adam Molin from [DENSO AUTOMOTIVE Deutschland GmbH](https://www.denso.com/de/de/about-us/company-information/dnde/) for their valuable feedback and evaluation of OpenSBT on the AVP Case Study in the Prescan simulator.

## Reference

If you use or extend OpenSBT please cite our framework. Here is an example BibTeX entry:

```bibtex
@inproceedings{10.1145/3639478.3640027,
    author = {Sorokin, Lev and Munaro, Tiziano and Safin, Damir and Liao, Brian Hsuan-Cheng and Molin, Adam},
    title = {OpenSBT: A Modular Framework for Search-based Testing of Automated Driving Systems},
    year = {2024},
    isbn = {9798400705021},
    publisher = {Association for Computing Machinery},
    address = {New York, NY, USA},
    url = {https://doi.org/10.1145/3639478.3640027},
    doi = {10.1145/3639478.3640027},
    booktitle = {Proceedings of the 2024 IEEE/ACM 46th International Conference on Software Engineering: Companion Proceedings},
    pages = {94–98},
    numpages = {5},
    keywords = {search-based software testing, metaheuristics, scenario-based testing, autonomous driving, automated driving},
    location = {, Lisbon, Portugal, },
    series = {ICSE-Companion '24}
}
```
## License

OpenSBT is licensed under the [Apache License, Version 2.0](LICENSE).
