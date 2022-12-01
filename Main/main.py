import pygame as pg
import moderngl as mgl
import sys

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

