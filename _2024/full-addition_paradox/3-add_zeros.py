#
# 3. Добавляем нули к равенству 1 = 1
#

from manim import *

from movi_ext import *

from auxfuncs import split2syms, get_person_svg_path


#%%
SceneExtension.video_orientation = 'landscape'


#%% Прибавляем нули к единице
class AddZeros(MovingCameraScene, SceneExtension):
    def construct(self):
        self.cnt = 0
        self.txt_new = MathTex('1', '=', '1')
        self.txt_old = None
        self.add_more(1)
        self.add_more(1)
        self.add_more(2, run_time=0.5)
        self.add_more(2, run_time=0.2)
        self.add_more(1, to_add='\\ldots', run_time=0.5)
        # Финальный вид
        #   0	1	2	3	4	5	6	7	8	9	10	11	12	13	    14  15	16
        #   1	+	0	+	0	+	0	+	0	+	0 	+ 	0 	+   \ldots	= 	1 	
        
        
        #   0	1	2	3	4	5	6	7	8	9	10	11	12	13	14	15	16	17	18	19	20	21	22	23	24	25	26	27	28	29	30	31	32	33	34	35	36	37	38	    39	40 
        #   1	+	(	1	-	1	)	+	(	1	- 	1 	) 	+ 	( 	1 	- 	1 	) 	+ 	( 	1 	- 	1 	) 	+ 	( 	1 	- 	1 	) 	+ 	( 	1 	- 	1 	)   +	\ldots	= 	1 	
        raw = '1' + ' + ( 1 - 1 ) ' * 6 + ' + \\ldots = 1'
        sym = split2syms(raw)
        self.txt_old = self.txt_new
        self.txt_old.generate_target()
        self.txt_old.target.move_to(ORIGIN)
        self.txt_new = MathTex(*sym).next_to(self.txt_old.target, UP)
        
        self.play(
            MoveToTarget(self.txt_old),
            self.camera.frame.animate.set(width=1.2 * self.txt_new.get_width())
        )
        
        # Представим нули разностями
        ani = [ReplacementTransform(self.txt_old[i], self.txt_new[i]) for i in (0,1)]
        src = range(2, 13)
        dst = (2,7,8,13,14,19,20,25,26,31,32)
        for i,j in zip(src,dst):
            target = self.txt_new[j] if i % 2 else self.txt_new[j:j+5]
            ani.append(ReplacementTransform(self.txt_old[i], target))
        src = (13,14,15,16)
        dst = (37,38,39,40)
        ani.extend([ReplacementTransform(self.txt_old[i], self.txt_new[j]) for i,j in zip(src,dst)])
        
        self.play(LaggedStart(*ani, lag_ratio=0.25))
        self.wait()
        
        uni = CreatureUnity().shift(2 * DOWN)
        self.play(Succession(
            FadeIn(uni),
            uni.look_around()
        ))
        
        # Переставим скобки
        #   0	1	2	3	4	5	6	7	8	9	10	11	12	13	14	15	16	17	18	19	20	21	22	23	24	25	26	27	28	29	30	31	32	33	34	35	    36	37	38	
        #   (	1	-	1	)	+	(	1	-	1	) 	+ 	( 	1 	- 	1 	) 	+ 	( 	1 	- 	1 	) 	+ 	( 	1 	- 	1 	) 	+ 	( 	1 	- 	1 	) 	+ 	\ldots	= 	1
        raw = '( 1 - 1 ) + ' * 6 + ' \\ldots = 1'
        sym = split2syms(raw)
        self.txt_old = self.txt_new
        self.txt_new = MathTex(*sym).next_to(self.txt_old, DOWN)
        
        for i in range(0, 31, 6):
            sliding_unity = self.txt_old[i+3]
            i_unit = 0 if i==0 else i + 1 - 4
            src = (i+2,i_unit,i+4,i+5,i+6,i+1)
            dst = range(i, i+6)
            ani = [ReplacementTransform(self.txt_old[i], self.txt_new[j]) for i,j in zip(src,dst)]
            #ani.append(ReplacementTransform(self.txt_old[i+1],self.txt_new[]))
            self.play(LaggedStart(
                *ani, lag_ratio=0.2),
                sliding_unity.animate.scale(1.5).set_color(YELLOW),
                uni.look_at(sliding_unity),
            )
            self.wait()


        # Подбираем остатки
        self.play(Succession(
            ReplacementTransform(self.txt_old[38:], self.txt_new[36:]),
            FadeOut(self.txt_old[37], target_position=self.txt_new[36], scale=0.5),
            FadeOut(self.txt_old[33], target_position=self.txt_new[36], scale=0.5),
        ))
        self.play(uni.look_around())
        
        
        #
        ## Верни единицу!
        #
        bub1 = uni.get_talk_bubble('куда?!', scale_bubble=0.5, shift_bubble=0.5*DOWN)
        bub2 = uni.get_talk_bubble('верни\nединицу!', scale_bubble=0.5, shift_bubble=0.5*DOWN)
        self.play(FadeIn(bub1, scale=0))
        self.wait()
        self.play(ReplacementTransform(bub1, bub2))
        self.wait()
        
        
        #   0	1	2	3	4	5	6	7	8	9	10	11	    12	13	14	
        #   0	+	0	+	0	+	0	+	0	+	0 	+ 	\ldots	= 	1 	
        raw = '0 + ' * 6 + ' \\ldots = 1'
        sym = split2syms(raw)
        self.txt_old = self.txt_new
        self.txt_new = MathTex(*sym).next_to(self.txt_old, UP).shift(UP)

        ani = []        
        src = (0,5,6,11,12,17,18,23,24,29,30,35)  # old
        dst = range(12)  # new
        for i,j in zip(src,dst):
            base = self.txt_old[i] if j % 2 else self.txt_old[i:i+5]
            ani.append(ReplacementTransform(base.copy(), self.txt_new[j]))
        ani.append(ReplacementTransform(self.txt_old[36:].copy(), self.txt_new[12:]))
        
        self.play(
            LaggedStart(*ani, lag_ratio=0.2),
            FadeOut(bub2),
            uni.look_at(self.txt_new[12])
        )
        self.wait()
        
        
        #
        # Единичка подсказывает, что она осталась где-то в хвосте...
        #
        uni.generate_target()
        uni.target.scale(0.3).next_to(self.txt_new[12], UP, buff=SMALL_BUFF).shift(0.1*LEFT)
        uni.target.body.set_color(RED)
        uni.target.eyes.set_color(GOLD)
        uni_cpy = uni.copy()
        uni_cpy.target.next_to(self.txt_old[36], UP, buff=SMALL_BUFF).shift(0.1*LEFT)
        bub3 = uni.target.get_talk_bubble('я здесь, в самом хвосте...', width=12, scale_bubble=0.3, bg_rect=False, stroke_width=2)
        self.play(Succession(
            AnimationGroup(
                MoveToTarget(uni_cpy),
                MoveToTarget(uni),
                lag_ratio=0.2
            ),
            Create(bub3)
        ))
        self.play(
            uni.look_at(self.txt_new[-1]),
            uni_cpy.look_at(self.txt_old[-1])
            )
        self.wait()
        
        txt = Text('Но где этот «хвост»?', font='sans-serif', color=YELLOW)
        txt.next_to(self.txt_old, DOWN).shift(DOWN)
        self.play(FadeIn(txt, scale=1.5), run_time=2)
        self.wait()
        
        #
        # n=5, 11
        #
        color_n = YELLOW
        color_np2 = GREEN
        def play_uni_and_minus_uni(pos, n, is_pos_equal_pos_p1=False, scale=0.6, run_time=2, wait=1):
            if not is_pos_equal_pos_p1:
                pos_p1 = pos + 2
                shift_pos = UP
                shift_mov = DOWN
            else:
                pos_p1 = pos
                shift_pos = DOWN
                shift_mov = UP
            pos_look = (pos + pos_p1) // 2
                
            txt_n = MathTex(f'n={n}', color=color_n).scale(scale).next_to(self.txt_old[pos], shift_pos)
            txt_np1 = MathTex(f'n={n+1}', color=color_np2).scale(scale).next_to(self.txt_old[pos_p1], shift_pos)
            self.play(Succession(
                AnimationGroup(
                    FadeIn(txt_n, shift=shift_mov, rate_func=there_and_back),
                    Indicate(self.txt_old[pos], color=color_n, scale_factor=1.5),
                    uni_cpy.look_at(self.txt_old[pos]),
                    run_time=run_time,
                ),
                AnimationGroup(
                    FadeIn(txt_np1, shift=shift_mov, rate_func=there_and_back),
                    Indicate(self.txt_old[pos_p1], color=color_np2, scale_factor=1.5),
                    run_time=run_time,
                ),
            ))
            self.wait(wait)

        play_uni_and_minus_uni(13, 5)
        play_uni_and_minus_uni(31, 11)
        play_uni_and_minus_uni(36, 100, is_pos_equal_pos_p1=True, run_time=1.5, wait=0.5)
        play_uni_and_minus_uni(36, 1000, is_pos_equal_pos_p1=True, scale=0.5, run_time=1, wait=0.2)
        play_uni_and_minus_uni(36, 100000, is_pos_equal_pos_p1=True, scale=0.4, run_time=1, wait=0.2)
        
        txt_upd = Text('До «хвоста» не добраться...',
                       font='sans-serif', color=RED)
        txt_upd.move_to(txt, DOWN).shift(0.5*DOWN)
        self.play(
            FadeOut(txt, shift=UP),
            Write(txt_upd),
            run_time=2
        )
        self.wait()
        
    
    def add_more(self, num, to_add='0', run_time=1, move_camera=False):
        for i in range (num):
            self.cnt += 1
            self.txt_old = self.txt_new
            if len(self.txt_old) == 1:
                self.txt_new = MathTex('1', '=', '1')
            else:
                self.txt_new = MathTex(*[sub.get_tex_string() for sub in self.txt_old[:-2]], '+', to_add, '=', '1')
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


