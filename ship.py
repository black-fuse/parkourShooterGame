from math import sin, cos, radians
from panda3d.core import Vec3, ClockObject, WindowProperties
from entity import Entity

class ship:
    def __init__(self, base) -> None:

        self.base = base

        self.shipObject = Entity(base, collider='dynamic')
        self.base.cam.reparentTo(self.shipObject.entity)


        #important stuff
        self.CamPos = Vec3(0.0, 0.0, 0.0)
        self.forward = Vec3(0.0, 1.0, 0.0)
        self.BaseSpeed = 3
        self.Speed = 20
        self.turningRadius = 40


        self.mouse_sensitivity = 0.1
        self.jaw = 0
        self.pitch = 0


        self.globalClock = ClockObject().getGlobalClock()
        self.base.taskMgr.add(self.update_cam, "updates the camera")

        self.mouse_hidden = base.config.GetBool("cursor-hidden", 0)
        base.accept("escape", self.toggleMouseVis)


        pass

    def processMouseMovement(self, x_offset, y_offset, constrain_pitch=True):
        x_offset *= self.mouse_sensitivity
        y_offset *= self.mouse_sensitivity

        self.jaw += x_offset
        self.pitch += y_offset

        if constrain_pitch:
            if self.pitch > 89:
                self.pitch = 89
            if self.pitch < -89:
                self.pitch = -89

        self.updateCameraVectors()


    def updateCameraVectors(self):
        front = Vec3(0.0, 1.0, 0.0)
        front.x = cos(radians(self.jaw)) * cos(radians(self.pitch))
        front.z = sin(radians(self.pitch))
        front.y = sin(radians(self.jaw)) * cos(radians(self.pitch))

        self.camera_front = front.normalized()
        self.camera_right = (self.camera_front.cross(Vec3(0.0, 0.0, 1.0))).normalized()

    def toggleMouseVis(self):
        if (self.mouse_hidden):
            props = WindowProperties()
            props.setCursorHidden(False)
            self.base.win.requestProperties(props)
            self.mouse_hidden = False
        else:
            props = WindowProperties()
            props.setCursorHidden(True)
            self.base.win.requestProperties(props)
            self.mouse_hidden = True

    def update_cam(self, task):
        dt = self.globalClock.dt


        if (self.mouse_hidden):
            md = self.base.win.getPointer(0)
            display_center = (self.base.win.getXSize() // 2, self.base.win.getYSize() // 2)
            mouse_pos = (md.getX(), md.getY())
            mouse_move = [mouse_pos[i] - display_center[i] for i in range(2)]

            self.processMouseMovement(-mouse_move[0], -mouse_move[1])

            self.base.win.movePointer(0, display_center[0], display_center[1])



        velocity = self.forward * self.BaseSpeed * dt

        key_down = self.base.mouseWatcherNode.isButtonDown
        if key_down("w"):
            velocity += self.forward * self.BaseSpeed * self.Speed * dt
            print(velocity)
        
        self.shipObject.collider.node().setLinearVelocity(velocity * 40.0)
        self.base.camera.setPos(self.CamPos)


        return task.cont
