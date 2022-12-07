import glm
import pygame as pg

# Parameters for the 'Camera' - FOV measured in degrees, near/far values used for perspective projection, speed used for
# movement speed, sensitivity used for rotation control with mouse.
FOV = 50
NEAR = 0.1
FAR = 100
SPEED = 0.01
SENSITIVITY = 0.05


class Camera:
    def __init__(self, app, position=(0, 2, -6), yaw=90, pitch=0):
        self.app = app
        self.aspect_ratio = app.WIN_SIZE[0] / app.WIN_SIZE[1]
        self.position = glm.vec3(position)
        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)
        self.yaw = yaw
        self.pitch = pitch
        self.view_matrix = self.get_view_matrix()
        self.projection_matrix = self.get_projection_matrix()

    def rotate(self):
        """
        Rotates the camera using mouse control
        """
        rel_x, rel_y = pg.mouse.get_rel()
        self.yaw += rel_x * SENSITIVITY
        self.pitch -= rel_y * SENSITIVITY
        self.pitch = max(-89, min(89, self.pitch))

    def update_camera_vectors(self):
        """
        Completes vector calculations in line with rotations
        :return:
        """
        yaw, pitch = glm.radians(self.yaw), glm.radians(self.pitch)
        self.forward.x = glm.cos(yaw) * glm.cos(pitch)
        self.forward.y = glm.sin(pitch)
        self.forward.z = glm.sin(yaw)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

    def update(self):
        """
        Updates camera position
        """
        self.move()
        self.rotate()
        self.update_camera_vectors()
        self.view_matrix = self.get_view_matrix()

    def move(self):
        """
        Moves the camera wits W/A/S/D for forward/left/backward/right , and Q/E for up/down
        """
        velocity = SPEED * self.app.delta_time
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.position += self.forward * velocity
        if keys[pg.K_s]:
            self.position -= self.forward * velocity
        if keys[pg.K_a]:
            self.position -= self.right * velocity
        if keys[pg.K_d]:
            self.position += self.right * velocity
        if keys[pg.K_SPACE]:
            self.position += self.up * velocity
        if keys[pg.K_LSHIFT]:
            self.position -= self.up * velocity

    def get_view_matrix(self):
        """
        Creates view matrix using GLM. View matrix moves geometry from world space to view space.
        in glm.lookAt, 1st parameter = position of camera, 2nd is position where camera is looking, 3rd is the
        normalised up vector, how the camera is oriented.
        :return: The created view matrix
        """
        view_matrix = glm.lookAt(self.position, self.position + self.forward, self.up)
        return view_matrix

    def get_projection_matrix(self):
        """
        Creates projection matrix using GLM. Projection matrix the mapping of 3D points to 2D points.
        :return: The created projection matrix
        """
        proj_matrix = glm.perspective(glm.radians(FOV), self.aspect_ratio, NEAR, FAR)
        return proj_matrix
