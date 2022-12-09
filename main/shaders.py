"""
Class that loads shader files
"""

class Shaders:
    def __init__(self, ctx):
        """
        The class that loads shaders
        :param ctx: An interactive 2D vector graphics protocol, previously created for the in GraphicsEngine
        """
        self.ctx = ctx
        self.programs = {'default': self.get_shader('default'),
                         'skybox': self.get_shader('skybox'),
                         'shadow': self.get_shader('shadow_map'),
                         'water': self.get_shader('water')}

    def get_shader(self, shader_name):
        """
        Gets the specified GLSL shader shaders.
        :param shader_name: The name of the shaders file.
        :return: The processed shaders.
        """
        with open(f'../shaders/{shader_name}.vert') as file:
            vertex_shader = file.read()
        with open(f'../shaders/{shader_name}.frag') as file:
            fragment_shader = file.read()

        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program

    def destroy(self):
        """
        Removes all created resources, acts as a garbage collector as OpenGL does not do this by itself.
        """
        for program in self.programs.values():
            program.release()
