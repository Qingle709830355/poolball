import numpy as np
from panda3d.core import SamplerState, TransparencyAttrib

from utils import constant, settings


class Ball:

    def __init__(self, ball_id, rvw):
        # 半径
        self.R = constant.R
        # 球质量
        self.M = constant.m
        # 角动量  2mr^2 / 5
        self.I = 2 * self.M * self.R ** 2 / 5
        # rvw   r: 位移向量, v 速度向量, w 角速度向量
        self.rvw = rvw
        # 编号
        self.ball_id = ball_id
        # 颜色
        self.color = None

    def draw(self):
        position = render.find("scene").find('cloth').attachNewNode(f"ball_{self.ball_id}_position")
        p = settings.ASSET_PATH / "balls" / "set_1"
        ball_path = p / f"{self.ball_id}.glb"
        # 加载球体模型
        ball = loader.loadModel(ball_path)
        # 放置到桌面上
        ball.reparentTo(position)
        # 加载球体材质
        ball_tex = ball.find_texture(ball_path.stem)
        ball_tex.set_minfilter(SamplerState.FT_linear)
        ball.setScale(self.get_scale_factor(ball))
        position.setPos(*self.rvw[0, :])
        self.ball = position
        self.init_shadow()

    def init_shadow(self):
        N = 20
        start, stop = 0.5, 0.9  # fraction of ball radius
        z_offset = 0.0005
        scales = np.linspace(start, stop, N)

        shadow_path = settings.ASSET_PATH / 'balls' / 'set_1' / f'shadow.glb'
        shadow_node = render.find('scene').find('cloth').attachNewNode(f'shadow_{self.ball_id}')
        shadow_node.setPos(self.rvw[0, 0], self.rvw[0, 1], 0)

        # allow transparency of shadow to change
        shadow_node.setTransparency(TransparencyAttrib.MAlpha)

        for i, scale in enumerate(scales):
            shadow_layer = base.loader.loadModel(shadow_path)
            shadow_layer.reparentTo(shadow_node)
            shadow_layer.setScale(self.get_scale_factor(shadow_layer) * scale)
            shadow_layer.setZ(z_offset * (1 - i / N))

        return shadow_node

    def get_pos(self):
        return self.ball.getPos()

    def get_scale_factor(self, node):
        """Find scale factor to match model size to ball's SI radius"""
        m, M = node.getTightBounds()
        model_R = (M - m)[0]/2

        return self.R / model_R




