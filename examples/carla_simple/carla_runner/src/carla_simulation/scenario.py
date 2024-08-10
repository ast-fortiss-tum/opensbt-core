# Copyright (c) 2022 fortiss GmbH
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

from pathlib import Path

from srunner.scenarios.open_scenario import OpenScenario
from srunner.scenarioconfigs.openscenario_configuration import OpenScenarioConfiguration
from srunner.scenariomanager.carla_data_provider import CarlaDataProvider
from srunner.scenariomanager.scenario_manager import ScenarioManager


class Scenario:

    _xosc = None

    def __init__(self, xosc):
        self._xosc = xosc

    def simulate(self, simulator, agent, recorder):
        client = simulator.get_client()

        world = client.get_world()

        CarlaDataProvider.set_client(client)
        CarlaDataProvider.set_world(world)

        config = OpenScenarioConfiguration(
            self._xosc,
            client,
            {}
        )

        CarlaDataProvider.set_traffic_manager_port(
            simulator.get_traffic_manager_port()
        )

        vehicles = []
        for vehicle in config.ego_vehicles:
            vehicles.append(
                CarlaDataProvider.request_new_actor(
                    vehicle.model,
                    vehicle.transform,
                    vehicle.rolename,
                    color=vehicle.color,
                    actor_category=vehicle.category
                )
            )

        controller = agent(simulator)

        scenario = OpenScenario(
            world,
            vehicles,
            config,
            self._xosc
        )

        recording = recorder.add_recording(
            Path(self._xosc.path).stem
        )

        manager = ScenarioManager()
        manager.load_scenario(scenario, controller)
        client.start_recorder(
            recording,
            True
        )
        manager.run_scenario()
        client.stop_recorder()
