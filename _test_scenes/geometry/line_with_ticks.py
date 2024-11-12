import itertools as it

from manim import *

from helpers.render import dev_render
from movi_ext import *


class LineWithTicksTest(Scene, SceneExtension):
    
    def construct(self):
        pA = ORIGIN + 3 * LEFT + 3 * DOWN
        pC = pA + 6 * RIGHT
        pB = pA + 4 * RIGHT + 6 * UP
        vertices = (pA, pB, pC)
        
        lines = VGroup(*[
            LineWithTicks(p1, p2) for p1,p2 in it.combinations(vertices, 2)
        ])

        [line.add_ticks_at_mid(i+1) for i,line in enumerate(lines)]

        self.play(Create(lines), run_time=2)
        self.wait()


#%% Быстрое тестирование 
if __name__ == '__main__':
    
    dev_render(__file__, LineWithTicksTest) 
