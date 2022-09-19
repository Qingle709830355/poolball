from objects.ball import Ball
from utils import settings, constant


class Cue:

    def __init__(self, **kwargs):
        # 球杆重量
        self.M = constant.M
        self.follow = None

    def draw(self, ball):
        self.init_model()
        self.init_focus(ball)

    def init_model(self):
        cue_path = settings.ASSET_PATH / "cue" / "cue.glb"
        cue = loader.loadModel(cue_path)
        cue.setName('cue_stick_model')
        cue_stick = render.find('scene').find('cloth').attachNewNode('cue_stick')
        cue.reparentTo(cue_stick)
        self.cue_stick = cue_stick
        self.cue = cue

    def init_focus(self, ball: Ball):
        # 初始化焦点, 一般跟随母球
        self.follow = ball
        self.cue.setPos(ball.R, 0, 0)
        self.cue_stick_focus = render.find('scene').find('cloth').attachNewNode('cue_stick_focus')
        self.update_focus()
        self.cue_stick.reparentTo(self.cue_stick_focus)

    def fix_cue_stick_to_camera(self, cam):
        self.cue.setH(cam.focus.getH())

    def update_focus(self):
        self.cue.setPos(self.follow.get_pos())

    def strike(self):
        # 击球动作
        pass