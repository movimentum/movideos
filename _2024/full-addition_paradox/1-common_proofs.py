#
# 1. Анимации "доказательств" 0 = 1
#

import os
import re

from manim import *

from movi_ext import *

from auxfuncs import split2syms


#%%
SceneExtension.video_orientation = 'landscape'


#%%
def get_svg_path(svg_sub_path):
    return os.path.join(repo_root, f'custom/svg/{svg_sub_path}.svg')


#%% Обычное доказательство путём деления на 0
class SimpleAlgebraic(Scene, SceneExtension):
    def construct(self):
        #   0	1	2	3   4
        #   a	=	b   +   c
        eq1_raw = 'a = b + c'
        eq1_sym = split2syms(eq1_raw)
        eq1 = MathTex(*eq1_sym)
        eq1_cpy = eq1.copy().scale(1.5).set_opacity(0.7).set_color(YELLOW).move_to(2 * UP)
        
        #   0	1	2	3	4	
        #   (	a	-	b	)	
        eq1_mult_raw = '( a - b )'
        eq1_mult_sym = split2syms(eq1_mult_raw)
        eq1_mult = MathTex(*eq1_mult_sym)
        eq1_mult.scale(0.7).next_to(eq1, UP)
        
        #   0	    1	2	3	4	5	6	7	8	9	10	11	12	   13	14	15	16	17	18	
        #   a	\cdot	(	a	-	b	)	=	(	b	+ 	c 	) 	\cdot	( 	a 	- 	b 	) 	
        eq2_raw = 'a \cdot ( a - b ) = ( b + c ) \cdot ( a - b )'
        eq2_sym = split2syms(eq2_raw)
        eq2 = MathTex(*eq2_sym)
        
        #   0	 1	2	3	4	5	6	7	8	9	10	11	12	13	14	15	16	
        #   a	^2	-	a	b	=	a	b	+	a	c 	- 	b 	^2	- 	b 	c  	
        eq3_raw = 'a ^2 - a b  =  a b + a c - b ^2 - b c'
        eq3_sym = split2syms(eq3_raw)
        eq3 = MathTex(*eq3_sym)
        eq3.next_to(eq2, DOWN)
        
        #   0	 1	2	3	4	5	6	7	8	9	10	11	12	13	14	15	16	
        #   a	^2	-	a	b	-	a	c	=	a	b 	- 	b 	^2	- 	b 	c 	
        eq3_reord_raw = 'a ^2 - a b - a c  =  a b - b ^2 - b c'
        eq3_reord_sym = split2syms(eq3_reord_raw)
        eq3_reord = MathTex(*eq3_reord_sym)
        eq3_reord.next_to(eq3, UP)
        
        #   0	    1	2	3	4	5	6	7	8	9	10	   11	12	13	14	15	16	17	18	
        #   a	\cdot	(	a	-	b	-	c	)	=	b 	\cdot	( 	a 	- 	b 	- 	c 	) 		
        eq4_raw = 'a \cdot ( a - b - c )  =  b \cdot ( a - b - c )'
        eq4_sym = split2syms(eq4_raw)
        eq4 = MathTex(*eq4_sym)
        eq4.next_to(eq3_reord, UP)
        
        #   0	1	2	
        #   a	=	b	
        eq5_raw = 'a = b'
        eq5_sym = split2syms(eq5_raw)
        eq5 = MathTex(*eq5_sym)
        
        #   0	1	2	
        #   0	=	1	
        eq6_raw = '0 = 1'
        eq6_sym = split2syms(eq6_raw)
        eq6 = MathTex(*eq6_sym)
        eq6.scale(2)
        
        
        self.play(Write(eq1))
        self.wait()
        
        self.play(FadeIn(eq1_mult))
        self.wait(0.2)
        
        self.play(
            ReplacementTransform(eq1[0], eq2[0]),
            ReplacementTransform(eq1[1], eq2[7]),
            ReplacementTransform(eq1[2], eq2[9]),
            ReplacementTransform(eq1[3], eq2[10]),
            ReplacementTransform(eq1[4], eq2[11]),
        )
        
        self.play(LaggedStart(
            FadeIn(eq2[1], target_position=DOWN),
            FadeIn(eq2[13], target_position=DOWN),
            ReplacementTransform(eq1_mult, eq2[2:7]),
            TransformFromCopy(eq1_mult, eq2[14:19]),
            FadeIn(eq2[8], scale=0.5),
            FadeIn(eq2[12], scale=0.5),
            lag_ratio=0.1
        ))
        self.wait()
        
        
        
        self.play(LaggedStart(
            ReplacementTransform(eq2[0], eq3[0]),
            FadeOut(*[eq2[i] for i in (1,2,6)]),
            ReplacementTransform(eq2[3], eq3[1]),
            ReplacementTransform(eq2[4], eq3[2]),
            FadeIn(eq3[3], target_position=eq2[0]),
            ReplacementTransform(eq2[5], eq3[4]),
            ReplacementTransform(eq2[7], eq3[5]),
        ))
        
        self.play(
            LaggedStart(
                FadeIn(eq3[6], target_position=eq2[15]),
                FadeIn(eq3[7], target_position=eq2[9]),
                ReplacementTransform(eq2[10], eq3[8]),
                ReplacementTransform(eq2[15], eq3[9]),
                FadeIn(eq3[10], target_position=eq2[11]),
                FadeIn(eq3[11], target_position=eq2[16]),
                ReplacementTransform(eq2[9], eq3[12]),
                TransformFromCopy(eq2[17], eq3[13]),
                ReplacementTransform(eq2[16], eq3[14]),
                ReplacementTransform(eq2[17], eq3[15]),
                ReplacementTransform(eq2[11], eq3[16]),
                lag_ratio=0.1
            ),
            FadeOut(*[eq2[i] for i in (8, 12, 13, 14, 18)])
        )
        self.wait(0.5)
        
        self.play(LaggedStart(
            ReplacementTransform(eq3[:5], eq3_reord[:5]),
            ReplacementTransform(eq3[5], eq3_reord[8]),
            ReplacementTransform(eq3[6:8], eq3_reord[9:11]),
            ReplacementTransform(eq3[8], eq3_reord[5]),
            ReplacementTransform(eq3[9:11], eq3_reord[6:8]),
            ReplacementTransform(eq3[11:], eq3_reord[11:]),
            lag_ratio=0.2
        ))
        self.wait()

        
        src = (0,1,2,4,5,7,8,9, 10,11,12,14,16)
        dst = (0,3,4,5,6,7,9,13,10,14,15,16,17)
        self.play(
            *[FadeOut(eq3_reord[i], target_position=eq4[0],  path_arc=180 * DEGREES) for i in (3,6)],
            *[FadeOut(eq3_reord[i], target_position=eq4[10], path_arc=-180 * DEGREES) for i in (13,15)],
            *[ReplacementTransform(eq3_reord[i], eq4[j]) for i,j in zip(src, dst)],
            *[FadeIn(eq4[i], scale=0.5) for i in (2,8,12,18)],
            *[FadeIn(eq4[i], target_position=UP) for i in (1,11)]
        )
        self.wait()
        

        cr1 = Cross(eq4[2:9], stroke_width=3)
        cr2 = Cross(eq4[12:], stroke_width=3)
        
        self.play(LaggedStart(
            Create(cr1),
            Create(cr2),
            lag_ratio=0.3
        ))
        self.wait(0.2)
        
        
        txt = Text('Ошибка — деление на ноль', font_size=28, color=YELLOW, opacity=0.5).next_to(eq1_cpy, UP)
        
        self.play(
            FadeIn(eq1_cpy, scale=2),
            FadeIn(txt), 
            run_time=3
        )
        self.play(FadeOut(eq1_cpy, scale=0.5))
        
        
        src = (0, 9, 10)
        dst = (0, 1, 2)
        rem = set(range(len(eq4))) - set(src)
        rem = tuple(rem)
        self.play(LaggedStart(
            AnimationGroup(
                FadeOut(txt, scale=0.5),
                FadeOut(cr1, scale=0.5),
                *[FadeOut(eq4[i], scale=0.2) for i in rem[:7]],
                FadeOut(cr2, scale=0.5),
                *[FadeOut(eq4[i], scale=0.2) for i in rem[7:]],
            ),
            *[ReplacementTransform(eq4[i], eq5[j]) for i,j in zip(src, dst)],
            lag_ratio=0.5
        ))
        self.wait()
        
        self.play(ReplacementTransform(eq5, eq6))
        self.wait()


