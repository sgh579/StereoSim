import numpy as np
from pathlib import Path

class Config:
    # --- 1. 路径管理 ---
    # 保持 BASE_DIR 为 Path 对象，不要转成 str，这样才能继续用 '/' 拼接
    BASE_DIR = Path(__file__).resolve().parent.parent
    OUTPUT_DIR = BASE_DIR / "output"
    # OUTPUT_DIR = BASE_DIR / "output" / "stereo_dataset_bunny"
    
    # --- 2. 相机配置 ---
    RESOLUTION = (400, 400)
    FOCAL_LENGTH = 1.32383  # 单位: mm
    BASELINE = 0.032        # 双目基线距离 (m)
    
    # --- 3. 轨迹模式配置 ---
    ORBIT_MODE = "linear" 
    # ORBIT_MODE = "circle" 
    
    NUM_FRAMES = 50
    RADIUS = 0.4        
    HEIGHT = 0.4        
    TARGET_POINT = np.array([0.0, 0.0, 0.0])

    POINTA = np.array([0.5, 0.5, 0.5])
    POINTB = np.array([0.2, 0.2, 0.2])
    
    # --- 4. 场景物体配置 ---
    SCENE_MODE = "diy"
    # SCENE_MODE = "import"
    
    # DIY 模式参数
    SPHERE_RADIUS = 0.1
    CUBE_SCALE = [0.05, 0.05, 0.1]
    CUBE_POS = [0.12, -0.12, 0.1]
    
    # IMPORT 模式参数
    # 直接使用 '/' 拼接，抛弃 os.path.join
    USD_PATH = BASE_DIR / "asset" / "bunny.obj"
    # USD_PATH = "http://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Isaac/2023.1.1/Isaac/Samples/Props/Stanford_Bunny/stanford_bunny.usd"
    
    MODEL_SCALE = [2, 2, 2]  
    MODEL_POS = [0.0, 0.0, 0.0]    

    @classmethod
    def prepare_output_dirs(cls):
        """在 main.py 调用，自动创建所需的文件夹结构"""
        left_dir = cls.OUTPUT_DIR / "left"
        right_dir = cls.OUTPUT_DIR / "right"
        
        # pathlib 的 mkdir 替代了 os.makedirs
        # parents=True 允许创建多级父目录，exist_ok=True 防止目录已存在时报错
        left_dir.mkdir(parents=True, exist_ok=True)
        right_dir.mkdir(parents=True, exist_ok=True)
        
        return left_dir, right_dir