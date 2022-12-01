import glm

# Parameters for the 'Camera' - FOV measured in degrees, near/far values used for perspective projection.
FOV = 50
NEAR = 0.1
FAR = 100

class Camera:
    def __init__(self, app):
        self.app = app
        self.aspect_ratio = app.WIN_SIZE[0] / app.WIN_SIZE[1]
        self.position = glm.vec3(2, 3, 3)
        self.up = glm.vec3(0, 1, 0)
        self.m_view = self.get_view_matrix()
        self.m_proj = self.get_projection_matrix()

    def get_view_matrix(self):
        """
        Creates view matrix using GLM. View matrix moves geometry from world space to view space.
        in glm.lookAt, 1st parameter = position of camera, 2nd is position where camera is looking, 3rd is the
        normalised up vector, how the camera is oriented.
        :return: The created view matrix
        """
        view_matrix = glm.lookAt(self.position, glm.vec3(0), self.up)
        return view_matrix

    def get_projection_matrix(self):
        """
        Creates projection matrix using GLM. Projection matrix the mapping of 3D points to 2D points.
        :return: The created projection matrix
        """
        proj_matrix = glm.perspective(glm.radians(FOV), self.aspect_ratio, NEAR, FAR)
        return proj_matrix
