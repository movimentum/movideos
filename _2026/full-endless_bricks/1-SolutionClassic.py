#
# 0. Завязка
#

import numpy as np

from manim import *

from movi_ext import *


#%%
SceneExtension.video_orientation = 'landscape'

SceneExtension.render_all_sections = False

np.random.seed(0xDEADBEEF)


#%%
class SolutionClassic(MovingCameraScene, SceneExtension):
    
    def construct(self):

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
        self.play(MoveToTarget(new_rects[0]), run_time=3)
        
        # Выделяем свес
        self.play(LaggedStart(*[Create(line) for line in new_lines], lag_ratio=0.1))
        self.wait()
        
        # Показываем центр масс одного кирпича
        self.show_mass_center(1)


        # Если верхний немного подвинуть, опрокинется
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


        # Ещё 1
        for i in range(3):
            new_rects, new_lines = self.add_rectangles_below(1, add_label=True)
            self.rescale_and_show(new_rects)
                
            self.play(LaggedStart(*[MoveToTarget(r) for r in self.rects], lag_ratio=0.1), run_time=1)
            self.wait()
                
            self.play(LaggedStart(*[Create(line) for line in new_lines], lag_ratio=0.1))
            self.wait()
            
            # Показываем центр масс одного кирпича
            self.show_mass_center(2+i)
            
        self.next_section('current', skip_animations=SceneExtension.skip(False))
        
        
        self.play(LaggedStart(
            ShowPassingFlashWithThinningStrokeWidth(
                SurroundingRectangle(self.rects[-1], buff=0.2).set_color(RED)),
            ShowPassingFlashWithThinningStrokeWidth(
                SurroundingRectangle(self.rects[0], buff=0.2).set_color(RED)),
            run_time=2,
            lag_ratio=0.1
        ))
        self.wait()
        
        vline = DashedLine(5 * DOWN, 5 * UP, color=BLUE).move_to(
            Group(self.rects[-1], self.rects[0]).get_center()
        )
        self.play(
            #FadeIn(vline, shift=2*UP),
            Write(vline),
            #rate_func=there_and_back,
            run_time=2
        )
        self.wait()
        
        self.play(FadeOut(vline, shift=UP, scale=1.2))
        self.wait()
        
        return        
        
        self.next_section('add_more_bricks', skip_animations=SceneExtension.skip(True))
                        
        # Ещё 4
        for i in range(4):
            new_rects, new_lines = self.add_rectangles_below(n if i < 3 else 10)
            self.rescale_and_show(new_rects)
            
            self.play(LaggedStart(*[MoveToTarget(r) for r in self.rects], lag_ratio=0.1), run_time=3)
            self.wait()
            
            self.play(LaggedStart(*[Create(line) for line in new_lines], lag_ratio=0.1))
            self.wait()
        
        self.play(LaggedStart(
            *[line.animate.align_to(self.rects[-1], DOWN) for line in self.lines],
            lag_ratio=0.1))
        
        
        self.play(self.camera.frame.animate.move_to(Group(*self.lines)).set(width=Group(*self.lines).width * 1.5),
                  *[line.animate.set_color([YELLOW_A,YELLOW_D][i%2]) for i,line in enumerate(self.lines)],
                  VGroup(*self.rects).animate.set_opacity(0.1)
                  #*[r.animate.set_opacity(0.3) for r in self.rects]
                  )
        self.wait()
        
        
        self.next_section('till_end', skip_animations=SceneExtension.skip(False))
        
        
        braces = [Brace(line) for line in self.lines]
        labels = [MathTex(f'\\dfrac{1}{i}').scale(1.5).next_to(br, DOWN) for i, br in enumerate(braces)]
        
        ani = []
        [ ani.extend((DrawBorderThenFill(br), FadeIn(label))) for br, label in zip(braces[1:10], labels[1:10]) ]
        self.play(LaggedStart(*ani, lag_ratio=0.1))
        self.wait()
        
        br_all = Brace(Group(*self.lines)).shift(2 * DOWN)
        #                   1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9
        text_array = (r' + '.join([rf'\dfrac{1}{i}' for i in range(1, 10)]) + r' + \ldots').split(' ')
        label_all = MathTex(*text_array).scale(1.5).next_to(br_all, DOWN).set_color(RED)
        
        self.play(DrawBorderThenFill(br_all))
        self.play(TransformMatchingShapes(VGroup(*labels[1:10]), label_all),
                  FadeOut(*braces[1:10], scale=0.5)
                  )
        self.wait()
        
        res_series = MathTex(r'\sum_{n=1}^{N}', r'\dfrac{1}{', r'n}').shift(2 * UP)
        res_series.next_to(Group(*self.lines), UP).shift(2 * UP)
        res_hrm = MathTex(r'\sum_{n=1}^{\infty}', r'\dfrac{1}{', r'n}', r'\rightarrow \infty').move_to(res_series, LEFT)
        
        #self.play(#FadeIn(res_series[1], scale=2),
        #          LaggedStart(*[ReplacementTransform(elem, res_series[1:3]) for elem in label_all[::2]],
        #                      lag_ratio = 0.1)
        #)
        
        self.play(
            LaggedStart(
                *[ReplacementTransform(elem, res_series[1:3]) for elem in label_all[::2]],
                lag_ratio = 0.1),
            LaggedStart(
                *[ReplacementTransform(elem, res_series[0]) for elem in label_all[1::2]],
                lag_ratio = 0.1),
            self.camera.frame.animate(run_time=3).move_to(res_hrm).set_width(res_hrm.get_width() * 1.2)
        )
        self.wait()
        
        
        self.play(
            TransformMatchingTex(res_series, res_hrm),
        #    self.camera.auto_zoom(res_hrm).scale(1.2)
        )
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
        self.play(self.camera.auto_zoom(grp, margin=1))
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

        