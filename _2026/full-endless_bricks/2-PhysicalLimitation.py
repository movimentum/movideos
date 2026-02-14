#
# 2. Физическое ограничение классического решения
#

import numpy as np

from manim import *

from movi_ext import *

from manim_cad_drawing_utils import *


#%%
SceneExtension.render_all_sections = False

np.random.seed(0xDEADBEEF)


#%% Расчёт наибольшей нагрузки
class PhysicalLimitation(MovingCameraScene, SceneExtension):
    
    video_orientation = 'portrait'
    
    def construct(self):

        #
        ## Добавляем плотность
        #
        self.next_section('density', skip_animations=SceneExtension.skip(True))
        density_range = TexCyr(r'$\rho =~$', '$1\,650~$', '$\ldots~$', '$1\,850~$', r'$\text{кг/м}^3$')
        density = TexCyr(r'$\rho \approx~$', '$1\,750~$', r'$\text{кг/м}^3$')
        
        self.play(Write(density_range))
        self.wait()
        
        self.play(
            FadeOut(density_range[1], shift=UL),
            FadeOut(density_range[2], shift=UP),
            FadeOut(density_range[3], shift=UR),
            ReplacementTransform(density_range[0], density[0]),
            ReplacementTransform(density_range[-1], density[-1]),
            FadeIn(density[1], shift=UP)
        )
        self.wait()
        
        #
        ## Добавляем массу
        #
        self.next_section('mass', skip_animations=SceneExtension.skip(True))
        
        eq = TexCyr(r'$\text{чистоплотность} = \dfrac{\text{чисто масса}}{\text{чисто объём}}$')
        self.play(
            density.animate.to_edge(UP),
            Write(eq)
        )
        self.wait()
        
        mass_zero = TexCyr(r'$\rho = \dfrac{m}{\text{объём}}$')
        self.play(TransformMatchingShapes(eq, mass_zero))
        self.wait()
       
        mass_first = TexCyr(r'$m = \rho \cdot \text{объём}$')
        self.play(TransformMatchingShapes(mass_zero, mass_first))
        self.wait()

        mass_second = TexCyr(r'$m = \rho \cdot \left(l \cdot w \cdot h \right)$')
        
        self.play(TransformMatchingShapes(mass_first, mass_second))
        self.wait()
        
        mass = TexCyr(r'$m\approx 3.5$ кг')
        mass.next_to(density, DOWN)
        
        self.play(TransformMatchingShapes(mass_second, mass))
        self.wait()
        
        #
        ## Добавляем предел прочности на сжатие
        #
        self.next_section('strengthlimit', skip_animations=SceneExtension.skip(True))
        
        sigma = TexCyr(r'$\sigma = 30$ МПа').next_to(mass, DOWN, buff=MED_LARGE_BUFF)
        self.play(Write(sigma))
        self.wait()

        h, w = 1, 3
        brick = Rectangle(height=h, width=w, color=BLUE, fill_opacity=0.5, fill_color=RED)
        brick.shift(5 * DOWN)
        self.play(DrawBorderThenFill(brick))
        self.wait()
        
        n = 8
        stack = [brick.copy().set_opacity(0.5).set_fill(opacity=0) for _ in range(n)]
        stack[0].next_to(brick, UP, buff=0)
        [stack[i].next_to(stack[i-1], UP, buff=0) for i in range(1, n)]
        shifts = RIGHT.reshape(1,3) * w * (np.random.rand(n,1) - 0.5)
        [el.shift(ds) for el, ds in zip(stack, shifts)]
        
        self.play(LaggedStart(
            *[FadeIn(b, shift=-ds) for b,ds in zip(stack,shifts)],
            lag_ratio=0.1
        ))
        self.wait()
        
 
        # Визуализируем нагрузку
        load = DistributedLoad(
            brick.get_top()[1],
            brick.get_left()[0] + 0.1,
            brick.get_right()[0] - 0.1
        )
        load.reconstruct_sin_wave()
        

        def move_stack_and_load_randomly(ampl=w*0.7, phase=None, wait_time=1):
            """ Смещает кирпичи в стопке случайным образом и двигает нагрузку """
            for b in stack:
                b.target = b.copy().align_to(brick, LEFT)
            
            shifts = RIGHT.reshape(1,3) * ampl * (np.random.rand(n,1) - 0.5)
            if phase == None:
                phase = np.random.rand() * 2 * PI
           
            *[b.target.shift(-ds) for b,ds in zip(stack, shifts)],
            
            self.play(
                LaggedStart(
                    *[MoveToTarget(b) for b in stack],
                    lag_ratio=0.1
                ),
                load.animate.reconstruct_sin_wave(phase)
            )
            self.wait(wait_time)

        
        self.play(Create(load))
        self.wait()
        
        [b.save_state() for b in stack] # сохраняем для будущего восстановления
        load.save_state()               #
        brick.save_state()              #
        
        
        move_stack_and_load_randomly()
        move_stack_and_load_randomly()
        move_stack_and_load_randomly(phase=PI/2)

        
        # Делаем ровную стопку и равномерную нагрузку
        ds = 4 * UP
        n_above = 4
        self.play(
            LaggedStart(
                *[b.animate
                   .align_to(brick, LEFT)
                   .shift(ds)
                   .set_stroke(opacity=0.5*(1-i/n_above))
                   for i,b in enumerate(stack[:n_above])
                ],
                lag_ratio=0.05
            ),
            LaggedStart(
                *[FadeOut(b) for b in stack[n_above:]],
                lag_ratio=0.05
            ),
            brick.animate.shift(ds),
            load.animate.make_even(lmin=0.8).shift(ds)
        )
        self.wait()
        
        
        #
        ## Рассчитываем количество кирпичей
        #
        self.next_section('max_number_of_bricks', skip_animations=SceneExtension.skip(True))
        
        Group(
            eq_sigma_0 := TexCyr(r'$\sigma = \text{давление}$'),
            eq_sigma_1 := TexCyr(r'$\sigma = \dfrac{\text{сила тяжести N кирпичей}}{\text{площадь кирпича}}$'),
            eq_sigma_2 := TexCyr(r'$\sigma = \dfrac{N\cdot mg}{l \cdot w}$'),
            eq_sigma_3 := TexCyr(r'$N = \dfrac{\sigma \cdot l \cdot w}{mg}$'),
            eq_sigma_4 := TexCyr(r'$N = \dfrac{30\cdot 10^6\, \text{Па}'
                                 r'\cdot 0.25\, \text{м} \cdot 0.12\, \text{м}}'
                                 r'{3.5\,\text{кг} \cdot 9.81\,\text{м/с}^2}$'),
            eq_N_bricks := TexCyr(r'$N \approx 26\,212$ штук')
        ).next_to(brick, DOWN).shift(2*DOWN)
        
        g_arrow = Arrow(UP, DOWN, color=RED_A).to_edge(LEFT, buff=LARGE_BUFF)
        g_arrow.set_stroke(opacity=[1,0])
        #g_txt = TexCyr(r'$g \approx 9.8 \dfrac{\text{м}}{\text{с}^2}$')
        g_txt = TexCyr(r'$g \approx 9.81\, \text{м/с}^2$')
        g_txt.scale(0.7).next_to(g_arrow, DOWN)
        
        self.play(Write(eq_sigma_0))
        self.wait()
        
        self.play(
            TransformMatchingShapes(eq_sigma_0, eq_sigma_1),
            Succession(FadeIn(g_arrow, shift=DOWN), Write(g_txt)),
            run_time=2
        )
        self.wait()
        
        self.play(TransformMatchingShapes(eq_sigma_1, eq_sigma_2), run_time=2)
        self.wait()
        
        self.play(TransformMatchingShapes(eq_sigma_2, eq_sigma_3), run_time=2)
        self.wait()
        
        self.play(TransformMatchingShapes(eq_sigma_3, eq_sigma_4), run_time=2)
        self.wait()
        
        self.play(TransformMatchingShapes(eq_sigma_4, eq_N_bricks), run_time=2)
        self.wait()
        
        self.play(
            eq_N_bricks.animate.set(color=GOLD).scale(1.2),
            ShowPassingFlashWithThinningStrokeWidth(
                SurroundingRectangle(eq_N_bricks, color=GOLD_A).scale(1.2),
                time_width=0.4),
            run_time=2
        )
        self.wait()
        
        # Показываем высоту стопки
        stack_br = Brace(VGroup(stack), RIGHT, color=BLUE).set_opacity(opacity=0.5)
        
        pre = eq_N_bricks.get_center()
        new = eq_N_bricks.copy().scale(1/1.2).rotate(PI/2).next_to(stack_br, RIGHT).get_center()
        mid = (new + pre) / 2
        dmid = rotate_vector(new - mid, PI/2)
        rotation_center = mid + dmid
        
        self.play(
            FadeIn(stack_br, shift=LEFT),
            Succession(
                eq_N_bricks.animate.scale(1/1.2),
                Rotate(eq_N_bricks, PI/2, about_point=rotation_center)
            )
        )
        self.wait()
        
        #
        ## Рассчитываем высоту и смещение
        #
        self.next_section('new_height_and_shift', skip_animations=SceneExtension.skip(True))

        txt_scale = 0.6
        grp_buff = LARGE_BUFF
        in_buff = MED_SMALL_BUFF
        
        # Высота
        txt_height = Text('Наибольшая высота башни', color=BLUE_A)
        txt_height.scale(txt_scale).next_to(brick, DOWN, buff=grp_buff)
        
        Group(
            eq_height_0 := TexCyr(r'$H = N\cdot h$'),
            eq_height_1 := TexCyr(r'$H = 26\,212 \cdot 6.5\,\text{см}$'),
            eq_height_2 := TexCyr(r'$H \approx 1.7$ км').set_color(GOLD)
        ).next_to(txt_height, DOWN, buff=in_buff)
        
        self.play(FadeIn(txt_height, shift=DOWN), Write(eq_height_0))
        self.wait()
        
        self.play(TransformMatchingShapes(eq_height_0, eq_height_1), run_time=2)
        self.wait()
        
        self.play(TransformMatchingShapes(eq_height_1, eq_height_2), run_time=2)
        self.wait()
        
        grp_height = VGroup(eq_height_2, txt_height)

        
        # Смещение
        txt_shift = Text('Наибольшее смещение', color=BLUE_A)
        txt_shift.scale(txt_scale).next_to(grp_height, DOWN, buff=grp_buff)
        
        Group(
            eq_shift_0 := TexCyr(r'\[L = \dfrac{l}{2} \cdot \sum_{i=1}^{N}{\dfrac{1}{i}}\]'),
            eq_shift_1 := TexCyr(r'\[L = \dfrac{25\,\text{см}}{2}\cdot \sum_{i=1}^{26\,212}{\dfrac{1}{i}}\]'),
            eq_shift_2 := TexCyr(r'$L \approx 1.35$ м').set_color(GOLD)
        ).next_to(txt_shift, DOWN, buff=in_buff)
        # eq_shift_0.next_to(txt_shift, DOWN, buff=in_buff)
        eq_shift_2.next_to(txt_shift, DOWN, buff=in_buff)
        
        self.play(FadeIn(txt_shift, shift=DOWN), Write(eq_shift_0))
        self.wait()
        
        self.play(TransformMatchingShapes(eq_shift_0, eq_shift_1), run_time=2)
        self.wait()
        
        self.play(TransformMatchingShapes(eq_shift_1, eq_shift_2), run_time=2)
        self.wait()
        
        
        #
        ## Давление на край кирпича
        #
        self.next_section('pointed_pressure', skip_animations=SceneExtension.skip(True))
        
        eq_height_2.generate_target()
        eq_shift_2.generate_target()
        
        eq_height_2.target.to_edge(UP).set_opacity(0.2)
        eq_shift_2.target.next_to(eq_height_2.target, DOWN).set_opacity(0.2)
        
        grp_stack_brace = VGroup(stack_br, eq_N_bricks)

        
        
        # Убираем ненужные элементы, временно затеняем нужные
        self.play(
            FadeOut(txt_shift, shift=UP*0.5),
            FadeOut(txt_height, shift=UP*0.5),
            FadeOut(g_txt, scale=0.5),
            FadeOut(g_arrow, shift=DOWN),
            *[Unwrite(eq) for eq in (density, mass, sigma)],
            *[MoveToTarget(eq) for eq in (eq_height_2, eq_shift_2)],
            grp_stack_brace.animate.scale(0.7).set_opacity(0.2).shift(RIGHT*0.7 + DOWN),
            
            run_time = 2
        )
        self.wait()
        
        self.play(
            Restore(brick),
            Restore(load),
            *[Restore(b) for b in stack]
        )
        self.wait()
        

            
        brick_shift = LEFT * 2    
        brick.generate_target()
        brick.target.shift(brick_shift)
        
        load.generate_target()
        load.target.make_even()
        load.target.shift(brick_shift)
        
        def ani_making_stack_harmonic(n, scale_shift=1):
            """ Смещает кирпичи в стопке гармонически """
            substack = stack[:n]
            
            for b in substack:
                b.generate_target()
                #b.target.align_to(brick.target, LEFT)
            
            substack[0].target.next_to(brick.target, UP, buff=0).align_to(brick.target, LEFT)
            [substack[i].target.next_to(substack[i-1].target, UP, buff=0).align_to(brick.target, LEFT) for i in range(1,n)]
            
            shifts = RIGHT.reshape(1,3) * np.cumsum([1/(n - i) for i in range(n)]).reshape(n,1)
            shifts *= scale_shift * w / 2

            *[b.target.shift(ds) for b,ds in zip(substack, shifts)],
            
            return LaggedStart(*[MoveToTarget(b) for b in substack], lag_ratio=0.1)
        
        self.play(
            ani_making_stack_harmonic(len(stack)),
            MoveToTarget(brick),
            MoveToTarget(load)
        )
        self.wait()
        
        
        # Линия центра тяжести
        cm_start = brick.get_corner(UR) + UP * 0.1
        cm_end = cm_start.copy()
        cm_end[1] = stack[-1].get_top()[1] + 0.2
        cm_line = DashedLine(cm_start, cm_end, color=YELLOW, stroke_opacity=0.5)
        
        self.play(Succession(
            Create(cm_line),
            Wait(2),
            FadeOut(cm_line, scale=1.5)
        ))
        self.wait()
        
        
        # Нагрузка на край 
        right = brick.get_right()[0]
        left = 0.13 * brick.get_left()[0] + 0.87 * right  # как подоходный налог забрали
        self.play(load.animate.expand_over_x(left, right, 8))
        self.wait()
        
        txt_new_area = MathTex(r"\sim 1\% \cdot l\cdot w").scale(0.7).next_to(load, LEFT)
        self.play(Write(txt_new_area))
        self.wait()
        
        
        #
        ## Пересчёт количества кирпичей
        #
        self.next_section('reassessment', skip_animations=SceneExtension.skip(False))
        
        eq_N_old = MathTex(r'N ', r'= {\sigma\cdot', r'l \cdot w', r' \over mg}')
        eq_N_new = MathTex(r'{N ', r'\over 100}', r'= {\sigma\cdot', r'{l \cdot w', r' \over 100}', r' \over mg}')
        
        eq_N_old.next_to(brick, RIGHT)
        eq_N_new.next_to(brick, RIGHT)
        
        self.play(Write(eq_N_old))
        self.wait()
        
        src = (0,1,2,3)
        dst = (0,2,3,5)
        self.play(
            *[ReplacementTransform(eq_N_old[i], eq_N_new[j]) for i,j in zip(src,dst)],
            FadeIn(eq_N_new[1], scale=0.2),
            FadeIn(eq_N_new[4], scale=0.2)
        )
        self.wait()
        
  
        stack_out = [stack.pop() for _ in range(3)]
        
        brick_shift = 2 * UP + 0.3 * LEFT
        brick.generate_target()
        load.generate_target()
        
        
        brick.target.shift(brick_shift)
        load.target.shift(brick_shift)
        
        
        self.play(
            *[FadeOut(s) for s in stack_out],
            ani_making_stack_harmonic(len(stack)),
            MoveToTarget(brick),
            MoveToTarget(load),
            FadeOut(txt_new_area, scale=0.5),
            eq_N_new[:2].animate
                .scale(1.2)
                .set_color(GOLD)
                .next_to(brick.target, RIGHT)
                .shift(2*UR+0.5*LEFT),
            FadeOut(eq_N_new[2:], shift=DOWN)
        )
        self.wait()
        
        
        stack_brace_2 = Brace(VGroup(stack), RIGHT, color=BLUE).set_opacity(opacity=0.5)
        eq_N_bricks_2 = TexCyr(r'$N \approx~$', '$262$', ' штук', r'и').rotate(PI/2).next_to(stack_brace_2, RIGHT, buff=SMALL_BUFF)
        eq_N_bricks_2.set_color(BLUE_A)
        grp_stack_brace_2 = VGroup(stack_brace_2, eq_N_bricks_2[:-1])
        
        
        brace_line = DashedLine(stack[0].get_corner(DR), stack_brace_2.get_corner(DL))
        brace_line.set_opacity(0.5).set_color(BLUE_A)
        
        self.play(LaggedStart(
            Create(brace_line),
            ReplacementTransform(stack_br, stack_brace_2),
            TransformMatchingShapes(eq_N_bricks, eq_N_bricks_2[:-1]),
            FadeIn(eq_N_bricks_2[-1], shift=DOWN),
            lag_ratio=0.2
        ))
        self.wait()
        
        self.play(
            ShowPassingFlashWithThinningStrokeWidth(
                SurroundingRectangle(eq_N_bricks_2[1], color=GOLD_A).scale(1.2),
                time_width=0.4),
            ShowPassingFlashWithThinningStrokeWidth(
                SurroundingRectangle(eq_N_new[:2], color=GOLD_A).scale(1.2),
                time_width=0.4),
        )
        self.wait()
        
        self.play(FadeOut(eq_N_new[:2], scale=0.5))
        self.wait()
        
        
        eq_height_3 = TexCyr(r'$H \approx 17$ м').set_color(GOLD)
        eq_shift_3 = TexCyr(r'$L \approx 77$ см').set_color(GOLD)
        
        eq_shift_3.next_to(brace_line, UP)
        eq_height_3.rotate(PI/2).next_to(stack_brace_2, LEFT).shift(DOWN*h*0.35)
        
        self.play(Succession(
            AnimationGroup(
                eq_height_2.animate.set_opacity(1),
                eq_shift_2.animate.set_opacity(1),
            ),
            LaggedStart(
                FadeOut(eq_height_2, shift=LEFT),
                FadeIn(eq_height_3, shift=RIGHT),
                lag_ratio=0.2
            ),
            LaggedStart(
                FadeOut(eq_shift_2, shift=RIGHT),
                FadeIn(eq_shift_3, shift=DOWN),
                lag_ratio=0.2
            ),
        ))
        self.wait()
        

