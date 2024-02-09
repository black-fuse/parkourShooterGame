from panda3d.core import ClockObject, WindowProperties, NodePath, Vec3


plane_turn_sensitivity = 0.1
plane_max_turn_speed = 4.0
plane_turn_smoothness = 10.0
thruster_strength = 0.05


class Ship(NodePath):
    def __init__(self, base):
        super().__init__("Ship")

        self.base = base
        
        self.ship_dummy = NodePath("ship_dummy")
        self.ship_dummy.reparentTo(self)

        self.ship_object = base.loader.loadModel("models/ship.egg")
        self.ship_object.reparentTo(self.ship_dummy)

        self.cam_dummy = NodePath("cam_dummy")
        self.cam_dummy.reparentTo(self)

        base.cam.reparentTo(self.cam_dummy)
        base.cam.setPos(0.0, -20.0, 5.0)

        self.cur_cam_jaw = 0

        self.cur_jaw = 0
        self.cur_pitch = 0
        self.target_jaw = 0
        self.target_pitch = 0

        self.forward = Vec3(0.0, -1.0, 0.0)
        self.velocity = Vec3(0.0, -1.0, 0.0)

        self.globalClock = ClockObject().getGlobalClock()
        base.taskMgr.add(self.updateShip, "update_cam")

        base.accept("escape", self.toggleMouseVis)
        self.mouse_hidden = base.config.GetBool("cursor-hidden", 0)

        self.reparentTo(base.render)

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

    def processMouseMovement(self, x_offset, y_offset):
        x_offset *= plane_turn_sensitivity
        y_offset *= plane_turn_sensitivity

        self.target_jaw += x_offset
        self.target_pitch += y_offset

    def updateShip(self, task):
        dt = self.globalClock.dt

        # mouse input
        if (self.mouse_hidden):
            md = self.base.win.getPointer(0)
            display_center = (self.base.win.getXSize() // 2, self.base.win.getYSize() // 2)
            mouse_pos = (md.getX(), md.getY())
            mouse_move = [mouse_pos[i] - display_center[i] for i in range(2)]

            self.processMouseMovement(-mouse_move[0], -mouse_move[1])

            self.base.win.movePointer(0, display_center[0], display_center[1])

        self.cur_jaw += min((self.target_jaw - self.cur_jaw) / plane_turn_smoothness, plane_max_turn_speed)
        self.cur_pitch += min((self.target_pitch - self.cur_pitch) / plane_turn_smoothness, plane_max_turn_speed)

        self.ship_dummy.setR(self.cur_jaw)
        self.ship_object.setP(self.cur_pitch)

        self.setPos(self.getPos() + self.velocity)

        self.forward = self.base.render.getRelativeVector(self.ship_object, Vec3(0.0, -1.0, 0.0))

        self.velocity = (self.forward * thruster_strength + self.velocity).normalized()


        self.cur_cam_jaw += (self.cur_jaw - self.cur_cam_jaw) / 20

        self.cam_dummy.lookAt((self.forward + self.velocity).normalized())
        self.cam_dummy.setR(-self.cur_cam_jaw)

        return task.cont