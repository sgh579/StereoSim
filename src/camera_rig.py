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
        # Convert NumPy quaternions to Gf.Quatd (Note: Isaac Sim defaults to real part w first).
        quat = Gf.Quatd(rig_quat[0], rig_quat[1], rig_quat[2], rig_quat[3])
        
        # In the modified local coordinate system, the +Y axis always represents the positive left side.
        local_left = Gf.Vec3d(0, 1, 0)
        
        # By directly applying a quaternion rotation to the local left-hand vector, we obtain the absolute left-hand vector in the world coordinate system.
        world_left = Gf.Rotation(quat).TransformDir(local_left)
        world_left_np = np.array(world_left)
        
        pos_l = center_pos + world_left_np * (self.baseline / 2.0)
        pos_r = center_pos - world_left_np * (self.baseline / 2.0)
        
        self.cam_l.set_world_pose(position=pos_l, orientation=rig_quat)
        self.cam_r.set_world_pose(position=pos_r, orientation=rig_quat)
        
        return pos_l, pos_r, rig_quat

    def set_stereo_pose_lookat(self, center_pos, target_point, roll=0.0):
        """
        Method 2: Setting up a stereo camera using gaze target logic

        :param center_pos: [x, y, z] World coordinates of the array center

        :param target_point: [x, y, z] World coordinates of the target point

        :param roll: Roll angle (angle). Default 0 indicates that the top should point towards the world +Z.
        """
        eye = Gf.Vec3d(*center_pos.tolist())
        target = Gf.Vec3d(*target_point.tolist())
        
        # Forward
        forward_dir = target - eye
        if forward_dir.GetLength() > 1e-6:
            forward_dir.Normalize()
        else:
            forward_dir = Gf.Vec3d(1, 0, 0) 
            
        # Roll and real up
        base_up = Gf.Vec3d(0, 0, 1) # default
        if roll != 0.0:
            roll_rot = Gf.Rotation(forward_dir, roll)
            actual_up = roll_rot.TransformDir(base_up)
        else:
            actual_up = base_up
            
        lookat_m = Gf.Matrix4d().SetLookAt(eye, target, actual_up)
        cam_matrix = lookat_m.GetInverse()
        
        # Isaac Sim convention correction: +X indicates the target, +Z indicates upwards.
        combined_rot = Gf.Rotation(Gf.Vec3d(1, 0, 0), -90) * Gf.Rotation(Gf.Vec3d(0, 1, 0), 90)
        correction = Gf.Matrix4d().SetRotate(combined_rot)
        
        final_matrix = correction * cam_matrix
        
        q = final_matrix.ExtractRotationQuat()
        rig_quat = np.array([q.GetReal(), *q.GetImaginary()])
        
        world_left = final_matrix.TransformDir(Gf.Vec3d(0, 1, 0))
        world_left_np = np.array(world_left)
        
        pos_l = center_pos + world_left_np * (self.baseline / 2.0)
        pos_r = center_pos - world_left_np * (self.baseline / 2.0)
        
        self.cam_l.set_world_pose(position=pos_l, orientation=rig_quat)
        self.cam_r.set_world_pose(position=pos_r, orientation=rig_quat)
        
        return pos_l, pos_r, rig_quat

    def capture(self):
        return self.cam_l.get_rgba(), self.cam_r.get_rgba()