#%% Геометрическое доказательство путём визуально ошибочного построения
class Geometric(MovingCameraScene, SceneExtension):
    def construct(self):
        pA = ORIGIN + 3 * LEFT + 3 * DOWN
        pC = pA + 6 * RIGHT
        pB = pA + 4 * RIGHT + 6 * UP
        tri_ABC = Polygon(pA, pB, pC, stroke_width=2)
        self.play(Create(tri_ABC))
        

        #
        # Срединный перпендикуляр
        #
        pK = (pA + pC) / 2
        pO = pK.copy() + 1 * UP
        sOK = Line(pO, pK, stroke_width=2)
        
        sAK = LineWithTicks(pA, pK)
        sAK.add_ticks_at_mid(2)
        sCK = LineWithTicks(pC, pK)
        sCK.add_ticks_at_mid(2)
        aOKC = RightAngle(sOK, sCK, 0.3, quadrant=(-1,-1), stroke_width=2)
        pO_dot = Dot(pO, color=BLUE)
        self.play(LaggedStart(
                    FadeIn(pO_dot, scale=3),
                    Create(sAK),
                    Create(sCK),
                    Create(aOKC),
                    Create(sOK),
                    lag_ratio=0.2
                ))
        

        #
        # Биссектрисса 
        #
        sAB = LineWithTicks(pA, pB)
        sBC = LineWithTicks(pB, pC)
        sBO = LineWithTicks(pB, pO, stroke_width=2)
        aABO = Angle(sAB, sBO, 0.8, quadrant=(-1,+1))
        aCBO = Angle(sBC, sBO, 0.6, other_angle=True)
        self.play(LaggedStart(
                    Create(aABO),
                    Create(aCBO),
                    Create(sBO),
                    lag_ratio=0.2
                  ))
        self.wait()

        #
        # Дополнительные перпендикуляры из точки O
        #
        pN = sBC.get_projection(pO)
        pM = sAB.get_projection(pO)
        sMO = LineWithTicks(pM, pO, stroke_width=2)
        sNO = LineWithTicks(pN, pO, stroke_width=2)
        aOMB = RightAngle(sMO, sAB, 0.2, quadrant=(1,1), stroke_width=2)
        aONB = RightAngle(sNO, sBC, 0.2, quadrant=(1,-1), stroke_width=2)
        self.play(LaggedStart(
                    Create(sMO),
                    Create(sNO),
                    Create(aOMB),
                    Create(aONB),
                    lag_ratio=0.2
                ))

        
        #
        # Отмечаем "равные" треугольники
        #
        tri_MBO = Polygon(pO, pM, pB, color=RED, fill_opacity=0.5)
        tri_NBO = Polygon(pO, pN, pB, color=RED, fill_opacity=0.5)
        self.play(Indicate(aABO), Indicate(aCBO),
                  Indicate(aOMB), Indicate(aONB),
                  Indicate(sBO),
                  run_time=3)
        self.play(FadeIn(tri_MBO),
                  FadeIn(tri_NBO),
                  run_time=3)
        self.play(FadeOut(tri_MBO),
                  FadeOut(tri_NBO))
        self.wait()
        
        # Следствие равенства треугольников
        sMO.add_ticks_at_mid(1)
        sNO.add_ticks_at_mid(1)
        self.play(Create(*sMO.submobjects),
                  Create(*sNO.submobjects)
                  )
        sMB = LineWithTicks(pM, pB, stroke_width=4, color=GOLD)
        sNB = LineWithTicks(pN, pB, stroke_width=4, color=GOLD)
        sMB.add_ticks_at_mid(3)
        sNB.add_ticks_at_mid(3)
        self.play(Create(sMB), Create(sNB))
        self.wait()
        
        
        #
        # Вторая пара треугольников
        #
        sAO = LineWithTicks(pA, pO, stroke_width=2)
        sCO = LineWithTicks(pC, pO, stroke_width=2)
        sAO.add_ticks_at_mid(4)
        sCO.add_ticks_at_mid(4)
        tri_AOK = Polygon(pA, pO, pK, color=RED, fill_opacity=0.5)
        tri_COK = Polygon(pC, pO, pK, color=RED, fill_opacity=0.5)
        self.play(Indicate(sAK), Indicate(sCK),
                  Indicate(sOK), Indicate(aOKC)
                  )
        self.play(FadeIn(tri_AOK), FadeIn(tri_COK))
        self.play(FadeOut(tri_AOK), FadeOut(tri_COK),
                  Create(sAO), Create(sCO))
        self.wait()
        

        #
        # Заключительная пара треугольников
        #
        tri_ONC = Polygon(pO, pN, pC, color=RED, fill_opacity=0.5)
        tri_OMA = Polygon(pO, pM, pA, color=RED, fill_opacity=0.5)
        sNC = LineWithTicks(pN, pC, stroke_width=4, color=BLUE)
        sMA = LineWithTicks(pM, pA, stroke_width=4, color=BLUE)
        sNC.add_ticks_at_mid(5)
        sMA.add_ticks_at_mid(5)
        self.play(Indicate(sMO), Indicate(sNO),
                  Indicate(sAO), Indicate(sCO),
                  Indicate(aOMB), Indicate(aONB),
                  )
        self.play(FadeIn(tri_ONC), FadeIn(tri_OMA))
        self.play(FadeOut(tri_ONC), FadeOut(tri_OMA),
                  Create(sNC), Create(sMA))
        self.wait()
        
        
        #
        # Вывод
        #
        grp = VGroup(sAO, sCO, sMO, sNO, sBO, sOK, sAK, sCK, aOMB, aONB,
                     aABO, aCBO, aOKC, pO_dot)
        self.play(FadeOut(grp, scale=0.5))
        self.wait()
        
        a1 = sAB.get_angle()
        direction_AB = np.array((-np.sin(a1), np.cos(a1), 0))
        a2 = sBC.get_angle()
        direction_BC = np.array((-np.sin(a2), np.cos(a2), 0))
        brAB = BraceLabel(Group(sMA, sMB), '2', brace_direction=direction_AB)
        brBC = BraceLabel(Group(sNC, sNB), '1', brace_direction=direction_BC)
        self.play(FadeIn(brAB, scale=0.2), FadeIn(brBC, scale=0.2))
        self.wait()
        
        grp = VGroup(tri_ABC, sMA, sMB, sNC, sNB)
        txt1 = MathTex('1')
        txtEq = MathTex('=').next_to(txt1, RIGHT)
        txt0 = MathTex('0').next_to(txtEq, RIGHT)
        grp_txt = VGroup(txt1, txtEq, txt0)
        grp_txt.move_to(ORIGIN)
        self.play(FadeOut(grp, scale=0.2),
                  ReplacementTransform(brAB, txt1),
                  ReplacementTransform(brBC, txt0),
                  FadeIn(txtEq, target_position=UP),
                  self.camera.frame.animate.set(width=3*grp_txt.get_width())
                  )
        self.wait()


