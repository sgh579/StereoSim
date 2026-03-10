from src.config import Config

from isaacsim import SimulationApp
simulation_app = SimulationApp({"headless": Config.HEADLESS_FLAG})

import numpy as np
from isaacsim.core.api import World

from src.camera_rig import StereoRig
from src.scene_utils import setup_stereo_scene
from src.data_handler import DatasetWriter

def calculate_trajectory(frame_idx, total_frames, config):
    """Calculate the center point position of the camera for the current frame based on the configuration."""
    if config.ORBIT_MODE == "circle":
        # Circular track logic
        angle = np.radians((frame_idx / total_frames) * 360)
        x = config.RADIUS * np.cos(angle)
        y = config.RADIUS * np.sin(angle)
        return np.array([x, y, config.HEIGHT])
    
    elif config.ORBIT_MODE == "linear":
        progress = frame_idx / (total_frames - 1)
        
        current_pos = config.POINTA + (config.POINTB - config.POINTA) * progress
        
        return current_pos
    
    else:
        raise ValueError(f"Unknown ORBIT_MODE: {config.ORBIT_MODE}")

def main():
    world = World(stage_units_in_meters=1.0)
    
    left_dir, right_dir = Config.prepare_output_dirs()
    
    setup_stereo_scene(world, Config)
    
    rig = StereoRig(
        resolution=Config.RESOLUTION, 
        focal_length=Config.FOCAL_LENGTH, 
        baseline=Config.BASELINE
    )
    
    writer = DatasetWriter(Config.OUTPUT_DIR)
    intrinsic_k = rig.cam_l.get_intrinsics_matrix()
    writer.save_metadata(Config, intrinsic_k)
    
    world.reset()
    
    # Preheat renderer: Allows lighting and textures to load completely, preventing a black screen on the first frame.
    print(">>> Warming up renderer...")
    for _ in range(30):
        world.step(render=True)

    print(f">>> Starting capture in {Config.ORBIT_MODE} mode...")

    try:
        for i in range(Config.NUM_FRAMES):
            center_pos = calculate_trajectory(i, Config.NUM_FRAMES, Config)
            
            pos_l, pos_r, quat = rig.set_stereo_pose_lookat(center_pos, Config.TARGET_POINT)
            
            world.step(render=True)
            simulation_app.update()
            
            img_l, img_r = rig.capture()
            
            if img_l is not None and img_r is not None:
                writer.write_frame(
                    frame_id=i, 
                    time=world.current_time, 
                    pos_l=pos_l, 
                    pos_r=pos_r, 
                    quat=quat, 
                    img_l=img_l, 
                    img_r=img_r
                )
            
            if i % 10 == 0:
                print(f"Captured {i}/{Config.NUM_FRAMES} frames...")

    except Exception as e:
        print(f"An error occurred during simulation: {e}")
    
    finally:
        writer.close()
        print(f">>> Task finished. Data saved to: {Config.OUTPUT_DIR}")
        simulation_app.close()



if __name__ == "__main__":
    main()