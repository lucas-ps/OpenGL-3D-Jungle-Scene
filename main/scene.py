from model import *
from vbo import *
import moderngl as mgl


class Scene:
    """
    A class which stores and manages objects in a scene
    """

    def __init__(self, app):
        self.app = app
        self.objects = []
        self.load()
        self.skybox = SkyBox(app)

    def add_object(self, name, obj_file, texture_file, rotation=(0, 0, 0), water=False):
        """
        todo
        """
        self.app.link.texture.add_texture(texture_file, name)
        self.app.link.vao.vbo.add_vbo(ObjVBO(self.app.ctx, file=obj_file), name)
        model = None
        if water:
            self.app.link.vao.add_vao(name, shader='water')
            model = ObjModel(app=self.app, vao_name=name, texture_id=name, rotation=rotation)
            self.water = model
        else:
            self.app.link.vao.add_vao(name)
            model = ObjModel(app=self.app, vao_name=name, texture_id=name, rotation=rotation)
        self.objects.append(model)

    def load(self):
        """
        Loads objects for the scene
        """

        self.add_object(name='ground', obj_file='../models/ground/ground.obj', texture_file='../textures/ground.jpg')
        self.add_object(name='rocks', obj_file='../models/ground/rocks.obj', texture_file='../textures/rock.jpg')

        self.add_object(name="trunks1", obj_file='../models/trees/trunks1.obj', texture_file='../textures/bark.jpg')
        self.add_object(name="trunks2", obj_file='../models/trees/trunks2.obj', texture_file='../textures/bark.jpg')
        self.add_object(name="leaves1", obj_file='../models/trees/leaves1.obj', texture_file='../textures/leaves.jpg')
        self.add_object(name="leaves2", obj_file='../models/trees/leaves2.obj', texture_file='../textures/leaves.jpg')

        self.add_object(name="fish", obj_file='../models/animals/fish.obj', texture_file='../textures/fish.jpg')
        self.add_object(name="monkey", obj_file='../models/animals/monkey.obj', texture_file='../textures/monkey.jpg')
        self.add_object(name="toucan", obj_file='../models/animals/toucan.obj', texture_file='../textures/toucan.jpg')
        self.add_object(name="frog", obj_file='../models/animals/frog.obj', texture_file='../textures/frog.jpg')

        self.app.ctx.enable(mgl.BLEND)
        self.add_object(name='water', obj_file='../models/water/water.obj', texture_file='../textures/water.png',
                        water=True)

    def update(self):
        self.water.rot.y = self.app.time
