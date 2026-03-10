import isaacsim.core.utils.prims as prim_utils
from pxr import UsdLux, Sdf

def setup_stereo_scene(world, config):
    world.scene.add_default_ground_plane()
    stage = prim_utils.get_current_stage()
    
    UsdLux.DomeLight.Define(stage, "/World/DomeLight").CreateIntensityAttr(1200.0)
    dist_light = UsdLux.DistantLight.Define(stage, "/World/DistantLight")
    dist_light.CreateIntensityAttr(2000.0)
    dist_light.AddRotateXYZOp().Set((45, 0, 45))

    if config.SCENE_MODE == "diy":
        prim_utils.create_prim(
            "/World/obj_sphere", "Sphere", 
            translation=(0.0, 0.0, config.SPHERE_RADIUS), 
            attributes={"radius": config.SPHERE_RADIUS}
        )
        prim_utils.create_prim(
            "/World/obj_cube", "Cube", 
            translation=tuple(config.CUBE_POS), 
            scale=tuple(config.CUBE_SCALE)
        )
        print(">>> Scene: DIY (Sphere + Cube) loaded.")

    elif config.SCENE_MODE == "import":
        prim_utils.create_prim(
            "/World/imported_model", 
            usd_path=config.USD_PATH,
            translation=tuple(config.MODEL_POS),
            scale=tuple(config.MODEL_SCALE) 
        )
        print(f">>> Scene: Stanford Bunny loaded from: {config.USD_PATH}")