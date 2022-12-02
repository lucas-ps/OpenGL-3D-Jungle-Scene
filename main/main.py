import moderngl as mgl
import sys
from model import *
from camera import Camera
from light import Light
from link import Link


class GraphicsEngine:
    def __init__(self, win_size=(1600, 900)):
        # Initiate pygame modules
        pg.init()

        # Set openGL attributes
        self.WIN_SIZE = win_size
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

        # Creating opengl content - DOUBLEBUF = 2 complete colour buffers for drawing (used for optimisation)
        pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)
        self.ctx = mgl.create_context()
        self.camera = Camera(self)
        self.link = Link(self)

        # Mouse settings
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)

        # Implementing time
        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0

        # Load phong lighting class
        self.light = Light()

        # Ensuring fragments show in the correct order of depth and culls faces that don't need to be rendered.
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)

        # Load the scene
        self.scene = Cube(self)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.mesh.destroy()
                pg.quit()
                sys.exit()

    def render(self):
        # Clear framebuffer
        self.ctx.clear(color=(0.08, 0.16, 0.18))

        # Render scene
        self.scene.render()

        # Swap buffers
        pg.display.flip()

    def get_time(self):
        """
        Gets time in seconds
        """
        self.time = pg.time.get_ticks() * 0.001

    def run(self):
        while True:
            self.get_time()
            self.check_events()
            self.camera.update()
            self.render()
            # Setting frame rate to 60Hz
            self.delta_time = self.clock.tick(60)

if __name__ == '__main__':
    app = GraphicsEngine()
    app.run()
