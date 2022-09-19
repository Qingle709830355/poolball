import numpy as np
from panda3d.core import Texture, NodePath

from utils import constant, settings, utils


class Table:

    def __init__(self, **kwargs):
        # 宽度
        self.width = kwargs.get('w')
        # 长度
        self.length = kwargs.get('l')
        # 高度
        self.height = kwargs.get('h')
        # 直线侧垫宽度
        self.cushion_width = 0.0508
        # 直线测点高度
        self.cushion_height = 0.036576
        self.corner_pocket_width = 0.118
        self.corner_pocket_angle = 5.3
        self.corner_pocket_depth = 0.0398
        self.corner_pocket_radius = 0.0612
        self.corner_jaw_radius = 0.02095
        self.side_pocket_width = 0.137
        self.side_pocket_angle = 7.14
        self.side_pocket_depth = 0.00437
        self.side_pocket_radius = 0.0645
        self.side_jaw_radius = 0.00795
        # 口袋
        self.packets = {}
        # 球垫
        self.ball_mats = {}

    def draw(self):
        # 画桌布
        self.init_cloth()

    def init_cloth(self):
        # 初始化桌布
        table_path = settings.ASSET_PATH / "table" / "7_foot" / "7_foot_pbr.glb"
        table = loader.loadModel(table_path)
        table.reparentTo(render.find("scene"))
        table.setScale(self.width, self.length, 1)
        table.setName("cloth")

    def get_cushion_segments(self):
        # 获取所有桌垫数据
        cw = self.cushion_width
        ca = (self.corner_pocket_angle + 45) * np.pi / 180
        sa = self.side_pocket_angle * np.pi / 180
        pw = self.corner_pocket_width
        sw = self.side_pocket_width
        h = self.cushion_height
        rc = self.corner_jaw_radius
        rs = self.side_jaw_radius
        dc = self.corner_jaw_radius / np.tan((np.pi / 2 + ca) / 2)
        ds = self.side_jaw_radius / np.tan((np.pi / 2 + sa) / 2)

        cushion_segments = {
            'linear': {
                # long segments
                '3': LinearCushionSegment(
                    '3_edge',
                    p1=(0, pw * np.cos(np.pi / 4) + dc, h),
                    p2=(0, (self.length - sw) / 2 - ds, h),
                    direction=1
                ),
                '6': LinearCushionSegment(
                    '6_edge',
                    p1=(0, (self.length + sw) / 2 + ds, h),
                    p2=(0, -pw * np.cos(np.pi / 4) + self.length - dc, h),
                    direction=1
                ),
                '15': LinearCushionSegment(
                    '15_edge',
                    p1=(self.width, pw * np.cos(np.pi / 4) + dc, h),
                    p2=(self.width, (self.length - sw) / 2 - ds, h),
                    direction=0
                ),
                '12': LinearCushionSegment(
                    '12_edge',
                    p1=(self.width, (self.length + sw) / 2 + ds, h),
                    p2=(self.width, -pw * np.cos(np.pi / 4) + self.length - dc, h),
                    direction=0
                ),
                '18': LinearCushionSegment(
                    '18_edge',
                    p1=(pw * np.cos(np.pi / 4) + dc, 0, h),
                    p2=(-pw * np.cos(np.pi / 4) + self.width - dc, 0, h),
                    direction=1
                ),
                '9': LinearCushionSegment(
                    '9_edge',
                    p1=(pw * np.cos(np.pi / 4) + dc, self.length, h),
                    p2=(-pw * np.cos(np.pi / 4) + self.width - dc, self.length, h),
                    direction=0
                ),
                # side jaw segments
                '5': LinearCushionSegment(
                    '5_edge',
                    p1=(-cw, (self.length + sw) / 2 - cw * np.sin(sa), h),
                    p2=(-ds * np.cos(sa), (self.length + sw) / 2 - ds * np.sin(sa), h),
                    direction=0
                ),
                '4': LinearCushionSegment(
                    '4_edge',
                    p1=(-cw, (self.length - sw) / 2 + cw * np.sin(sa), h),
                    p2=(-ds * np.cos(sa), (self.length - sw) / 2 + ds * np.sin(sa), h),
                    direction=1
                ),
                '13': LinearCushionSegment(
                    '13_edge',
                    p1=(self.width + cw, (self.length + sw) / 2 - cw * np.sin(sa), h),
                    p2=(self.width + ds * np.cos(sa), (self.length + sw) / 2 - ds * np.sin(sa), h),
                    direction=0
                ),
                '14': LinearCushionSegment(
                    '14_edge',
                    p1=(self.width + cw, (self.length - sw) / 2 + cw * np.sin(sa), h),
                    p2=(self.width + ds * np.cos(sa), (self.length - sw) / 2 + ds * np.sin(sa), h),
                    direction=1
                ),
                # corner jaw segments
                '1': LinearCushionSegment(
                    '1_edge',
                    p1=(pw * np.cos(np.pi / 4) - cw * np.tan(ca), -cw, h),
                    p2=(pw * np.cos(np.pi / 4) - dc * np.sin(ca), -dc * np.cos(ca), h),
                    direction=1
                ),
                '2': LinearCushionSegment(
                    '2_edge',
                    p1=(-cw, pw * np.cos(np.pi / 4) - cw * np.tan(ca), h),
                    p2=(-dc * np.cos(ca), pw * np.cos(np.pi / 4) - dc * np.sin(ca), h),
                    direction=0
                ),
                '8': LinearCushionSegment(
                    '8_edge',
                    p1=(pw * np.cos(np.pi / 4) - cw * np.tan(ca), cw + self.length, h),
                    p2=(pw * np.cos(np.pi / 4) - dc * np.sin(ca), self.length + dc * np.cos(ca), h),
                    direction=0
                ),
                '7': LinearCushionSegment(
                    '7_edge',
                    p1=(-cw, -pw * np.cos(np.pi / 4) + cw * np.tan(ca) + self.length, h),
                    p2=(-dc * np.cos(ca), -pw * np.cos(np.pi / 4) + self.length + dc * np.sin(ca), h),
                    direction=1
                ),
                '11': LinearCushionSegment(
                    '11_edge',
                    p1=(cw + self.width, -pw * np.cos(np.pi / 4) + cw * np.tan(ca) + self.length, h),
                    p2=(self.width + dc * np.cos(ca), -pw * np.cos(np.pi / 4) + self.length + dc * np.sin(ca), h),
                    direction=1
                ),
                '10': LinearCushionSegment(
                    '10_edge',
                    p1=(-pw * np.cos(np.pi / 4) + cw * np.tan(ca) + self.width, cw + self.length, h),
                    p2=(-pw * np.cos(np.pi / 4) + self.width + dc * np.sin(ca), self.length + dc * np.cos(ca), h),
                    direction=0
                ),
                '16': LinearCushionSegment(
                    '16_edge',
                    p1=(cw + self.width, +pw * np.cos(np.pi / 4) - cw * np.tan(ca), h),
                    p2=(self.width + dc * np.cos(ca), pw * np.cos(np.pi / 4) - dc * np.sin(ca), h),
                    direction=0
                ),
                '17': LinearCushionSegment(
                    '17_edge',
                    p1=(-pw * np.cos(np.pi / 4) + cw * np.tan(ca) + self.width, -cw, h),
                    p2=(-pw * np.cos(np.pi / 4) + self.width + dc * np.sin(ca), -dc * np.cos(ca), h),
                    direction=1
                ),
            },
            'circular': {
                '1t': CircularCushionSegment('1t', center=(pw * np.cos(np.pi / 4) + dc, -rc, h), radius=rc),
                '2t': CircularCushionSegment('2t', center=(-rc, pw * np.cos(np.pi / 4) + dc, h), radius=rc),
                '4t': CircularCushionSegment('4t', center=(-rs, self.length / 2 - sw / 2 - ds, h), radius=rs),
                '5t': CircularCushionSegment('5t', center=(-rs, self.length / 2 + sw / 2 + ds, h), radius=rs),
                '7t': CircularCushionSegment('7t', center=(-rc, self.length - (pw * np.cos(np.pi / 4) + dc), h), radius=rc),
                '8t': CircularCushionSegment('8t', center=(pw * np.cos(np.pi / 4) + dc, self.length + rc, h), radius=rc),
                '10t': CircularCushionSegment('10t', center=(self.width - pw * np.cos(np.pi / 4) - dc, self.length + rc, h),
                                              radius=rc),
                '11t': CircularCushionSegment('11t', center=(self.width + rc, self.length - (pw * np.cos(np.pi / 4) + dc), h),
                                              radius=rc),
                '13t': CircularCushionSegment('13t', center=(self.width + rs, self.length / 2 + sw / 2 + ds, h), radius=rs),
                '14t': CircularCushionSegment('14t', center=(self.width + rs, self.length / 2 - sw / 2 - ds, h), radius=rs),
                '16t': CircularCushionSegment('16t', center=(self.width + rc, pw * np.cos(np.pi / 4) + dc, h), radius=rc),
                '17t': CircularCushionSegment('17t', center=(self.width - pw * np.cos(np.pi / 4) - dc, -rc, h), radius=rc),
            },
        }
        return cushion_segments


