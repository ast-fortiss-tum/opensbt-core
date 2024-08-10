# Copyright (c) 2022 fortiss GmbH
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

import os


class Recorder:

    def __init__(self, directory):
        self.directory = directory
        self.recordings = list()
        if not os.path.isdir(directory):
            os.mkdir(directory)

    def add_recording(self, name):
        recording =  "{}/{}.log".format(
            self.directory,
            name
        )
        self.recordings.append(recording)
        return recording

    def get_recordings(self):
        return self.recordings
