from model import *


class Scene:
    """
    A class which stores and manages objects in a scene
    """

    def __init__(self, app):
        self.app = app
        self.objects = []
        self.load()

    def add_object(self, obj):
        """
        Adds an object to the object list
        :param obj: The object to add
        """
        self.objects.append(obj)

    def load(self):
        """
        Loads objects for the scene
        """
        """self.add_object(Cube(self.app))
        self.add_object(Cube(self.app, position=(-2.5, 0, 0), rotation=(45, 0, 0), scale=(1, 2, 1)))
        self.add_object(Cube(self.app, position=(2.5, 0, 0), rotation=(0, 0, 45), scale=(1, 1, 2)))"""

        # Create a 30x30 grid of boxes spaced apart at width y
        n, y = 30, 2
        for x in range(-n, n, y):
            for z in range(-n, n, y):
                self.add_object(Cube(self.app, position=(x, -y, z)))

    def render(self):
        """
        Renders each object in the object list
        """
        for obj in self.objects:
            obj.render()
