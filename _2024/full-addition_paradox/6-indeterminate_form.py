#
# Неопределённость \infty - \infty
#

from manim import *

from movi_ext import *

from auxfuncs import split2syms
from number_bag import NumberBag
from series import Series, SeriesGeometric


#%%
SceneExtension.video_orientation = 'landscape'


#%%
class TwoInfDiffLimit(Scene, SceneExtension):
    def construct(self):
        
        #
        ## Что такое бесконечность?
        #
        nl = NumberLine(
            x_range=[0, 10.5],
            include_numbers=True,
            include_tip=True
        )
        nl.set_color(GRAY_A)
        self.play(Create(nl))
        self.wait()
        
        dot = Dot(color=BLUE).move_to(nl.n2p(0))
        dot.generate_target()
        dot.target.move_to(nl.n2p(11))
        infty = MathTex('\infty', color=BLUE).next_to(dot.target, UP)
        self.play(FadeIn(dot, shift=DOWN))
        self.wait()
        
        self.play(Succession(
            MoveToTarget(dot, run_time=3),
            FadeIn(infty, shift=DOWN, scale=2),
        ))
        self.wait()
        
        self.play(VGroup(nl, dot, infty).animate.to_edge(UP))
        self.wait()
        
        #
        ## Выявляем неопределённость
        #
        scale = 1.5
        inf2 = MathTex('\infty', '-', '1', '=', '\infty', color=GRAY_A).scale(scale)
        inf3 = MathTex('\infty', '-', '2', '=', '\infty', color=GRAY_A).scale(scale)
        inf2[0].set_color(BLUE)
        inf3[0].set_color(BLUE)
        inf2[-1].set_color(GREEN)
        inf3[-1].set_color(RED)
        inf2.shift(UP)
        inf3.next_to(inf2, DOWN).shift(DOWN)
        
        
        inf21 = MathTex('\infty', '-', '\infty', '=', '1', color=GRAY_A).scale(scale)
        inf31 = MathTex('\infty', '-', '\infty', '=', '2', color=GRAY_A).scale(scale)
        inf21[0].set_color(BLUE)
        inf31[0].set_color(BLUE)
        inf21[2].set_color(GREEN)
        inf31[2].set_color(RED)
        inf21.move_to(inf2)
        inf31.move_to(inf3)

        # Проявляем результат inf - число = inf
        self.play(Succession(
            ReplacementTransform(infty.copy(), inf2[0]),
            LaggedStart(*[FadeIn(v, shift=DOWN) for v in inf2[1:1+3]],
                        lag_ratio=0.2),
            FadeIn(inf2[-1], shift=LEFT)
        ))
        self.wait()
        self.play(Succession(
            ReplacementTransform(infty.copy(), inf3[0]),
            LaggedStart(*[FadeIn(v, shift=UP) for v in inf3[1:1+3]],
                        lag_ratio=0.2),
            FadeIn(inf3[-1], shift=LEFT)
        ))
        self.wait()
        
        # Меняем местами число и inf, выявляя неопределённость
        src = (0,1,2,3,4)
        dst = (0,1,4,3,2)
        arcs = (0,0,90,0,90)
        self.play(
            *[ReplacementTransform(inf2[i], inf21[j], path_arc=a*DEGREES) for i,j,a in zip(src,dst,arcs)],
            *[ReplacementTransform(inf3[i], inf31[j], path_arc=-a*DEGREES) for i,j,a in zip(src,dst,arcs)]
        )
        self.play(inf31.animate.shift(0.5*UP))
        self.wait()
        
        txt = Text('неопределённость', font='sans-serif', color=GRAY_A)
        inf4 = MathTex('\infty', '-', '\infty', color=GRAY_A).scale(2)
        txt_grp = VGroup(txt, inf4).arrange().next_to(inf31, DOWN).shift(DOWN)
        self.play(Succession(
            Write(txt_grp),
            Circumscribe(txt_grp),
        ))
        self.wait()
        
        
        # Убираем лишнее        
        self.play(
            txt_grp.animate.scale(0.8).to_edge(UP),
            Uncreate(nl),
            LaggedStart(
                *[FadeOut(x, shift=3*RIGHT) for x in (dot, infty)],
                *[FadeOut(x, scale=2) for x in (inf21, inf31)],
            )
        )
        self.wait()
        
        
        #######################################################################
        ################### Демонстрация примеров #############################
        #######################################################################
        
        grp_all = VGroup()
        
        # 2n - n
        nn = np.arange(1,11)
        vv_big = 2 * nn.copy()
        vv_small = nn.copy()
        cap_strings = ('2n', 'n', '\infty')
        grp = self.prepare_drawings(nn, vv_big, vv_small, cap_strings)
        grp_all.add(grp)
        
        # # n + 1/n - (n - 1/n)
        # vv_big = nn.copy()
        # cap_strings = ('n + 1/n', '\\left( n - 1/2n \\right)', '0')
        # grp = self.prepare_drawings(nn, vv_big, vv_small, cap_strings)
        # grp_all.add(grp)
        
        # n+3 - n
        vv_big = nn.copy() + 3
        cap_strings = ('n +  3', 'n', '3')
        grp = self.prepare_drawings(nn, vv_big, vv_small, cap_strings)
        grp_all.add(grp)
        
        # sqrt(n + 1) - sqrt(n - 1)
        nn = np.arange(1, 32, 3)
        vv_big = np.sqrt(nn + 1)
        vv_small = np.sqrt(nn - 1)
        cap_strings = ('\sqrt{n + 1}', '\sqrt{n - 1}', '0')
        grp = self.prepare_drawings(nn, vv_big, vv_small, cap_strings, n_digits=1)
        grp_all.add(grp)
        
        # sqrt(n^2 + n) - sqrt(n^2 - n)        
        nn = np.arange(1, 11)
        vv_big = np.sqrt(nn**2 + nn)
        vv_small = np.sqrt(nn**2 - nn)
        cap_strings = ('\sqrt{n^2 + n}', '\sqrt{n^2 - n}', '1')
        grp = self.prepare_drawings(nn, vv_big, vv_small, cap_strings, n_digits=1)
        grp_all.add(grp)
        
        # ln(2n) - ln(n)        
        nn = np.arange(1, 72, 7)
        vv_big = np.log(2*nn + 3)
        vv_small = np.log(nn)
        cap_strings = ('\ln (2n+2)', '\ln (n)', '\ln 2')
        grp = self.prepare_drawings(nn, vv_big, vv_small, cap_strings,
                                    n_digits=2, cap_pos=DR)
        grp_all.add(grp)
        
        ############### Series_pos - Series_neg ###############################
        ser = Series(np.log(2))
        n_terms = 60
        nn = np.arange(1, 1+n_terms//2)[::3]
        vv_big, vv_small = ser.calc_sums_pos_neg(n_terms)
        vv_big = vv_big[::3]
        vv_small = vv_small[::3]
        #   0	1	2	3	    4	5	6	7	8	9	   10	11	12	13	14	15	   16	17	18	19	    20	21	22	23	   24	25	26	27	28	29	30	31	   32	33	34 35	          36	     37	  38	
        #   1	-	{	1	\over	2	}	+	{	1	\over	3 	} 	- 	{ 	1 	\over	4 	} 	+ 	\ldots	+ 	{ 	1 	\over	2n	- 	1 	} 	- 	{ 	1 	\over	2n	}  tendsto...	\ln2	\approx	0.69
        raw = '1'
        for i in range(2, 2+3):
            operation = ' + ' if i % 2 else ' - '
            element = '{ 1 \over ' + f'{i}' + ' }'
            raw += operation
            raw += element
        raw += ' + \ldots '
        raw += '+ { 1 \over 2n - 1 } '
        raw += '- { 1 \over 2n }'
        lim = '\ln2 \\approx 0.69'
        grp_final = self.prepare_drawings(nn, vv_big, vv_small, (raw, lim),
                                          n_digits=2, base_scale_digits=0.4,
                                          cap_scale=0.65, cap_pos=DR)
        eq_final = grp_final[-1][0]
        src = (0, 7, 19, 21)
        dst = (1, 13, 21, 29)
        eq_final_pos = [eq_final[i:j] for i,j in zip(src,dst)]  # NB! with \ldots
        src = (1, 13, 19, 29)
        dst = (7, 19, 21, 35)
        eq_final_neg = [eq_final[i:j] for i,j in zip(src,dst)]
        [eq.set_color(GREEN) for eq in eq_final_pos]
        [eq.set_color(RED) for eq in eq_final_neg]
        eq_final[19:21].set_color(GRAY_A)
        #---------------------------------------------------------------------#
        
        
        ############# Series_pos - Series_neg после перестановки ##############
        ser = Series(np.log(2)/2)
        n_terms = 30
        nn = np.arange(1, 1+n_terms)[::3]
        vv_big, vv_small = ser.calc_sums_pos_neg_neg(n_terms)
        vv_big = vv_big[::3]
        vv_small = vv_small[::3]
        #   0	1	2	3	    4	5	6	7	8	9	   10	11	12	13	    14	15	16	17	   18	19	20	21	22	23	24	25	   26	27	28	29	30	31	32	33	   34	35	36	37	       38       39	   40	41	42       43	  44	
        #   1	-	{	1	\over	2	}	-	{	1	\over	4 	} 	+ 	\ldots	+ 	{ 	1 	\over	3n	- 	2 	} 	- 	{ 	1 	\over	3n	- 	1 	} 	- 	{ 	1 	\over	3n	} 	tendsto... {       \ln2	\over	2 	} 	\approx	0.35	
        raw = '1'
        raw += ' - { 1 \over 2 } '
        raw += ' - { 1 \over 4 } '
        raw += ' + \ldots '
        raw += ' + { 1 \over 3n - 2 } '
        raw += ' - { 1 \over 3n - 1 }'
        raw += ' - { 1 \over 3n }'
        lim = ' { \ln2 \\over 2 } \\approx 0.35'
        grp_reord = self.prepare_drawings(
            nn, vv_big, vv_small, (raw, lim),
            n_digits=2, base_scale_digits=0.4,
            cap_scale=0.65, cap_pos=DR
        )
        eq_reord = grp_reord[-1][0]
        
        src = (0, 13, 15)
        dst = (1, 15, 23)
        eq_reord_pos = [eq_reord[i:j] for i,j in zip(src,dst)]  # NB! with \ldots
        src = (1, 7, 13, 23, 31)
        dst = (7, 13, 15, 31, 37)
        eq_reord_neg = [eq_reord[i:j] for i,j in zip(src,dst)]
        [eq.set_color(GREEN) for eq in eq_reord_pos]
        [eq.set_color(RED) for eq in eq_reord_neg]
        eq_reord[13:15].set_color(GRAY_A)
        #---------------------------------------------------------------------#


        txt_grp.generate_target()  # " неопределённость inf - inf
        txt_grp.target.shift(2*RIGHT)
        grp_all.next_to(txt_grp.target, DOWN).shift(0.5*DOWN)
        grp_all_cpy = grp_all[:-1].copy()
        grp_all_cpy.scale(0.3).arrange(DOWN).move_to(ORIGIN).to_edge(LEFT)
        
        def graph_anim(grp, run_time=None):
            """ Последовательная отрисовка примера """
            ani = []
            ani.append(Create(grp[:2]))  # ax, xlabel
            ani.append(Write(grp[5]))  # cap
            ani.append(LaggedStart(  # dots
                Create(grp[2]['vertex_dots']),
                Create(grp[3]['vertex_dots']),
                lag_ratio=0.1,
            ))
            ani.append(AnimationGroup(  # graphs
                Create(grp[2]['line_graph']),
                Create(grp[3]['line_graph']),
            ))
            ani.append(Create(grp[4]))  # diffs
            return Succession(*ani, run_time=run_time)
        
        # Рисуем первый пример
        self.play(
            MoveToTarget(txt_grp),
            graph_anim(grp_all[0])
        )
        self.wait()
        
        # Рисуем остальные примеры
        run_times = [2] * (len(grp_all) - 1)
        run_times[-1] = None
        for g1, g1_cpy, g2, run_time in zip(grp_all[:-1], grp_all_cpy, grp_all[1:], run_times):
            self.play(
                ReplacementTransform(g1, g1_cpy),
                graph_anim(g2, run_time=run_time)
            )
            self.wait()



        #######################################################################
        ######################## Анализ нашего ряда ###########################
        #######################################################################

        #
        ## Обновляем пример на исследуемый ряд
        #        
        grp_main = grp_all[-1]  # текущая пример, сейчас крупным планом
        txt_grp.generate_target()
        txt_grp.target.move_to(ORIGIN).to_edge(UP)
        grp_final.scale(1.1).next_to(txt_grp.target, DOWN)
        self.play(
            FadeOut(grp_all_cpy, scale=2, shift=LEFT),
            MoveToTarget(txt_grp),
            ReplacementTransform(grp_main, grp_final),
        )
        self.wait()


        #
        ## Добавляем ряды с мешками для аналогии
        #
        ################# Частичная сумма положительных членов ################
        #   0	1	2	3	    4	5	6	7	     8	9	10	11	   12	13	14	15	16                                             17	    18	
        #   1	+	{	1	\over	3	}	+	\ldots	+	{ 	1 	\over	2n	- 	1 	}  \underset{n\rightarrow\infty}{\longrightarrow}	\infty	
        raw = '1'
        for i in range(2, 2+3):
            if not i % 2:
                continue
            element = ' + { 1 \\over ' + f'{i}' + ' }'
            raw += element
        raw += ' + \ldots'
        raw += ' + { 1 \\over 2n - 1 }'
        tends = r' \underset{n\rightarrow\infty}{\longrightarrow} '
        raw += tends + '\infty'
        sym = split2syms(raw)
        eq_pos = MathTex(*sym, color=GREEN).scale(0.6)
        src = (0,1,7,9)
        dst = (1,7,9,17)
        eq_pos_grouped = [eq_pos[i:j] for i,j in zip(src,dst)]
        #---------------------------------------------------------------------#
        
        
        ################# Частичная сумма отрицательных членов ################
        #   0	1	    2	3	4	5	6	7	    8	9	10	11	    12	13	14	15	   16	17	18                                             19	    20	
        #   {	1	\over	2	}	+	{	1	\over	4	} 	+ 	\ldots	+ 	{ 	1 	\over	2n	}  \underset{n\rightarrow\infty}{\longrightarrow}	\infty	       
        raw = ''
        for i in range(2, 2+3):
            if i % 2:
                continue
            element = ' + { 1 \\over ' + f'{i}' + ' }'
            raw += element
        raw += ' + \ldots'
        raw += ' + { 1 \\over 2n }'
        tends = r' \underset{n\rightarrow\infty}{\longrightarrow} '
        raw += tends + '\infty'
        sym = split2syms(raw[3:])
        eq_neg = MathTex(*sym, color=RED).scale(0.6)
        src = (0,5, 11,13)
        dst = (5,11,13,19)
        eq_neg_grouped = [eq_neg[i:j] for i,j in zip(src,dst)]
        #---------------------------------------------------------------------#


        lim = MathTex(tends, '\ln2')  # предел рядом с графиком
        lim.set_color(GOLD_A).scale(0.9).next_to(grp_final[-2][-1], RIGHT)
        
        # Мешки
        bag_pos = NumberBag(GREEN, GREEN_A, GREEN_E, 5, 5, None).scale(0.3)
        bag_neg = NumberBag(RED, RED_A, RED_E, 5, 5, None).scale(0.3)
        
        eq_pos.next_to(bag_pos)
        eq_neg.next_to(bag_neg)
        grp_pos = VGroup(bag_pos, eq_pos).shift(2*LEFT + 2*UP)
        grp_neg = VGroup(bag_neg, eq_neg).shift(0.5*RIGHT)
        grp_pos.rotate(10*DEGREES)
        grp_neg.rotate(8*DEGREES)
        
        #
        ## Появление частичных сумм из полной суммы, мешков и предела
        #
        self.play(LaggedStart(
            *[ReplacementTransform(base.copy(), sub) for base,sub in zip(eq_final_neg,eq_neg_grouped)],
            lag_ratio=0.1
        ))
        self.wait()
        
        self.play(LaggedStart(
            *[ReplacementTransform(base.copy(), sub) for base,sub in zip(eq_final_pos,eq_pos_grouped)],
            lag_ratio=0.1
        ))
        self.wait()
        
        self.play(
            FadeIn(bag_pos, shift=RIGHT),  # мешки
            FadeIn(bag_neg, shift=RIGHT),  #
            FadeIn(eq_pos[17:], shift=LEFT),  # пределы
            FadeIn(eq_neg[19:], shift=LEFT),  #
        )
        self.wait()

        self.play(ReplacementTransform(eq_final[35:35+2].copy(), lim))
        self.wait()
        
        
        #
        ## Пересортируем слагаемые (+,-,-)
        #
        grp_reord.scale(1.1).next_to(txt_grp.target, DOWN)
        lim_reord = MathTex(tends, '{', '\ln2', '\\over 2}')
        lim_reord.set_color(GOLD_A).scale(0.8).next_to(grp_reord[-2][-1], RIGHT)
        
        # grp_final и grp_reord имеют структуру
        # (ax, xlabel, line_big, line_small, lines_diff, cap)
        src = [eq_final_pos[0], *eq_final_neg[:3], eq_final_pos[3], eq_final_neg[3]]
        dst = [eq_reord_pos[0], *eq_reord_neg[:5], ]
        self.play(
            Succession(
                AnimationGroup(
                    ReplacementTransform(grp_final[-1][-1], grp_reord[-1][-1]),
                    *[ReplacementTransform(a,b) for a,b in zip(src,dst)],
                    FadeOut(eq_final_pos[1], scale=0.25),
                    FadeIn(eq_reord_pos[2], shift=DOWN),
                    TransformMatchingShapes(eq_final[35:], eq_reord[37:]),
                    lag_ratio=0.05,
                ),
                ReplacementTransform(grp_final[:-1], grp_reord[:-1]),
                TransformMatchingTex(lim, lim_reord),
            ),
            FadeOut(grp_pos, scale=0.5),
            FadeOut(grp_neg, scale=0.5),
        )
        self.wait()


    def generate_caption(self, cap_strings, scale=1.7):
        tends = r' \underset{n\rightarrow\infty}{\longrightarrow} '
        lim = cap_strings[-1]
        if len(cap_strings) == 2:
            sym = split2syms(cap_strings[0])
            cap = MathTex(*(sym + [tends] + lim.split(' '))).scale(scale)
            cap.set_color(GRAY_A)
        elif len(cap_strings) == 3:
            tex_big, tex_small = cap_strings[:2]
            cap = MathTex(tex_big, '-', tex_small, tends, lim).scale(scale)
            cap.set_color(GRAY_A)
            cap[0].set_color(GREEN)
            cap[2].set_color(RED)
        else:
            raise ValueError('cap_string должен содержать 1 или 2 строки')
        rect = SurroundingRectangle(
            cap,
            buff=MED_SMALL_BUFF,
            corner_radius=0.2,
            color=GRAY_A
        )
        return VGroup(cap, rect)
        
        
    def prepare_drawings(self, nn, vv_big, vv_small, cap_strings,
                         n_digits=0, base_scale_digits=0.5,
                         cap_scale=1.2, cap_pos=UL):
        """ Готовит оси и рисует в них заданные функции """
        nmax = nn[-1]
        dn = nn[-1] // 4
        dn = 1 if not dn else dn
        vmax = np.ceil(vv_big[-1] * 1.1)
        dv = int(vv_big[-1] / 4)
        dv = 1 if not dv else dv
        ax = Axes(
            x_range=[0, nmax, dn], y_range=[0, vmax, dv],
            x_length=10, y_length=6,
            axis_config={"numbers_to_exclude": []},
            x_axis_config={"numbers_to_include": [0]}
        )
        ax.add_coordinates()
        xlabel, _ = ax.get_axis_labels(x_label=MathTex('n'), y_label='')
        xlabel.shift(0.5*DOWN)
        
        line_big = ax.plot_line_graph(
            x_values=nn,
            y_values=vv_big,
            line_color=GREEN,
            vertex_dot_radius=0.1,
            vertex_dot_style=dict(stroke_width=1, fill_color=GREEN_A),
            stroke_width=4,
        )
        
        line_small = ax.plot_line_graph(
            x_values=nn,
            y_values=vv_small,
            line_color=RED,
            vertex_dot_radius=0.1,
            vertex_dot_style=dict(stroke_width=1, fill_color=RED_A),
            stroke_width=4,
        )
        
        lines_diff = VGroup()
        for n, vb, vs in zip(nn, vv_big, vv_small):
            ps = ax.c2p(n,vs)
            pb = ax.c2p(n,vb)
            d = np.linalg.norm(ps-pb)
            scale = base_scale_digits if d>1 else base_scale_digits * d
            line = Line(ps, pb).set_color(GOLD)
            dist = vb - vs
            label = Text(f'{dist:.{n_digits}f}').set_color(GOLD_A).scale(scale).rotate(90*DEGREES)
            label.add_background_rectangle()
            label.next_to(line, LEFT, buff=SMALL_BUFF)
            line.add(label)
            lines_diff.add(line)
        
        cap = self.generate_caption(cap_strings, scale=cap_scale)
        if cap_pos is UL:
            xpos = max(0.5, 0.05*nmax)
            ypos = vmax
        elif cap_pos is DR:
            xpos = min(nmax*0.95, nmax-1)
            ypos = min(0.5, vmax * 0.05)
        else:
            raise NotImplementedError('cap_pos should be only UL or DR')
        cap.move_to(ax.c2p(xpos, ypos), cap_pos)
        
        grp = VGroup(ax, xlabel, line_big, line_small, lines_diff, cap)
        grp.scale(0.85).move_to(ORIGIN)
        
        return grp


#%% Суммы геометрической прогрессии с конечными пределами
class TwoFiniteDiffLimit(TwoInfDiffLimit, SceneExtension):
    def construct(self):
        n_terms = 10
        nn = np.arange(1, 1+n_terms)
        
        #
        ## Базовое уравнение
        #
        #   0	1	    2	3	4	5	6	7	    8	9	10	11	12	13	   14	15	16	17	18	19	   20	21	22	23	24	25	   26	27	28	29	30	31	   32	33	34	35	36	37	   38	 39	40	41	42	43	   44	 45	46	47	    48	49	50	51	   52	      53	54	55	56	57	   58	    59	60	      61	62	63	   64	65	66	
        #   {	1	\over	2	}	-	{	1	\over	4	} 	+ 	{ 	1 	\over	8 	} 	- 	{ 	1 	\over	16	} 	+ 	{ 	1 	\over	32	} 	- 	{ 	1 	\over	64	} 	+ 	{ 	1 	\over	128	} 	- 	{ 	1 	\over	256	} 	+ 	\ldots	+ 	{ 	1 	\over	2^{2n-1}	} 	- 	{ 	1 	\over	2^{2n}	} 	\tendsto	{ 	1 	\over	3 	} 	
        raw  = '{ 1 \over 2 } '
        raw += ' - { 1 \over 4 } '
        raw += ' + { 1 \over 8 } '
        raw += ' - { 1 \over 16 } '
        raw += ' + { 1 \over 32 } '
        raw += ' - { 1 \over 64 } '
        raw += ' + { 1 \over 128 } '
        raw += ' - { 1 \over 256 } '
        raw += ' + \ldots '
        raw += ' + { 1 \over 2^{2n-1} } '
        raw += ' - { 1 \over 2^{2n} }'
        lim = ' { 1 \\over 3 }'
        
        grp_simple = self.prepare_drawings(
            nn, nn, nn, (raw, lim),
            n_digits=4, base_scale_digits=0.3,
            cap_scale=0.65, cap_pos=DR
        )
        eq_base = grp_simple[-1][0]
        src = (0, 11, 23, 35, 47, 49)
        dst = (5, 17, 29, 41, 49, 55)
        eq_base_pos = [eq_base[i:j] for i,j in zip(src,dst)]  # NB! with \ldots
        src = (5, 17, 29, 41, 47, 55)
        dst = (11,23, 35, 47, 49, 61)
        eq_base_neg = [eq_base[i:j] for i,j in zip(src,dst)]
        [eq.set_color(GREEN) for eq in eq_base_pos]
        [eq.set_color(RED) for eq in eq_base_neg]
        eq_base[47:49].set_color(GRAY_A)
        eq_base.scale(1).set_opacity(0.8).move_to(ORIGIN).to_edge(UP)
        
        
        
        #
        ## Ряд геометрической прогрессии
        #
        ser = SeriesGeometric(1/2, -1/2)
        vv_big, vv_small = ser.get_every_cumsum(n_terms, shape=(1,1))
        vv_big = vv_big
        vv_small = -vv_small
        #   0	1	    2	3	4	5	6	7	    8	9	10	11	12	13	   14	15	16	17	18	19	   20	21	22	23	    24	25	26	27	   28	      29	30	31	32	33	   34	 35	      36	37	38	   39	40	41	
        #   {	1	\over	2	}	-	{	1	\over	4	} 	+ 	{ 	1 	\over	8 	} 	- 	{ 	1 	\over	16	} 	+ 	\ldots	+ 	{ 	1 	\over	2^{2n-1}	} 	- 	{ 	1 	\over	2n}	\tendsto	{ 	1 	\over	3 	} 
        raw  = '{ 1 \over 2 } '
        raw += ' - { 1 \over 4 } '
        raw += ' + { 1 \over 8 } '
        raw += ' - { 1 \over 16 } '
        raw += ' + \ldots '
        raw += ' + { 1 \over 2^{2n-1} } '
        raw += ' - { 1 \over 2^{2n} }'
        lim = ' { 1 \\over 3 }'

        grp_simple = self.prepare_drawings(
            nn, vv_big, vv_small, (raw, lim),
            n_digits=4, base_scale_digits=0.3,
            cap_scale=0.65, cap_pos=DR
        )
        eq_simple = grp_simple[-1][0]
        
        src = (0, 11, 23, 25)
        dst = (5, 17, 25, 31)
        eq_simple_pos = [eq_simple[i:j] for i,j in zip(src,dst)]  # NB! with \ldots
        src = (5, 17, 23, 31)
        dst = (11,23, 25, 36)
        eq_simple_neg = [eq_simple[i:j] for i,j in zip(src,dst)]
        [eq.set_color(GREEN) for eq in eq_simple_pos]
        [eq.set_color(RED) for eq in eq_simple_neg]
        eq_simple[13:15].set_color(GRAY_A)
        #---------------------------------------------------------------------#
        
        
        #
        ## Предел не меняется
        #
        # grp_simple = (ax, xlabel, line_big, line_small, lines_diff, cap)
        #
        tends = r' \underset{n\rightarrow\infty}{\longrightarrow} '
        eq_lim = MathTex(tends, '{', '1', '\\over', '3', '}')
        eq_lim.set_color(GOLD_A).scale(0.8).next_to(grp_simple[-2][-1], RIGHT)
        
        eq_up = MathTex(tends, '{', '2', '\\over', '3', '}')
        eq_up.set_color(GREEN).scale(0.4).next_to(grp_simple[2]['line_graph'].get_corner(UR), RIGHT)
        
        eq_bot = MathTex(tends, '{', '1', '\\over', '3', '}')
        eq_bot.set_color(RED).scale(0.4).next_to(grp_simple[3]['line_graph'].get_corner(UR), RIGHT)
        
        txt_simple = Text('положительный — отрицательный', color=GRAY_A)
        txt_dbl = Text('положительный — два отрицательных', color=GRAY_A)
        txt_tri = Text('положительный — три отрицательных', color=GRAY_A)
        txt_simple.scale(0.5).next_to(grp_simple[2]['line_graph'], UP).shift(0.5*UP)
        txt_dbl.scale(0.5).next_to(grp_simple[2]['line_graph'], UP).shift(0.5*UP)
        txt_tri.scale(0.5).next_to(grp_simple[2]['line_graph'], UP).shift(0.5*UP)
        
        #
        ## Ряд геометрической прогрессии, +,-,-
        #
        vv_big, vv_small = ser.get_every_cumsum(n_terms, shape=(1,2))
        vv_big = vv_big
        vv_small = -vv_small
        #   0	1	    2	3	4	5	6	7	    8	9	10	11	12	13	   14	15	16	17	    18	19	20	21	   22	      23	24	25	26	27	   28	      29	30	31	32	33	   34	 35	      36	37	38	   39	40	41	
        #   {	1	\over	2	}	-	{	1	\over	4	} 	- 	{ 	1 	\over	16	} 	+ 	\ldots	+ 	{ 	1 	\over	2^{3n-2}	} 	- 	{ 	1 	\over	2^{3n-1}	} 	- 	{ 	1 	\over	3n}	\tendsto	{ 	1 	\over	3 	} 	
        raw  = '{ 1 \over 2 } '
        raw += ' - { 1 \over 4 } '
        raw += ' - { 1 \over 16 } '
        raw += ' + \ldots '
        raw += ' + { 1 \over 2^{2n-1} } '
        raw += ' - { 1 \over 2^{4n-2} } '
        raw += ' - { 1 \over 2^{4n} }'
        lim = ' { 1 \\over 3 }'

        grp_dbl = self.prepare_drawings(
            nn, vv_big, vv_small, (raw, lim),
            n_digits=4, base_scale_digits=0.3,
            cap_scale=0.65, cap_pos=DR
        )
        eq_dbl = grp_dbl[-1][0]
        
        src = (0, 17, 19)
        dst = (5, 19, 25)
        eq_dbl_pos = [eq_dbl[i:j] for i,j in zip(src,dst)]  # NB! with \ldots
        src = (5, 11,17,25,31)
        dst = (11,17,19,31,36)
        eq_dbl_neg = [eq_dbl[i:j] for i,j in zip(src,dst)]
        [eq.set_color(GREEN) for eq in eq_dbl_pos]
        [eq.set_color(RED) for eq in eq_dbl_neg]
        eq_dbl[17:19].set_color(GRAY_A)
        #---------------------------------------------------------------------#
        
        
        #
        ## Ряд геометрической прогрессии, +,-,-,-
        #
        vv_big, vv_small = ser.get_every_cumsum(n_terms, shape=(1,3))
        vv_big = vv_big
        vv_small = -vv_small
        #        0	1	2	3	    4	       5	6	7	8	9	   10	      11	12	13	14	15	   16	      17	18	19	20	21	   22	    23	24	      25	26	27	   28	29	30	
        #   \ldots	+	{	1	\over	2^{2n-1}	}	-	{	1	\over	2^{6n-4}	} 	- 	{ 	1 	\over	2^{6n-2}	} 	- 	{ 	1 	\over	2^{6n}	} 	\tendsto	{ 	1 	\over	3 	} 
        raw  = '\ldots '
        raw += ' + { 1 \over 2^{2n-1} } '
        raw += ' - { 1 \over 2^{6n-4} } '
        raw += ' - { 1 \over 2^{6n-2} } '
        raw += ' - { 1 \over 2^{6n} } '
        lim = ' { 1 \\over 3 }'

        grp_tri = self.prepare_drawings(
            nn, vv_big, vv_small, (raw, lim),
            n_digits=4, base_scale_digits=0.3,
            cap_scale=0.65, cap_pos=DR
        )
        eq_tri = grp_tri[-1][0]
        
        src = (0, 1)
        dst = (1, 7)
        eq_tri_pos = [eq_tri[i:j] for i,j in zip(src,dst)]  # NB! with \ldots
        src = (0, 7,13,19)
        dst = (1,13,19,25)
        eq_tri_neg = [eq_tri[i:j] for i,j in zip(src,dst)]
        [eq.set_color(GREEN) for eq in eq_tri_pos]
        [eq.set_color(RED) for eq in eq_tri_neg]
        eq_tri[0:1].set_color(GRAY_A)
        #---------------------------------------------------------------------#
        
        #
        ## Базовое уравнение
        #
        self.play(FadeIn(eq_base, shift=DOWN))
        self.wait()
        
        #
        ## (+,-)
        #
        self.play(
            Create(grp_simple),
            FadeIn(txt_simple, shift=DOWN),
            )
        self.wait()
        
        #
        ## Добавляем пределы для каждой ветви
        #
        self.play(
            ReplacementTransform(eq_base[61:].copy(), eq_lim),
            FadeIn(eq_up, scale=2),
            FadeIn(eq_bot, scale=2),
            )
        self.wait()
        
        
        #
        ## Уточняющая надпись
        #
        ax = grp_simple[0]
        arr = Arrow(ax.c2p(-0.5, 0.1), grp_simple[3].get_left(), color=BLUE)
        txt_arr = Text(
            'почти все\nизменения\nпроисходят\nздесь',
            font='sans-serif',
            color=BLUE,
            line_spacing=0.6
        )
        txt_arr.scale(0.5).next_to(arr, LEFT, buff=SMALL_BUFF).shift(0.5*DOWN)
        self.play(Succession(
            Write(txt_arr),
            GrowArrow(arr),
        ))
        self.wait()
        
        #
        ## (+,-,-)
        #
        self.play(
            ReplacementTransform(grp_simple, grp_dbl),
            FadeOut(txt_simple, shift=DOWN),
            FadeIn(txt_dbl, shift=DOWN),
        )
        self.wait()
        
        #
        ## (+,-,-,-)
        #
        self.play(
            ReplacementTransform(grp_dbl[:-1], grp_tri[:-1]),
            ReplacementTransform(grp_dbl[-1][-1], grp_tri[-1][-1]),
            TransformMatchingTex(eq_dbl, eq_tri),
            FadeOut(txt_dbl, shift=DOWN),
            FadeIn(txt_tri, shift=DOWN),
        )
        self.wait()


#%% Тестовый рендер
if __name__ == '__main__':
    
    from helpers.render import dev_render
    
    dev_render(__file__, TwoFiniteDiffLimit)