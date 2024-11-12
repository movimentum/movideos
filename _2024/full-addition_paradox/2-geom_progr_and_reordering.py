#
# 2. Геометрическая прогрессия и перегруппировка слагаемых
#

from manim import *

from movi_ext import *

from auxfuncs import split2syms, questions_to_background
from number_bag import NumberBag


#%%
SceneExtension.video_orientation = 'landscape'


#%%
class ReorderingSum(MovingCameraScene, SceneExtension):
    def construct(self):
        #   0	1	2	3	    4	5	6	7	8	9	   10	11	12	13	14	15	   16	17	18	19	20	21	   22	23	24	25	26	27	   28	29	30	31	32	33	   34	35	36	37	38	39	   40	41	42	43	44	45	   46	47	48	49	50	51	   52	53	54	55	56	57	   58	59	60	61	62	63	   64	65	66	67	    68	69	 70	71	
        #   1	-	{	1	\over	2	}	+	{	1	\over	3 	} 	- 	{ 	1 	\over	4 	} 	+ 	{ 	1 	\over	5 	} 	- 	{ 	1 	\over	6 	} 	+ 	{ 	1 	\over	7 	} 	- 	{ 	1 	\over	8 	} 	+ 	{ 	1 	\over	9 	} 	- 	{ 	1 	\over	10	} 	+ 	{ 	1 	\over	11	} 	- 	{ 	1 	\over	12	} 	+ 	\ldots	= 	\ln	2 	
        eq1_raw = '1'
        for i in range(2, 2+11):
            operation = ' + ' if i % 2 else ' - '
            element = '{ 1 \over ' + f'{i}' + ' }'
            eq1_raw += operation
            eq1_raw += element
        eq1_raw += ' + \ldots = \ln 2'
        eq1_sym = split2syms(eq1_raw)
        eq1 = MathTex(*eq1_sym)
        self.camera.frame.set(width=1.1 * eq1.get_width())
        self.play(Write(eq1))
        self.wait()
        
        # Напоминание об исходной суме
        eq1_cpy = eq1.copy()
        self.play(eq1_cpy.animate.to_edge(UP).scale(0.5).set_color(BLUE).set_opacity(0.7))
        self.wait()
        
        
        
        #        0	1	2	3	4	    5	6	7	8	9	10	   11	12	13	     14	15	    16	17	18	   19	20	21	22	23	24	   25	26	27	28	29	30	   31	32	33	     34	35	    36	37	38	   39	40	41	42	43	44	   45	46	47	48	49	50	   51	52	53	     54	55	    56	57	58	   59	60	61	62	63	64	   65	66	67	68	69	70	   71	72	73	     74	75	    76	77	 78	79	
        #   \left(	1	-	{	1	\over	2	}	-	{	1 	\over	4 	} 	\right)	+ 	\left(	{ 	1 	\over	3 	} 	- 	{ 	1 	\over	6 	} 	- 	{ 	1 	\over	8 	} 	\right)	+ 	\left(	{ 	1 	\over	5 	} 	- 	{ 	1 	\over	10	} 	- 	{ 	1 	\over	12	} 	\right)	+ 	\left(	{ 	1 	\over	7 	} 	- 	{ 	1 	\over	14	} 	- 	{ 	1 	\over	16	} 	\right)	+ 	\ldots	= 	\ln	2 	
        eq2_raw = '\\left( 1 - { 1 \\over 2 } - { 1 \\over 4  }  \\right) + '
        eq2_raw += '\\left( { 1 \\over 3 } - { 1 \\over 6 } - { 1 \\over 8 } \\right) + '
        eq2_raw += '\\left( { 1 \\over 5 } - { 1 \\over 10 } - { 1 \\over 12 } \\right) + '
        eq2_raw += '\\left( { 1 \\over 7 } - { 1 \\over 14 } - { 1 \\over 16 } \\right) + '
        eq2_raw += '\\ldots = \\ln 2'
        eq2_sym = split2syms(eq2_raw)
        eq2 = MathTex(*eq2_sym)
        eq2.next_to(eq1, DOWN)
        
        #
        # Выписываем скобки
        #
        dst = (0, 14, 15, 16, 34, 35, 36, 54, 55, 56, 74)
        self.play(
            LaggedStart(
                *[FadeIn(eq2[i], scale=0.2) for i in dst],
                lag_ratio=0.1
            ),
            self.camera.frame.animate.set(width=1.1*eq2.get_width())
        )
        
        #
        # Заполняем скобку 1
        #
        ani = []
        # 1
        src = (0,)
        dst = (1,)
        ani.append(AnimationGroup(*[ReplacementTransform(eq1[i], eq2[j]) for i,j in zip(src, dst)]))
        # -1/2
        src = (1,2,3,4,5,6)
        dst = (2,3,4,5,6,7)
        ani.append(AnimationGroup(*[ReplacementTransform(eq1[i], eq2[j]) for i,j in zip(src, dst)]))
        # -1/4
        src = (13,14,15,16,17,18)
        dst = (8, 9, 10,11,12,13)
        ani.append(AnimationGroup(*[ReplacementTransform(eq1[i], eq2[j]) for i,j in zip(src, dst)]))
        self.play(AnimationGroup(*ani, lag_ratio=0.5))
        self.wait()
        
        
        #
        # Заполняем скобку 2
        #
        ani = []
        # 1/3
        src = list(range(8, 8+5))
        dst = list(range(17, 17+5))
        ani.append(AnimationGroup(*[ReplacementTransform(eq1[i], eq2[j]) for i,j in zip(src, dst)]))
        # -1/6
        src = list(range(25, 25+6))
        dst = list(range(22, 22+6))
        ani.append(AnimationGroup(*[ReplacementTransform(eq1[i], eq2[j]) for i,j in zip(src, dst)]))
        # -1/8
        src = list(range(37, 37+6))
        dst = list(range(28, 28+6))
        ani.append(AnimationGroup(*[ReplacementTransform(eq1[i], eq2[j]) for i,j in zip(src, dst)]))
        self.play(
            AnimationGroup(*ani, lag_ratio=0.5),
            FadeOut(eq1[7], scale=0.2)
        )
        self.wait()
        
        
        #
        # Заполняем скобку 3
        #
        ani = []
        # 1/5
        src = list(range(20, 20+5))
        dst = list(range(37, 37+5))
        ani.append(AnimationGroup(*[ReplacementTransform(eq1[i], eq2[j]) for i,j in zip(src, dst)]))
        # -1/10
        src = list(range(49, 49+6))
        dst = list(range(42, 42+6))
        ani.append(AnimationGroup(*[ReplacementTransform(eq1[i], eq2[j]) for i,j in zip(src, dst)]))
        # -1/12
        src = list(range(61, 61+6))
        dst = list(range(48, 48+6))
        ani.append(AnimationGroup(*[ReplacementTransform(eq1[i], eq2[j]) for i,j in zip(src, dst)]))
        self.play(
            AnimationGroup(*ani, lag_ratio=0.5),
            FadeOut(eq1[19], scale=0.2)
        )
        self.wait()
        
        
        #
        # Заполняем скобку 4
        #
        ani = []
        # 1/7
        src = list(range(32, 32+5))
        dst = list(range(57, 57+5))
        ani.append(AnimationGroup(*[ReplacementTransform(eq1[i], eq2[j]) for i,j in zip(src, dst)]))
        # -1/14, -1/16
        ani.append(ReplacementTransform(eq1[68].copy(), eq2[62:68]))
        ani.append(ReplacementTransform(eq1[68].copy(), eq2[68:74]))
        self.play(
            AnimationGroup(*ani, lag_ratio=0.5),
            FadeOut(eq1[31], scale=0.2)
        )
        self.wait()
        
        
        #
        # Завершаем преобразование равенств
        #
        self.play(ReplacementTransform(eq1[67:], eq2[75:]))
        self.wait()
        
        self.play(
            LaggedStart(
                FadeOut(eq1[43:49], target_position=eq2[76].get_center()),
                FadeOut(eq1[55:61], target_position=eq2[76].get_center()),
                lag_ratio=0.2
            ),
            Circumscribe(eq2[76], run_time=2),
        )
        self.play(eq2.animate.move_to(UP))
        self.wait()
        
        
        
        #
        ### ПРЕОБРАЗОВАНИЯ: шаг 2
        #
        
        # Складываем первые два члена в каждой скобке
        br21 = Brace(eq2[1:8])
        br22 = Brace(eq2[17:28])
        br23 = Brace(eq2[37:48])
        br24 = Brace(eq2[57:68])
        br_grp = VGroup(br21, br22, br23, br24)
        sub21 = MathTex('1 \over 2').next_to(br21, DOWN)
        sub22 = MathTex('1 \over 6').next_to(br22, DOWN)
        sub23 = MathTex('1 \over 10').next_to(br23, DOWN)
        sub24 = MathTex('1 \over 14').next_to(br24, DOWN)
        subs_grp = VGroup(sub21, sub22, sub23, sub24)
        #self.play(LaggedStart(*[DrawBorderThenFill(br) for br in br_grp]))
        #self.wait()

        
        #
        # Формируем результат
        #
        #        0	1	2	    3	4	5	6	7	8	    9	10	11	     12	13	    14	15	16	   17	18	19	20	21	22	   23	24	25	     26	27	    28	29	30	   31	32	33	34	35	36	   37	38	39	     40	41	    42	43	44	   45	46	47	48	49	50	   51	52	53	     54	55	    56	57	 58	59	
        #   \left(	{	1	\over	2	}	-	{	1	\over	4 	} 	\right)	+ 	\left(	{ 	1 	\over	6 	} 	- 	{ 	1 	\over	8 	} 	\right)	+ 	\left(	{ 	1 	\over	10	} 	- 	{ 	1 	\over	12	} 	\right)	+ 	\left(	{ 	1 	\over	14	} 	- 	{ 	1 	\over	16	} 	\right)	+ 	\ldots	= 	\ln	2 	
        eq3_raw = '\\left( { 1 \\over 2 } - { 1 \\over 4  }  \\right) + '
        eq3_raw += '\\left( { 1 \\over 6 } - { 1 \\over 8 } \\right) + '
        eq3_raw += '\\left( { 1 \\over 10 } - { 1 \\over 12 } \\right) + '
        eq3_raw += '\\left( { 1 \\over 14 } - { 1 \\over 16 } \\right) + '
        eq3_raw += '\\ldots = \\ln 2'
        eq3_sym = split2syms(eq3_raw)
        eq3 = MathTex(*eq3_sym)
        eq3.next_to(Group(eq2, br_grp, subs_grp), DOWN)
        
        #
        # Скобка 1
        #
        self.play(LaggedStart(
            DrawBorderThenFill(br21),
            Write(sub21),
            lag_ratio=0.5
        ))
        self.wait()
        
        src = (0,) + tuple(range(8,8+8))
        dst = (0,) + tuple(range(6,6+8))
        self.play(*[ReplacementTransform(eq2[i], eq3[j]) for i,j in zip(src,dst)])
        self.wait()
        self.play(
            TransformMatchingShapes(sub21, eq3[1:6]),
            FadeOut(eq2[1:8], br21, scale=0.5)
        )
        self.wait()
        
        #
        # Скобка 2
        #
        self.play(LaggedStart(
            DrawBorderThenFill(br22),
            Write(sub22),
            lag_ratio=0.5
        ))
        self.wait()
        
        src = (16,) + tuple(range(28,28+8))
        dst = (14,) + tuple(range(20,20+8))
        self.play(*[ReplacementTransform(eq2[i], eq3[j]) for i,j in zip(src,dst)])
        self.wait()
        self.play(
            TransformMatchingShapes(sub22, eq3[15:20]),
            FadeOut(eq2[17:28], br22, scale=0.5)
        )
        self.wait()
        
        #
        # Скобки 3 и 4
        #
        self.play(LaggedStart(
            DrawBorderThenFill(br23),
            Write(sub23),
            DrawBorderThenFill(br24),
            Write(sub24),
            lag_ratio=0.2
        ))
        self.wait(0.5)
        
        src = (36,) + tuple(range(48,48+8))
        dst = (28,) + tuple(range(34,34+8))
        ani = [ReplacementTransform(eq2[i], eq3[j]) for i,j in zip(src,dst)]
        src = (56,) + tuple(range(68,68+8))
        dst = (42,) + tuple(range(48,48+8))
        ani.extend([ReplacementTransform(eq2[i], eq3[j]) for i,j in zip(src,dst)])
        self.play(*ani)
        self.wait()
        self.play(
            TransformMatchingShapes(sub23, eq3[29:34]),
            FadeOut(eq2[37:48], br23, scale=0.5),
            TransformMatchingShapes(sub24, eq3[43:48]),
            FadeOut(eq2[57:68], br24, scale=0.5)
        )
        self.play(ReplacementTransform(eq2[76:], eq3[56:] ))
        self.wait()
        
        
        
        #
        ### Умножим обе части на 2
        #
        eq4_raw = '2 \\cdot \\left( { 1 \\over 2 } - { 1 \\over 4  }  \\right) + '
        eq4_raw += '2 \\cdot \\left( { 1 \\over 6 } - { 1 \\over 8 } \\right) + '
        eq4_raw += '2 \\cdot \\left( { 1 \\over 10 } - { 1 \\over 12 } \\right) + '
        eq4_raw += '2 \\cdot \\left( { 1 \\over 14 } - { 1 \\over 16 } \\right) + '
        eq4_raw += '\\ldots = 2 \\cdot \\ln 2'
        eq4_sym = split2syms(eq4_raw)
        eq4 = MathTex(*eq4_sym)
        eq4.next_to(eq3, UP)
        
        self.play(LaggedStart(
            ReplacementTransform(eq3[0 :0 +14], eq4[2 : 2+14]),
            ReplacementTransform(eq3[14:14+14], eq4[18:18+14]),
            ReplacementTransform(eq3[28:28+14], eq4[34:34+14]),
            ReplacementTransform(eq3[42:42+16], eq4[50:50+16]),
            ReplacementTransform(eq3[58:], eq4[68:]),
            lag_ratio=0.2
        ))
        src = (0,1,16,17,32,33,48,49,66,67)
        self.play(LaggedStart(
            *[FadeIn(eq4[i], scale=0.2) for i in src],
            lag_ratio=0.1
        ))
        self.wait()
        
        
        #
        ### Выполняем умножение
        #
        eq5_raw = '\\left( { 1 \\over 1 } - { 1 \\over 2  }  \\right) + '
        eq5_raw += '\\left( { 1 \\over 3 } - { 1 \\over 4 } \\right) + '
        eq5_raw += '\\left( { 1 \\over 5 } - { 1 \\over 6 } \\right) + '
        eq5_raw += '\\left( { 1 \\over 7 } - { 1 \\over 8 } \\right) + '
        eq5_raw += '\\ldots = 2 \\cdot \\ln 2'
        eq5_sym = split2syms(eq5_raw)
        eq5 = MathTex(*eq5_sym)
        eq5.next_to(eq4, UP)
        
        src = tuple(range(2,2+14)) + tuple(range(18,18+14)) + tuple(range(34,34+14)) + tuple(range(50,70))
        dst = tuple(range(len(src)))
        src_mults = set(range(src[-1])) - set(src)
        self.play(
            *[ReplacementTransform(eq4[i], eq5[j]) for i,j in zip(src,dst)],
            LaggedStart(
                *[FadeOut(eq4[i], target_position=eq4[i].get_center() + DOWN) for i in src_mults],
                lag_ratio=0.1
            )
        )
        self.wait()
        
        
        #
        ### Убираем скобки
        #
        #   0	1	    2	3	4	5	6	7	    8	9	10	11	12	13	   14	15	16	17	18	19	   20	21	22	23	24	25	   26	27	28	29	30	31	   32	33	34	35	36	37	   38	39	40	41	42	43	   44	45	46	47	    48	49	50	   51	 52	53	
        #   {	1	\over	1	}	-	{	1	\over	2	} 	+ 	{ 	1 	\over	3 	} 	- 	{ 	1 	\over	4 	} 	+ 	{ 	1 	\over	5 	} 	- 	{ 	1 	\over	6 	} 	+ 	{ 	1 	\over	7 	} 	- 	{ 	1 	\over	8 	} 	+ 	\ldots	= 	2 	\cdot	\ln	2 	
        eq6_raw = '{ 1 \\over 1 } - { 1 \\over 2  } + '
        eq6_raw += '{ 1 \\over 3 } - { 1 \\over 4 } + '
        eq6_raw += '{ 1 \\over 5 } - { 1 \\over 6 } + '
        eq6_raw += '{ 1 \\over 7 } - { 1 \\over 8 } + '
        eq6_raw += '\\ldots = 2 \\cdot \\ln 2'
        eq6_sym = split2syms(eq6_raw)
        eq6 = MathTex(*eq6_sym)
        eq6.move_to(eq5)
        
        self.play(TransformMatchingTex(eq5, eq6))
        self.wait()
        
        
        #
        ### Приходим к выводу
        #
        eq7_raw = '\\ln 2 = 2 \\cdot \\ln 2'
        eq7_sym = split2syms(eq7_raw)
        eq7 = MathTex(*eq7_sym)
        eq7.move_to(eq6)
        
        self.play(eq1_cpy.animate.scale(2).set_opacity(1))
        self.wait()
        
        src = tuple(range(49))
        self.play(LaggedStart(
            *[FadeOut(eq6[i], target_position=eq7[:2].get_center()) for i in src],
            GrowFromCenter(eq7[:2]),
            ReplacementTransform(eq6[-5:], eq7[-5:]),
            self.camera.frame.animate.set(width=3*eq7.get_width()),
            lag_ratio=0.02
        ))
        self.wait()
        
        crs = VGroup(*[Cross(mob, color=RED, stroke_width=2) for mob in (eq7[:2], eq7[-2:])])
        eq8_raw = '1 = 2'
        eq8_sym = split2syms(eq8_raw)
        eq8 = MathTex(*eq8_sym)
        eq8.next_to(eq7, DOWN)
        
        self.play(Create(crs))
        self.play(
            ReplacementTransform(eq7[2:-2], eq8),
            FadeOut(eq7[:2], scale=3, target_position=2*UP),
            FadeOut(eq7[-2:], scale=3, target_position=2*UP),
            FadeOut(crs, scale=3, target_position=2*UP)
        )
        self.wait()
        
        
        eq9_raw = '0 = 1'
        eq9_sym = split2syms(eq9_raw)
        eq9 = MathTex(*eq9_sym)
        eq9.move_to(ORIGIN).scale(2)
        self.play(*[ReplacementTransform(eq8[i],eq9[i]) for i in range(3)])
        self.wait()


