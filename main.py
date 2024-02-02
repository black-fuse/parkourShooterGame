from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFile, Vec3
from panda3d.bullet import BulletWorld, BulletDebugNode
from physics import physics

class window(ShowBase):
    def __init__(self, fStartDirect=True, windowType=None):
        loadPrcFile("config/config.prc")
        super().__init__(fStartDirect, windowType)

        self.bullet_world = BulletWorld()
        self.bullet_world.setGravity(Vec3(0, 0, -9.81))

        self.NewObject(scale=(10,10,1))
    
    def NewObject(self, model='models/cube.egg', position=(0,0,0), scale=(1,1,1), texture='textures/blue.png'):
        self.object = self.loader.loadModel(model)
        self.object.setPos(position)
        self.object.setScale(scale)
        texture = self.loader.loadTexture(texture)
        self.object.setTexture(texture)
        physics.applyBoxCollider(self, self.object)
        self.object.reparentTo(self.render)
    

    def update(self, task):
        dt = self.globalclock.dt

        key_down = self.mouseWatcherNode.isButtonDown

        self.bullet_world.doPhysics(dt)


        if key_down("escape"):
            quit()

        return task.cont

window().run()