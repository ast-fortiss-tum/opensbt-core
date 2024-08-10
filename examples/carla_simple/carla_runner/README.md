# CARLA Interface for Scenario-based Testing

Evaluate scenarios using a highly parallelizable CARLA setup!

```
from carla_simulation import balancer

traces = balancer.run_scenarios(scenario_dir="/tmp/scenarios")
```

## Prerequisites

### CARLA

The CARLA server must already be running when the simulation is started. Due to its lightweight, ease of use, and modularity, a Docker-based setup is preferred. Instructions can be found [here](https://carla.readthedocs.io/en/latest/build_docker/).

The CARLA interface will instruct the server to record the simulation runs and to store the data in the container's `/tmp/recordings` folder. In order to access these files, this directory is mounted by the host as well. However, make sure that the user with ID `1000` must be the directory's owner!

Make sure that the `PYTHONPATH` includes all of the dependencies required by the CARLA Scenario Runner and the `CARLA_ROOT` and `SCENARIO_RUNNER_ROOT` point to the respective local repositories (to be cloned from [here](https://github.com/carla-simulator/carla) and [here](https://github.com/carla-simulator/scenario_runner) respectively).

### Docker

Instructions to install Docker are available [here](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository). The NVIDIA Container Toolkit can be installed as described [here](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#installation-guide).

## Getting Started

To start the container with default settings, run `docker compose up` in this repository's root folder. Instructions on Docker Compose can be found [here](https://docs.docker.com/compose/). By using the `--scale` flag, the number of CARLA servers to start can be adapted (e.g., `docker compose up --scale carla-server=3`). By default two instances will be launched.

Once CARLA is up and running, execute the `balancer.py` script.

The 3D visualization can be turned on by setting the `_rendering_carla` variable in the `runner.py` accordingly.

### Python Wheel

The easiest way to get the CARLA interface up and running is to build it as a Python package and install it.

To build the package, run `python -m build` in the repository's root directory. Once completed, install the `*.whl` package found in the newly created `dist/` folder via `python -m pip install /path/to/the/package.whl`.

### Visual Studio Code

If you use [Visual Studio Code](https://code.visualstudio.com/), the following launch file might be useful reference:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "CARLA",
            "type": "python",
            "request": "launch",
            "program": "balancer.py",
            "console": "integratedTerminal",
            "env": {
                "CARLA_ROOT": "~/Repositories/CARLA/Simulator",
                "PYTHONPATH": "~/Repositories/CARLA/Simulator/PythonAPI/carla/dist/carla-0.9.13-py3.7-linux-x86_64.egg:~/Repositories/CARLA/Simulator/PythonAPI/carla/agents:~/Repositories/CARLA/Simulator/PythonAPI/carla:~/Repositories/CARLA/ScenarioRunner",
                "SCENARIO_RUNNER_ROOT": "~/Repositories/CARLA/ScenarioRunner"
            }
        }
    ]
}
```
