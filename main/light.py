"""
Class for implementing Phong lighting
"""

import glm


class Light:
    def __init__(self, position=(3, 3, -3), colour=(1, 1, 1)):
        self.position = glm.vec3(position)
        self.colour = glm.vec3(colour)

        # Intensities
        self.intensity_ambient = 0.1 * self.colour  # ambient
        self.intensity_diffuse = 0.8 * self.colour  # diffuse
        self.intensity_specular = 1 * self.colour  # specular
