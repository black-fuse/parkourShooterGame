from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFile, Vec3, ClockObject
from panda3d.bullet import BulletWorld, BulletDebugNode
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *

from entity import Entity
from lighting import Lighting
from scene import scene
import random

class window(ShowBase):
    def __init__(self, fStartDirect=True, windowType=None):
        loadPrcFile("config/config.prc")
        super().__init__(fStartDirect, windowType)


        self.task_mgr.add(self.update, "update funciton")
        self.clock = ClockObject().getGlobalClock()


        self.bullet_world = BulletWorld()
        self.bullet_world.setGravity(Vec3(0, 0, -9.81))


        self.OpenMenu()
    
    def OpenMenu(self):
        self.StartButton = DirectButton(text="start",command=self.LoadScene,scale=0.3)
        self.QuitButton = DirectButton(text="quit", command=quit, scale=0.3)

        self.QuitButton.setPos((0,0,-0.8))

    def LoadScene(self):
        self.camLens.setFov(90.0)
        self.camLens.setNearFar(0.1, 10000.0)
        scene(self)
        self.StartButton.destroy()
        self.QuitButton.destroy()


    def update(self, task):
        dt = self.clock.dt

        key_down = self.mouseWatcherNode.isButtonDown

        self.bullet_world.doPhysics(dt)

        if key_down("`"):
            quit()

        return task.cont

window().run()