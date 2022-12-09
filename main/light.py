"""
Class that sets necessary parameters for Phong lighting
"""

import glm


class Light:
    def __init__(self, position=(50, 50, -10), colour=(1, 1, 1)):
        self.position = glm.vec3(position)
        self.colour = glm.vec3(colour)
        self.direction = (0, 0, 0)

        # Intensities
        self.intensity_ambient = 0.1 * self.colour  # ambient
        self.intensity_diffuse = 0.8 * self.colour  # diffuse
        self.intensity_specular = 1 * self.colour  # specular

        self.view_matrix_light = self.get_view_matrix()

    def get_view_matrix(self):
        """
        Calculates a view matrix used for lighting/shadow mapping
        :return: The calculated view matrix
        """
        return glm.lookAt(self.position, self.direction, glm.vec3(0, 1, 0))
