#
# Цитаты классиков
#


from manim import *

from movi_ext import *

from auxfuncs import get_person_svg_path


#%%
SceneExtension.video_orientation = 'landscape'


#%% Цитата Абеля
class QuoteAbel(Scene, SceneExtension):
    fn = get_person_svg_path('abel')
    
    def construct(self):
        svg = self.prepare_svg_mobject(self.fn, height=6, stroke_color=BLUE)

        cap = Text('Абель Нильс Хенрик', font='sans-serif', color=BLUE).set(width=svg.width)
        cap.next_to(svg, DOWN)
        grp = VGroup(svg, cap).move_to(ORIGIN).to_edge(RIGHT)
        
        text = """
        «Расходящиеся ряды есть,
        в общем случае, нечто ужасное,
        и позор тому, кто основывает
        свои доказательства на них!
        Мы можем доказать что угодно,
        используя такие ряды.
        Они рождают множество
        чудес и приводят к огромному
        количеству парадоксов.»
        """
        sub_text = '''
        из письма Абеля своему
        учителю и другу Хольмбоэ,
        16 января 1826 года
        '''
        
        quote = Text(text, font='sans-serif', font_size=24, line_spacing=0.8, color=GRAY_A)
        quote_sub = Text(sub_text, font='sans-serif', font_size=24, line_spacing=0.6, color=GRAY_C).scale(0.7)
        quote_sub.next_to(quote, UP, aligned_edge=LEFT).shift(0.5 * LEFT)
        quote_grp = VGroup(quote_sub, quote)
        quote_grp.scale(1.15).next_to(grp, LEFT, buff=LARGE_BUFF)
        
        self.play(
            Write(cap),
            Create(svg[:6], run_time=8),
            Succession(
                Create(svg[6], run_time=10),
                Create(svg[7:], run_time=5),
            ),
            Write(quote_grp)
        )
        self.wait()
        
        
    def prepare_svg_mobject(self, *args, **kwargs):
        """ *args, **kwargs -- как в SVGMobject """
        svg = SVGMobject(*args, **kwargs)
        for mob in svg.submobjects:
            if not mob.stroke_width:
                mob.stroke_width = 1
        return svg


