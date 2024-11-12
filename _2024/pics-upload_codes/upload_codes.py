from manim import *

from movi_ext import *


SceneExtension.CONFIG = dict(
    pixel_width = 2000,
    pixel_height = 2000,
    frame_width = 13,
    frame_height = 13
)


#%%
class UploadCodesPic(Scene, SceneExtension):
    def construct(self):
        fop = 0.6
        sop = 1
        
        circle = Circle(
            fill_opacity=fop,
            stroke_opacity=sop,
            color=BLUE_D,
            fill_color=BLUE_A
        ).scale(0.5)
        square = Square(
            fill_opacity=fop,
            stroke_opacity=sop,
            color=BLUE_A,
            fill_color=BLUE_D
        )
        
        tr = Transform(circle, square, rate_func=linear)
        tr.begin()
        
        grp = VGroup()
        for alpha in np.linspace(0, 1, 5):
            tr.interpolate(alpha)
            mob = tr.mobject.copy()
            grp.add(mob)
        
        grp.arrange(buff=MED_LARGE_BUFF)
        txt = Text('Открыл исходники манимаций', font='PT Sans Caption')
        txt.next_to(grp, DOWN, buff=MED_LARGE_BUFF).set_color(GRAY_A)
        grp.add(txt)
        grp.move_to(ORIGIN)
        
        self.add(grp)


#%% Тестовый рендер
if __name__ == '__main__':
    
    from helpers.render import dev_render
    
    dev_render(__file__, UploadCodesPic)