#%%
class DistributedLoad(VGroup):
    
    def __init__(self, low, left, right, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.low = low
        self.left = left
        self.right = right

        self.phase = 0        
        self.ampl = 0.3
        self.lmin = 0.7
        self.num = 15  # количество стрелок
        self.reconstruct_sin_wave(ampl=0)
        
    
    def reconstruct_sin_wave(self, phase=None, lmin=None, ampl=None, num_arrows=None):
        
        if not num_arrows:
            num_arrows = self.num
        else:
            self.num = num_arrows
        
        if not lmin:
            lmin = self.lmin
        else:
            self.lmin = lmin
        
        if not ampl:
            ampl = self.ampl
        else:
            self.ampl = ampl
        
        if not phase:
            phase = self.phase
        else:
            self.phase = phase
        
        arrows = VGroup()
        for i in range(num_arrows):
            x_pos = self.left + (i/(num_arrows-1)) * (self.right - self.left)
            
            wave = np.sin(2 * np.pi * (i/num_arrows) + phase * 2)
            wave = ampl * (1 + wave)
            
            arrow_length = lmin + wave
            
            arrow = Arrow(
                start=[x_pos, self.low + arrow_length, 0],
                end=[x_pos, self.low, 0],
                color=interpolate_color(RED, YELLOW, arrow_length),
                stroke_width=1 + 3 * wave,
                max_tip_length_to_length_ratio=0.15,
                buff=SMALL_BUFF
            )
            arrows.add(arrow)
        self.is_even = False
        self.become(arrows)
    
    
    def expand_over_x(self, left, right, num_arrows):
        """ Распределяет текущую нагрузку от start до end """
        self.left = left
        self.right = right
        self.num = num_arrows
        self.reconstruct_sin_wave()


    def make_even(self, lmin=0.7):
        self.phase = 0
        self.ampl = 0
        self.lmin = lmin
        self.reconstruct_sin_wave()
   

class TestDistributedLoadArrows(Scene, SceneExtension):
    def construct(self):
        
        rect = Rectangle()
        
        load = DistributedLoad(
            rect.get_top()[1],
            rect.get_left()[0],
            rect.get_right()[0]
        )
        
        self.add(rect, load)
        
        for phase in (None, 2, 0.5, 0.3):
            self.play(load.animate.reconstruct_sin_wave(phase))
            self.wait(0.5)
            
        self.play(load.animate.make_even(lmin=1))
        self.wait(0.5)
        

#%% Кирпич с размерами
class BrickBreak(ThreeDScene, SceneExtension):
    
    video_orientation = 'landscape'
        
    
    dimensions = 3, 2, 1  # длина, ширина, высота кирпича
    n_parts = 4, 3, 2  # количество осколков по длине, ширине, высоте
    
    # Список ракурсов камеры (phi, theta, zoom)
    camera_views = [
        (90, -90, 1),   # Вид спереди
        (0, 0, 1),      # Вид сверху
        (90, 0, 1),     # Вид сбоку
        (60, 45, 1),    # Изометрический вид 1
        (120, -45, 1),  # Диагональный вид снизу
        (70, 300, 0.7), # Изометрический вид c меньшим масштабом
        (75, 150, 0.7),
    ]
    
    def construct(self):
        
        l, w, h    = self.dimensions  # длина, ширина, высота кирпича
        nl, nw, nh = self.n_parts     # количество осколков по длине, ширине, высоте    
        
        self.begin_ambient_camera_rotation(rate=0.1)
        self.set_camera_orientation(phi=60*DEGREES, theta=45*DEGREES, zoom=1)
        
        
        #
        ## Основной кирпич и его ноша
        #
        self.next_section('begining', skip_animations=SceneExtension.skip(True))
        
        # Исходный кирпич
        brick = self.make_brick().shift(IN*2)

        # Кирпичи сверху (n штук), сдвинутые случайным образом
        n = 6
        
        def stack(mobj, target):
            mobj.next_to(target, OUT, buff=0).shift(np.random.uniform(-1,1) * RIGHT)
        
        bricks_above = [
            brick.copy().set_color(BLUE).set_opacity(0.5).set_stroke(opacity=0.5)
            for _ in range(n)]
        
        stack(bricks_above[0], brick)
        [ stack(bricks_above[i], bricks_above[i-1])  for i in range(1, n) ]
        
        self.play(DrawBorderThenFill(brick), run_time=3)
        self.wait()
        
        self.play(LaggedStart(
            *[FadeIn(b, shift=IN) for b in bricks_above],
            lag_ratio=0.5,
            run_time=2
        ))
        
        self.wait()

        #
        ## Осколки
        #
        self.next_section('disassembling', skip_animations=SceneExtension.skip(True))
        
        dl, dw, dh = l/nl, w/nw, h/nh

        pieces = VGroup()

        for i in range(nl):
            for j in range(nw):
                for k in range(nh):
                    # Создаём каждый осколок
                    piece = Prism(
                        dimensions=[dl, dw, dh],
                        fill_color=np.random.choice([RED_D, RED_E, MAROON_D, MAROON_E]),
                        fill_opacity=0.9,
                        stroke_color=WHITE,
                        stroke_width=1
                    )
                    
                    # Позиционируем осколок в нужном месте исходного кирпича
                    offset_x = -l/2 + dl/2 + i * dl
                    offset_y = -w/2 + dw/2 + j * dw
                    offset_z = -h/2 + dh/2 + k * dh
                    
                    piece.move_to(brick.get_center() + offset_x * RIGHT + offset_y * UP + offset_z * OUT)
                    
                    piece.set_fill(
                        opacity=0.9,
                        color=np.random.choice(
                            [RED_A, RED_B, RED_C, RED_D,
                             RED_E, LIGHT_GRAY, DARK_GRAY])
                    )
                    piece.set_stroke(color=BLUE_A)
                    
                    pieces.add(piece)
        
        [ piece.save_state() for piece in pieces ]
        
        self.play(
            FadeOut(brick),
            FadeIn(pieces),
            run_time=1.5
        )
        
        self.wait()

        
        #
        ## Разлёт осколков
        #
        explosion_force = 6
        
        directions  = np.random.uniform(-1, 1, size=(len(pieces),3))
        directions /= np.linalg.norm(directions, axis=0)
        
        axes = np.random.uniform(-1, 1, size=(len(pieces),3))
        axes /= np.linalg.norm(axes)
        
        angles = np.random.uniform(PI/4, PI/2, size=len(pieces))
        
        animations = [
            piece.animate
            .move_to(piece.get_center() + direction * explosion_force)
            .rotate(angle, axis=axis, about_point=piece.get_center())
            for piece, direction, axis, angle
            in zip(pieces, directions, axes, angles)
        ]
        
        text = Text('Ох, сколько кирпичей было сломано...')
        self.add_fixed_in_frame_mobjects(text)
        text.scale(0.6).to_edge(UP)
        
        self.play(
            Write(text),
            LaggedStart(*animations, lag_ratio=0.01),
            LaggedStart(
                *[FadeOut(b, shift=OUT) for b in bricks_above[::-1]],
                lag_ratio=0.1),
            run_time=2
        )
        self.wait(4)
        

        #
        ## Восстановление кирпича
        #
        self.next_section('reassembling', skip_animations=SceneExtension.skip(True))
        
        self.play(
            FadeOut(text, shift=OUT*0.4),
            LaggedStart(
                *[Restore(piece) for piece in pieces],
                #*[FadeOut(piece, shift=5*(np.random.rand(3) * (1,1,0) - [0.5,0.5,0])) for piece in pieces],
                run_time=2,
                lag_ratio=0.01
        ))
        self.wait()
        
        self.play(
            FadeIn(brick),
            FadeOut(pieces),
            run_time=1.5
        )
        self.wait()
        
        
        #
        ## Размеры кирпича
        #
        self.next_section('Sizing', skip_animations=SceneExtension.skip(True))
        
        self.play(brick.animate.shift(OUT*2))
        self.wait()
        
        def make_dim(start, end, direction, align_direction, text,
                     text_scale=0.7, arrow_scale=0.5, offset=1.5):
            dim = Linear_Dimension(brick.get_critical_point(start),
                                   brick.get_critical_point(end),
                                   text=TexCyr(text).scale(text_scale),
                                   direction=direction,
                                   offset=offset,
                                   outside_arrow=True,
                                   color=BLUE)
            dim.set_opacity(0.5)
            dim.next_to(brick, direction, buff=0).align_to(brick,align_direction)
            dim['text'].set_opacity(1.0)
            dim['arrow1'].scale(arrow_scale)
            dim['arrow2'].scale(arrow_scale)
            return dim
        
        dimL = make_dim(RIGHT, LEFT, UP, IN, r'$l = 25$ см')
        dimH = make_dim(OUT, IN, RIGHT, DOWN, r'$h = 6.5$ см')
        dimW = make_dim(UP, DOWN, LEFT, IN, r'$w = 12$ см')
        
        dimH['text'].rotate(PI/2, Y_AXIS).rotate(-PI/2, axis=Z_AXIS, about_point=dimH['arrow1'].get_center())
        
        self.play(
            FadeIn(dimL, shift=DOWN),
            FadeIn(dimW, shift=OUT),
            FadeIn(dimH, shift=LEFT),
            run_time=2
        )
        self.wait(2)
        
        self.change_camera_view(0, wait=5)
        self.change_camera_view(1, wait=5)
        self.change_camera_view(2, wait=5)
        self.change_camera_view(3, wait=5)
        self.change_camera_view(4, wait=5)
        
        
        #
        ## Добавляем стопку сверху и визуализируем размеры
        #
        self.next_section('Sizing', skip_animations=SceneExtension.skip(True))
        
        self.change_camera_view(5, wait=1)
        
        def stack_one_side(mobj, target):
            mobj.next_to(target, OUT, buff=0).shift(np.random.uniform(0.4, 0.8) * RIGHT)
            
        n = 3
        bricks_above = [
            brick.copy().set_color(BLUE).set_fill(opacity=0.4).set_stroke(opacity=0.6)
            for _ in range(n)]
        
        stack_one_side(bricks_above[0], brick)
        [ stack_one_side(bricks_above[i], bricks_above[i-1])  for i in range(1, n) ]
        
        self.play(LaggedStart(
            *[FadeIn(b, shift=IN) for b in bricks_above],
            lag_ratio=0.5,
            run_time=2
        ))
        
        self.wait()
        
        
        #
        ## Убираем старые размерности, добавляем новые
        #
        self.next_section('NewDimensions', skip_animations=SceneExtension.skip(True))
        
        self.stop_ambient_camera_rotation()
        self.begin_ambient_camera_rotation(rate=0.05)
        
        # Вспомогательные линии
        corner = bricks_above[-1].get_corner(UR + IN)
        corner_projection = corner.copy()
        corner_projection[2] = brick.get_critical_point(IN)[2]
        vline = DashedLine(corner, corner_projection, color=BLUE_A, stroke_opacity=0.5)
        overshoot_shadow = DashedLine(corner_projection, brick.get_corner(IN + UR), color=BLUE_A, stroke_opacity=0.5)

        # Вынос стопки
        dim_stack_overshoot = Linear_Dimension(
            brick.get_right() * [1,1,0],
            bricks_above[-1].get_right() * [1,1,0],
            text=TexCyr(r'$L$'),#.scale(0.7),
            direction=UP,
            offset=1.5,
            outside_arrow=True,
            color=BLUE)
        dim_stack_overshoot.set_opacity(0.5)
        dim_stack_overshoot.align_to(brick,IN).shift(UP)
        dim_stack_overshoot['text'].set_opacity(1.0)
        dim_stack_overshoot['arrow1'].scale(0.5)
        dim_stack_overshoot['arrow2'].scale(0.5)
        
        # Высота стопки
        dim_stack_height = Linear_Dimension(
            corner,
            corner_projection,
            text=TexCyr(r'$H$'),#.scale(0.7),
            direction=RIGHT,
            offset=1.5,
            outside_arrow=True,
            color=BLUE)
        dim_stack_height.set_opacity(0.5)
        dim_stack_height['text'].set_opacity(1.0)
        dim_stack_height['arrow1'].scale(0.5)
        dim_stack_height['arrow2'].scale(0.5)
        dim_stack_height['text'].rotate(PI/2, Y_AXIS).rotate(-PI/2, axis=Z_AXIS, about_point=dim_stack_height['arrow1'].get_center())
        
        self.play(
            *[FadeOut(d) for d in (dimL,dimH,dimW)],
            FadeIn(dim_stack_overshoot),
            FadeIn(dim_stack_height),
            Create(vline),
            Create(overshoot_shadow)
        )
        
        self.wait(5)
        
        # @todo Подогнать смену ракурсов по длительности перед визуализацией зоны нагрузки
        # Периодически меняем ракурсы
        for _ in range(5):
            self.camera_jump_during_ambient_rotation(
                theta=self.camera.get_theta() + np.random.uniform(PI/6, PI/3),
                phi = self.camera.get_phi()   + np.random.uniform(-PI/20, PI/20),
                zoom = self.camera.get_zoom() + np.random.uniform(-0.1, 0.1),
                new_rate=0.05,
                run_time=0.5
            )
            self.wait(5)
        
        
        #
        ## Визуализация локализованной зоны нагрузки
        #
        self.next_section('LoadLocalized', skip_animations=SceneExtension.skip(False))
        
        
        area = brick[1].copy().stretch(0.15, dim=0, about_edge=RIGHT)
        params = dict(offset=0.1, stroke_color=YELLOW, stroke_width=1)
        hatch1 = Hatch_lines(area, angle=PI/4, **params)
        hatch2 = Hatch_lines(area, angle=PI/4 + PI/2, **params)
        self.play(Create(hatch1), Create(hatch2))
        self.wait()
        
        # Периодически меняем ракурсы
        for _ in range(5):
            self.camera_jump_during_ambient_rotation(
                theta=self.camera.get_theta() + np.random.uniform(PI/6, PI/3),
                phi = self.camera.get_phi()   + np.random.uniform(-PI/20, PI/20),
                zoom = self.camera.get_zoom() + np.random.uniform(-0.1, 0.1),
                new_rate=0.05,
                run_time=0.5
            )
            self.wait(5)
        
        
        # Останавливаем вращение камеры
        self.stop_ambient_camera_rotation()

        

    def make_brick(self, fill_params=(RED_D, 0.9), edge_params=(WHITE, 3.0)):
        """ Создаёт кирпич """

        fill_color, fill_opacity = fill_params
        edge_color, edge_width = edge_params
        
        return Prism(dimensions=self.dimensions,
                     fill_color=fill_color,
                     fill_opacity=fill_opacity,
                     stroke_color=edge_color,
                     stroke_width=edge_width)
    
    
    def change_camera_view(self, i, run_time=2, wait=0.5):
        phi, theta, zoom = self.camera_views[i]
        self.move_camera(
            phi=phi * DEGREES,
            theta=theta * DEGREES,
            zoom=zoom,
            run_time=run_time,
            #frame_center=brick.get_center()
        )
        if wait > 0:
            self.wait(wait)

    
    def camera_jump_during_ambient_rotation(self, new_rate, phi=None, theta=None, zoom=None, run_time=None):
        self.stop_ambient_camera_rotation()
        self.move_camera(phi=phi, theta=theta, zoom=zoom, run_time=run_time)
        self.begin_ambient_camera_rotation(rate=new_rate)
    
    
    def draw_axes(self):
        """ Рисуем 3D оси """
        w = 3
        dX = w / 2
        axes = ThreeDAxes(
            x_range=(-dX, dX, 1),
            y_range=(-dX, dX, 1),
            z_range=(-dX, dX, 1),
            x_length=w,
            y_length=w,
            z_length=w
        )
        axes.set_opacity(1.0).set_color(YELLOW_A)
        
        self.play(Create(axes))
        self.wait(2)
        

#%% Тестовый рендер
if __name__ == '__main__':
    
    from helpers.render import dev_render
    
    dev_render(__file__, BrickBreak)

        