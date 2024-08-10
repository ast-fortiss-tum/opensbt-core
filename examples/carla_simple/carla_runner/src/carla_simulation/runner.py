# Copyright (c) 2022 fortiss GmbH
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

import os

from carla_simulation.simulator import Simulator
from carla_simulation.scenario import Scenario
from carla_simulation.recorder import Recorder


class Runner:

    _host_carla = None
    _port_carla = 2000
    _timeout_carla = 10
    _rendering_carla = False
    _resolution_carla = 0.1

    _recording_dir = '/tmp/recordings'
    _metrics_dir = 'metrics'

    _agent_class = None
    _metric_class = None

    def __init__(self, host, agent, metric, rendering=False):
        self._host_carla = host
        self._agent_class = agent
        self._metric_class = metric
        self._rendering_carla = rendering

    def run(self, directory, queue, evaluations):
        while not queue.empty():
            pattern = queue.get()

            simulator = self.get_simulator(
                self._host_carla,
                self._port_carla,
                self._timeout_carla,
                self._rendering_carla,
                self._resolution_carla
            )
            scenarios = self.get_scenarios(directory, pattern)
            recorder = self.get_recorder(self._recording_dir)
            evaluator = self.get_evaluator()
            agent = self.get_agent()

            for scenario in scenarios:
                scenario.simulate(simulator, agent, recorder)

            recordings = recorder.get_recordings()

            for recording in recordings:
                evaluations.append(
                    evaluator.evaluate(
                        simulator,
                        recording
                    )
                )
                os.remove(recording)

            queue.task_done()

    def get_simulator(self, host, port, timeout, rendering = True, resolution = 0.1):
        return Simulator(
            host = host,
            port = port,
            timeout = timeout,
            rendering = rendering,
            resolution = resolution
        )

    def get_scenarios(self, directory, pattern):
        scenarios = None
        with os.scandir(directory) as entries:
            scenarios = [
                Scenario(entry)
                    for entry in entries
                        if entry.name.endswith(pattern) and entry.is_file()
            ]
        return scenarios

    def get_evaluator(self):
        return self._metric_class()

    def get_agent(self):
        return self._agent_class

    def get_recorder(self, directory):
        return Recorder(directory)
