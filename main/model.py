import numpy as np
import glm
import pygame as pg


class BaseModel:
    """
    A base model for object models
    """
    def __init__(self, app, vao_name, texture_id):
        self.app = app
        self.model_matrix = self.get_model_matrix()
        self.texture_id = texture_id
        self.vao = app.link.vao.vaos[vao_name]
        self.shader = self.vao.program
        self.camera = self.app.camera

    def update(self): ...

    def get_model_matrix(self):
        model_matrix = glm.mat4()
        return model_matrix

    def render(self):
        """
        Renders the Vertex Array Object and calls 'update' method.
        """
        self.update()
        self.vao.render()


class Cube(BaseModel):
    def __init__(self, app, vao_name='cube', texture_id=0):
        super().__init__(app, vao_name, texture_id)
        self.on_init()

    def update(self):
        """
        Updates the cube everytime it is called by rotating it.
        """
        self.texture.use()
        self.shader['m_model'].write(self.model_matrix)
        self.shader['m_view'].write(self.camera.m_view)
        self.shader['camPos'].write(self.camera.position)
    def on_init(self):
        """
        Runs when object is created, passes light intensity, texture and projection, view and model matrices.
        """
        # Lighting
        self.shader['light.position'].write(self.app.light.position)
        self.shader['light.Ia'].write(self.app.light.intensity_ambient)
        self.shader['light.Id'].write(self.app.light.intensity_diffuse)
        self.shader['light.Is'].write(self.app.light.intensity_specular)

        # Textures
        self.texture = self.app.link.texture.textures[self.texture_id]
        self.shader['u_texture_0'] = 0
        self.texture.use()

        # Matrices
        self.shader['m_proj'].write(self.app.camera.m_proj)
        self.shader['m_view'].write(self.app.camera.m_view)
        self.shader['m_model'].write(self.model_matrix)
