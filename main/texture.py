import pygame as pg
import moderngl as mgl


class Texture:
    """
    Class that creates and manages Textures
    """

    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.textures = {0: self.get_texture(path='../textures/wooden_crate.png'),
                         1: self.get_texture(path='../textures/cat.jpg'),
                         'skybox': self.get_texture_cube('../textures/skybox2/', 'png'),
                         'depth_texture': self.get_depth_texture()}

    def get_depth_texture(self):
        """
        Generates a depth texture used in shadow mapping
        :return: The generated depth texture
        """
        dt = self.ctx.depth_texture(self.app.WIN_SIZE)
        dt.repeat_x = False
        dt.repeat_y = False
        return dt

    def get_texture_cube(self, path, ext='png'):
        """
        Used for getting cube textures (ie. skybox).
        :param path: Path to the textures.
        :param ext: The file extension eg. png.
        :return: The fetched and processed cube texture.
        """
        faces = ['right', 'left', 'top', 'bottom', 'front', 'back']
        textures = []
        for face in faces:
            textures.append(pg.image.load(path + f'{face}.{ext}').convert())
        size = textures[0].get_size()
        texture_cube = self.ctx.texture_cube(size=size, components=3, data=None)

        for i in range(6):
            texture_data = pg.image.tostring(textures[i], 'RGB')
            texture_cube.write(face=i, data=texture_data)

        return texture_cube

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