#%%
class GeometricProgression(MovingCameraScene, SceneExtension):
    def construct(self):
        self.n = 1
        self.eq = self.make_geom_prog_equation(1)
        self.play(Write(self.eq))
        
        self.seg = NumberLine(
                       x_range=[0,1,1],
                       length=12,
                       include_numbers=True,
            )
        self.seg.shift(2 * UP)
        self.play(Create(self.seg))
        self.wait()
        
        ps = self.seg.n2p(0)
        grp_all = VGroup()
        for n in range(1, 6):
            color = YELLOW if n % 2 else RED
            pe = self.seg.n2p(1 - 1/2**n)
            grp = self.prepare_portion_line(ps, pe, n, color)
            grp_all.add(grp)
            ps = pe
            
            self.play(
                GrowFromCenter(grp),
                self.iterate_geom_prog_equation()
            )
            self.wait()
        
        p_rem = self.seg.n2p(1 - 1/64)
        pe = self.seg.n2p(1)
        arr = Arrow(
            self.eq[-5].get_top(),
            p_rem,
            color=BLUE,
            stroke_width=3,
            buff=SMALL_BUFF
        )
        line = Line(ps, pe, color=BLUE, stroke_width=10)
        
        dots = self.eq[-5]
        self.play(Wiggle(dots))
        self.play(Succession(
            dots.animate.scale(1.2).set_color(BLUE),
            GrowArrow(arr),
            FocusOn(p_rem)
        ))
        self.play(FadeIn(line, target_position=line.get_center() - DOWN))
        self.wait()
        
        #
        ### Геометрическая прогрессия
        #
        eq_pwr = self.make_geom_prog_equation(6, elem_style='power')
        eq_pwr.next_to(self.eq, DOWN)
        self.play(
            *[ReplacementTransform(self.eq[i], eq_pwr[i]) for i in range(len(self.eq))],
            FadeOut(arr, scale=0.2)
        )
        self.wait()
        
        br = Brace(eq_pwr[:-4], UP)
        raw = '{ b_{1} \\over 1 - q } = { 1/2 \\over 1 - 1/2 } = 1'
        sym = split2syms(raw)
        eq_txt = Text('Геометрическая прогрессия: ', font_size=24, color=BLUE)
        eq_geom = MathTex(*sym).scale(0.7).set_color(BLUE)
        eq_geom.next_to(eq_txt, RIGHT)
        eq_geom_grp = VGroup(eq_txt, eq_geom).next_to(br, UP)
        self.play(LaggedStart(
            DrawBorderThenFill(br),
            Write(eq_geom_grp),
            lag_ratio=0.5
        ))
        self.wait()
        
        
        #
        ## А теперь каждый чётный не прибавляем, а вычитаем
        #
        eq_pwr_pm = self.make_geom_prog_equation(6, elem_style='power', alter_sign=True, summ='1/3')
        eq_pwr_pm.move_to(eq_pwr)
        [eq_pwr_pm[i].set_color(YELLOW) for i in (5,17)]  # отмечаем знаки минуса цветом
        br_pm = Brace(eq_pwr_pm[:-4], UP)
        self.play(
            LaggedStart(
                *[ReplacementTransform(eq_pwr[i], eq_pwr_pm[i]) for i in range(len(eq_pwr) - 1)],
                FadeOut(eq_pwr[-1], scale=2),
                lag_ratio=0.01
            ),
            ReplacementTransform(br, br_pm)
        )
        self.wait()
        
        raw = '{ b_{1} \\over 1 - q } = { 1/2 \\over 1 + 1/2 } = { 1 \\over 3 }'
        sym = split2syms(raw)
        eq_geom_pm = MathTex(*sym).scale(0.7).set_color(BLUE)
        eq_geom_pm.next_to(eq_txt, RIGHT)
        eq_geom_pm[-9].set_color(YELLOW)  # отмечаем знаки минуса цветом
        eq_geom_pm[-5:].set_color(YELLOW)  #
        
        self.play(
            *[ReplacementTransform(eq_geom[i], eq_geom_pm[i]) for i in range(len(eq_geom)-1)],
            ReplacementTransform(eq_geom[-1], eq_geom_pm[-4]),
            *[FadeIn(eq_geom_pm[i]) for i in (-1,-2,-3,-5)],
        )
        self.play(FadeIn(eq_pwr_pm[-1].set_color(YELLOW)))
        self.wait()
        
        
        # TODO: сделать это перед сменой знаков (выше)
        #
        ### Перегруппируем отрезки
        #
        for grp in grp_all:
            grp.generate_target()
        
        grp_all[3].target.align_to(self.seg.n2p(0), LEFT)  # 1/16 -
        grp_all[1].target.align_to(grp_all[3].target.get_right(), LEFT)  # 1/4 -
        grp_all[0].target.align_to(grp_all[1].target.get_right(), LEFT)  # 1/2 +
        grp_all[2].target.align_to(grp_all[0].target.get_right(), LEFT)  # 1/8 +
        grp_all[4].target.align_to(grp_all[2].target.get_right(), LEFT)  # 1/32 +

        self.play(*[MoveToTarget(grp, path_arc=45 * DEGREES) for grp in grp_all])
        self.wait()
        
        self.play(Circumscribe(Group(grp_all, self.seg)))
        self.wait()
        
        grp_plus = Group(*[grp_all[i] for i in (0,2,4)])
        grp_minus = Group(*[grp_all[i] for i in (1,3)])
        plus = MathTex('+', stroke_width=5).scale(2).set_color(YELLOW).next_to(grp_plus, DOWN)
        minus = MathTex('-', stroke_width=5).scale(2).set_color(RED).next_to(grp_minus, DOWN)
        self.play(
            Circumscribe(grp_plus),
            GrowFromCenter(plus)
        )
        self.play(
            Circumscribe(grp_minus, color=RED),
            GrowFromCenter(minus)
        )
        self.wait()
        self.play(LaggedStart(
            *[FadeOut(sign, target_position=sign.get_center() + UP) for sign in (plus, minus)],
            lag_ratio=0.5
        ))
        self.wait()
        
        
        #
        ### Переходим к обобщению геометрической прогрессии
        #

        # Убираем отрезок и передвигаем обозначение
        eq_geom_grp = VGroup(eq_txt, eq_geom_pm)
        self.play(
            *[FadeOut(v, shift=UP) for v in (grp_all, line, self.seg)],
            eq_geom_grp.animate.to_edge(UP),
            Unwrite(br_pm)
        )
        self.wait()
        
        # Меняем уравнение суммы на общий вид
        raw = '{ b_{1} \\over 1 - q } = { 1 \\over 1 - (-x) } '
        sym = split2syms(raw)
        eq_geom = MathTex(*sym).scale(0.7).set_color(BLUE)
        eq_geom.next_to(eq_txt, RIGHT)
        eq_geom_grp = VGroup(eq_txt, eq_geom)
        self.play(
            *[ReplacementTransform(eq_geom_pm[i], eq_geom[i]) for i in range(len(eq_geom))],
            FadeOut(eq_geom_pm[len(eq_geom):], shift=RIGHT),
            eq_pwr_pm.animate.set_color(GRAY).set_opacity(0.5)
        )
        self.wait()
        
        raw = '{ b_{1} \\over 1 - q } = { 1 \\over 1 + x } '
        sym = split2syms(raw)
        eq_txt2 = eq_txt.copy()
        eq_geom2 = MathTex(*sym).scale(0.7).set_color(BLUE)
        eq_geom2.next_to(eq_txt2, RIGHT)
        eq_geom_grp2 = VGroup(eq_txt2, eq_geom2)
        eq_geom_grp2.move_to(ORIGIN).to_edge(UP)
        self.play(
            ReplacementTransform(eq_txt, eq_txt2),
            ReplacementTransform(eq_geom[:-2], eq_geom2[:-2]),
            TransformMatchingShapes(eq_geom[-2:],eq_geom2[-2:])
        )
        self.wait()
        
        # Преобразуем уравнение
        #   0	1	2	3	 4	5	6	 7	8	9	10	11	12	13	14	15	    16	17	18	   19	20	21	22	
        #   1	-	x	+	x^	2	-	x^	3	-	x^	4 	+ 	x^	5 	+ 	\ldots	= 	{1	\over	1 	+ 	x}	
        raw = '1 - x + x^ 2 - x^ 3 + x^ 4 - x^ 5 + \ldots = {1 \\over 1 + x}'
        sym = split2syms(raw)
        eq_geom_gen = MathTex(*sym)
        self.play(TransformMatchingShapes(eq_pwr_pm, eq_geom_gen))
        self.wait()
        
        #          0	     1	2	3	4	5	 6	7	8	 9	10	11	12	13	14	15	16	17	    18	     19	20	21	      22	23	   24	25	26	27	28	
        #   \int^1_0	\left(	1	-	x	+	x^	2	-	x^	3 	+ 	x^	4 	- 	x^	5 	+ 	\ldots	\right)	dx	= 	\int^1_0	{1	\over	1 	+ 	x}	dx
        raw = '\\int^1_0 \\left( 1 - x + x^ 2 - x^ 3 + x^ 4 - x^ 5 + \\ldots \\right) dx = \int^1_0 {1 \\over 1 + x} dx'
        sym = split2syms(raw)
        eq_geom_gen_int = MathTex(*sym)
        #self.play(TransformMatchingTex(eq_geom_gen, eq_geom_gen_int))  # тоже неплохо, но хочется разделить действия
        self.play(
            ReplacementTransform(eq_geom_gen[:17], eq_geom_gen_int[2:2+17]),
            ReplacementTransform(eq_geom_gen[17], eq_geom_gen_int[21]),
            ReplacementTransform(eq_geom_gen[18:], eq_geom_gen_int[23:-1])
        )
        self.wait()
        self.play(*[FadeIn(eq_geom_gen_int[i], shift=UP) for i in (0,1,19,20,22,-1)])
        self.wait()
        
        # Результат интегрирования
        #   0	1	 2	    3	 4	5	 6	    7	 8	9	10	   11	12	13	14	   15	16	17	18	   19	20	21	    22	23	 24	25	
        #   1	-	{1	\over	2}	+	{1	\over	3}	-	{1	\over	4}	+ 	{1	\over	5}	+ 	{1	\over	6}	+ 	\ldots	= 	\ln	2 	
        raw = '1 - {1 \\over 2} + {1 \\over 3} - {1 \\over 4} + {1 \\over 5} - {1 \\over 6} + \ldots = \\ln 2'
        sym = split2syms(raw)
        eq_int_res = MathTex(*sym).next_to(eq_geom_gen_int, 2*DOWN)
        #self.play(TransformMatchingTex(eq_geom_gen_int, eq_int_res))
        #self.wait()
        
        
        # Выполняем почленное интегрирование
        #eq_base = eq_geom_gen_int.copy()
        def get_interm_anims(eq, src, dst, dst2):
            ani1 = [ReplacementTransform(eq_geom_gen_int[i].copy(), eq[j]) for i,j in zip(src, dst)]
            ns = dst[-1] + 1
            ani2 = [FadeIn(eq[ns:], shift=UP)]
            src_eq = range(ns, len(eq))
            ani3 = [ReplacementTransform(eq[i], eq_int_res[j]) for i,j in zip(src_eq, dst2)]
            ani3.append(FadeOut(eq[:ns], scale=0.5))
            return [ani1, ani2, ani3]
        
        def play_interm_anims(anims, run_time=1, wait_time=0.5):
            for ani in anims:
                self.play(*ani,
                          run_time=run_time)
                self.wait(wait_time)
                
        raws = (
            '\\int^1_0 1 dx = 1',                   # 1
            '\\int^1_0 x dx = {1 \\over 2}',     # x
            '\\int^1_0 x^ 2 dx = {1 \\over 3}',  # x^2
            '\\int^1_0 x^ 3 dx = {1 \\over 4}',  # x^3
            '\\int^1_0 x^ 4 dx = {1 \\over 5}',  # x^4
            '\\int^1_0 x^ 5 dx = {1 \\over 6}',  # x^5
            )
        
        subs = ((2,), (4,), (6,7), (9,10), (12,13), (15,16), )
        starts2 = (0,2,6,10,14,18)
        
        sign_poss = (3,5,8,11,14,17)
        run_tms = (1, 1, 0.5, 0.4, 0.3, 0.2)
        wait_tms = (1, 1, 0, 0, 0, 0)
        
        for raw, sub, st, spos, r_t, w_t in zip(raws, subs, starts2, sign_poss, run_tms, wait_tms):
            sym = split2syms(raw)
            eq = MathTex(*sym).scale(0.7).set_color(YELLOW)
            src = (0,) + sub + (20,21)
            dst = list(range(len(src)))
            dst2 = list(range(st, st + len(eq) - len(src)))
            eq.next_to(eq_geom_gen_int[src[1]], UP).shift(0.5*UP)
            anims = get_interm_anims(eq, src, dst, dst2)
            anims.append([
                ReplacementTransform(
                    eq_geom_gen_int[spos].copy(),
                    eq_int_res[dst2[-1]+1])
                ])
            play_interm_anims(anims, run_time=r_t, wait_time=w_t)
        
        
        # "..."
        self.play(
            ReplacementTransform(eq_geom_gen_int[18].copy(), eq_int_res[22]),
            ReplacementTransform(eq_geom_gen_int[21].copy(), eq_int_res[23])
        )
        self.wait()
        
        eq_sub = MathTex('\\ln', '(x+1)', '\\right|', '^1', '_0')
        eq_sub.next_to(eq_geom_gen_int[21], RIGHT).shift(UP).set_color(YELLOW)
        eq_sub2 = MathTex('\\ln', '2', '-', '\\ln', '1')
        eq_sub2.next_to(eq_geom_gen_int[21], RIGHT).shift(2*UP).set_color(YELLOW)
        self.play(Succession(
            Indicate(eq_geom_gen_int[22:]),
            Write(eq_sub)
        ))
        self.wait()
        self.play(TransformMatchingShapes(eq_sub, eq_sub2))
        self.wait()
        self.play(
            ReplacementTransform(eq_sub2[:2], eq_int_res[-2:]),
            FadeOut(eq_sub2[2:], scale=0.25)
        )
        self.wait()
        
        
        # Завершаем сцену
        self.play(
            FadeOut(eq_geom_gen_int, scale=2),
            FadeOut(eq_geom_grp2, shift=UP),
            self.camera.frame.animate.move_to(eq_int_res).set(width=1.5*eq_int_res.get_width()),
            eq_int_res.animate.set_color(GREEN),
            run_time=2
        )
        self.play(Circumscribe(eq_int_res))
        self.wait()
        

    def prepare_portion_line(self, p1, p2, n, color, sign=''):
        ''' Рисуем линию от p1 до p2 с меткой 1/2^n над ней + тик в p2 '''
        tick = self.seg.ticks[0].copy().move_to(p2)
        line = Line(p1, p2, color=color, stroke_width=4)
        
        if not sign:
            label = MathTex('1 \\over ' + str(2**n)).next_to(line, UP).set_color(color)
        else:
            label = MathTex(sign + '{ 1 \\over ' + str(2**n) + ' }').next_to(line, UP).set_color(color)
        label.next_to(line, UP).set_color(color)
        size  = (p2-p1)[0]
        if size < 1:
            label.scale(size**0.5)
        return VGroup(tick, line, label)
        
    
    def iterate_geom_prog_equation(self, nmax=6) -> Animation:
        self.n += 1
        eq_new = self.make_geom_prog_equation(self.n, nmax=nmax)
        ani = []
        if self.n == 2:  # первое преобразование
            ani.extend([ReplacementTransform(self.eq[i], eq_new[i]) for i in (-1,-2)])
            ani.append(ReplacementTransform(self.eq[:-2], eq_new[:-2]))
        else:
            ne = len(eq_new) - 5 - 3
            ani.extend([ReplacementTransform(self.eq[i], eq_new[i]) for i in range(ne)])
            ani.extend([ReplacementTransform(self.eq[i], eq_new[i]) for i in (-1,-2)])
            ani.append(FadeIn(eq_new[ne:-2]))
        self.eq = eq_new
        return AnimationGroup(*ani)
    

    def make_geom_prog_equation(self, n, nmax=6, alter_sign=False, summ='1',
                                elem_style='simple', return_raw=False):
        """ Создаём уравнение 1 = 1, в котором левая часть поделена на n частей
            геометрической прогрессии 1/2, 1/4, 1/8, 1/16, 1/32...
        """
        assert n > 0, "Количество членов слева должно быть не менее 1"
        
        if n == 1:
            return MathTex('1', '=', '1')
        
        raw = ''
        for i in range(1, min(n, nmax)):
            operation = ' + ' if (not alter_sign or i % 2) else ' - '
            if elem_style == 'simple':
                element = '{ 1 \over ' + f'{2**i}' + ' }'
            elif elem_style == 'power':
                element = '{ 1 \over ' + '2^' + f'{{{i}}}' + ' }'
            raw += operation if i > 1 else ''
            raw += element
        # дополнительные скобки {} для поддержания нужного количества элементарных элементов
        raw += operation + element + ' = ' + summ if n < nmax else ' + { { \ldots } } = ' + summ
        
        sym = split2syms(raw)
        eq = MathTex(*sym)
        return eq if not return_raw else (eq, raw)


