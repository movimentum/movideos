#
# Мешок со слагаемыми
#

from manim import *

from helpers.render import dev_render
from movi_ext import *


#%%
class NumberBag(VMobject):
    def __init__(self, c, fc, cc, nxc, nyc, cap, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bag = Rectangle(height=2, width=3, color=c, fill_color=fc,
                        fill_opacity=0.5, stroke_width=1)
        circles = VGroup(*[
            Circle(radius=r, color=cc, stroke_width=0.5, fill_opacity=0.7)
            for r in np.linspace(0.1, 0.01, nxc*nyc)
            ])
        circles.arrange_in_grid(nxc,nyc,buff=0)
        circles.set(height=0.9*bag.get_height())
        circles.move_to(bag)

        txt = cap
        if isinstance(cap, str) and cap:
            txt = Text(cap, font='sans-serif', font_size=24)

        self.add(bag)
        if txt:
            txt.set_color(c).next_to(bag, DOWN)
            self.add(txt)
        self.add(*circles)
        
        self.bag = self.submobjects[0]
        self.txt = self.submobjects[1] if txt else None
        self.idx_circles = 2 if txt else 1
        self.circles = circles


    def get_all_possible_circles(self):
        return self.circles

    
    def add_all_circles(self):
        self.remove_remaining_circles()
        self.add(*self.circles)
    
    
    def remove_circles(self, n):
        i = self.idx_circles
        c_to_remove = self.submobjects[i:i+n]
        self.remove(*c_to_remove)
        return c_to_remove
    
    
    def remove_remaining_circles(self):
        i = self.idx_circles
        n = len(self.submobjects[i:])
        return self.remove_circles(n)
        
    

#%% Тест сцены с мешками
class NumberBagTest(Scene, SceneExtension):
    
    video_orientation = 'landscape'
    
    def construct(self):
        bag_pos = NumberBag(GREEN, GREEN_A, GREEN_E, 5, 5, 'положительные слагаемые')
        bag_neg = NumberBag(RED, RED_A, RED_E, 5, 5, 'отрицательные слагаемые')
        bag_neg.next_to(bag_pos, RIGHT)
        
        self.add(VGroup(bag_pos, bag_neg).move_to(ORIGIN))


if __name__ == '__main__':

    dev_render(__file__, NumberBagTest)
    