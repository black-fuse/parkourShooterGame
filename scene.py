from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFile, Vec3
from panda3d.bullet import BulletWorld, BulletDebugNode
from direct.filter.CommonFilters import CommonFilters
from camera import CameraController
from entity import Entity
from ship import ship
import random

class scene():
    def __init__(self,base) -> None:
        
        #CameraController(base)
        ship(base)
        cf = CommonFilters(base.win, base.cam)
        cf.setBloom(intensity = 5)
        ShowBase.setBackgroundColor(base, 0.0, 0.0, 0.0, 1.0)

        base.bullet_world = BulletWorld()
        base.bullet_world.setGravity(Vec3(0, 0, -9.81))
        
        skybox = Entity(base, scale = (1000, 1000, 1000), texture='textures/skybox/cubemap.png', model = "models/skybox.egg")
        skybox.entity.setTwoSided(True)

        for x in range(500):
            Entity(base, model='models/sphere', position=(random.randint(-100,100), random.randint(-100,100), random.randint(-100,100)), scale=(0.2,0.2,0.2), color = (1, random.uniform(0.8,1), random.uniform(0.5,1), 1))

        
        #Lighting(self, False)