#%%
class PreliminaryConclusion(GeometricProgression, SceneExtension):
    eq_scale = 0.6
    txt_scale = 0.5

    def construct(self):
        cap = Text('Подытожим...', color=GRAY_A).to_edge(UP)
        bl1 = Text('1. Нашли сумму')
        #      0      1           2           3           4           5      6    7   8    9
        raw = '1 -{1\\over2} +{1\\over3} -{1\\over4} +{1\\over5} -{1\\over6} + \ldots = \\ln2'
        sym = split2syms(raw)
        eq1 = MathTex(*sym)
        
        bl2 = Text('2. Переставили в ней слагаемые')
        #      0      1           2           3           4           5      6    7   8    9      10
        raw = '1 -{1\\over2} -{1\\over4} +{1\\over3} -{1\\over6} -{1\\over8} + \ldots = {\\ln2 \\over2}'
        sym = split2syms(raw)
        eq2 = MathTex(*sym)
        
        bl3 = Text('3. Значение суммы поменялось')
        
        bl4 = Text('4. Сделали парадоксальный вывод')
        eq4 = MathTex('0 = 1')
        
        bl_grp = VGroup(bl1, bl2, bl3, bl4).scale(self.txt_scale)
        bl_grp.arrange(DOWN, aligned_edge=LEFT, buff=LARGE_BUFF).move_to(ORIGIN).to_edge(LEFT)
        
        eq1.scale(self.eq_scale).next_to(bl1, RIGHT).align_to(bl_grp.get_right() + LARGE_BUFF, LEFT)
        eq2.scale(self.eq_scale).next_to(Group(bl2, bl3), RIGHT).align_to(bl_grp.get_right() + LARGE_BUFF, LEFT)
        eq4.scale(self.eq_scale*1.5).next_to(bl4, RIGHT).align_to(bl_grp.get_right() + LARGE_BUFF, LEFT)
        
        grp_all = VGroup(bl_grp, eq1, eq2, eq4).move_to(ORIGIN)
        
        
        self.add(cap)
                
        # 1. Нашли сумму
        self.play(LaggedStart(
            Write(bl1),
            FadeIn(eq1, shift=LEFT),
            lag_ratio=0.5
        ))
        self.wait()

        
        # 2. Переставили в ней слагаемые
        self.play(Write(bl2))
        src = tuple(range(8+1))   + (7,)
        dst = (0,1,3,2,7,4,6,7,8) + (5,)
        self.play(LaggedStart(
            *[ReplacementTransform(eq1[i].copy(), eq2[j]) for i,j in zip(src, dst)],
            lag_ratio=0.2
        ))
        self.wait()
        
        
        # 3. Значение суммы поменялось
        self.play(Write(bl3))
        self.play(
            ReplacementTransform(eq1[9].copy(), eq2[9]),
            FadeIn(eq2[10], shift=LEFT)
        )
        self.wait()
        
        
        # 4. Пришли к парадоксальному выводу
        self.play(LaggedStart(
            Write(bl4),
            FadeIn(eq4, shift=LEFT, rate_func=rate_functions.ease_in_out_back),
            lag_ratio = 0.5
        ))
        self.wait()
        
        
        # Окрашиваем верные и неверные результаты
        grp_true = VGroup(bl1, bl2, bl3, eq1, eq2)
        grp_false = VGroup(bl4, eq4)
        self.play(Succession(
            AnimationGroup(
                grp_true.animate.set_color(GREEN),
                Circumscribe(grp_true, color=GREEN)
            ),
            AnimationGroup(
                grp_false.animate.set_color(RED),
                Circumscribe(grp_false, color=RED)
            ),
        ))
        self.wait()
        
        
        # Завершение вопросами
        q_marks = questions_to_background(75, self.camera.frame, opacity=0.2, scale=3, color=GRAY)
        self.play(LaggedStart(
            *[GrowFromCenter(q_mark) for q_mark in q_marks],
            lag_ratio=0.02)
        )
        self.wait()
        
        ani_grp = AnimationGroup(
            *[FadeOut(q_mark, scale=1.5) for q_mark in q_marks],
            lag_ratio=0.05,
            run_time=2
        )
        self.play(
            FadeOut(grp_all),
            FadeOut(cap, shift=UP),
            ani_grp,
            run_time=2
        )
        self.wait()