#%% Доказательство с помощью неоднозначности комплексного корня
class ComplexMultivalue(MovingCameraScene, SceneExtension):
    def construct(self):
        #   0	1	     2	 3	4	
        #   i	=	\sqrt{	-1	}
        eq1_raw = 'i = \sqrt{ -1 }'
        eq1_sym = split2syms(eq1_raw)
        eq1 = MathTex(*eq1_sym)
        self.add(eq1)
        
        #   0	1	     2	 3	    4	5	6	
        #   i	=	\sqrt{	-1	\over	1	}	
        eq2_raw = 'i = \sqrt{ -1 \over 1 }'
        eq2_sym = split2syms(eq2_raw)
        eq2 = MathTex(*eq2_sym)
        
        self.play(
            ReplacementTransform(eq1[:4], eq2[:4]),
            ReplacementTransform(eq1[4], eq2[6]),
            FadeIn(eq2[4:6], scale=0.5)
        )
        self.wait()
        
        c3 = eq2[3].get_center()        
        c5 = eq2[5].get_center()
        self.play(
            eq2[3].animate.move_to(c5),
            eq2[5].animate.move_to(c3)
        )
        self.wait()
        
        #   0	1 	     2	3	4	    5	     6	 7	8	
        #   i	={	 \sqrt{	1	}	\over	\sqrt{	-1	}}
        eq3_raw = 'i ={ \sqrt{ 1 } \over \sqrt{ -1 }}'
        eq3_sym = split2syms(eq3_raw)
        eq3 = MathTex(*eq3_sym)
        
        src = (0,1,2,3,4,5,6)
        dst = (0,1,2,7,5,3,4)
        self.play(
            TransformFromCopy(eq2[2], eq3[6]),
            *[ReplacementTransform(eq2[i], eq3[j]) for i,j in zip(src,dst)],
        )
        self.wait()
        
        #   0	 1	2	    3	4	5	
        #   i	={	1	\over	i	}	
        eq4_raw = 'i ={ 1 \over i }'
        eq4_sym = split2syms(eq4_raw)
        eq4 = MathTex(*eq4_sym)
        self.play(
            ReplacementTransform(eq3[3], eq4[2]),
            ReplacementTransform(eq3[7], eq4[4]),
            ReplacementTransform(eq3[5], eq4[3]),
            ReplacementTransform(eq3[:2], eq4[:2]),
            FadeOut(eq3[2], scale=2),
            FadeOut(eq3[6], scale=0.5),
        )
        self.wait()
        
        #   0	 1	2	3	4	
        #   i	^2	=	1	}	
        eq5_raw = 'i ^2 = 1 }'
        eq5_sym = split2syms(eq5_raw)
        eq5 = MathTex(*eq5_sym)
        self.play(
            ReplacementTransform(eq4[0], eq5[0]),
            ReplacementTransform(eq4[1], eq5[2]),
            ReplacementTransform(eq4[2], eq5[3]),
            ReplacementTransform(eq4[4], eq5[1]),
            FadeOut(eq4[3])
        )
        self.wait()
        
        #   0	1	2	3	
        #   -	1	=	1	
        eq6_raw = '- 1 = 1'
        eq6_sym = split2syms(eq6_raw)
        eq6 = MathTex(*eq6_sym)
        self.play(
            ReplacementTransform(eq5[0], eq6[1]),
            ReplacementTransform(eq5[1], eq6[0]),
            ReplacementTransform(eq5[2:], eq6[2:]),
        )
        self.wait()
        
        #   0	1	2	
        #   1	=	0
        eq7_raw = '1 = 0'
        eq7_sym = split2syms(eq7_raw)
        eq7 = MathTex(*eq7_sym)
        self.play(
            FadeOut(eq6[0], scale=0.5),
            ReplacementTransform(eq6[1:3], eq7[0:2]),
            ReplacementTransform(eq6[3], eq7[2]),
            self.camera.frame.animate.set(width=3*eq7.get_width())
        )
        self.wait()


