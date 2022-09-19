import numpy as np
from abc import ABC, abstractmethod

from utils import action, utils


class Mode:
    # 基础模式
    keymap = None

    def __init__(self):
        if self.keymap is None:
            raise Exception('基础模式中，keymap参数不能为空')

    def task_action(self, keystroke, action_name, action_state):
        base.accept(keystroke, self.update_keymap, [action_name, action_state])

    def update_keymap(self, action_name, action_state):
        self.keymap[action_name] = action_state

    def add_task(self, method, name):
        base.taskMgr.add(method, name)

    def remove_task(self, name):
        base.taskMgr.remove(name)

    @abstractmethod
    def enter(self):
        pass

    @abstractmethod
    def exit(self):
        pass


class CameraMode(Mode):
    # 相机控制模式
    keymap = {
        action.move: False,  # move camera
        action.quit: False,  # exit to menu
        action.zoom: False,  # zoom the camera
    }

    def enter(self):
        # self.mouse.hide()
        self.mouse.relative()
        self.mouse.track()

        self.task_action('escape', action.quit, True)
        self.task_action('mouse1', action.zoom, True)
        self.task_action('mouse1-up', action.zoom, False)
        self.task_action('v', action.move, True)
        self.task_action('v-up', action.move, False)
        # self.add_task(self.update_camera, 'update_camera')
        self.add_task(self.view_task, 'view_task')
        self.add_task(self.quit_task, 'quit_task')

    def exit(self):
        self.remove_task('view_task')
        self.remove_task('quit_task')

    def update_camera(self):
        fx, fy = 20, 3
        with self.mouse:
            alpha_x = self.player_cam.focus.getH() - fx * self.mouse.get_dx()
            alpha_y = max(min(0, self.player_cam.focus.getR() + fy * self.mouse.get_dy()), -90)
        self.player_cam.focus.setH(alpha_x)
        self.player_cam.focus.setR(alpha_y)
        self.cue.fix_cue_stick_to_camera(self.player_cam)

    def view_task(self, task):
        if self.keymap[action.zoom]:
            self.zoom_camera()
        elif self.keymap[action.move]:
            self.move_camera()
            self.exit()
        else:
            self.update_camera()

        return task.cont

    def quit_task(self, task):
        if self.keymap[action.quit]:
            self.keymap[action.quit] = False

        return task.cont

    def scale_focus(self):
        """Scale the camera's focus object

        The focus marker is a small dot to show where the camera is centered, and where it rotates
        about. This helps a lot in navigating the camera effectively. Here the marker is scaled
        so that it is always a constant size, regardless of how zoomed in or out the camera is.
        """
        # `dist` is the distance from the camera to the focus object and is equivalent to:
        # cam_pos, focus_pos = self.player_cam.node.getPos(render), self.player_cam.focus_object.getPos(render)
        # dist = (cam_pos - focus_pos).length()
        dist = self.player_cam.node.getX()
        self.player_cam.focus_object.setScale(0.002*dist)

    def zoom_camera(self):
        with self.mouse:
            s = -self.mouse.get_dy() * 0.3

        self.player_cam.node.setPos(utils.multiply_cw(self.player_cam.node.getPos(), 1 - s))
        self.scale_focus()

    def move_camera(self):
        print("准备移动相机")
        with self.mouse:
            dxp, dyp = self.mouse.get_dx(), self.mouse.get_dy()

        h = self.player_cam.focus.getH() * np.pi / 180 + np.pi / 2
        dx = dxp * np.cos(h) - dyp * np.sin(h)
        dy = dxp * np.sin(h) + dyp * np.cos(h)

        f = 0.6
        self.player_cam.focus.setX(self.player_cam.focus.getX() + dx * f)
        self.player_cam.focus.setY(self.player_cam.focus.getY() + dy * f)

    def rotate_camera(self):
        if self.keymap[action.fine_control]:
            fx, fy = 2, 0
        else:
            fx, fy = 13, 3

        with self.mouse:
            alpha_x = self.player_cam.focus.getH() - fx * self.mouse.get_dx()
            alpha_y = max(min(0, self.player_cam.focus.getR() + fy * self.mouse.get_dy()), -90)

        self.player_cam.focus.setH(alpha_x)
        self.player_cam.focus.setR(alpha_y)