#%%
class GeometricProgressionRevisited(GeometricProgression, SceneExtension):
    def construct(self):
        self.n = 1
        #   0	1	    2	3	4	5	6	7	    8	9	10	11	12	13	   14	15	16	17	18	19	   20	21	22	23	24	25	   26	27	28	29	30	31	   32	33	34	35	36	37	   38	 39	40	41	42	43	    44	45	46	47	48	
        #   {	1	\over	2	}	+	{	1	\over	4	} 	+ 	{ 	1 	\over	8 	} 	+ 	{ 	1 	\over	16	} 	+ 	{ 	1 	\over	32	} 	+ 	{ 	1 	\over	64	} 	+ 	{ 	1 	\over	128	} 	+ 	{ 	{ 	\ldots	} 	} 	= 	1 	
        eq_pos, raw_pos = self.make_geom_prog_equation(8, nmax=8, alter_sign=False, summ='1', return_raw=True)
        #   0	1	    2	3	4	5	6	7	    8	9	10	11	12	13	   14	15	16	17	18	19	   20	21	22	23	24	25	   26	27	28	29	30	31	   32	33	34	35	36	37	   38	 39	40	41	42	43	    44	45	46	47	       48	
        #   {	1	\over	2	}	-	{	1	\over	4	} 	+ 	{ 	1 	\over	8 	} 	- 	{ 	1 	\over	16	} 	+ 	{ 	1 	\over	32	} 	- 	{ 	1 	\over	64	} 	+ 	{ 	1 	\over	128	} 	+ 	{ 	{ 	\ldots	} 	} 	= 	{1\over3}	
        eq_alt, raw_alt = self.make_geom_prog_equation(8, nmax=8, alter_sign=True, summ='{1\\over3}', return_raw=True)
        src = (0, 11, 23, 35)
        dst = (5, 17, 29, 41)
        eq_pos_pos = [eq_pos[i:j] for i,j in zip(src,dst)]
        eq_alt_pos = [eq_alt[i:j] for i,j in zip(src,dst)]
        src = (5, 17, 29)
        dst = (11, 23, 35)
        eq_pos_neg = [eq_pos[i:j] for i,j in zip(src,dst)]
        eq_alt_neg = [eq_alt[i:j] for i,j in zip(src,dst)]
        [eq.set_color(GRAY_A) for eq in eq_pos_pos]
        [eq.set_color(BLUE) for eq in eq_pos_neg]
        [eq.set_color(GREEN) for eq in eq_alt_pos]
        [eq.set_color(RED) for eq in eq_alt_neg]

        
        self.seg = NumberLine(
            x_range=[0,1,1],
            length=12,
            include_numbers=True,
        )
        self.seg.shift(2 * UP)
        
        ps = self.seg.n2p(0)
        grp_pos = VGroup()
        grp_alt = VGroup()
        for n in range(1, 10):
            color_common = GRAY_A if n % 2 else BLUE
            color_signed = GREEN if n % 2 else RED
            sign = '' if n % 2 else '-'
            pe = self.seg.n2p(1 - 1/2**n)
            pos = self.prepare_portion_line(ps, pe, n, color_common)
            alt = self.prepare_portion_line(ps, pe, n, color_signed, sign=sign)
            grp_pos.add(pos)
            grp_alt.add(alt)
            ps = pe


        #
        ## Вводим единичный отрезок и уравнение, делим отрезок
        #
        self.play(
            LaggedStart(
                Create(self.seg),
                *[GrowFromCenter(grp) for grp in grp_pos],
                lag_ratio = 0.1,
            ),
            Write(eq_pos)
        )
        self.wait()
        
        
        #
        ## Делаем знакочередующуюся сумму
        #
        self.play(
            *[ReplacementTransform(x,y) for x,y in zip(eq_pos, eq_alt)],
            TransformMatchingShapes(grp_pos, grp_alt)
        )
        self.wait()
        
        
        #
        ## Анимация под текст "Если снова перетряхнуть ряд и поменять порядок, сумма тоже поменяется!"
        #
        q_mark = MathTex('?', color=YELLOW).scale(4).next_to(eq_alt, RIGHT, buff=MED_LARGE_BUFF)
        self.play(Succession(
            LaggedStart(
                *[Wiggle(eq, scale_value=1.2, run_time=2) for eq in (eq_alt_pos + eq_alt_neg)],
                lag_ratio=0.1
            ),
            AnimationGroup(
                Indicate(eq_alt[47:], scale_factor=1.5),
                FadeIn(q_mark, scale=2, rate_func=there_and_back),
                run_time=5,
            )
        ))
        self.wait()
        
        
        #
        ### Перегруппируем отрезки
        #
        seg_new = NumberLine(
            x_range=[-1/3,2/3],
            length=12,
            include_numbers=True,
        ).shift(2*DOWN)
        seg_new.add_labels({
            -1/3: r'$-{1 \over 3}$',
            2/3:  r'${2 \over 3}$'
        })
        seg_new.shift(self.seg.n2p(0) - seg_new.n2p(-1/3))
        t1 = seg_new.get_tick(-1/3)
        t2 = seg_new.get_tick(2/3)
        seg_new.add(t1,t2)
        

        [sub.generate_target() for sub in grp_alt]
        
        ps = seg_new.n2p(0)
        dpos = ps - self.seg.n2p(0)
        for grp in grp_alt[::2]:
            grp.target.shift(dpos)
            line = grp.target[1]
            dpos_local = ps - line.get_left()
            grp.target.shift(dpos_local)
            ps = line.get_right()
        
        pe = seg_new.n2p(0)
        for grp in grp_alt[1::2]:
            grp.target.shift(dpos)
            line = grp.target[1]
            dpos_local = pe - line.get_right()
            grp.target.shift(dpos_local)
            pe = line.get_left()
            
        
        self.play(
            LaggedStart(
                *[MoveToTarget(grp, path_arc=45 * DEGREES) for grp in grp_alt],
                FadeOut(self.seg, shift=UP),
                FadeIn(seg_new, shift=UP, run_time=2),
                lag_ratio=0.1,
                ),
            eq_alt.animate.scale(0.5).set_opacity(0.5).to_edge(DOWN),
        )
        self.bring_to_back(seg_new)
        self.wait()
        
        
        #
        ## Ограниченные мешки
        #
        br_pos = Brace(grp_alt[::2], color=GREEN).shift(0.5*DOWN)
        br_neg = Brace(grp_alt[1::2], color=RED).shift(0.5*DOWN)
        
        bag_pos = NumberBag(GREEN, GREEN_A, GREEN_E, 5, 5, None).scale(0.3)
        bag_neg = NumberBag(RED, RED_A, RED_E, 5, 5, None).scale(0.3)
        
        eq_pos = MathTex('{b_1 \\over 1 - q} = {1/2 \\over 1 - 1/4} = {2 \\over 3}', color=GRAY_A)
        eq_neg = MathTex('{b_1 \\over 1 - q} = {1/4 \\over 1 - 1/4} = {1 \\over 3}', color=GRAY_A)
        eq_pos.scale(0.5).next_to(bag_pos)
        eq_neg.scale(0.5).next_to(bag_neg)
        bag_pos_grp = VGroup(bag_pos, eq_pos).next_to(br_pos, DOWN)
        bag_neg_grp = VGroup(bag_neg, eq_neg).next_to(br_neg, DOWN)
        
        self.play(
            DrawBorderThenFill(br_pos),
            DrawBorderThenFill(br_neg),
            FadeIn(bag_pos_grp, shift=UP),
            FadeIn(bag_neg_grp, shift=UP),
        )
        self.wait()
        
        eq_inf = MathTex('\infty', '-', '\infty', color=GRAY_A)
        eq_inf[0].set_color(GREEN)
        eq_inf[-1].set_color(RED)
        eq_inf.scale(2)
        eq_inf.shift(DOWN)
        
        eq_res = MathTex('{2\\over3}', '-', '{1\\over 3}', '=', '{1\\over3}', '\equiv', '{b_1\\over 1-q}', color=GRAY_A)
        eq_res[0].set_color(GREEN)
        eq_res[2].set_color(RED)
        eq_res.scale(0.8)
        eq_res.shift(2*DOWN)
        
        cr = Cross(eq_inf)
        self.play(FadeIn(eq_inf, scale=3, rate_func=rate_functions.ease_in_circ))
        self.wait()
        
        self.play(
            Succession(
                FadeIn(cr),
                LaggedStart(
                    *[ReplacementTransform(eq_inf[i], eq_res[i]) for i in range(3)],
                    lag_ratio=0.2
                ),
            ),
            FadeOut(cr),
        )
        self.wait()
        self.play(LaggedStart(*[FadeIn(x, shift=DOWN) for x in eq_res[3:]]))
        self.wait()
             
        txt = Text('неопределённости больше нет!', color=BLUE)
        txt.scale(0.5)
        txt.next_to(eq_res, UP)
        grp = VGroup(txt, eq_res, eq_alt)
        grp_others = VGroup(br_pos, br_neg, bag_pos_grp, bag_neg_grp, seg_new, grp_alt)
        self.play(
            Write(txt),
            eq_alt.animate.set_opacity(1),
            grp_alt.animate.set_opacity(0.2),
            self.camera.frame.animate.move_to(grp).set(width=1.5*grp.get_width())
        )
        self.wait()
        

#%% Тестовый рендер
if __name__ == '__main__':
    
    from helpers.render import dev_render
    
    dev_render(__file__, GeometricProgressionRevisited)