import numpy as np
import glm
import pygame as pg


class BaseModel:
    """
    A base model for object models
    """

    def __init__(self, app, vao_name, texture_id, position=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1)):
        self.app = app
        self.pos = position
        # Converts euler angles into openGL compatible format
        self.rot = glm.vec3([glm.radians(a) for a in rotation])
        self.scale = scale
        self.model_matrix = self.get_model_matrix()
        self.texture_id = texture_id
        self.vao_name = vao_name
        self.vao = app.link.vao.vaos[vao_name]
        self.shader = self.vao.program
        self.camera = self.app.camera

    def update(self): ...

    def get_model_matrix(self):
        model_matrix = glm.mat4()

        # Translate object to position
        model_matrix = glm.translate(model_matrix, self.pos)

        # Rotate object around XYZ axis as specified in parameters
        model_matrix = glm.rotate(model_matrix, self.rot.x, glm.vec3(1, 0, 0))
        model_matrix = glm.rotate(model_matrix, self.rot.y, glm.vec3(0, 1, 0))
        model_matrix = glm.rotate(model_matrix, self.rot.z, glm.vec3(0, 0, 1))

        # Scale objects
        model_matrix = glm.scale(model_matrix, self.scale)

        return model_matrix

    def render(self):
        """
        Renders the Vertex Array Object and calls 'update' method.
        """
        self.update()
        self.vao.render()


class ExtendedBaseModel(BaseModel):
    """
    An extended base model class that contains methods for objects.
    """

    def __init__(self, app, vao_name, texture_id, position, rotation, scale):
        super().__init__(app, vao_name, texture_id, position, rotation, scale)
        self.on_init()

    def update(self):
        """
        Updates the cube everytime it is called by rotating it.
        """
        self.texture.use(location=0)
        self.shader['m_model'].write(self.model_matrix)
        self.shader['m_view'].write(self.camera.view_matrix)
        self.shader['camPos'].write(self.camera.position)

    def update_shadow(self):
        """
        Updates shadows with model movements.
        """
        self.shadow_shader['m_model'].write(self.model_matrix)

    def render_shadow(self):
        """
        Completes shadow render.
        """
        self.update_shadow()
        self.shadow_vao.render()

    def on_init(self):
        """
        Runs when object is created, passes shadow, light intensity, texture, projection, view and model matrices.
        """
        self.shader['m_view_light'].write(self.app.light.view_matrix_light)

        self.shader['u_resolution'].write(glm.vec2(self.app.WIN_SIZE))

        # Depth texture
        self.depth_texture = self.app.link.texture.textures['depth_texture']
        self.shader['shadowMap'] = 1
        self.depth_texture.use(location=1)

        # Shadows
        self.shadow_vao = self.app.link.vao.vaos[f"shadow_{self.vao_name}"]
        self.shadow_shader = self.shadow_vao.program
        self.shadow_shader['m_proj'].write(self.app.camera.projection_matrix)
        self.shadow_shader['m_view_light'].write(self.app.light.view_matrix_light)
        self.shadow_shader['m_model'].write(self.model_matrix)

        # Lighting
        self.shader['light.position'].write(self.app.light.position)
        self.shader['light.Ia'].write(self.app.light.intensity_ambient)
        self.shader['light.Id'].write(self.app.light.intensity_diffuse)
        self.shader['light.Is'].write(self.app.light.intensity_specular)

        # Textures
        self.texture = self.app.link.texture.textures[self.texture_id]
        self.shader['u_texture_0'] = 0
        self.texture.use(location=0)

        # Matrices
        self.shader['m_proj'].write(self.app.camera.projection_matrix)
        self.shader['m_view'].write(self.app.camera.view_matrix)
        self.shader['m_model'].write(self.model_matrix)


class Cube(ExtendedBaseModel):
    def __init__(self, app, vao_name='cube', texture_id=0, position=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, texture_id, position, rotation, scale)


class SkyBox(BaseModel):
    def __init__(self, app, vao_name='skybox', texture_id='skybox', position=(0, 0, 0), rotation=(0, 0, 0),
                 scale=(1, 1, 1)):
        super().__init__(app, vao_name, texture_id, position, rotation, scale)
        self.on_init()

    def update(self):
        """
        Updates the skybox when camera moves
        """
        self.shader['m_view'].write(glm.mat4(glm.mat3(self.app.camera.view_matrix)))

    def on_init(self):
        """
        Runs when skybox is created, passes light intensity, texture and projection, view and model matrices.
        """
        # Textures
        self.texture = self.app.link.texture.textures[self.texture_id]
        self.shader['u_texture_skybox'] = 0
        self.texture.use(location=0)

        # Matrices
        self.shader['m_proj'].write(self.app.camera.projection_matrix)
        self.shader['m_view'].write(glm.mat4(glm.mat3(self.app.camera.view_matrix)))


class MovingCube(Cube):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update(self):
        self.model_matrix = self.get_model_matrix()
        super().update()


class ObjModel(ExtendedBaseModel):
    def __init__(self, app, vao_name='ground', texture_id='ground', position=(0, 0, 0), rotation=(0, 0, 0),
                 scale=(1, 1, 1)):
        super().__init__(app, vao_name, texture_id, position, rotation, scale)

    def update(self):
        self.model_matrix = self.get_model_matrix()
        super().update()
