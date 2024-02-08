from panda3d.core import ClockObject, WindowProperties, NodePath


class Ship(NodePath):
    def __init__(self, base):
        super().__init__("Ship")

        self.base = base
        
        self.ship_dummy = NodePath("ship_dummy")
        self.ship_dummy.reparentTo(self)

        self.ship_object = base.loader.loadModel("models/ship.egg")
        self.ship_object.reparentTo(self.ship_dummy)

        self.mouse_sensitivity = 0.1

        self.cur_jaw = 0
        self.cur_pitch = 0
        self.target_jaw = 0
        self.target_pitch = 0

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
        x_offset *= self.mouse_sensitivity
        y_offset *= self.mouse_sensitivity

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

        self.cur_jaw = (self.target_jaw - self.cur_jaw) / 2
        self.cur_pitch = (self.target_pitch - self.cur_pitch) / 2

        self.ship_dummy.setR(self.cur_jaw)
        self.ship_object.setP(self.cur_pitch)

        return task.cont