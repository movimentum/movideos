from importlib.resources import files

from manim import *


#%%
class CreatureLambda(SVGMobject):
    svg_file = 'lambda.svg'
    svg_pack = f'{__package__}.assets' if __package__ else 'assets'

    
    def __init__(self, *args, light_source_pos=[-20,10,0], **kwargs):
        
        self.svg_path = files(self.svg_pack).joinpath(self.svg_file)
        
        super().__init__(self.svg_path, *args, **kwargs)
    
        #
        # Баг или фича? Иначе такого свойства нет у SVGMobject, так как stroke_width=None при инициализации... и для submobject берётся значение из файла
        #
        self.stroke_width = 0.25
        
        self._separate_parts()
        
        self.body.set_color(WHITE)
        self.eyes.set_color(RED_A)
        self.pupils.set_color(BLACK)
        self.flares.set_color(WHITE)
        
    
    def _separate_parts(self):
        self.body = self.submobjects[6]
        self.eyes = VGroup(*[
            self.submobjects[0],
            self.submobjects[1]
        ])
        self.pupils = VGroup(*[
            self.submobjects[2],
            self.submobjects[3]
        ])
        self.flares = VGroup(*[
            self.submobjects[5],
            self.submobjects[4]
        ])
        self.eye_parts = VGroup(self.eyes, self.pupils, self.flares)


    def look(self, direction):
        norm = np.linalg.norm(direction)
        if norm == 0:
            return
        direction /= norm
        self.looking_direction = direction
        for pupil, eye, flare in zip(self.pupils, self.eyes, self.flares):
            eye_center = eye.get_center()
            right = eye.get_right() - eye_center
            up = eye.get_top() - eye_center
            vect = direction[0] * right + direction[1] * up
            v_norm = np.linalg.norm(vect)
            
            flare_displacement = pupil.get_center() - flare.get_center()
            
            pupil_radius = 0.5 * pupil.get_width()
            vect_pupil = vect * (v_norm - 0.75 * pupil_radius) / v_norm
            pupil.move_to(eye_center + vect_pupil)
            
            flare.move_to(pupil.get_center() + flare_displacement)
        return self


    def look_at(self, point_or_mobject):
        if isinstance(point_or_mobject, Mobject):
            point = point_or_mobject.get_center()
        else:
            point = point_or_mobject
        self.look(point - self.eyes.get_center())
        return self
    

#%% Быстрое тестирование 
if __name__ == '__main__':
    svg = CreatureLambda()
    svg.show()
    svg.shift(DR * 3)
    svg.show()
    