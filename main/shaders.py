class Shaders:
    def __init__(self, ctx):
        """
        The class that loads shaders
        :param ctx: An interactive 2D vector graphics protocol, previously created for the in GraphicsEngine
        """
        self.ctx = ctx
        self.programs = {'default': self.get_program('default')}

    def get_program(self, shader_name):
        """
        Gets program .vert and .frag file and produces a
        :param shader_name: The name of the program file.
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
