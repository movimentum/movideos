#
# Абсолютная и условная сходимость
#

from manim import *

from movi_ext import *

from auxfuncs import split2syms, shapes_to_background
from number_bag import NumberBag
from series import Series


#%%
SceneExtension.video_orientation = 'landscape'


#%% Демонстрация сходимости к любому числу путём "туда-сюда"
class AbsConventConvergence(Scene, SceneExtension):
    def construct(self):

        self.add_shapes_to_background()

        eq_raw = '1'
        for i in range(2, 2+5):
            operation = ' + ' if i % 2 else ' - '
            element = '{ 1 \over ' + f'{i}' + ' }'
            eq_raw += operation
            eq_raw += element
        eq_raw += ' + \ldots'
        eq_sym = split2syms(eq_raw)
        eq_conv = MathTex(*eq_sym, color=GRAY_A)
        
        eq_raw = '\Biggl| 1 \Biggr|'
        for i in range(2, 2+5):
            sign = ' + ' if i % 2 else ' - '
            element = f'\Biggl| {sign} ' + '{ 1 \over ' + f'{i}' + ' } \Biggr|'
            eq_raw += '+'
            eq_raw += element
        eq_raw += ' + \ldots'
        eq_sym = split2syms(eq_raw)
        eq_conv_abs = MathTex(*eq_sym, color=GRAY_A)
        
        txt1 = Text('сходится', font='sans-serif', color=GREEN).set_opacity(0.7)
        txt2 = Text('рассходится', font='sans-serif', color=RED).set_opacity(0.7)
        txt3 = txt1.copy()
        txt4 = txt1.copy()
        
        grp_conv = VGroup(eq_conv, txt1, eq_conv_abs, txt2)
        grp_conv.arrange_in_grid(rows=2, cols=2, cell_alignment=LEFT)
        box = SurroundingRectangle(grp_conv, color=GOLD, buff=MED_SMALL_BUFF, corner_radius=0.5)
        cap = Text('условно сходящийся ряд', font='sans-serif', color=GOLD).scale(1.2)
        cap.next_to(box, UP)
        grp_conv = VGroup(*grp_conv, box, cap)
        
       
        raw = '1'
        raw += ' - { 1 \over 2 } '
        raw += ' + { 1 \over 2^2 } '
        raw += ' - { 1 \over 2^3 } '
        raw += ' + { 1 \over 2^4 } '
        raw += ' - { 1 \over 2^5 } '
        raw += ' + \ldots '
        eq_sym = split2syms(raw)
        eq_geom = MathTex(*eq_sym, color=GRAY_A)
        
        raw = '\Biggl| 1 \Biggr|'
        raw += '+ \Biggl| - { 1 \over 2 } \Biggr| '
        raw += '+ \Biggl| + { 1 \over 2^2 } \Biggr| '
        raw += '+ \Biggl| - { 1 \over 2^3 } \Biggr| '
        raw += '+ \Biggl| + { 1 \over 2^4 } \Biggr| '
        raw += '+ \Biggl| - { 1 \over 2^5 } \Biggr| '
        raw += '+ \ldots'
        eq_sym = split2syms(raw)
        eq_geom_abs = MathTex(*eq_sym, color=GRAY_A)

        
        grp_geom = VGroup(eq_geom, txt3, eq_geom_abs, txt4)
        grp_geom.arrange_in_grid(rows=2, cols=2, cell_alignment=LEFT)
        box2 = SurroundingRectangle(grp_geom, color=BLUE, buff=MED_SMALL_BUFF, corner_radius=0.5)
        cap2 = Text('абсолютно сходящийся ряд', font='sans-serif', color=GOLD).scale(1.2)
        cap2.next_to(box2, UP)
        grp_geom = VGroup(*grp_geom, box2, cap2)
        
        
        #
        # Добавляем 2 мешка с положительными и отрицательными элементами
        #
        pos1 = NumberBag(GREEN, GREEN_A, GREEN_E, 5, 5, '')
        neg1 = NumberBag(RED, RED_A, RED_E, 5, 5, '')
        neg1.next_to(pos1, RIGHT)
        grp1 = VGroup(pos1, neg1)
        txt_bag1 = Text('бездонные', font='sans-serif', color=GRAY).next_to(grp1, DOWN)
        grp1.add(txt_bag1)
        grp1.next_to(grp_conv, RIGHT, buff=LARGE_BUFF).align_to(grp_conv, DOWN)
        grp_conv.add(grp1)
        
        pos2 = NumberBag(GREEN, GREEN_A, GREEN_E, 5, 5, '')
        neg2 = NumberBag(RED, RED_A, RED_E, 5, 5, '')
        neg2.next_to(pos2, RIGHT)
        grp2 = VGroup(pos2, neg2)
        txt_bag2 = Text('ограниченные', font='sans-serif', color=GRAY).next_to(grp2, DOWN)
        grp2.add(txt_bag2)
        grp2.next_to(grp_geom, RIGHT, buff=LARGE_BUFF).align_to(grp_geom, DOWN)
        grp_geom.add(grp2)
        
        
        Group(grp_conv, grp_geom).arrange(DOWN, buff=1.8*LARGE_BUFF).scale(0.5).move_to(ORIGIN)
        
        
        #
        ## Исходные ряды
        #        
        self.play(Succession(
            AnimationGroup(
                Create(eq_geom),
                Create(eq_conv),
            ),
            AnimationGroup(
                Create(txt1),
                Create(txt3),
            ),
        ))
        self.wait()
        
        #
        ## Абсолютно сходящийся
        #
        self.play(
            FadeIn(grp2, scale=2),
            Create(box2),
            Write(cap2),
        )
        self.wait()
        
        #
        ## Условно сходящийся
        #
        self.play(
            FadeIn(grp1, scale=2),
            Create(box),
            Write(cap),
        )
        self.wait()

        #
        ## Математическое определение условной и абсолютной сходимостей
        #
        self.play(Succession(
            AnimationGroup(
                TransformMatchingTex(eq_geom.copy(), eq_geom_abs),
                TransformMatchingTex(eq_conv.copy(), eq_conv_abs),
                ),
            AnimationGroup(
                Create(txt2),
                Create(txt4),
                ),
        ))
        self.wait()

    
    def add_shapes_to_background(self, n=100, opacity=0.05,
                                 expand=(-12,12), scale=0.4, seed=13):
        kwargs = dict(n=n, scale=scale, opacity=opacity, expand=expand,
                      seed=seed)
        self.bg_shapes = shapes_to_background(**kwargs)
        [self.add(x) for x in self.bg_shapes]


#%% Тестовый рендер
if __name__ == '__main__':
    
    from helpers.render import dev_render
    
    dev_render(__file__, AbsConventConvergence)