#%% Выдающиеся математики
class DistinguishedMathematicians(QuoteAbel):
    fn_abel = get_person_svg_path('abel')
    fn_riemann = get_person_svg_path('riemann')
    fn_cauchy = get_person_svg_path('cauchy')
    fn_dirichlet = get_person_svg_path('dirichlet')
    
    def construct(self):
        h_tgt = 2
        h0 = 6
        abel = self.prepare_svg_mobject(self.fn_abel, height=h0, stroke_color=BLUE, stroke_width=2)
        cauchy = self.prepare_svg_mobject(self.fn_cauchy, height=h0, stroke_color=BLUE, stroke_width=2)
        dirichlet = self.prepare_svg_mobject(self.fn_dirichlet, height=h0, stroke_color=BLUE, stroke_width=2)
        riemann = self.prepare_svg_mobject(self.fn_riemann, height=h0, stroke_color=BLUE, stroke_width=2)
        
        def get_cap_grp(svg, txt, quote=None, eq=None, txt_scale=0.4,
                        color=None, line_spacing=-1, quote_buff=LARGE_BUFF):
            cap = Text(txt, color=svg.get_color(), font='sans-serif')
            cap.scale(txt_scale).next_to(svg, DOWN, buff=SMALL_BUFF)
            grp = VGroup(svg, cap)
            if quote:
                cap2 = Text(quote, color=color, font='sans-serif', line_spacing=line_spacing)
                cap2.scale(txt_scale)
                cap2_grp = VGroup(cap2)
                if eq:
                    eq.next_to(cap2, DOWN, buff=MED_LARGE_BUFF)
                    cap2_grp.add(eq)
                cap2_grp.next_to(svg, LEFT, buff=quote_buff)
                grp.add(cap2_grp)
            return grp
        
        settings = dict(
            txt_scale=0.7,
            color=GRAY_A,
            line_spacing=0.6
        )
        
        # Абель, исходный
        eq_abel = MathTex('1-1+1-1+1-1+\ldots', color=RED)
        abel_grp = get_cap_grp(
            abel, 'Нильс Хенрик Абель, 1826',
            quote='называл расходящиеся\nряды ужасными\nи стыдил тех,\nкто использует их\nдля доказательств',
            eq=eq_abel,
            **settings
        ).set(width=10.5).to_edge(RIGHT)
        
        # Коши, исходный
        eq_cauchy = MathTex('1-{1\\over2}+{1\\over3}-{1\\over4}+\ldots', color=GREEN)
        #settings['txt_scale'] = 0.65
        cauchy_grp = get_cap_grp(
            cauchy, 'Огюстен Луи Коши, 1833',
            quote='впервые показал,\nчто от перестановки\nслагаемых\nв нашем ряду\nего сумма меняется',
            eq=eq_cauchy,
            **settings
        ).set(width=10.5).to_edge(RIGHT)
        
        # Дирихле, исходный
        eq_dirichlet = MathTex('1-{1\\over2}+{1\\over4}-{1\\over8}+{1\\over16}+\ldots', color=GREEN)
        dirichlet_grp = get_cap_grp(
            dirichlet, 'Петер Густав Лежён Дирихле, 1837',
            quote='указал,\nчто перестановка\nслагаемых не влияет\nна сумму, если\nряд сходится абсолютно',
            eq=eq_dirichlet,
            quote_buff=SMALL_BUFF,
            **settings
        ).set(width=10.5).to_edge(RIGHT)
        

        caps = ('Абель, 1826', 'Коши, 1833', 'Дирихле, 1837')
        svg_copy = [svg.copy().set(height=h_tgt) for svg in (abel, cauchy, dirichlet)]
        grp_copy = [get_cap_grp(svg,cap) for svg,cap in zip(svg_copy, caps) ]
        grp_target = VGroup(*grp_copy)
        grp_target.arrange(DOWN, buff=MED_SMALL_BUFF).move_to(ORIGIN).to_edge(LEFT)
        
        abel_grp_tgt, cauchy_grp_tgt, dirichlet_grp_tgt = grp_target


        #
        ## Анимируем Коши, Дирихле и Абеля
        #
        def animate_one(base, target, first_run_time=5):
            self.play(
                Write(base[1:]),
                Create(base[0]),
                run_time=first_run_time
            )
            self.wait()
            self.play(
                ReplacementTransform(base[0], target[0]),
                FadeOut(base[1:], scale=2),
                FadeIn(target[1:], shift=RIGHT)
            )
            self.wait()
        
        animate_one(cauchy_grp, cauchy_grp_tgt)
        animate_one(dirichlet_grp, dirichlet_grp_tgt)
        animate_one(abel_grp, abel_grp_tgt)
        
        #
        ## Риман и его теорема
        #
        text = """
«Можно так
переставить члены
условно сходящегося
ряда, что его сумма
будет любым наперёд
задуманным числом»
"""
        sub_text = '''
Из Трактатов Королевского
общества наук в Гёттингене
«О представимости функции
тригонометрическим рядом»,
1868 год
'''
        settings['txt_scale'] = 0.5
        riemann_grp = get_cap_grp(
            riemann.set(width=0.87*riemann.get_width()), 'Георг Фридрих Бернхард Риман',
            **settings
        ).to_edge(RIGHT)
        quote = Text(text, font='sans-serif', font_size=24, line_spacing=0.8, color=GRAY_A)
        quote_sub = Text(sub_text, font='sans-serif', font_size=24, line_spacing=0.6, color=GRAY_C).scale(0.7)
        quote_sub.next_to(quote, UP, aligned_edge=LEFT).shift(0.5 * LEFT)
        quote_grp = VGroup(quote_sub, quote)
        quote_grp.scale(1.15).next_to(riemann_grp, LEFT, buff=MED_SMALL_BUFF)
        
        self.play(
            Create(riemann_grp[0], run_time=10),
            Succession(
                Write(riemann_grp[1]),
                Write(quote_grp)
            )
        )
        self.wait()
        

#%%
class QuotePushkin(QuoteAbel):
    fn = get_person_svg_path('pushkin')
    
    def construct(self):
        svg = self.prepare_svg_mobject(self.fn, height=5.5, stroke_color=BLUE)
        
        text = '''
        «Полки ряды свои сомкнули.
        '''
        text2 = '''
        ...
        Тогда-то свыше вдохновенный
        Раздался звучный глас Петра:
        "За дело, с Богом!"...
        Его глаза Сияют.»
        '''
        sub_text = '''
        «Полтава», март 1829 года
        '''
        
        quote = Text(text, font='sans-serif', font_size=24, line_spacing=0.8, color=GRAY_A, t2c={'ряды': GOLD})
        quote2 = Text(text2, font='sans-serif', font_size=24, line_spacing=0.8, color=GRAY_A, t2c={'глас Петра:': GOLD, '"За дело, с Богом!"': GOLD})
        quote_sub = Text(sub_text, font='sans-serif', font_size=24, line_spacing=0.6, color=GRAY_C).scale(0.7)
        quote_sub.next_to(quote, UP, aligned_edge=LEFT).shift(0.5 * LEFT)
        quote2.next_to(quote, DOWN, aligned_edge=LEFT)
        quote_grp = VGroup(quote_sub, quote, quote2)
        quote_grp.scale(1).next_to(svg, LEFT, buff=MED_LARGE_BUFF)
        
        svg_grp = VGroup(svg, quote_grp).move_to(ORIGIN)
        
        self.play(
            Create(svg[0], run_time=8),
            LaggedStart(
                *[Create(x, run_time=1) for x in svg[1:]],
            ),
            Write(quote_grp[:-1], run_time=4)
        )
        self.wait()
        
        self.play(Write(quote2))
        self.wait()


#%% Тестовый рендер
if __name__ == '__main__':
    
    from helpers.render import dev_render
    
    dev_render(__file__, QuotePushkin)