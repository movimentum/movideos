#
# 4. Расходимость гармонического ряда через сравнение площадей
#

from manim import *

from movi_ext import *

from auxfuncs import split2syms
from number_bag import NumberBag


#%%
SceneExtension.video_orientation = 'landscape'


#%%
class TwoBags(MovingCameraScene, SceneExtension):
    def construct(self):
        #
        ## Ряд (-1)^n не устроил
        #
        #   0	1	2	3	4	5	6	7	8	9	10	11	12	13	14	15	16	17	18	19	    20	
        #   1	-	1	+	1	-	1	+	1	-	1 	+ 	1 	- 	1 	+ 	1 	- 	1 	+ 	\ldots	
        raw = '1 - 1 + 1 - 1 + 1 - 1 + 1 - 1 + 1 - 1 + \\ldots'
        sym = split2syms(raw)
        eq_div = MathTex(*sym)
        eq_div.to_edge(UP)
        src = (3, 7, 11, 15)
        eq_div_pos = [eq_div[0]] + [eq_div[i:i+2] for i in src]
        eq_div_neg = [eq_div[i-2:i] for i in src] + [eq_div[17:17+2]]
        
        cr_div = Cross(eq_div, stroke_color=BLUE, stroke_width=2)
        self.play(FadeIn(eq_div, shift=DOWN))
        self.play(Create(cr_div), run_time=2)
        self.wait()

        
        #
        ## Но при чём здесь он, если наш исходный ряд сходился к ln2?
        #
        #   0	1	2	3	    4	5	6	7	8	9	   10	11	12	13	14	15	   16	17	18	19	20	21	   22	23	24	25	26	27	   28	29	30	31	32	33	   34	35	36	37	38	39	   40	41	42	43	44	45	   46	47	48	49	50	51	   52	53	54	55	56	57	   58	59	60	61	62	63	   64	65	66	67	    68	69	 70	71	
        #   1	-	{	1	\over	2	}	+	{	1	\over	3 	} 	- 	{ 	1 	\over	4 	} 	+ 	{ 	1 	\over	5 	} 	- 	{ 	1 	\over	6 	} 	+ 	{ 	1 	\over	7 	} 	- 	{ 	1 	\over	8 	} 	+ 	{ 	1 	\over	9 	} 	- 	{ 	1 	\over	10	} 	+ 	{ 	1 	\over	11	} 	- 	{ 	1 	\over	12	} 	+ 	\ldots	= 	\ln	2 	
        raw = '1'
        for i in range(2, 2+11):
            operation = ' + ' if i % 2 else ' - '
            element = '{ 1 \over ' + f'{i}' + ' }'
            raw += operation
            raw += element
        raw += ' + \ldots = \ln 2'
        sym = split2syms(raw)
        eq = MathTex(*sym).scale(0.8)
        src = (7, 19, 31, 43, 55)
        eq_pos = [eq[0]] + [eq[i:i+6] for i in src]
        eq_neg = [eq[i-6:i] for i in src] + [eq[61:61+6]]
        self.play(FadeIn(eq, shift=DOWN))
        self.wait()

        
        #
        ## В обоих чередуются знаки. Выделим мешки + и -
        #
        self.play(
            LaggedStart(
                *[term.animate.set_color(GREEN) for term in eq_div_pos],
                lag_ratio=0.1
            ),
            LaggedStart(
                *[term.animate.set_color(GREEN) for term in eq_pos],
                lag_ratio=0.1
            ),
        )
        self.wait()
        self.play(
            LaggedStart(
                *[term.animate.set_color(RED) for term in eq_div_neg],
                lag_ratio=0.1
            ),
            LaggedStart(
                *[term.animate.set_color(RED) for term in eq_neg],
                lag_ratio=0.1
            ),
        )
        self.wait()
        
        # Убираем расходящийся ряд        
        self.play(
            FadeOut(VGroup(eq_div, cr_div)),
            eq.animate.to_edge(UP)
        )
        self.wait()
        
        
        #
        ## Показать составление суммы путём выбора членов из мешков -- когда-то
        ## вытащим каждое слагаемое из обоих мешков, то есть, переберём их все
        #
        bag_pos = NumberBag(GREEN, GREEN_A, GREEN_E, 5, 5, 'положительные слагаемые')
        bag_neg = NumberBag(RED, RED_A, RED_E, 5, 5, 'отрицательные слагаемые')
        bag_grp = VGroup(bag_pos, bag_neg)
        bag_grp.arrange(buff=2*LARGE_BUFF).next_to(eq, DOWN)
        bag_neg.align_to(bag_pos, UP)
        bag_pos.remove_remaining_circles()
        bag_neg.remove_remaining_circles()
        
        self.play(FadeIn(bag_grp, scale=0),
                  rate_func=rate_functions.ease_out_back)
        self.wait()
        
        
        # Перетаскиваем элементы в мешки
        circles = bag_pos.get_all_possible_circles()
        eq_pos_extended = eq_pos + [eq[68]] * (len(circles) - len(eq_pos))
        self.play(LaggedStart(
            *[ReplacementTransform(
                term.copy().set_color(c.get_color()), c
                ) for term,c in zip(eq_pos_extended, circles)
             ],
            lag_ratio=0.2
        ))
        bag_pos.add_all_circles()  # TODO: если FadeOut(bag_pos), то circles останутся, так как в submobjects, по-видимому, хранится копия... Придётся отдельно делать FadeOut(bag_pos.circles)
        self.wait()
        
        circles = bag_neg.get_all_possible_circles()
        eq_neg_extended = eq_neg + [eq[68]] * (len(circles) - len(eq_neg))
        self.play(LaggedStart(
            *[ReplacementTransform(
                term.copy().set_color(c.get_color()), c
                ) for term,c in zip(eq_neg_extended, circles)
             ],
            lag_ratio=0.1
        ))
        bag_neg.add_all_circles()  # TODO: то же, что и для bag_pos
        self.wait()
        
        
        #
        ## Строим подпись-ряд к каждому мешку
        #
        #   0	1	2	3	    4	5	6	7	8	9	   10	11	12	13	14	15	   16	17	18	19	20	21	   22	23	24	25	26	27	   28	29	30	31	    32	
        #   1	+	{	1	\over	3	}	+	{	1	\over	5 	} 	+ 	{ 	1 	\over	7 	} 	+ 	{ 	1 	\over	9 	} 	+ 	{ 	1 	\over	11	} 	+ 	\ldots	
        raw = '1'
        for i in range(2, 2+11):
            if not i % 2:
                continue
            element = ' + { 1 \\over ' + f'{i}' + ' }'
            raw += element
        raw += ' + \ldots'
        sym = split2syms(raw)
        subeq_pos = MathTex(*sym, color=GREEN).scale(0.8)
        subeq_pos.next_to(bag_pos, DOWN)
        src = (1,7,13,19,25)
        subeq_pos_grouped = [subeq_pos[0]] + [subeq_pos[i:i+6] for i in src]
        
        #   0	1	2	    3	4	5	6	7	8	    9	10	11	12	13	14	   15	16	17	18	19	20	   21	22	23	24	25	26	   27	28	29	30	31	32	   33	34	35	36	    37	
        #   -	{	1	\over	2	}	-	{	1	\over	4 	} 	- 	{ 	1 	\over	6 	} 	- 	{ 	1 	\over	8 	} 	- 	{ 	1 	\over	10	} 	- 	{ 	1 	\over	12	} 	+ 	\ldots	
        raw = ''
        for i in range(2, 2+11):
            if i % 2:
                continue
            element = '- { 1 \\over ' + f'{i}' + ' } '
            raw += element
        raw += ' + \ldots'
        sym = split2syms(raw)
        subeq_neg = MathTex(*sym, color=RED).scale(0.8)
        subeq_neg.next_to(bag_neg, DOWN)
        src = (0,6,12,18,24,30)
        subeq_neg_grouped = [subeq_neg[i:i+6] for i in src]
        
        self.play(
            LaggedStart(
                *[ReplacementTransform(
                    term.copy(), subterm
                ) for term,subterm in zip(eq_pos, subeq_pos_grouped)
                ],
                lag_ratio=0.2
            ),
            FadeIn(subeq_pos[-2:], shift=DOWN),
        )
        self.wait()
        
        self.play(
            LaggedStart(
                *[ReplacementTransform(
                    term.copy(), subterm
                ) for term,subterm in zip(eq_neg, subeq_neg_grouped)
                ],
                lag_ratio=0.2
            ),
            FadeIn(subeq_neg[-2:], shift=DOWN),
        )
        self.wait()
        
        
        #
        ## Приближаемся к гармоническому ряду...
        #
        #   0	1	2	    3	4	5	    6	     7	8	9	10	11	   12	13	14	15	16	17	   18	19	20	21	22	23	   24	25	26	27	28	29	   30	31	32	33	34	35	   36	37	38	39	    40	     41	
        #   -	{	1	\over	2	}	\cdot	\left(	1	+	{ 	1 	\over	2 	} 	+ 	{ 	1 	\over	3 	} 	+ 	{ 	1 	\over	4 	} 	+ 	{ 	1 	\over	5 	} 	+ 	{ 	1 	\over	6 	} 	+ 	\ldots	\right)	
        raw = '- { 1 \\over 2 } \cdot \left( 1 ' 
        for i in range(2, 2+5):
            element = ' + { 1 \\over ' + f'{i}' + ' } '
            raw += element
        raw += ' + \ldots \\right)'
        sym = split2syms(raw)
        harmonic = MathTex(*sym, color=RED).scale(0.8)
        harmonic.next_to(subeq_neg, DOWN)
        
        self.play(TransformMatchingTex(subeq_neg.copy(), harmonic))
        self.wait()
        
        grp = harmonic[8:-1]
        grp.generate_target()
        grp.target.set_color(GOLD_E).move_to(ORIGIN).to_edge(DOWN).shift(UP)
        self.camera.frame.save_state()
        subeq_grp = VGroup(subeq_pos, subeq_neg).save_state()
        self.play(
            LaggedStart(
                *[FadeOut(harmonic[i], scale=0.25) for i in (list(range(8)) + [-1]) ],
                lag_ratio=0.05
            ),
            MoveToTarget(grp),
            self.camera.frame.animate.move_to(grp.target).set(width=1.5 * grp.target.get_width()),
            subeq_grp.animate.set_opacity(0.3),
        )
        self.wait()
        br = Brace(grp, color=GOLD_A)
        txt = Text('гармонический ряд', color=GOLD_A, font='sans-serif', font_size=24).next_to(br, DOWN)
        self.play(
            DrawBorderThenFill(br),
            Write(txt))
        self.wait()
        
        
        #
        ## Далее идёт обсуждение гармонического ряда
        #
        
        self.next_section('after_harmonic_divergence_proof')
        
        #
        ## Демонстрируем бездонный колодец с отрицательными членами
        #
        self.play(
            Restore(self.camera.frame),
            Restore(subeq_grp),
            FadeOut(VGroup(br,txt,grp), shift=DOWN, scale=0.5),
        )
        self.wait()
        
        bag_neg.bag.generate_target()
        bag_neg.bag.target.stretch(4, dim=1).align_to(bag_pos.bag, UP)
        inf_neg_sign = MathTex('-', '\infty', color=RED).scale(3).move_to(bag_neg.bag.target)
        self.play(
            Succession(Write(inf_neg_sign)),
            MoveToTarget(bag_neg.bag)
        )
        self.wait()
        
        
        #
        ## Следовательно, бездонный и с положительными членами, иначе сумма ряда была бы бесконечна
        #
        br1 = Brace(subeq_pos, DOWN, stroke_width=2, color=GREEN_A)
        #gr_sign = MathTex('>', color=GREEN).scale(1.5).rotate(-90*DEGREES).next_to(br1, DOWN)
        gr_sign = Text('больше, чем:', font='sans-serif', color=GREEN_A).scale(0.5).next_to(br1, DOWN)

        #   0	1	    2	3	4	5	6	7	    8	9	10	11	12	13	   14	15	16	17	18	19	   20	21	22	23	24	25	   26	27	28	29	30	31	   32	33	34	35	    36	
        #   {	1	\over	2	}	+	{	1	\over	4	} 	+ 	{ 	1 	\over	6 	} 	+ 	{ 	1 	\over	8 	} 	+ 	{ 	1 	\over	10	} 	+ 	{ 	1 	\over	12	} 	+ 	\ldots	
        raw = '{ 1 \\over 2 } '
        for i in range(4, 11+2):
            if i % 2:
                continue
            element = '+ { 1 \\over ' + f'{i}' + ' } '
            raw += element
        raw += ' + \ldots'
        sym = split2syms(raw)
        subeq_pos_est = MathTex(*sym, color=GOLD).scale(0.8)
        subeq_pos_est.next_to(gr_sign, DOWN)
        src = (5,11,17,23,29)
        subeq_pos_est_grouped = [subeq_pos_est[:5]] + [subeq_pos_est[i:i+6] for i in src]
        
        self.play(DrawBorderThenFill(br1), Write(gr_sign))
        self.play(LaggedStart(
            *[AnimationGroup(
                Indicate(prev, scale_factor=1.5),
                ReplacementTransform(prev_neg, new),
                ) for prev,prev_neg,new in zip(
                    subeq_pos_grouped,
                    subeq_neg_grouped,
                    subeq_pos_est_grouped
                    )
            ],
            lag_ratio=1
        ))
        self.play(
            Indicate(subeq_pos[-2:], scale_factor=1.5),
            ReplacementTransform(subeq_neg[-2:], subeq_pos_est[-2:]),
        )
        self.wait()
        
        inf_pos_sign = MathTex('+', '\infty', color=GREEN).scale(3).move_to(subeq_pos_est)
        self.play(ReplacementTransform(subeq_pos_est, inf_pos_sign))
        self.wait()
        
        
        #
        ## Демонстрируем бездонный колодец с положительными членами
        #
        bag_pos.bag.generate_target()
        bag_pos.bag.target.stretch(4, dim=1).align_to(bag_neg.bag, UP)
        inf_pos_sign.generate_target()
        inf_pos_sign.target.move_to(bag_pos.bag.target)
        self.play(
            FadeOut(VGroup(subeq_pos,gr_sign,br1), shift=UP, scale=2),
            MoveToTarget(bag_pos.bag),
            MoveToTarget(inf_pos_sign)
        )
        self.wait()
        
        
        #
        ## Сколько нужно вынуть слагаемых, чтобы получить -100?
        #
        def get_table(vals, tex_strings, mob):
            mobj = [MathTex(s) for s in tex_strings]
            txts = [MathTex(str(v)) for v in vals]
            
            data = [MathTex('\Sigma'), MathTex("n")]  # сначала заголовки
            [data.extend([v,m]) for v,m in zip(txts, mobj)]
            tbl = VGroup(*data)
            tbl.arrange_in_grid(rows=len(vals)+1, cols=2, cell_alignment=DL, buff=(MED_LARGE_BUFF, MED_SMALL_BUFF))
            tbl.move_to(mob).to_edge(DOWN).set_color(GRAY_A)
            tbl.add_background_rectangle(buff=SMALL_BUFF, corner_radius=SMALL_BUFF)
            return tbl
            
        vals = [-2,-5,-10,-100]
        tex_strings = ['31','12400','10^9', '10^{87}']
        tbl_neg = get_table(vals, tex_strings, bag_neg)
        
        vals = ['+2','+5','+10','+100']
        tex_strings = ['8','3100','10^8', '10^{86}']
        tbl_pos = get_table(vals, tex_strings, bag_pos)
        
        self.play(Create(tbl_pos), Create(tbl_neg))
        self.wait()
        
        box = SurroundingRectangle(Group(tbl_pos[-2:], tbl_neg[-2:]), color=BLUE, corner_radius=0.2)
        txt = Text('Чтобы получить\nв сумме 100,\nнужно взять\nслагаемых больше, \nчем атомов\nво вселенной!',
                   font='sans-serif', line_spacing=0.5)
        txt.scale(0.5).next_to(box, UP).shift(0.15*RIGHT).set_color(BLUE)
        last_el_grp = VGroup(tbl_pos[-2:], tbl_neg[-2:])
        att_grp = VGroup(box, txt, last_el_grp)
        self.play(
            Succession(
                Create(box),
                Write(txt)
            ),
            tbl_pos[:-2].animate.set_opacity(0.1),
            tbl_neg[:-2].animate.set_opacity(0.1),
            bag_grp.animate.set_opacity(0.1),
            eq.animate.set_opacity(0.1),
            inf_pos_sign.animate.set_opacity(0.35),
            inf_neg_sign.animate.set_opacity(0.35),
            last_el_grp.animate.set_color(BLUE),
            self.camera.frame.animate.move_to(att_grp).set(width=1.1*att_grp.get_width())
        )
        self.wait()
        


