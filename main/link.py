from vao import VAO
from texture import Texture


class Link:
    """
    Class that links main app objects to Textures and VAOs (and by extension shaders, VBOs)
    """

    def __init__(self, app):
        self.app = app
        self.vao = VAO(app.ctx)
        self.texture = Texture(app.ctx)

    def destroy(self):
        """
        Calls destroy functions for VAOs, VBOs, Shaders and textures.
        """
        self.vao.destroy()
        self.texture()

