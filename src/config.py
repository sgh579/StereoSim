import numpy as np
from pathlib import Path

class Config:
    HEADLESS_FLAG = False
    
    BASE_DIR = Path(__file__).resolve().parent.parent
    OUTPUT_DIR = BASE_DIR / "output"
    
    RESOLUTION = (400, 400)
    FOCAL_LENGTH = 1.32383  # unit: mm
    BASELINE = 0.032        
    
    ORBIT_MODE = "linear" 
    # ORBIT_MODE = "circle" 
    
    NUM_FRAMES = 50
    RADIUS = 0.4        
    HEIGHT = 0.4        
    TARGET_POINT = np.array([0.0, 0.0, 0.0])

    POINTA = np.array([0.5, 0.5, 0.5])
    POINTB = np.array([0.2, 0.2, 0.2])
    
    SCENE_MODE = "diy"
    # SCENE_MODE = "import"
    
    # parameters for DIY mode
    SPHERE_RADIUS = 0.1
    CUBE_SCALE = [0.05, 0.05, 0.1]
    CUBE_POS = [0.12, -0.12, 0.1]
    
    # parameters for IMPORT mode
    USD_PATH = BASE_DIR / "asset" / "bunny.obj"
    
    MODEL_SCALE = [2, 2, 2]  
    MODEL_POS = [0.0, 0.0, 0.0]    

    @classmethod
    def prepare_output_dirs(cls):
        left_dir = cls.OUTPUT_DIR / "left"
        right_dir = cls.OUTPUT_DIR / "right"
        
        left_dir.mkdir(parents=True, exist_ok=True)
        right_dir.mkdir(parents=True, exist_ok=True)
        
        return left_dir, right_dir