import pygame as pg
import moderngl as mgl


class Texture:
    """
    Class that creates and manages Textures
    """

    def __init__(self, ctx):
        self.ctx = ctx
        self.textures = {0: self.get_texture(path='../textures/wooden_crate.png'),
                         1: self.get_texture(path='../textures/cat.jpg')}

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

        # Generate MIP maps for optimisation and antialiasing.
        texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
        texture.build_mipmaps()

        # Anisotropic filtering for antialiasing and improving sharpness lost by MIP maps.
        texture.anisotropy = 32

        return texture

    def destroy(self):
        """
        Acts as a garbage collector for textures
        """
        for texture in self.textures.values():
            texture.release