#%% Определяем сумму числового ряда
class SeriesSumDefinition(MovingCameraScene, SceneExtension):
    def construct(self):
        ax = Axes(
            x_range=[0, 20, 5],
            y_range=[0, 1.3],
            x_length=10,
            y_length=5.5,
        )
        ax.add_coordinates()
        labels = ax.get_axis_labels(
            Text('количество n\nслагаемых').scale(0.3),
            Text("сумма \nn слагаемых").scale(0.3)
        )
        labels[0].shift(DOWN)
        labels[1].shift(LEFT)
        alim = 0.5
        lim_line = ax.plot(lambda x: alim, stroke_width=2, color=BLUE)
        lim_label = MathTex('S_{lim} = {1 \\over 2}', color=BLUE).scale(0.7).next_to(ax.c2p(0,alim), LEFT)

        
        series_conv = np.cumsum([3/4 / (-2)**(i-1) for i in np.arange(1,1+20)])
        xx = np.arange(1, 1+20)
        line_conv = ax.plot_line_graph(
            x_values=xx,
            y_values=series_conv,
            line_color=GREEN_E,
            vertex_dot_radius=0.05,
            vertex_dot_style=dict(stroke_width=2, stroke_color=GREEN_A, fill_color=GREEN_C),
            stroke_width=2,
        )
        eq_conv = MathTex('{3 \\over 4} - {3 \\over 8} + {3 \\over 16} - \\ldots + { 3 \\over 4\cdot (-2)^{n-1} } = ', '\sum^{', 'n}', '_{i=1}{ 3 \\over 4\cdot (-2)^{i-1} }')
        eq_conv.scale(0.5).set_color(GREEN).to_corner(UR)
        
        lines_conv_to_lim_line = VGroup(*[
            Line(
                ax.c2p(x,y),
                ax.c2p(x,alim),
                stroke_width=1,
                color=GREEN_A
            ) for x,y in zip(xx, series_conv)
        ])


        series_div = np.cumsum([(-1)**i for i in range(20)])
        line_div = ax.plot_line_graph(
            x_values=xx,
            y_values=series_div,
            line_color=RED_E,
            vertex_dot_radius=0.05,
            vertex_dot_style=dict(stroke_width=2, stroke_color=RED_A, fill_color=RED_C),
            stroke_width=2,
        )
        eq_div = MathTex('1 - 1 + 1 - \\ldots + (-1)^n = ', '\sum^{', 'n}', '_{i=0} (-1)^i')
        eq_div.scale(0.5).set_color(RED_E).to_corner(UR).shift(DOWN)
        
        lines_div_to_lim_line = VGroup(*[
            Line(
                ax.c2p(x,y),
                ax.c2p(x,alim),
                stroke_width=1,
                color=RED_A
            ) for x,y in zip(xx, series_div)
        ])
        
        
        eq_conv_res = MathTex('\sum^{', '\\infty}', '_{i=1}{ 3 \\over 4\cdot (-2)^{i-1} }').scale(0.5)
        eq_div_res = MathTex('\sum^{', '\infty}', '_{i=0} (-1)^i').scale(0.5)
        txt_scale = 0.4
        txt_conv_res = Text('сходится').scale(txt_scale).next_to(eq_conv_res, RIGHT)
        txt_div_res = Text('расходится').scale(txt_scale).next_to(eq_div_res, RIGHT)
        txt_conv_series = Text('Ряд').scale(txt_scale).next_to(eq_conv_res, LEFT)
        txt_div_series = Text('Ряд').scale(txt_scale).next_to(eq_div_res, LEFT)
        
        conv_grp = VGroup(eq_conv_res, txt_conv_res, txt_conv_series).set_color(GREEN).to_corner(UR)
        div_grp = VGroup(eq_div_res, txt_div_res, txt_div_series).set_color(RED).to_corner(UR).shift(DOWN)
        
        
        ####################
        ##### Анимация #####
        ####################
        
        # Добавляем оси
        self.play(Create(ax), Write(labels))
        self.wait()
        
        #
        ## Сходящийся ряд
        #
        self.play(Write(eq_conv))
        self.play(Create(line_conv), run_time=4)
        self.wait()
        
        self.play(Create(lim_line), Write(lim_label))
        self.wait()
        
        self.play(LaggedStart(
            *[Create(line) for line in lines_conv_to_lim_line],
            lag_ratio=0.05
        ))
        self.wait()
        
        self.play(FadeOut(lines_conv_to_lim_line, shift=UP))
        self.wait()
        
        # Ряд сходится!
        self.play(LaggedStart(
            FadeOut(eq_conv[:-3], scale=0.5, shift=UP),
            ReplacementTransform(eq_conv[-3:], eq_conv_res),
            FadeIn(txt_conv_series, shift=RIGHT),
            FadeIn(txt_conv_res, shift=LEFT),
            lag_ratio=0.2,
        ))
        self.play(Indicate(eq_conv_res[0], scale_factor=1.5))  # векторные объекты перепутаны для 0 и 1, это особенность компилляции latex... https://github.com/ManimCommunity/manim/issues/3548
        self.wait()
        
        
        #
        ## Расходящийся ряд
        #
        self.play(Write(eq_div))
        self.play(Create(line_div), run_time=4)
        self.play(LaggedStart(
            *[Create(line) for line in lines_div_to_lim_line],
            lag_ratio=0.1
        ))
        self.wait()
        
        # Ряд расходится!
        self.play(LaggedStart(
            FadeOut(eq_div[:-3], scale=0.5, shift=DOWN),
            ReplacementTransform(eq_div[-3:], eq_div_res),
            FadeIn(txt_div_series, shift=RIGHT),
            FadeIn(txt_div_res, shift=LEFT),
            lag_ratio=0.3
        ))
        self.play(Indicate(eq_div_res[0], scale_factor=1.5))
        self.wait()
        
        
        self.next_section('Divergent series summation methods')
        
        #
        ## Возможность суммирования расходящихся рядов
        #
        eu_path = get_person_svg_path('euler')
        svg = SVGMobject(eu_path, height=1.8, stroke_color=BLUE)
        for mob in svg.submobjects:
            if not mob.stroke_width:
                mob.stroke_width = 1
        cap = Text('Леонард Эйлер', color=svg.get_color(), font='sans-serif')
        cap.set(width=svg.get_width()).next_to(svg, DOWN, buff=SMALL_BUFF)
        
        
        text = '''
        Если у нас есть сумма
        1 - 1 + 1 - 1 + 1 - 1 + ...,
        то единственное её
        разумное значение есть 1/2
        '''
        quote = Text(text, font='sans-serif', line_spacing=0.8, font_size=24, color=GRAY_A)
        quote.scale(0.7).next_to(Group(svg,cap), LEFT)
        svg_grp = VGroup(svg, cap, quote).to_edge(UP, buff=MED_SMALL_BUFF).shift(RIGHT)
        
        op_med = 0.8
        op_min = 0.1
        arr = Arrow(txt_div_series.get_left(), svg_grp.get_right(), color=RED).set_opacity(0.8)
        self.play(
            conv_grp.animate.set_opacity(op_min),
            div_grp.animate.set_opacity(op_med),
            lines_div_to_lim_line.animate.set_stroke(opacity=op_med),
            line_conv.animate.set_stroke(opacity=op_min),
            line_conv['vertex_dots'].animate.set_opacity(op_min),
            line_div.animate.set_stroke(opacity=op_med),
            line_div['vertex_dots'].animate.set_opacity(op_med),
            ax.animate.set_opacity(op_med),
            lim_label.animate.set_opacity(op_med),
            lim_line.animate.set_opacity(op_med),
            labels.animate.set_opacity(op_min),
            GrowArrow(arr),
        )
        self.wait()
        
        txt = Text('методы cуммирования', font='sans-serif', color=GOLD)
        txt2 = Text('расходящихся рядов', font='sans-serif', color=GOLD).next_to(txt, DOWN)
        txt_grp = VGroup(txt, txt2)
        txt_grp.scale(0.75).next_to(svg_grp, DOWN, buff=LARGE_BUFF)
        final_grp = VGroup(txt_grp, svg_grp)
        self.play(
            div_grp.animate.set_opacity(op_min),
            lines_div_to_lim_line.animate.set_stroke(opacity=op_min),
            line_div.animate.set_stroke(opacity=op_min),
            line_div['vertex_dots'].animate.set_opacity(op_min),
            ax.animate.set_opacity(op_min),
            lim_label.animate.set_opacity(op_min),
            lim_line.animate.set_opacity(op_min),
            arr.animate.set_opacity(op_min),
            LaggedStart(
                LaggedStart(
                    Create(svg, run_time=5),
                    FadeIn(svg_grp[1:], shift=RIGHT),
                    lag_ratio=0.2
                ),
                self.camera.frame.animate().move_to(final_grp).set(width=2*final_grp.get_width()),
                lag_ratio=2
            )
        )
        
        self.play(Write(txt_grp))
        self.wait()
        self.play(
            FadeOut(final_grp, scale=2),
            self.camera.frame.animate.set(width=0.04*self.camera.frame.get_width()),
            run_time=3,
            rate_func=rate_functions.ease_in_cubic
        )
        self.wait()


#%% Тестовый рендер
if __name__ == '__main__':
    
    from helpers.render import dev_render
    
    dev_render(__file__, SeriesSumDefinition)