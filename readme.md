# StereoSim: Isaac Sim Stereo Camera Dataset Generation Tool

StereoSim is a lightweight, high-precision stereo vision dataset generation framework based on NVIDIA Isaac Sim. Since Isaac Sim doesn't natively support stereo cameras, developers have to define their own left and right cameras based on the native camera classes. However, this also allows developers more freedom to control the camera pose.

## Environment & Installation

### 1. Install NVIDIA Isaac Sim (Prerequisite)
This project heavily relies on the core Isaac Sim API. Please ensure Isaac Sim is properly installed before running the tool.
* **Supported Versions:** `5.1.0` or `6.0.0`
* **Strong Recommendation:** It is recommended to install Isaac Sim by **building from source**.

### 2. Configure the Startup Script
If you did **not** install via a source build (e.g., you used the Omniverse Launcher), you **must** manually modify the startup script located in the project root.

Open `StereoSim.sh` and locate the `isaac_sim_package_path` variable. Update it to point to your actual local Isaac Sim Python environment path:

```bash
# Example path for source build (default):
export isaac_sim_package_path="/home/username/isaacsim/_build/linux-x86_64/release"

# Example path for Omniverse Launcher installation:
# export isaac_sim_package_path="/home/username/.local/share/ov/pkg/isaac-sim-5.1.0"
```

## Quick Start

The script will automatically clean the old `output` directory and launch the Isaac Sim environment:
```bash
./StereoSim.sh

```

## Project Structure

```text
StereoSim/
├── StereoSim.sh          # Core startup script (handles env vars and paths)
├── output/               # Auto-generated output directory (cleared on startup)
│   ├── left/             # Left camera rendered images
│   └── right/            # Right camera rendered images
├── asset/                # External 3D models (e.g., bunny.obj)
└── src/
    ├── main.py           # Simulation main loop and entry point
    ├── stereo_config.py  # Global configuration (Pathlib, camera/scene params)
    ├── camera_rig.py     # Core stereo rig class (Absolute pose / LookAt solver)
    ├── scene_utils.py    # Scene setup tools (DIY geometry / USD import)
    └── data_handler.py   # Dataset saving and pose recording logic

```

## Core Configuration (src/config.py)

All simulation parameters are centralized in the `Config` class within `src.config.py`. You can easily modify the following:

* **Camera Hardware:** Custom resolution (`RESOLUTION`), focal length (`FOCAL_LENGTH`), and stereo baseline distance (`BASELINE`).
* **Trajectory Mode:**
* `ORBIT_MODE = "linear"`: Linear translation scan.
* `ORBIT_MODE = "circle"`: Orbit capture around a target point.


* **Scene Mode:**
* `SCENE_MODE = "diy"`: Generates built-in basic geometries like spheres and cubes.
* `SCENE_MODE = "import"`: Loads external USD or OBJ models (requires configuring `USD_PATH`).



## Camera Pose Control 

1. **Direct Pose Assignment (`set_stereo_pose`):**
By passing the center coordinates and absolute quaternion, the system automatically derives the separation vectors for the left and right cameras in the world coordinate system.
2. **Look-At Tracking (`set_stereo_pose_lookat`):**
Simply pass the camera position, target point position, and an optional **roll angle**, and the system will automatically construct a LookAt matrix while keeping the left and right optical axes strictly parallel.