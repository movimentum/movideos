#
# 0. Завязка
#

import numpy as np

from manim import *

from movi_ext import *


#%%
SceneExtension.video_orientation = 'landscape'


#%%
class TransformTwoSvg(Scene, SceneExtension):
    def construct(self):
        
        svg_straight = self.prepare_svg_mobject(
            'assets/person-straight.svg',
            width=2,
            stroke_color=BLUE
        )
        
        svg_inclined = self.prepare_svg_mobject(
            'assets/person-inclined.svg',
            width=2,
            stroke_color=BLUE
        ).align_to(svg_straight, DOWN)
        
        svg_straight[2].set_color(BLUE_B)
        svg_inclined[2].set_color(BLUE_B)
        
        svg_straight_copy = svg_straight.copy()
       
        self.play(Create(svg_straight_copy, run_time=2))
        
        self.play(
            ReplacementTransform(svg_straight_copy, svg_inclined),
            #rate_func=there_and_back,
            run_time=2
        )
        self.wait()
        
        self.play(
            ReplacementTransform(svg_inclined, svg_straight),
            #rate_func=there_and_back,
            run_time=2
        )
        self.wait()
        
        self.play(Uncreate(svg_straight))
        self.wait()
        
        
    def prepare_svg_mobject(self, *args, **kwargs):
        """ *args, **kwargs -- как в SVGMobject """
        svg = SVGMobject(*args, **kwargs)
        for mob in svg.submobjects:
            if not mob.stroke_width:
                mob.stroke_width = 1
        return svg


#%% Тестовый рендер
if __name__ == '__main__':
    
    from helpers.render import dev_render
    
    dev_render(__file__, TransformTwoSvg)

