from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFile, Vec3, ClockObject
from panda3d.bullet import BulletWorld, BulletDebugNode
from direct.filter.CommonFilters import CommonFilters
from camera import CameraController
from entity import Entity
from ship import Ship
from lighting import Lighting
import random

class scene():
    def __init__(self,base) -> None:
        self.base = base
        self.clock = ClockObject().getGlobalClock()

        Lighting(base)
        #CameraController(base)

        base.disableMouse()
        Ship(base)


        cf = CommonFilters(base.win, base.cam)
        cf.setBloom(intensity = 10)
        ShowBase.setBackgroundColor(base, 0.0, 0.0, 0.0, 1.0)

        Entity(base, position=(0,0,-100), scale=(1000,1000,1),color=(1,0,0,1))

        base.bullet_world = BulletWorld()
        base.bullet_world.setGravity(Vec3(0, 0, -9.81))
        
        skybox = Entity(base, scale = (1000, 1000, 1000), texture='textures/skybox/cubemap.png', model = "models/skybox.egg", color = (0.1, 0.1, 0.1, 1))
        skybox.entity.setTwoSided(True)

        #Entity(base, position = (0,10,-2),rotation = (0,90,0), collider = 'dynamic', color=(0.2, 0.2, 0.2, 1), model='models/ship.obj')

        Entity(base, model='models/zup-axis')

        for x in range(500):
            Entity(base, model='models/sphere', position=(random.randint(-500,500), random.randint(-500,500), random.randint(-500,500)), scale=(0.5,0.5,0.5), color = (1, random.uniform(0.8,1), random.uniform(0.5,1), 1))

        
        #Lighting(self, False)
    
    def update_Scene(self, task):
        dt = self.clock.dt

        self.base.bullet_world.doPhysics(dt)

        return task