#%% Доказательство программиста
class Programmistic(Scene, SceneExtension):
    def construct(self):
        txt0 = Text('void main() {').shift(3*UP)
        txt1 = Text('int t = 1;').next_to(txt0, DOWN).align_to(txt0, LEFT).shift(LARGE_BUFF * RIGHT)
        txt2 = Text('t = t + 1;').next_to(txt1, DOWN).align_to(txt0, LEFT).shift(LARGE_BUFF * RIGHT)
        txt3 = Text('}').next_to(txt2, DOWN).align_to(txt0, LEFT)
        
        txt4 = Text('0 = 1', font_size=60).shift(DOWN).set_color(YELLOW)
        arr = Arrow(txt2.get_bottom(), txt4.get_top(), color=YELLOW)
        self.play(LaggedStart(
            Write(txt0),
            Write(txt1),
            Write(txt2),
            Write(txt3),
            lag_ratio=0.5)
        )
        self.wait()
        
        self.play(GrowArrow(arr))
        self.play(Write(txt4))
        self.play(Circumscribe(txt4), Circumscribe(txt2))
        self.wait()


class Programmistic2(Scene, SceneExtension):
    def construct(self):
        code_fn = r'asserts\zero_is_one.cpp'
        
        rendered_code = Code(file_name=code_fn, tab_width=4, background="window",
                            language="cpp", font="Monospace")
        rendered_code.shift(UP)
        
        txt4 = Text('0 = 1', font_size=60).next_to(rendered_code, DOWN).shift(DOWN).set_color(YELLOW)
        arr = Arrow(rendered_code.get_bottom(), txt4.get_top(), color=GRAY_B)
        self.play(Write(rendered_code))
        self.wait()
        
        self.play(GrowArrow(arr))
        self.play(Write(txt4))
        self.play(Circumscribe(txt4))
        self.wait()


