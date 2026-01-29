#
# 2. Физическое ограничение классического решения
#

import numpy as np

from manim import *

from movi_ext import *

from manim_cad_drawing_utils import *


#%%
SceneExtension.video_orientation = 'landscape'

SceneExtension.render_all_sections = False

np.random.seed(0xDEADBEEF)


#%%
class PhysicalLimitation(ThreeDScene, SceneExtension):
    
    phi = PI / 2.5
    theta = PI / 3
    
    def construct(self):
        
        self.begin_ambient_camera_rotation()

        #
        ## Начало
        #
        self.next_section('3D-brick', skip_animations=SceneExtension.skip(False))
        
        # Оси
        w = 3
        dX = w / 2
        axes = ThreeDAxes(
            x_range=(-dX, dX, 1),
            y_range=(-dX, dX, 1),
            z_range=(-dX, dX, 1),
            x_length=w,
            y_length=w,
            z_length=w
        )
        axes.set_opacity(1.0).set_color(YELLOW_A)
        self.set_camera_orientation(phi=self.phi, theta=self.theta)
        
        self.play(Create(axes))
        
        self.wait(2)

        
        
#%% Тестовый рендер
if __name__ == '__main__':
    
    from helpers.render import dev_render
    
    dev_render(__file__, PhysicalLimitation)

        