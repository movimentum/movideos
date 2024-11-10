from importlib import import_module
from os.path import dirname

from manim import tempconfig

from .config import update_config_for_dev, update_config_for_scene


#%%
def render(scene_class, render_all_sections, preview):
    
    scene_class.render_all_sections = render_all_sections
    
    with tempconfig({"preview": preview}):    
        
        scene = scene_class()
        scene.render()


def dev_render(fpath, scene_class, preview=True, render_all_sections=False):
    
    update_config_for_dev(fpath, scene_class.video_orientation,
                          config_aux=scene_class.CONFIG)
    
    render(scene_class, render_all_sections, preview)


def prod_render(fpath, class_name, preview=False, render_all_sections=True):
    mpath = '.'.join(fpath.split('/'))[:-3]
    module = import_module(mpath)
    scene_class = getattr(module, class_name)

    media_subdir = dirname(fpath)

    update_config_for_scene(
        quality='prod',
        orientation=scene_class.video_orientation,
        media_subdir=media_subdir,
        save_sections=True,
        config_aux=scene_class.CONFIG
    )
    
    render(scene_class, render_all_sections, preview)
