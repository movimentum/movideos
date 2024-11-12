#
# 0. Вводная анимация (суммирование единиц) и обложка
#

import os

from manim import *

from movi_ext import *

from auxfuncs import shapes_to_background


#%%
SceneExtension.video_orientation = 'landscape'


#%%
def get_person_svg(fn):
    ''' name -- имя файла svg без разширения, например, abel'''
    return os.path.join(repo_root, f'custom/svg/persons/{fn}.svg')


#%%
class IntroAddUnities(MovingCameraScene, SceneExtension):
    def construct(self):
        self.add_shapes_to_background()
        
        uni = CreatureUnity().scale(0.5).shift(DOWN)
        uni_h = uni.get_height()
        self.camera.frame.save_state()
        self.camera.frame.set(height=6*uni_h).move_to(uni).shift(UP)
        self.play(FadeIn(uni, scale=0.95),
                  run_time=2)
        self.wait()
        
        self.txt_new = MathTex('1')
        self.txt_old = None
        
        self.play(LaggedStart(
            uni.look_at(self.txt_new),
            FadeIn(
                self.txt_new,
                shift=2*DOWN,
                rate_func=rate_functions.ease_out_sine,
                run_time=3
            ),
            lag_ratio=1
        ))

        self.play(Restore(self.camera.frame))

        self.cnt = 0

        self.add_more(1)
        self.play(uni.look_at(self.txt_new))
        self.wait()
        
        self.add_more(4, run_time=0.5)
        self.play(uni.look_around(d=(-1,1)))
        self.wait()

        self.wait()
        self.add_more(10, run_time=0.25)
        
        self.play(self.camera.frame.animate.set(width=self.txt_new.width * 1.2).move_to(self.txt_new))
        self.add_more(10, run_time=0.1, move_camera=True)
        self.wait()
        
        self.add_more(20, run_time=0.05, move_camera=True)
        self.add_more(30, run_time=0.01, move_camera=False)
        self.wait()


        s_tex = MathTex(
            r'\sum_{n=1}', f'^{{{self.cnt}}}', '1', '=', '75'
        ).move_to(ORIGIN).shift(2 * UP)
        
        s_tex2 = MathTex('\\Rightarrow').rotate(-90*DEGREES).next_to(s_tex, DOWN)
        s_tex3 = MathTex('0 = 1').next_to(s_tex2, DOWN)
        s_grp = VGroup(s_tex, s_tex2, s_tex3)
        self.play(
            TransformMatchingShapes(self.txt_new, s_tex),
            self.camera.frame.animate.set(width=s_tex.width * 4.5).move_to(s_grp),
            run_time=2
        )
        self.play(Succession(Write(s_tex2), Write(s_tex3)))
        self.wait()
        
        
        # Добавим вопросов
        # TODO: использовать функцию auxfuncs.questions_to_background
        n = 75
        positions = (np.random.rand(n, 3) - 0.5) * self.camera.frame.get_width()
        positions += self.camera.frame.get_center()
        positions[:,2] = 0
        scales = np.random.rand(n) * 2
        q_marks = [MathTex(r'?').scale(sc).set_color(RED).set_opacity(0.5).move_to(pos) for sc,pos in zip(scales,positions)]
        self.play(LaggedStart(
            *[GrowFromCenter(q_mark) for q_mark in q_marks],
            lag_ratio=0.02
        ))
        self.wait()
        
        ani_g1 = AnimationGroup(FadeOut(s_grp), run_time=2)
        ani_g2 = AnimationGroup(
            self.camera.frame.animate.set(width=s_tex.width*2.0),
            run_time=4,
            rate_func=linear
        )
        ani_g3 = AnimationGroup(
            *[FadeOut(q_mark) for q_mark in q_marks],
            lag_ratio=0.05,
            run_time=5
        )
        self.play(ani_g1, ani_g2, ani_g3, FadeOut(*self.bg_shapes))
        self.wait()
    
        
    def add_shapes_to_background(self, n=150, scale=0.25, opacity=0.1,
                                 expand=(45,45), center=(-19,0),
                                 seed=int('24539be',16)):
        kwargs = dict(n=n, scale=scale, opacity=opacity, expand=expand,
                      center=center, seed=seed)
        self.bg_shapes = shapes_to_background(**kwargs)
        [self.add(x) for x in self.bg_shapes]


    def add_more(self, num, run_time=1, move_camera=False):
        for i in range (num):
            self.cnt += 1
            self.txt_old = self.txt_new
            if len(self.txt_old) == 1:
                self.txt_new = MathTex('1', '=', '1')
            else:
                self.txt_new = MathTex('1', '+', *[sub.get_tex_string() for sub in self.txt_old[:-1]], f'{self.cnt}')
            self.txt_new.move_to(ORIGIN, RIGHT)
            if not move_camera:
                self.play(
                    TransformMatchingShapes(self.txt_old, self.txt_new),
                    run_time=run_time
                )
            else:
                self.play(
                    TransformMatchingShapes(self.txt_old, self.txt_new),
                    self.camera.frame.animate.set(width=self.txt_new.width * 1.2).move_to(self.txt_new),
                    run_time=run_time
                )


