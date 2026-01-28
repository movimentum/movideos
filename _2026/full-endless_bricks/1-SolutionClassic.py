#
# 0. Завязка
#

import numpy as np

from manim import *

from movi_ext import *

from manim_cad_drawing_utils import *


#%%
SceneExtension.video_orientation = 'landscape'

SceneExtension.render_all_sections = False

np.random.seed(0xDEADBEEF)


#%%
class SolutionClassic(MovingCameraScene, SceneExtension):
    
    def construct(self):

        #
        ## Начало
        #
        self.next_section('begining', skip_animations=SceneExtension.skip(True))
        
        n = 4
        h = (4 - 1) / n * 2
        w = 8 * h
        self.width = w
        self.height = h
        self.stroke_width = 5

        r_base = self.get_rectangle().to_corner(UL)
        r_base.generate_target()
        r_base.target.to_corner(UR)
        self.r_base = r_base
        self.add(r_base)
        #self.play(self.camera.auto_zoom(r_base.target, margin=1))
        
        
        self.rects = [r_base]
        self.lines = [Line(r_base.target.get_corner(DL),
                           r_base.target.get_corner(DL))]

        # Первый кирпич
        self.play(MoveToTarget(r_base), run_time=3)
        self.wait()
        
        # Второй кирпич        
        new_rects, new_lines = self.add_rectangles_below(1, add_label=True)        
        self.rescale_and_show(new_rects)
        self.wait()
        
        # Визуализируем длину кирпича
        dimL = Linear_Dimension(self.rects[0].get_critical_point(RIGHT),
                                self.rects[0].get_critical_point(LEFT),
                                text=MathTex('L').scale(1.3),
                                direction=UP,
                                offset=2.5,
                                outside_arrow=True,
                                ext_line_offset=0,
                                color=BLUE).set_opacity(0.5)
        dimL['text'].set_opacity(1.0)
        self.play(FadeIn(dimL, shift=DOWN), run_time=2)
        self.wait()
        
        self.play(MoveToTarget(new_rects[0]), run_time=3)
        
        # Выделяем свес
        self.play(LaggedStart(*[Write(line) for line in new_lines], lag_ratio=0.1))
        self.wait()
        
        # Показываем центр масс одного кирпича
        self.show_mass_center(1)
        self.wait()
        
        self.play(FadeOut(dimL, shift=UP), run_time=2)
        self.wait()


        #
        ## Если верхний немного подвинуть, опрокинется
        #
        self.next_section('instability', skip_animations=SceneExtension.skip(True))
        
        
        grp = VGroup(r_base, new_lines[0])
        grp.save_state()
        self.play(grp.animate.shift(0.1 * RIGHT))
        self.play(self.camera.frame.animate(rate_func=smooth).scale(1.3), 
                  Rotate(grp,
                         angle=-PI/2,
                         about_point=self.rects[-1].get_corner(UR),
                         rate_func=rate_functions.ease_out_bounce
                         ),
                  run_time=3
                  )
        self.wait()
        self.play(Rotate(grp, angle=PI/2, about_point=self.rects[-1].get_corner(UR)), run_time=3)
        self.play(Restore(grp))
        self.wait()
        

        #
        ## Добавляем больше кирпичей
        #
        self.next_section('add_more', skip_animations=SceneExtension.skip(True))

        for i in range(3):
            new_rects, new_lines = self.add_rectangles_below(1, add_label=True)
            self.rescale_and_show(new_rects)
                
            self.play(LaggedStart(*[MoveToTarget(r) for r in self.rects], lag_ratio=0.1), run_time=1)
            self.wait()
                
            self.play(LaggedStart(*[Create(line) for line in new_lines], lag_ratio=0.1))
            self.wait()
            
            # Показываем центр масс одного кирпича
            self.show_mass_center(2+i)
            self.wait()


        #
        ## Пять кирпичей = верхний выступает за край нижнего
        #
        self.next_section('overshoot', skip_animations=SceneExtension.skip(True))
        
        [rect.save_state() for rect in self.rects]
        [line.save_state() for line in self.lines]
        
        # Это подтвердит и простое суммирование свесов
        #               0              1         2            3             4    5               6      7             8     9              10
        sum1 = MathTex('{L \\over 2}', '\\cdot', '\\left(', '{1 \\over 1}', '+', '{1 \\over 2}', '+', '{1 \\over 3}', '+', '{1 \\over 4}', '\\right)')
        sum1.next_to(self.rects[-1], RIGHT).shift(2*RIGHT)
        #self.play(Write(sum1))
        
        remaining = (1,2,4,6,8,10)
        
        self.play(
            LaggedStart(
                TransformFromCopy(self.lines[-1][-1][0], sum1[0]),
                TransformFromCopy(self.lines[1][-1][-1], sum1[3]),
                TransformFromCopy(self.lines[2][-1][-1], sum1[5]),
                TransformFromCopy(self.lines[3][-1][-1], sum1[7]),
                TransformFromCopy(self.lines[4][-1][-1], sum1[9]),
                lag_ratio=0.1
            ),
            *[FadeIn(sum1[idx], shift=DOWN) for idx in remaining],
            run_time=2
        )
        self.wait()
        
       
        self.play(
            LaggedStart(
                ShowPassingFlashWithThinningStrokeWidth(
                    SurroundingRectangle(self.rects[-1], buff=0.2).set_color(RED)),
                ShowPassingFlashWithThinningStrokeWidth(
                    SurroundingRectangle(self.rects[0], buff=0.2).set_color(RED)),
                run_time=2,
                lag_ratio=0.1
            ),
            *[rect.animate.set_opacity(0.2) for rect in self.rects[1:5-1]],
            *[line.animate.set_opacity(0.2) for line in self.lines],
            self.rects[0].animate.set_stroke(width=2*self.stroke_width).set_color(GOLD),
            self.rects[-1].animate.set_stroke(width=2*self.stroke_width).set_color(GOLD)
        )
        
        self.wait()
        
        sum2 = MathTex('{L \\over 2}', '\\cdot', '\\left(', '{12 \\over 12}', '+', '{6 \\over 12}', '+', '{4 \\over 12}', '+', '{3 \\over 12}', '\\right)')
        sum2.move_to(sum1)
        self.play(ReplacementTransform(sum1, sum2))
        self.wait()
        
        sum3 = MathTex('{L \\over 2}', '\\cdot', '{12 + 6 + 4 + 3 \\over 12}')
        sum3.move_to(sum2, RIGHT)
        self.play(TransformMatchingShapes(sum2, sum3))
        self.wait()
        
        sum4 = MathTex('{L \\over 2}', '\\cdot', '{25 \\over 12}', '>', 'L')
        sum4.set(color=GOLD)
        sum4.move_to(sum3, LEFT).scale(1.2)
        self.play(Succession(
            TransformMatchingShapes(sum3, sum4[:-2]),
            FadeIn(sum4[-2:], shift=LEFT)
        ))
        

        vline = DashedLine(5 * DOWN, 5 * UP, color=BLUE).move_to(
            Group(self.rects[-1], self.rects[0]).get_center()
        )
        
        self.play(
            #FadeIn(vline, shift=2*UP),
            Write(vline),
            Indicate(sum4),
            #rate_func=there_and_back,
            run_time=2
        )
        self.wait()
        
        self.play(
            FadeOut(vline, shift=UP, scale=1.2),
            FadeOut(sum4, shift=DOWN, scale=0.8),
            LaggedStart(
                *[Restore(rect) for rect in self.rects],
                *[Restore(line) for line in self.lines],
                lag_ratio=0.2,
            )
        )
        self.wait()
        
        
        #
        ## Добавляем больше кирпичей
        #
        self.next_section('add_more_bricks', skip_animations=SceneExtension.skip(True))
                        
        for i in range(3):
            new_rects, new_lines = self.add_rectangles_below(n * (i + 1))
            self.rescale_and_show(new_rects)
            
            self.play(LaggedStart(*[MoveToTarget(r) for r in new_rects], lag_ratio=0.1), run_time=3)
            self.wait()
            
            self.play(LaggedStart(*[Create(line) for line in new_lines], lag_ratio=0.1))
            self.wait()
        
        self.play(LaggedStart(
            *[line.animate.align_to(self.rects[-1], DOWN) for line in self.lines],
            lag_ratio=0.1))
        
        
        self.play(self.camera.frame.animate.move_to(Group(*self.lines)).set(width=Group(*self.lines).width * 1.5),
                  *[line.animate.set_color([BLUE,RED][i%2]) for i,line in enumerate(self.lines)],
                  VGroup(*self.rects).animate.set_opacity(0.1)
                  #*[r.animate.set_opacity(0.3) for r in self.rects]
                  )
        self.wait()
        
        
        #
        ## Суммируем вклады
        #
        self.next_section('sum_contributions', skip_animations=SceneExtension.skip(True))
        
        # Показываем дробные значения вкладов
        braces = [Brace(line) for line in self.lines]
        labels = [
            MathTex(f'\\dfrac{1}{i}').scale(1.5 - i * 0.085).next_to(br, DOWN)
            for i, br in enumerate(braces)
        ]
        dots = MathTex('\\ldots', color=BLUE_A)
        dots.scale(3).next_to(VGroup(self.lines[10:]), 4 * DOWN)
        labels.append(dots)
        
        ani = []
        [ ani.extend( (DrawBorderThenFill(br), FadeIn(label)) )
          for br, label in zip(braces[1:10], labels[1:10]) ]
        ani.append(Write(labels[-1]))
        self.play(LaggedStart(*ani, lag_ratio=0.1))
        self.wait()
        
        # Переводим в сумму гармонического ряда
        br_all = Brace(Group(*self.lines)).shift(3 * DOWN)
        #                   1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9
        text_array = (r' + '.join([rf'\dfrac{1}{i}' for i in range(1, 10)]) + r' + \ldots').split(' ')
        label_all = MathTex(*text_array)
        label_all.scale(1.5).next_to(br_all, 1.2*DOWN).set_color(RED)
        
        shifts = np.random.rand(9,3) - [0.5, 0.5, 0.5]
        shifts[:,2] = 0
        shifts *= 5
        
        self.play(DrawBorderThenFill(br_all))
        self.play(
            TransformMatchingShapes(VGroup(*labels[1:10]), label_all[:-1]),
            ReplacementTransform(dots, label_all[-1]),
            run_time=5
        )
        self.play(LaggedStart(
            *[ FadeOut(brace, shift=shift, scale=0.5)
               for brace,shift in zip(braces[1:10], shifts) ],
            lag_ratio=0.1
        ))
        
        self.wait()
        

        #
        ## Суммируем вклады
        #
        self.next_section('harmonic_series', skip_animations=SceneExtension.skip(False))
        
        res_series = MathTex(r'\sum_{n=1}^{N}', r'\dfrac{1}{', r'n}').shift(2 * UP)
        res_series.next_to(Group(*self.lines), UP).shift(2 * UP)
        res_hrm = MathTex(r'{L \over 2} \cdot', r'\sum_{n=1}', r'^{\infty}', r'\dfrac{1}{', r'n}', r'\rightarrow', r'\infty').move_to(res_series, LEFT)
        # Совмещаем суммы
        res_hrm.align_to(res_series, DOWN)
        res_hrm.shift(res_series.get_corner(DL)- res_hrm[1:].get_corner(DL))
        # Подкрашиваем бесконечную сумму и первую дробь
        res_hrm[-2].set_color(BLUE_B)
        res_hrm[-1].set_color(BLUE)
        res_hrm[0].set_opacity(0.3)
        #res_hrm.submobjects[2].set_color(BLUE) # не можем достучаться до верхнего предела (непреодолённая проблема latex)
        
        self.play(
            LaggedStart(
                *[ReplacementTransform(elem, res_series[1:3]) for elem in label_all[::2]],
                lag_ratio = 0.1),
            LaggedStart(
                *[ReplacementTransform(elem, res_series[0]) for elem in label_all[1::2]],
                lag_ratio = 0.1),
            self.camera.frame.animate(run_time=3)
                .move_to(res_hrm)
                .set_width(res_hrm.get_width() * 2)
        )
        self.wait()

        # Подпись для L/2
        bot = res_hrm[0].get_bottom() + 0.15 * DL
        ptr = Arrow(bot + 0.5 * DOWN, bot, buff=0.05)
        ptr.set_opacity(0.5)
        txt = Text('полкирпича').scale(0.25).next_to(ptr, DOWN)
        txt.set_opacity(0.5)   
        ptr_grp = VGroup(ptr, txt)
        
        self.play(TransformMatchingShapes(res_series, res_hrm[1:-2]))
        self.play(
            FadeIn(res_hrm[-2:], shift=LEFT),
            FadeIn(res_hrm[0], shift=RIGHT)
        )
        self.play(FadeIn(ptr_grp, shift=0.25*UP))
        self.wait()
        self.play(FadeOut(ptr_grp, shift=0.25*DOWN))
        self.wait()
        
        # Выделить бесконечный предел
        self.play(ShowPassingFlashWithThinningStrokeWidth(
            SurroundingRectangle(res_hrm[-2:], buff=0.2).set_color(RED),
            time_width=0.4,
            run_time=3,
        ))
        self.wait()

    
    
    def get_rectangle(self):
        return Rectangle(height=self.height,
                         width=self.width,
                         stroke_width=self.stroke_width,
                         color=None,
                         stroke_color=WHITE
                         )

        
    def add_rectangles_below(self, n, add_label=False):
        """ Добавить снизу n кирпичей """
        rects = [self.get_rectangle() for i in range(n)]
        n_old = len(self.rects)
        self.rects.extend(rects)
        n_new = len(self.rects)
        lines = []
        for i in range(n_old, n_new):
            r = self.rects[i]
            r_base = self.rects[i-1]
            r.next_to(r_base, DOWN, buff=0)
            r.generate_target()
            r.target.next_to(r_base.target, DOWN, buff=0)
            r.target.shift(self.width / 2 / i * LEFT)
            line = Line(r.target.get_corner(UR),
                        r_base.target.get_corner(DR),
                        color=YELLOW,
                        stroke_width=2 * self.stroke_width)
            if add_label:
                label = MathTex(f'\\frac{{L}}{2} \\cdot ', f'\\frac{1}{{{i}}}').next_to(line, UP)
                label[0].set_color(GRAY_D)
                line.add(label)
            lines.append(line)
        
        self.lines.extend(lines)
        return rects, lines  # только добавленные
    
    
    def rescale_and_show(self, new_rects=None):
        grp = Group(*[r.target for r in self.rects])
        #self.play(self.camera.auto_zoom(grp, margin=MED_LARGE_BUFF).align_to(self.r_base.target, RIGHT))
        self.play(self.camera.auto_zoom(grp, margin=3))
        if new_rects:
            self.play(*[Create(r) for r in new_rects])
        self.wait()
    
    
    def show_mass_center(self, N=None):
        rects = self.rects[:N]
        
        n = len(rects)
        dots = VGroup(*[Dot(x.get_center()) for x in rects])
        
        cm_h = UP * self.height * n
        cm = DashedLine(ORIGIN, cm_h, color=GOLD)
        
        centers = np.array([x.get_center() for x in rects])
        cm_pos = np.mean(centers, axis=0)
        cm.move_to(cm_pos)
        
        
        self.play(
            LaggedStart(
                *[FadeIn(dot, shift=DOWN) for dot in dots]
        ))
        self.play(Create(cm))
        self.play(Uncreate(cm), FadeOut(dots, shift=DOWN))
        
        
#%% Тестовый рендер
if __name__ == '__main__':
    
    from helpers.render import dev_render
    
    dev_render(__file__, SolutionClassic)

        