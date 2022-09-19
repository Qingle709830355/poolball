from pathlib import Path

import simplepbr
from direct.showbase.ShowBase import ShowBase

import numpy as np
from panda3d.core import loadPrcFile

from billiards.objects.table import Table
from billiards.objects.ball import Ball
from billiards.utils import constant, settings
from billiards.objects.mouse import Mouse
from billiards.objects.camera import PlayerCam
from core.mode import CameraMode
from objects.cue import Cue

loadPrcFile(settings.CONFIG_PATH / "config.prc")


class MyGame(ShowBase, CameraMode):

    def __init__(self):
        ShowBase.__init__(self)
        # 关闭默认的相机配置
        self.disableMouse()
        # 基础设置
        self.setBackgroundColor(0.04, 0.04, 0.04)
        simplepbr.init(enable_shadows=1, max_lights=13)
        self.mouse = Mouse()
        self.player_cam = PlayerCam()
        self.init_scene()
        self.cue.fix_cue_stick_to_camera(self.player_cam)
        # self.task_mgr.add(self.update_camera, "update_camera")

    def init_scene(self):
        self.scene = self.render.attachNewNode("scene")
        table = Table(w=0.9906, l=1.9812, h=0.708)
        table.draw()
        ball1 = Ball(ball_id='cue', rvw=np.array([
            [0.4, 0.35, constant.R],
            [0, 0, 0],
            [0, 0, 0]
        ]))
        ball1.draw()

        for i in range(5, 15):
            ball = Ball(ball_id=str(i), rvw=np.array([
                [0.9 - constant.R * (i - 4) * 2.5, 1.7, constant.R],
                [0, 0, 0],
                [0, 0, 0]
            ]))
            ball.draw()
        self.player_cam.create_focus(
            parent=self.render.find("scene").find("cloth"),
            pos=(table.width/2, table.length/2, constant.R)
        )

        # 画球杆
        cue = Cue()
        cue.draw(ball1)
        self.cue = cue
        self.enter()


app = MyGame()
app.run()
