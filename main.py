from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFile, Vec3
from panda3d.bullet import BulletWorld, BulletDebugNode
from entity import Entity
from lighting import Lighting
import random

class window(ShowBase):
    def __init__(self, fStartDirect=True, windowType=None):
        loadPrcFile("config/config.prc")
        super().__init__(fStartDirect, windowType)

        ShowBase.setBackgroundColor(self, 0.0, 0.0, 0.0, 1.0)

        self.bullet_world = BulletWorld()
        self.bullet_world.setGravity(Vec3(0, 0, -9.81))

        Entity(self, scale=(10,10,1), color=(1,0,0,1))
        Entity(self, position=(1, 1, 1), color=(0,0,0.3,1))

        for x in range(500):
            Entity(self, position=(random.randint(-100,100), random.randint(-100,100), random.randint(-100,100)), scale=(0.2,0.2,0.2))

        
        #Lighting(self, False)
    


    def update(self, task):
        dt = self.globalclock.dt

        key_down = self.mouseWatcherNode.isButtonDown

        self.bullet_world.doPhysics(dt)

        if key_down("escape"):
            quit()

        return task.cont

window().run()