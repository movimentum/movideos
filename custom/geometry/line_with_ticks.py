#
# Линия с засечками, например, для обозначения равенства отрезков
#

from manim import *


class LineWithTicks(Line):
    size = 0.1
    spacing_to_size_ratio = 0.75
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.preconfigure()
        self.ticks = VGroup()

    
    def preconfigure(self):
        length = self.get_length()
        if length < 1:
            self.size *= length
        self.spacing = self.size * self.spacing_to_size_ratio
        
        
    def add_ticks_at_mid(self, n):
        """ Добавить штрихи в середину отрезка """
        self.remove(self.ticks)
        ticks = VGroup()
        for i in range(n):
            tick = Line(self.size * DOWN, self.size * UP, stroke_width=self.stroke_width / 1.5)
            tick.shift(self.spacing * i * RIGHT)
            ticks.add(tick)
        ticks.rotate(self.get_angle())
        ticks.move_to(self.get_center())
        self.ticks = ticks
        self.add(ticks)


#%% Быстрое тестирование 
if __name__ == '__main__':
    line = LineWithTicks()
    line.add_ticks_at_mid(2)
    line.show()
