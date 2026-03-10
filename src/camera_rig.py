import numpy as np
from pxr import Gf
from isaacsim.sensors.camera import Camera

class StereoRig:
    def __init__(self, resolution, focal_length, baseline):
        self.baseline = baseline
        self.cam_l = Camera(prim_path="/World/cam_l", resolution=resolution)
        self.cam_r = Camera(prim_path="/World/cam_r", resolution=resolution)
        
        for cam in [self.cam_l, self.cam_r]:
            cam.initialize()
            cam.set_focal_length(focal_length)
            cam.set_clipping_range(near_distance=0.01, far_distance=10000.0)

    def set_stereo_pose(self, center_pos, rig_quat):
        """
        Method 1: Setting up a stereo camera using a given absolute pose

        Suitable for scenarios with an externally input fixed trajectory or rigid attachment to the end effector of a robotic arm.

        :param center_pos: [x, y, z] World coordinates of the array center

        :param rig_quat: [w, x, y, z] Absolute pose quaternion of the array
        """
        # 将 numpy 的四元数转为 Gf.Quatd (注意: Isaac Sim 默认实部 w 在前)
        quat = Gf.Quatd(rig_quat[0], rig_quat[1], rig_quat[2], rig_quat[3])
        
        # 在修正后的局部坐标系中，+Y 轴始终代表正左侧
        local_left = Gf.Vec3d(0, 1, 0)
        
        # 将局部的左侧向量直接施加四元数旋转，得到世界坐标系下的绝对左侧向量
        world_left = Gf.Rotation(quat).TransformDir(local_left)
        world_left_np = np.array(world_left)
        
        # 计算左右相机位置
        pos_l = center_pos + world_left_np * (self.baseline / 2.0)
        pos_r = center_pos - world_left_np * (self.baseline / 2.0)
        
        self.cam_l.set_world_pose(position=pos_l, orientation=rig_quat)
        self.cam_r.set_world_pose(position=pos_r, orientation=rig_quat)
        
        return pos_l, pos_r, rig_quat

    def set_stereo_pose_lookat(self, center_pos, target_point, roll=0.0):
        """
        方法二：使用注视目标逻辑设置双目相机
        
        :param center_pos: [x, y, z] 阵列中心的世界坐标
        :param target_point: [x, y, z] 目标点的世界坐标
        :param roll: 横滚角 (角度)。默认 0 表示上方尽量指向世界 +Z
        """
        eye = Gf.Vec3d(*center_pos.tolist())
        target = Gf.Vec3d(*target_point.tolist())
        
        # 1. 计算视线方向 (Forward)
        forward_dir = target - eye
        if forward_dir.GetLength() > 1e-6:
            forward_dir.Normalize()
        else:
            forward_dir = Gf.Vec3d(1, 0, 0) # 极端重合情况
            
        # 2. 处理横滚角 (Roll) 以计算真实的 Up 向量
        base_up = Gf.Vec3d(0, 0, 1) # 默认世界朝上
        if roll != 0.0:
            # 如果传入了 Roll，让基础 Up 向量绕着视线方向旋转
            roll_rot = Gf.Rotation(forward_dir, roll)
            actual_up = roll_rot.TransformDir(base_up)
        else:
            actual_up = base_up
            
        # 3. 计算 LookAt 矩阵
        lookat_m = Gf.Matrix4d().SetLookAt(eye, target, actual_up)
        cam_matrix = lookat_m.GetInverse()
        
        # 4. Isaac Sim 惯例修正：+X指目标，+Z朝上
        combined_rot = Gf.Rotation(Gf.Vec3d(1, 0, 0), -90) * Gf.Rotation(Gf.Vec3d(0, 1, 0), 90)
        correction = Gf.Matrix4d().SetRotate(combined_rot)
        
        final_matrix = correction * cam_matrix
        
        # 提取四元数用于相机赋值
        q = final_matrix.ExtractRotationQuat()
        rig_quat = np.array([q.GetReal(), *q.GetImaginary()])
        
        # 5. 直接从最终的变换矩阵中提取世界坐标下的左侧向量 (+Y 轴)
        # 这种做法跳过了所有的手算交叉乘积，绝对不会出错
        world_left = final_matrix.TransformDir(Gf.Vec3d(0, 1, 0))
        world_left_np = np.array(world_left)
        
        # 6. 设置最终位置
        pos_l = center_pos + world_left_np * (self.baseline / 2.0)
        pos_r = center_pos - world_left_np * (self.baseline / 2.0)
        
        self.cam_l.set_world_pose(position=pos_l, orientation=rig_quat)
        self.cam_r.set_world_pose(position=pos_r, orientation=rig_quat)
        
        return pos_l, pos_r, rig_quat

    def capture(self):
        """获取最新的 RGBA 图像"""
        return self.cam_l.get_rgba(), self.cam_r.get_rgba()