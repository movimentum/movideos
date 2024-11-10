from importlib.resources import files

from manim import *


#%%
class CreatureUnity(SVGMobject):
    svg_file = 'unity.svg'
    svg_pack = f'{__package__}.assets' if __package__ else 'assets'

    
    def __init__(self, *args, light_source_pos=[-20,10,0], **kwargs):
        
        self.svg_path = files(self.svg_pack).joinpath(self.svg_file)
        
        super().__init__(self.svg_path, *args, **kwargs)
        self._separate_parts()
        self.update_light_source_pos(light_source_pos)
    

    def _separate_parts(self):
        self.body, self.eyeR, self.pupilR, self.glareR, \
                   self.eyeL, self.pupilL, self.glareL  = self.submobjects
        self.eyes = VGroup(self.eyeL, self.eyeR)
        self.pupils = VGroup(self.pupilL, self.pupilR)
        self.glares = VGroup(self.glareL, self.glareR)
        self.eyeL_grp = VGroup(self.eyeL, self.pupilL, self.glareL)
        self.eyeR_grp = VGroup(self.eyeR, self.pupilR, self.glareR)
        self.eyes_grp = VGroup(self.eyeL_grp, self.eyeR_grp)


    def adjust_grale(f):
        """ Декоратор, перестраивающий расположение бликов на зрачках
            по направлению к источнику света
        """
        def wrapped(*args, **kwargs):
            try:
                self = args[0]
                for glare, pupil in zip(self.glares, self.pupils):
                    c = pupil.get_center()
                    v1 = glare.get_center() - c
                    v2 = self.light_source_pos - c
                    v2 /= np.linalg.norm(v2)  # make direction
                    dv = v2 * np.linalg.norm(v1) - v1
                    glare.shift(dv)
            except AttributeError:
                print('EXEPTION')
            finally:
                return f(*args, **kwargs)
        return wrapped        


    def update_light_source_pos(self, point):
        """ Перестраивает положение бликов на зрачках по направлению к источнику света """
        if point:
            self.light_source_pos = np.array(point)
        for glare, pupil in zip(self.glares, self.pupils):
            c = pupil.get_center()
            v1 = glare.get_center() - c
            v2 = self.light_source_pos - c
            v2 /= np.linalg.norm(v2)  # make direction
            dv = v2 * np.linalg.norm(v1) - v1
            glare.shift(dv)
 
    
    def look_at_no_anim(self, point_or_mob):
        ''' Задать направление взгляда '''
        point = point_or_mob
        if isinstance(point_or_mob, Mobject):
            point = point_or_mob.get_center()
        ani = []
        for eye,pupil,glare in zip(self.eyes, self.pupils, self.glares):
            c = eye.get_center()
            v1 = pupil.get_center() - c
            v2 = point - c
            a1 = angle_of_vector(v1)
            a2 = angle_of_vector(v2)
            angle = a2 - a1
            VGroup(pupil, glare).rotate(angle, about_point=c)
            
    
    def look_at(self, point_or_mob):
        ''' Задать направление взгляда '''
        point = point_or_mob
        if isinstance(point_or_mob, Mobject):
            point = point_or_mob.get_center()
        ani = []
        for eye,pupil,glare in zip(self.eyes, self.pupils, self.glares):
            c = eye.get_center()
            v1 = pupil.get_center() - c
            v2 = point - c
            a1 = angle_of_vector(v1)
            a2 = angle_of_vector(v2)
            angle = a2 - a1
            pupil_target = pupil.copy().rotate(angle, about_point=c)
            
            ani.append(Rotate(VGroup(pupil, glare), angle, about_point=c))
        return AnimationGroup(*ani)
    
    
    def blink(self, amount=0.2):
        grpL = VGroup(self.eyeL, self.pupilL, self.glareL)
        grpR = VGroup(self.eyeR, self.pupilR, self.glareR)
        ani = LaggedStart(
                grpL.animate(rate_func=there_and_back).stretch(amount, dim=1, about_point=grpL.get_bottom()),
                grpR.animate(rate_func=there_and_back).stretch(amount, dim=1, about_point=grpR.get_bottom()),
                lag_ratio=0.1
            )
        return ani

    
    def smile(self):
        body_target = self.body.copy().rotate(90 * DEGREES)
        ani = []
        ani.append(Rotate(self.body, 90 * DEGREES))
        shift = self.eyeL_grp.get_width() / 2
        ani.append(self.eyeL_grp.animate.next_to(body_target, UP, buff=0).shift(shift * LEFT))
        ani.append(self.eyeR_grp.animate.next_to(body_target, UP, buff=0).shift(shift * RIGHT))
        return AnimationGroup(*ani)
    
    
    def look_around(self, d=(1,1)):
        """ Делает полный оборот зрачками
            d -- направление оборота левого и правого глаз;
                 +1 -- против часовой стрелки
                 -1 -- по часовой стрелке
        """
        ani = []
        for i, (eye, pupil, glare) in enumerate(self.eyes_grp):
            c = eye.get_center()
            ani.append(Rotate(VGroup(pupil, glare), d[i]*360*DEGREES, about_point=c))
        return AnimationGroup(*ani)
    
    
    def get_talk_bubble(self, content, scale_bubble=None, shift_bubble=None, bg_rect=False, **kwargs):
        bubble = RoundedRectangle(**kwargs)
        if bg_rect:
            bubble.add_background_rectangle()
        if scale_bubble:
            bubble.scale(scale_bubble)
            
        w0, h0 = bubble.get_width(), bubble.get_height()
        d0 = 0.1 * min(w0, h0)
        color = bubble.get_color()
        c1 = Circle(d0, color=color, stroke_width=1).next_to(bubble, DL, buff=-0.05)
        c2 = Circle(d0 / 2, color=color, stroke_width=1).next_to(c1, DL, buff=-0.05)
        if len(content) > 0:
            if isinstance(content[0], str):
                cmob = Text(content)
            else:
                cmob = content
            w, h = cmob.get_width(), cmob.get_height()
            scale = 0.9 * min( w0/w, h0/h)
            cmob.scale(scale)
            cmob.move_to(bubble)
            bubble.add(cmob)
        bubble.add(c1, c2)
        buff = SMALL_BUFF * scale_bubble if scale_bubble else SMALL_BUFF
        bubble.next_to(self, UR, buff=buff).shift(self.get_height() * 0.2 * DOWN)
        if shift_bubble is not None:
            bubble.shift(shift_bubble)
        self.bubble = bubble
        return bubble
    

#%% Быстрое тестирование 
if __name__ == '__main__':
    svg = CreatureUnity(light_source_pos=[-5,2,0])
    svg.show()
    svg.shift(DR * 3)
    svg.show()
    