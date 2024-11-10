from manim import *

from helpers.render import dev_render
from movi_ext import *


#%%
class CreatureUnityTest(Scene, SceneExtension):
    
    video_orientation = 'landscape'
    
    def construct(self):
        unity = CreatureUnity().scale(0.5)
        dot = Dot().move_to(LEFT + UP)
        self.remove(unity.eyeL_grp, unity.eyeR_grp)
        self.add(unity, dot)
        
        self.play(LaggedStart(
            DrawBorderThenFill(unity.eyeL_grp),
            DrawBorderThenFill(unity.eyeR_grp)
            ))
        self.play(unity.look_at(dot))
        self.wait()
        
        unity_copy = unity.copy()
        self.play(unity.smile())
        self.play(unity.look_at(dot))
        self.wait()
        unity.generate_target()
        unity.target.stretch(2,0)
        unity.target.stretch(0.5,1)
        self.play(MoveToTarget(unity))
        
        unity.generate_target()
        unity.target.stretch(2,0)
        unity.target.stretch(0.5,1)
        self.play(MoveToTarget(unity))
        
        unity.generate_target()
        unity.target.stretch(2,0)
        unity.target.stretch(0.5,1)
        self.play(MoveToTarget(unity))
        self.wait()
        

        self.play(Transform(unity, unity_copy))
        self.wait()


#%% Тестовый рендер
if __name__ == '__main__':
    
    dev_render(__file__, CreatureUnityTest)