from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFile

class window(ShowBase):
    def __init__(self, fStartDirect=True, windowType=None):
        super().__init__(fStartDirect, windowType)

window().run()