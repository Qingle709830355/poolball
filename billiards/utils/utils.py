import numpy as np


from panda3d.core import *


def panda_path(path):
    return str(Filename.fromOsSpecific(str(path)))


def unit_vector(vector):
    """获取单位向量"""
    return vector / np.linalg.norm(vector)


def angle(v2, v1=(1,0)):
    """
    计算v1, v2 在x, y 轴的逆时针角度
    :param v2:
    :param v1:
    :return:
    """

    ang2 = np.arctan2(v2[1], v2[0])
    ang1 = np.arctan2(v1[1], v1[0])

    return ang2 - ang1


def coordinate_rotation(v, phi):
    rotation = np.array([[np.cos(phi), -np.sin(phi), 0],
                         [np.sin(phi), np.cos(phi), 0],
                         [0, 0, 1]])

    return np.matmul(rotation, v)


def normalize(*args):
    myVec = LVector3(*args)
    myVec.normalize()
    return myVec


def make_rectangle(x1, y1, z1, x2, y2, z2, name='rectangle'):
    fmt = GeomVertexFormat.getV3n3cpt2()
    vdata = GeomVertexData('rectangle', fmt, Geom.UHDynamic)

    vertex = GeomVertexWriter(vdata, 'vertex')
    normal = GeomVertexWriter(vdata, 'normal')
    #texcoord = GeomVertexWriter(vdata, 'texcoord')

    # make sure we draw the sqaure in the right plane
    if x1 != x2:
        vertex.addData3(x1, y1, z1)
        vertex.addData3(x2, y1, z1)
        vertex.addData3(x2, y2, z2)
        vertex.addData3(x1, y2, z2)

        # FIXME calculate the norm
        normal.addData3(normalize(0,0,1))
        normal.addData3(normalize(0,0,1))
        normal.addData3(normalize(0,0,1))
        normal.addData3(normalize(0,0,1))

    else:
        vertex.addData3(x1, y1, z1)
        vertex.addData3(x2, y2, z1)
        vertex.addData3(x2, y2, z2)
        vertex.addData3(x1, y1, z2)

        # FIXME calculate the norm
        normal.addData3(normalize(0,0,1))
        normal.addData3(normalize(0,0,1))
        normal.addData3(normalize(0,0,1))
        normal.addData3(normalize(0,0,1))

    # FIXME calculate with a scale or something
    #scale = 1
    #texcoord.addData2f(0.0, scale)
    #texcoord.addData2f(0.0, 0.0)
    #texcoord.addData2f(scale, 0.0)
    #texcoord.addData2f(scale, scale)

    tris = GeomTriangles(Geom.UHDynamic)
    tris.addVertices(0, 1, 3)
    tris.addVertices(1, 2, 3)

    rectangle = Geom(vdata)
    rectangle.addPrimitive(tris)
    rectangle_node = GeomNode(name)
    rectangle_node.addGeom(rectangle)

    return rectangle_node


def unit_vector_fast(vector, handle_zero=False):
    """Returns the unit vector of the vector (just-in-time compiled)

    Notes
    =====
    - Unlike unit_vector, this does not support 2D arrays
    - Speed comparison in pooltool/tests/speed/unit_vector.py
    """
    norm = np.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)
    if handle_zero and norm == 0.0:
        norm = 1.0
    return vector / norm


def multiply_cw(v, c):
    return LVector3(v[0]*c, v[1]*c, v[2]*c)