#%% 
class HarmonicDivergence(MovingCameraScene, SceneExtension):
    def construct(self):
        ax = Axes(
            x_range=[0, 7],
            y_range=[0, 1.5],
            x_length=10,
        )
        ax.add_coordinates()
        
        func_recip = lambda x: 1 / x
        curve = ax.plot(func_recip, x_range=[0.7, 6.5], discontinuities=[0,], dt=0.5)
        curve.set(stroke_width=5, color=GOLD)

        rects = ax.get_riemann_rectangles(
            curve,
            x_range=[1, 6],
            dx=1,
            color=(TEAL, BLUE_B, DARK_BLUE),
            input_sample_type="left",
        )
        rects.set_opacity(0.5)

        #self.add(ax, rects, curve)
        self.play(Create(ax))
        self.play(Create(curve))
        self.wait()
        
        #
        ### Рисуем горизонтальные линии
        #
        lines = [ ax.get_lines_to_point(ax.c2p(i,func_recip(i))) for i in range(1, 6) ]
        dots = [ Dot(ax.c2p(i,func_recip(i)), color=GOLD).set_opacity(0.6) for i in range(1, 6) ]
        lines_grp = VGroup(*lines)
        lines_grp.set_color(GRAY).set_opacity(0.5)
        self.play(
            LaggedStart(*[Create(dot) for dot in dots], lag_ratio=0.5),
            LaggedStart(*[Create(line) for line in lines], lag_ratio=0.5),
            run_time=1
        )
        self.wait()
        
        rect_labels = []
        for i, r in enumerate(rects):
            tex_string = '1' if not i else '1 \\over ' + str(i+1)
            label = MathTex(tex_string).scale(0.5).next_to(r, UP)
            rect_labels.append(label)
        self.play(
            LaggedStart(*[FadeIn(label, shift=DOWN) for label in rect_labels], lag_ratio=0.5),
            LaggedStart(*[FadeIn(r, shift=UP) for r in rects], lag_ratio=0.5))
        self.wait()
        
        
        #
        ### Отмечаем площадь под кривой
        #
        area = ax.get_area(
            curve,
            x_range=(1, 6.001),  # 0,001 для того, чтобы исключить полосу минимальной величины при вычитании (см. ниже diff)
            color=(RED_A, RED_E),
            opacity=0.6,
            stroke_width=4,
        )
        area.set(stroke_color=YELLOW, stroke_opacity=1)
        self.play(DrawBorderThenFill(area))
        self.wait()
        
        
        # Разница фигур
        scale = 0.3
        
        area_orig = area.copy()
        area_target = area.copy().set(stroke_width=2).scale(scale)
        plus_sign = MathTex('+').next_to(area_target, RIGHT)
        
        diff_orig = VGroup(*[ Difference(r, area_orig, color=TEAL, fill_opacity=0.5).set(stroke_width=2) for r in rects ])
        diff_target = diff_orig.copy()
        diff_target.scale(scale).next_to(plus_sign, RIGHT)
        
        eq_sign = MathTex('=').next_to(area_target, LEFT)
        rects_target = rects.copy().scale(scale).next_to(eq_sign, LEFT)
        
        VGroup(rects_target, eq_sign, area_target, plus_sign, diff_target).to_corner(UR)


        self.play(LaggedStart(
            ReplacementTransform(rects.copy(), rects_target),
            FadeIn(eq_sign, shift=UP),
            lag_ratio=0.5
        ))
        self.play(ReplacementTransform(area_orig, area_target))
        self.play(LaggedStart(
            FadeIn(plus_sign, shift=UP),
            ReplacementTransform(diff_orig, diff_target),
            lag_ratio=0.5
        ))
        self.wait()
        
        
        #
        ## Делаем формулы
        #
        eq1 = MathTex('1', '+', '{1 \\over 2}', '+', '{1 \\over 3}', '+', '{1 \\over 4}', '+', '{1 \\over 5}', '+', '\\ldots', '+', '{1 \\over n}')
        eq1.scale(0.5).next_to(rects_target, DOWN)
        
        eq2 = MathTex('\intop_{', '1', '}^{n+1}','{1 \\over x}', 'dx')
        eq2.scale(0.5).next_to(area_target, DOWN)
        
        txt1 = Text('что-то', font_size=18)
        txt2 = Text('больше нуля', font_size=18).next_to(txt1, DOWN)
        txt = VGroup(txt1, txt2).next_to(diff_target, DOWN)
        
        src = tuple(range(5))
        dst = tuple(range(0,9,2))
        self.play(
            LaggedStart(
                *[TransformMatchingShapes(rect_labels[i], eq1[j]) for i,j in zip(src,dst)],
                lag_ratio=0.2
            ),
            *[FadeIn(eq1[i], shift=DOWN) for i in (1,3,5,7,9,10)]
        )
        self.play(Succession(
            Write(eq2),
            FadeIn(txt, shift=UP)
        ))
        self.wait()
        
        gr_sign = MathTex('>').move_to(eq_sign)
        
        est_grp = VGroup(eq1, rects_target, gr_sign, area_target, eq2)
        fad_grp = VGroup(diff_target, txt, plus_sign)
        
        est_grp.generate_target()
        est_grp.target.scale(1.5).to_corner(UR)
        est_grp.remove(gr_sign)
        gr_sign = est_grp.target[2]
        est_grp.target.remove(gr_sign)
        
        self.play(
            MoveToTarget(est_grp),
            ReplacementTransform(eq_sign, gr_sign),
            FadeOut(fad_grp, shift=UP)
        )
        self.play(Circumscribe(gr_sign))
        self.wait()
        
        
        #
        ## Оставляем в сцене только ряд и интеграл
        #
        ax_components_grp = VGroup(curve, rects, lines_grp, VGroup(*dots))
        self.play(
            FadeOut(rects_target, scale=0.5),
            FadeOut(area_target, scale=0.5),
            FadeOut(area, scale=0.5),
            FadeOut(ax_components_grp, scale=0.5),
            Uncreate(ax)
        )
        
        eq_grp = VGroup(eq1, gr_sign, eq2)
        eq_grp.generate_target()
        eq1.target, gr_sign.target, eq2.target = eq_grp.target
        gr_sign.target.scale(1/1.5)
        eq1.target.next_to(gr_sign.target, LEFT)
        eq2.target.next_to(gr_sign.target, RIGHT)
        eq_grp.target.move_to(ORIGIN)
        self.play(
            MoveToTarget(eq_grp),
            self.camera.frame.animate.set(width=2*eq_grp.target.get_width())
        )
        self.wait()
        
        
        #
        ## Делаем вывод, что сумма ряда не может быть конечным числом
        #
        #              0       1    2      3         4      5    6      7
        eq3 = MathTex('=', '\\ln', 'x', '\\right|', '^{n', '+', '1}', '_{1}')
        # NB! Порядок важен: сначала ^, затем _. Иначе в manim идёт путаница: хотим рисовать eq[i], а рисует eq[j], j != i (меняет местами члены уравнения только при рисовании)
        eq3.set_color(YELLOW).next_to(eq2, RIGHT)
        eq_grp.add(eq3)
        self.play(Write(eq3))
        self.play(eq_grp.animate.move_to(ORIGIN))
        self.wait()
        #              0      1     2    3    4    5    6    7     8      9
        eq4 = MathTex('=', '\\ln', '(', 'n', '+', '1', ')', '-', '\\ln', '1')
        eq4.set_color(YELLOW).next_to(eq2, RIGHT)
        
        eq4.shift(UP)
        self.play(
            ReplacementTransform(eq3[7], eq4[9]),
            ReplacementTransform(eq3[1].copy(), eq4[8]),
            ReplacementTransform(eq3[3].copy(), eq4[7]),
        )
        src = (0, 1, 4, 5, 6)
        dst = (0, 1, 3, 4, 5)
        self.play(
            *[ReplacementTransform(eq3[i], eq4[j]) for i,j in zip(src,dst)],
            *[FadeIn(eq4[i], shift=DOWN) for i in (2, 6)],
            *[FadeOut(eq3[i], scale=0.5) for i in (2,3)],
        )
        self.play(eq4.animate.shift(DOWN))
        self.wait()

        self.play(eq4[-3:].animate.set_color(RED))
        self.play(*[FadeOut(eq4[i], scale=0.5) for i in (-1,-2,-3)])
        self.wait()


#%% Тестовый рендер
if __name__ == '__main__':
    
    from helpers.render import dev_render
    
    dev_render(__file__, HarmonicDivergence)