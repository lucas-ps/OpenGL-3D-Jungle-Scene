from model import *
from vbo import *


class Scene:
    """
    A class which stores and manages objects in a scene
    """

    def __init__(self, app):
        self.app = app
        self.objects = []
        self.load()
        self.skybox = SkyBox(app)

    def add_object(self, name, obj_file, texture_file):
        """
        todo
        """
        self.app.link.vao.vbo.add_vbo(ObjVBO(self.app.ctx, file=obj_file), name)
        self.app.link.vao.add_vao(name)
        self.app.link.texture.add_texture(texture_file, name)
        model = ObjModel(app=self.app, vao_name=name, texture_id=name, rotation=(180, 0, 0))
        self.objects.append(model)


    def load(self):
        """
        Loads objects for the scene
        """

        self.add_object(name='ground', obj_file='../models/ground.obj', texture_file='../textures/ground.jpg')

