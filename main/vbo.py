"""
Class that holds VBOs for objects
"""

import numpy as np
import pywavefront


class VBO:
    def __init__(self, ctx):
        self.vbos = {'skybox': SkyBoxVBO(ctx)}

    def add_vbo(self, vbo, name):
        self.vbos[name] = vbo

    def destroy(self):
        """
        Acts as a garbage collector for VBO objects
        """
        for vbo in self.vbos.values():
            vbo.destroy()


class BaseVBO:
    def __init__(self, ctx):
        """
        Base class that loads Vertex Buffer Objects (VBO) - object that holds vertex data (position, normal vector,
        colour, etc.) to the GPU for non-immediate-mode rendering
        :param ctx: An interactive 2D vector graphics protocol, previously created for the in GraphicsEngine
        """
        self.ctx = ctx
        self.vbo = self.get_vbo()
        self.format: str = None
        self.attrib: list = None
        self.file = None

    def get_vbo(self):
        """
        Creates and returns a VBO.
        :return: The created VBO.
        """
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        return vbo

    def destroy(self):
        """
        Acts as a garbage collector for VBOs
        """
        self.vbo.release()

class SkyBoxVBO(BaseVBO):
    """
    Extends BaseVBO for use to render basic the skybox
    :param ctx: An interactive 2D vector graphics protocol, previously created for the in GraphicsEngine
    """
    def __init__(self, ctx):
        super().__init__(ctx)
        self.format = '3f'
        self.attribs = ['in_position']

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
        vertex_data = np.flip(vertex_data, 1).copy(order='C')

        return vertex_data


class ObjVBO(BaseVBO):
    def __init__(self, app, file):
        """
        Initialises a VBO from an obj file with parameters needed.
        :param app: Previously created graphical engine
        """
        self.ctx = app
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']
        self.file = file
        self.ctx = app
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        self.vbo = vbo

    def get_vertex_data(self):
        """
        Uses pywavefront to parse cat obj file for vertex data.
        :return: A numpy array of vertex data.
        """
        objs = pywavefront.Wavefront(self.file, cache=True, parse=True)
        obj = objs.materials.popitem()[1]
        vertex_data = obj.vertices
        vertex_data = np.array(vertex_data, dtype='f4')
        return vertex_data
