import numpy as np
import glm
import pygame as pg


class Cube:
    def __init__(self, app):
        """
        Sets the cube's app, ctx (2D vector graphics protocol), vertex buffer object and shader program.
        :param app: The app to render to.
        """
        self.app = app
        self.ctx = app.ctx
        self.vbo = self.get_vbo()
        self.shader_program = self.get_shader_program('default')
        self.vao = self.get_vao()
        self.m_model = self.get_model_matrix()
        self.texture = self.get_texture(path='../textures/wooden_crate.png')
        self.on_init()

    def on_init(self):
        """
        Runs when object is created, passes texture and projection, view and model matrices.
        """
        self.shader_program['u_texture_0'] = 0
        self.texture.use()
        self.shader_program['m_proj'].write(self.app.camera.m_proj)
        self.shader_program['m_view'].write(self.app.camera.m_view)
        self.shader_program['m_model'].write(self.m_model)

    def get_texture(self, path):
        """
        Loads the texture image from a given path.
        :param path: path to the image.
        :return: ctx texture object.
        """
        texture = pg.image.load(path).convert()
        # Makes texture compatible with pygame's axis system
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.ctx.texture(size=texture.get_size(), components=3, data=pg.image.tostring(texture, 'RGB'))
        return texture


    def update(self):
        """
        Updates the cube everytime it is called by rotating it.
        """
        model_matrix = glm.rotate(self.m_model, self.app.time * 0.5, glm.vec3(0, 1, 0))
        self.shader_program['m_model'].write(model_matrix)
        self.shader_program['m_view'].write(self.app.camera.m_view)

    def get_model_matrix(self):
        model_matrix = glm.mat4()
        return model_matrix

    def render(self):
        """
        Renders the Vertex Array Object and calls 'update' method.
        """
        self.update()
        self.vao.render()

    def destroy(self):
        """
        Removes all created resources, acts as a garbage collector as OpenGL does not do this by itself.
        """
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()

    def get_vao(self):
        """
        Creates and returns Vertex Array Object (VAO) - object containing one or more Vertex Buffer Objects and is
        designed to store the information for a complete rendered object. In the buffer, '3f' refers to the buffer
        format and 'in_position' is an input attribute that defines how vertexes are stored in the VBO.
        :return: The created VAO
        """
        vao = self.ctx.vertex_array(self.shader_program, [(self.vbo, '2f 3f', 'in_texcoord_0', 'in_position')])
        return vao

    def get_vertex_data(self):
        """
        Sets vertex co-ordinates for a triangle.
        :return: Vertex data for a triangle.
        """
        vertices = [(-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1), (-1, 1, -1), (-1, -1, -1), (1, -1, -1), (1, 1, -1)]
        indices = [(0, 2, 3), (0, 1, 2),
                   (1, 7, 2), (1, 6, 7),
                   (6, 5, 4), (4, 7, 6),
                   (3, 4, 5), (3, 5, 0),
                   (3, 7, 4), (3, 2, 7),
                   (0, 6, 1), (0, 5, 6)]
        vertex_data = self.get_data(vertices, indices)

        texture_coord = [(0, 0), (1, 0), (1, 1), (0, 1)]
        texture_coord_indices = [(0, 2, 3), (0, 1, 2),
                                 (0, 2, 3), (0, 1, 2),
                                 (0, 1, 2), (2, 3, 0),
                                 (2, 3, 0), (2, 0, 1),
                                 (0, 2, 3), (0, 1, 2),
                                 (3, 1, 2), (3, 0, 1)]
        texture_coord_data = self.get_data(texture_coord, texture_coord_indices)
        vertex_data = np.hstack([texture_coord_data, vertex_data])

        return vertex_data

    @staticmethod
    def get_data(vertices, indices):
        """
        Static method to create an array for generating vertex data above.
        :param vertices: The array of vertices.
        :param indices: The array of indices.
        :return: A numpy array  of vertices and their indices.
        """
        data = [vertices[ind]
                for triangle in indices
                for ind in triangle]
        return np.array(data, dtype='f4')

    def get_vbo(self):
        """
        Creates and returns a Vertex Buffer Object (VBO) - object that holds vertex data (position, normal vector,
        colour, etc.) to the GPU for non-immediate-mode rendering.
        :return: The created VBO.
        """
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        return vbo

    def get_shader_program(self, shader_name):
        """
        Gets shader .vert and .frag file and produces a
        :param shader_name: The name of the shader file.
        """
        with open(f'../shaders/{shader_name}.vert') as file:
            vertex_shader = file.read()
        with open(f'../shaders/{shader_name}.frag') as file:
            fragment_shader = file.read()

        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program
