"""
Class for Vertex Array Objects (VAO) - object containing one or more Vertex Buffer Objects and is designed to store
the information for a complete rendered object. The VAO dictionary is initialised with a cube VAO.
"""

from vbo import VBO
from shaders import Shaders


class VAO:
    def __init__(self, ctx):
        self.ctx = ctx
        self.vbo = VBO(ctx)
        self.shaders = Shaders(ctx)
        self.vaos = {
            'skybox': self.get_vao(
                program=self.shaders.programs['skybox'],
                vbo=self.vbo.vbos['skybox'])
        }

    def get_vao(self, program, vbo):
        """
        Creates and returns a VAO. In the buffer, '3f' refers to the buffer format and 'in_position' is an input
        attribute that defines how vertexes are stored in the VBO.
        :return: The created VAO
        """
        vao = self.ctx.vertex_array(program, [(vbo.vbo, vbo.format, *vbo.attribs)], skip_errors=True)
        return vao

    def add_vao(self, name, shader='default'):
        """
        todo
        """
        if shader == 'water':
            self.vaos[name] = self.get_vao(
                program=self.shaders.programs['water'],
                vbo=self.vbo.vbos[name])
            self.vaos["shadow_"+name] = self.get_vao(
                program=self.shaders.programs['shadow'],
                vbo=self.vbo.vbos[name])
        else:
            self.vaos[name] = self.get_vao(
                    program=self.shaders.programs['default'],
                    vbo=self.vbo.vbos[name])
            self.vaos["shadow_"+name] = self.get_vao(
                program=self.shaders.programs['shadow'],
                vbo=self.vbo.vbos[name])
    def destroy(self):
        """
        Calls destroy function for VBOs and Shaders
        """
        self.vbo.destroy()
        self.shaders.destroy()
