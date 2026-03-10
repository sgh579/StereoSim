import os
import csv
import numpy as np
from PIL import Image
import shutil

class DatasetWriter:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.left_dir = os.path.join(output_dir, "left")
        self.right_dir = os.path.join(output_dir, "right")

        
        os.makedirs(self.left_dir, exist_ok=True)
        os.makedirs(self.right_dir, exist_ok=True)
        
        self.csv_path = os.path.join(output_dir, "camera_poses.csv")
        self.csv_file = open(self.csv_path, 'w', newline='')
        self.writer = csv.writer(self.csv_file)
        
        self.writer.writerow([
            "frame", "time", 
            "p_l_x", "p_l_y", "p_l_z", "q_w", "q_x", "q_y", "q_z",
            "p_r_x", "p_r_y", "p_r_z"
        ])

    def save_metadata(self, config, intrinsic_matrix):
        """
        Stores dataset descriptions and camera intrinsics.

        intrinsic_matrix: A 3x3 NumPy array
        """
        meta_path = os.path.join(self.output_dir, "dataset_info.txt")
        with open(meta_path, "w", encoding="utf-8") as f:
            f.write("=== Synthetic Stereo Dataset Metadata ===\n")
            f.write(f"Scene Mode: {config.SCENE_MODE}\n")
            f.write(f"Orbit Mode: {config.ORBIT_MODE}\n")
            f.write(f"Resolution: {config.RESOLUTION[0]}x{config.RESOLUTION[1]}\n")
            f.write(f"Focal Length: {10 * config.FOCAL_LENGTH}mm\n")
            f.write(f"Stereo Baseline: {config.BASELINE}m\n")
            f.write("-" * 40 + "\n")
            f.write("Camera Intrinsic Matrix (K):\n")
            f.write(np.array2string(intrinsic_matrix, separator=', '))
            f.write("\n\n" + "-" * 40 + "\n")
            f.write("Scene Details:\n")
            if config.SCENE_MODE == "diy":
                f.write(f" - Sphere Radius: {config.SPHERE_RADIUS}m\n")
                f.write(f" - Cube Scale: {config.CUBE_SCALE}m\n")
            else:
                f.write(f" - Imported USD: {config.USD_PATH}\n")

            # Specific formatted output
            f.write("=== Easy Copy Format (K_flat and Baseline) ===\n")
            
            # Flatten the 3x3 matrix into a list containing 9 elements.
            k_flat = intrinsic_matrix.flatten()
            k_line = " ".join([f"{x:1}" for x in k_flat])
            
            f.write(k_line + "\n")
            f.write(f"{config.BASELINE}\n")
        print(f">>> Metadata and Intrinsics saved to: {meta_path}")

    def write_frame(self, frame_id, time, pos_l, pos_r, quat, img_l, img_r):
        file_name = f"{frame_id:04d}.png"
        
        img_l_pix = Image.fromarray(img_l[:, :, :3].astype(np.uint8))
        img_r_pix = Image.fromarray(img_r[:, :, :3].astype(np.uint8))
        
        img_l_pix.save(os.path.join(self.left_dir, file_name))
        img_r_pix.save(os.path.join(self.right_dir, file_name))
        
        self.writer.writerow([
            frame_id, f"{time:.4f}",
            pos_l[0], pos_l[1], pos_l[2], 
            quat[0], quat[1], quat[2], quat[3],
            pos_r[0], pos_r[1], pos_r[2]
        ])

    def close(self):
        if hasattr(self, 'csv_file'):
            self.csv_file.close()
            print(">>> CSV file closed.")