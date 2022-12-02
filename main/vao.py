from vbo import VBO
from shaders import Shaders


class VAO:
    """
    Class for Vertex Array Objects (VAO) - object containing one or more Vertex Buffer Objects and is designed to store
    the information for a complete rendered object. The VAO dictionary is initialised with a cube VAO.
    """

    def __init__(self, ctx):
        self.ctx = ctx
        self.vbo = VBO(ctx)
        self.program = Shaders(ctx)
        self.vaos = {}
        self.vaos['cube'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['cube'])

    def get_vao(self, program, vbo):
        """
        Creates and returns a VAO. In the buffer, '3f' refers to the buffer format and 'in_position' is an input
        attribute that defines how vertexes are stored in the VBO.
        :return: The created VAO
        """
        vao = self.ctx.vertex_array(program, [(vbo.vbo, vbo.format, *vbo.attribs)])
        return vao

    def destroy(self):
        """
        Calls destroy function for VBOs and Shaders
        """
        self.vbo.destroy()
        self.program.destroy()