#%%
class Cover(IntroAddUnities):
    fn_abe = get_person_svg('abel')
    fn_rie = get_person_svg('riemann')
    
    font = 'Unutterable'
    # font = 'Hiykaya'
    
    def construct(self):
        self.add_shapes_to_background(expand=(15,15), center=(0,0), opacity=0.15, seed=12345)
        
        eq_prdx = MathTex('0', '=', stroke_width=7, color=RED_E).scale(4.8)
        zero = eq_prdx[0]
        zero.set_color(GOLD_E)
        uni = CreatureUnity(stroke_width=2.5)
        sc = zero.height / uni.body.height * 1.1
        uni.scale(sc)
        uni.next_to(eq_prdx, RIGHT, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*1.1).align_to(zero, DOWN)
        uni.body.set_color(GOLD_E)
        uni.eyes.set_color(GOLD_A)
        uni.look_at_no_anim(eq_prdx[0])
        grp = VGroup(eq_prdx, uni)
        grp.move_to(ORIGIN).shift(0.1*UP)
        
        # Риман
        c = BLUE_A
        c_txt = BLUE_B
        sw = 1
        sw_svg = 1.5
        sc_txt = 1/1.8

        riemann = SVGMobject(
            self.fn_rie,
            height=4,
            stroke_color=BLUE_D,
            stroke_width=sw_svg,
            stroke_opacity=0.85
        )
        riemann.to_edge(LEFT).shift(0.4*UP+1.7*RIGHT)
        txt = Text(
            'доигрался, сынок?',
            font=self.font,
            color=c_txt
        ).scale(sc_txt*1.1)
        rec = SurroundingRectangle(
            txt,
            color=c,
            buff=MED_SMALL_BUFF,
            corner_radius=0.2,
            stroke_width=sw,
            fill_opacity=0.2
        )
        c1 = Circle(radius=0.2, color=c, stroke_width=sw).next_to(rec, DL, buff=0).shift(0.2*UP)
        c2 = Circle(radius=c1.radius/1.618, color=c, stroke_width=sw).next_to(c1, DL, buff=0).shift(0.2*UP)
        
        txt.add(rec, c1, c2)
        txt.next_to(riemann, UR, buff=-1).shift(0.5*LEFT+0.1*UP)
        rie_grp = VGroup(riemann, txt, rec)

    
        # Абель
        abel = SVGMobject(
            self.fn_abe,
            height=4,
            stroke_color=BLUE_D,
            stroke_width=sw_svg,
            stroke_opacity=0.85
        )
        abel.to_corner(DR).shift(1.4*LEFT+0.7*UP)
        txt = Text(
            'я только слагаемые\nместами переставил, пап... :(',
            line_spacing=0.8,
            font=self.font,
            color=c_txt
        ).scale(sc_txt*0.9)
        rec = SurroundingRectangle(
            txt,
            color=c,
            buff=MED_SMALL_BUFF,
            corner_radius=0.2,
            stroke_width=sw,
            fill_opacity=0.2
        )
        c1 = Circle(radius=0.2, color=c, stroke_width=sw).next_to(rec, UR, buff=0).shift(0.2*LEFT)
        c2 = Circle(radius=c1.radius/1.618, color=c, stroke_width=sw).next_to(c1, UR, buff=0).shift(0.2*LEFT)

        txt.add(rec, c1, c2)
        txt.next_to(abel, DL, buff=-1).shift(0.5*LEFT+0.5*UP)
        abe_grp = VGroup(abel, txt, rec)
 
        uni.look_at_no_anim(abel.get_center()+UP)
        
        grp_all = VGroup(rie_grp, abe_grp, grp)
        grp_all.move_to(ORIGIN)
        
        self.add(grp_all)


#%% Тестовый рендер
if __name__ == '__main__':
    
    from helpers.render import dev_render
    
    dev_render(__file__, Cover)
