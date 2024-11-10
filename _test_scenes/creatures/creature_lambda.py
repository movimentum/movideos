from manim import *

from helpers.render import dev_render
from movi_ext import *


#%%
class CreatureLambdaTest(Scene, SceneExtension):
    
    video_orientation = 'landscape'
    
    def construct(self):
        lam = CreatureLambda().scale(0.5)
        dot = Dot().move_to(LEFT + UP)
        self.remove(lam.eyes)
        self.add(lam, dot)
        
        self.play(LaggedStart(
            DrawBorderThenFill(lam.eyes)
        ))
        self.play(lam.animate.become(lam.copy().look_at(dot)))
        self.wait()
        


#%% Тестовый рендер
if __name__ == '__main__':
    
    dev_render(__file__, CreatureLambdaTest)