#%% Жизненно-административное доказательство
class Administrative(MovingCameraScene, SceneExtension):
    fn_lamppost = get_svg_path('objects/lamppost')
    fn_check = get_svg_path('simple/checkmark')
    
    def construct(self):
        svg_plan = SVGMobject(self.fn_lamppost, stroke_color=BLUE)
        for mob in svg_plan.submobjects:
            if not mob.stroke_width:
                mob.stroke_width = 1
        
        check_plan = SVGMobject(self.fn_check, stroke_color=GREEN, stroke_width=1, fill_color=GREEN_A)
        check_plan.scale(0.2)
        check_fact = check_plan.copy()
        
        svg_plan.scale(2)
        svg_fact = svg_plan.copy()
        txt_plan = Text('смета: 1 шт.', font='sans-serif', color=BLUE).scale(0.5).next_to(svg_plan, DOWN)
        txt_fact = Text('факт: 0 шт.', font='sans-serif', color=RED).scale(0.5).next_to(svg_fact, DOWN)
        
        txt2_plan = Text('УТВЕРЖДЕНО', weight=BOLD, font='sans-serif', color=GREEN).scale(0.5)
        txt2_fact = Text('РАБОТЫ ПРИНЯТЫ', weight=BOLD, font='sans-serif', color=GREEN).scale(0.5)
        
        grp_check_plan = VGroup(check_plan, txt2_plan)
        grp_check_fact = VGroup(check_fact, txt2_fact)
        grp_check_plan.arrange(aligned_edge=DOWN,buff=SMALL_BUFF).rotate(45*DEGREES).move_to(svg_plan)
        grp_check_fact.arrange(aligned_edge=DOWN,buff=SMALL_BUFF).rotate(45*DEGREES).move_to(svg_fact)
        
        grp = VGroup(
            VGroup(svg_plan, txt_plan, grp_check_plan),
            VGroup(svg_fact, txt_fact, grp_check_fact),
        ).arrange(buff=MED_LARGE_BUFF, aligned_edge=UP)
        
        #
        ## По плану
        #
        run_tms = [2, 2] + [0.5] * (len(svg_plan) - 2)
        self.play(
            Write(txt_plan),
            LaggedStart(
                *[Create(svg, run_time=dt) for svg,dt in zip(svg_plan, run_tms)],
                lag_ratio=0.1,
            )
        )
        self.wait()
        
        #
        ## По смете
        #
        self.play(
            LaggedStart(
                *[Create(svg, run_time=dt) for svg,dt in zip(svg_fact, run_tms)],
                lag_ratio=0.2,
            )
        )
        self.play(LaggedStart(
            FadeOut(svg_fact.copy(), scale=3, run_time=3),
            svg_fact.animate(run_time=2).set_stroke(BLUE, opacity=0.2),
            Write(txt_fact),
            lag_ratio=0.1
        ))
        
        #
        ## Всё утверждено
        #
        self.play(Succession(
            FadeIn(grp_check_plan, scale=3, run_time=1, rate_func=rate_functions.ease_in_expo),
            FadeIn(grp_check_fact, scale=3, run_time=1, rate_func=rate_functions.ease_in_expo),
        ))

        #
        ## Результат
        #
        res_eq = MathTex('1', '=', '0', color=GRAY_A)        
        res_eq[0].set_color(BLUE)
        res_eq[-1].set_color(RED)
        self.play(
            Write(res_eq),
            self.camera.frame.animate.move_to(res_eq).set(width=3*res_eq.get_width()),
            grp.animate.set_opacity(0.2),
        )
        self.wait()


#%% Тестовый рендер
if __name__ == '__main__':
    
    from helpers.render import dev_render
    
    dev_render(__file__, Administrative)