class LinearCushionSegment:
    # 直线桌垫
    def __init__(self, linear_id, p1, p2, direction=2):
        self.linear_id = linear_id
        self.p1 = np.array(p1, dtype=np.float64)
        self.p2 = np.array(p2, dtype=np.float64)

        p1x, p1y, p1z = self.p1
        p2x, p2y, p2z = self.p2

        if p1z != p2z:
            raise ValueError(f"LinearCushionSegment with id '{self.linear_id}' has points p1 and p2 with different cushion heights (h)")
        self.height = p1z

        if (p2x - p1x) == 0:
            self.lx = 1
            self.ly = 0
            self.l0 = -p1x
        else:
            self.lx = - (p2y - p1y) / (p2x - p1x)
            self.ly = 1
            self.l0 = (p2y - p1y) / (p2x - p1x) * p1x - p1y

        self.normal = utils.unit_vector_fast(np.array([self.lx, self.ly, 0]))

        if direction not in {0, 1, 2}:
            raise Exception("LinearCushionSegment :: `direction` must be 0, 1, or 2.")

        self.direction = direction


class CircularCushionSegment:
    # 圆形桌垫
    def __init__(self, circular_id, center, radius):

        self.circular_id = circular_id
        self.center = center
        self.height = center[2]

        self.a, self.b = self.center[:2]
