# Copyright (c) 2020 Universitat Autonoma de Barcelona (UAB)
# Copyright (c) 2022 fortiss GmbH
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

import math

from srunner.metrics.tools.metrics_log import MetricsLog

DEBUG = False

class RawData:

    def evaluate(self, simulator, recording):
        info = simulator.get_client().show_recorder_file_info(recording, True)
        log = MetricsLog(info)

        result = {
            "simTime": 0,
            "times": [],
            "location": {
                "ego": [],
                "adversary": []
            },
            "velocity": {
                "ego": [],
                "adversary": []
            },
            "speed": {
                "ego": [],
                "adversary": []
            },
            "acceleration": {
                "ego": [],
                "adversary": []
            },
            "yaw": {
                "ego": [],
                "adversary": []
            },
            "collisions": {},
            "actors": {},
            "otherParams": {}
        }

        type_ped = "walker.pedestrian"
        type_vehicle = "vehicle"

        peds = {}
        vehicles = {}

        ego_id = -1
        adv_id = -1

        # assumption is there is one actor name "adversary" and one "hero" == ego agent
        # actor is defined by its role name (should be unique)

        actor_list = log._actors

        for id, actor in actor_list.items():
            if "role_name" in actor:
                name = actor["role_name"]
                if name == "adversary":
                    adv_id = id
                elif name == "hero":
                    ego_id = id
                elif actor["type_id"].startswith(type_ped):
                    peds[id] = (actor)
                elif actor["type_id"].startswith(type_vehicle):
                    vehicles[id] = actor

        start, end = log.get_actor_alive_frames(ego_id)

        for actor_id, actor in vehicles.items():
            start_adv, end_adv = log.get_actor_alive_frames(actor_id)

            name = actor["role_name"]

            if name != "hero":
                set_state_result_actor(log, name, actor_id, result, start_adv, end_adv)

        for actor_id, actor in peds.items():
            start_adv, end_adv = log.get_actor_alive_frames(actor_id)

            name = actor["role_name"]
            set_state_result_actor(log, name,actor_id, result, start_adv, end_adv)

        set_state_result_actor(log, "ego", ego_id, result, start, end)
        set_state_result_actor(log, "adversary", adv_id, result, start, end)

        result["simTime"] = log.get_elapsed_time(log.get_total_frame_count() - 1)

        frames_time_list = []
        for i in range(start, end):
            frames_time_list.append(log.get_elapsed_time(i))

        result["times"] = frames_time_list
        result["collisions"] = log.get_actor_collisions(ego_id)
        result["actors"] = {
            "ego" : "ego",
            "adversary" : "adversary",
            "vehicles" : [actor["role_name"] for actor in vehicles.values()],
            "pedestrians" : [actor["role_name"] for actor in peds.values()]
        }
        if len(result["collisions"]) > 0:
            result["otherParams"]["isCollision"] = True
        else:
            result["otherParams"]["isCollision"] = False

        return result

def set_state_result_actor(log, name, adv_id, result, start, end):
    frames_time_list = []
    adv_location_profile = []
    adv_velocity_profile = []
    adv_speed_profile = []
    adv_acceleration_profile = []
    adv_rotation_profile = []
    adv_yaw_profile = []
    adv_pitch_profile = []
    adv_roll_profile = []

    for i in range(start, end):
        frames_time_list.append(log.get_elapsed_time(i))

        adv_location = log.get_actor_transform(adv_id, i).location
        adv_location_profile.append((adv_location.x, adv_location.y))
        adv_rotation = log.get_actor_transform(adv_id, i).rotation
        adv_rotation_profile.append((adv_rotation.pitch, adv_rotation.yaw, adv_rotation.roll))

        adv_yaw_profile.append(adv_rotation.yaw)
        adv_pitch_profile.append(adv_rotation.pitch)
        adv_roll_profile.append(adv_rotation.roll)

        adv_velocity = log.get_actor_velocity(adv_id, i)
        adv_velocity_profile.append([adv_velocity.x, adv_velocity.y, adv_velocity.z])

        adv_speed = math.sqrt(adv_velocity.x ** 2 + adv_velocity.y ** 2 + adv_velocity.z ** 2)
        adv_speed_profile.append(adv_speed)
        adv_acceleration = log.get_actor_acceleration(adv_id, i)
        adv_acceleration_profile.append((adv_acceleration.x, adv_acceleration.y, adv_acceleration.z))

        result["location"][name]= adv_location_profile
        result["velocity"][name] = adv_velocity_profile
        result["speed"][name] = adv_speed_profile
        result["acceleration"][name] = adv_acceleration_profile
        result["yaw"][name] = adv_yaw_profile