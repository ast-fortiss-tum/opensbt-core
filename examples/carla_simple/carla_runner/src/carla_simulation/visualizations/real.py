# Copyright (c) 2021 Universitat Autonoma de Barcelona (UAB)
# Copyright (c) 2022 fortiss GmbH
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

import pygame

class CameraView:

    """
    CARLA Camera Visualization
    """

    def __init__(self, camera_id):
        self._width = 800
        self._height = 600
        self._surface = None

        self._camera_id = camera_id

        pygame.init()
        pygame.font.init()
        self._clock = pygame.time.Clock()
        self._display = pygame.display.set_mode((self._width, self._height), pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption("CARLA")

    def run(self, input_data):
        """
        Run the GUI
        """
        # Process data
        image_center = input_data[self._camera_id][1][:, :, -2::-1]

        # Display image
        self._surface = pygame.surfarray.make_surface(image_center.swapaxes(0, 1))
        if self._surface is not None:
            self._display.blit(self._surface, (0, 0))
        pygame.display.flip()

    def quit(self):
        """
        Stops the pygame window
        """
        pygame.quit()
