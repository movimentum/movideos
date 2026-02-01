#
# 2. Физическое ограничение классического решения
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
class PhysicalLimitation(ThreeDScene, SceneExtension):
    
    phi = PI / 2.5
    theta = PI / 3
    
    def construct(self):
        
        self.begin_ambient_camera_rotation()

        #
        ## Начало
        #
        self.next_section('3D-brick', skip_animations=SceneExtension.skip(False))
        
        # Оси
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
        self.set_camera_orientation(phi=self.phi, theta=self.theta)
        
        self.play(Create(axes))
        
        self.wait(2)

########################################
class AnimatedBrickTest(ThreeDScene, SceneExtension):
    def construct(self):
        # Размеры кирпича
        a, b, c = 4, 2, 1  # длина, ширина, высота
        
        # Создание кирпича
        brick = Cube(
            side_length=1,
            fill_color=RED_E,
            fill_opacity=0.9,
            stroke_color=WHITE,
            stroke_width=2
        ).scale([a, b, c])
        
        # Создание текстовых меток
        title = Text("Кирпич с размерами", font_size=36, color=YELLOW)
        title.to_edge(UP)
        
        dimensions_text = Text(
            f"Длина (a) = {a}\nШирина (b) = {b}\nВысота (c) = {c}",
            font_size=24,
            color=WHITE
        )
        dimensions_text.to_edge(DOWN)
        
        # Начальная настройка сцены
        self.add_fixed_in_frame_mobjects(title, dimensions_text)
        self.set_camera_orientation(phi=70 * DEGREES, theta=45 * DEGREES)
        
        # Анимация появления
        self.play(
            Write(title),
            Create(brick),
            Write(dimensions_text),
            run_time=2
        )
        self.wait(1)
        
        # Создание линий размеров
        # Длина (a)
        length_start = brick.get_corner(DL + IN)
        length_end = brick.get_corner(DR + IN)
        length_line = DashedLine(length_start, length_end, color=YELLOW, stroke_width=2)
        length_label = Text("a", color=YELLOW, font_size=28)
        length_label.next_to(length_line.get_center(), DOWN + OUT, buff=0.2)
        
        # Ширина (b)
        width_start = brick.get_corner(DR + IN)
        width_end = brick.get_corner(DR + OUT)
        width_line = DashedLine(width_start, width_end, color=GREEN, stroke_width=2)
        width_label = Text("b", color=GREEN, font_size=28)
        width_label.next_to(width_line.get_center(), RIGHT + OUT, buff=0.2)
        
        # Высота (c)
        height_start = brick.get_corner(DL + IN)
        height_end = brick.get_corner(UL + IN)
        height_line = DashedLine(height_start, height_end, color=BLUE, stroke_width=2)
        height_label = Text("c", color=BLUE, font_size=28)
        height_label.next_to(height_line.get_center(), LEFT + OUT, buff=0.2)
        
        # Добавление размеров
        self.play(
            Create(length_line),
            Write(length_label),
            run_time=1
        )
        
        self.play(
            Create(width_line),
            Write(width_label),
            run_time=1
        )
        
        self.play(
            Create(height_line),
            Write(height_label),
            run_time=1
        )
        
        self.wait(0.5)
        
        # Список ракурсов камеры (phi, theta, zoom)
        camera_views = [
            (90, -90, 1.3),   # Вид спереди
            (0, 0, 1.3),      # Вид сверху
            (90, 0, 1.3),     # Вид сбоку
            (60, 45, 1.2),    # Изометрический вид 1
            (120, -45, 1.3),  # Диагональный вид снизу
        ]
        
        # Анимация смены ракурсов
        for i, (phi, theta, zoom) in enumerate(camera_views):
            self.move_camera(
                phi=phi * DEGREES,
                theta=theta * DEGREES,
                zoom=zoom,
                run_time=2,
                frame_center=brick.get_center()
            )
            self.wait(0.5)  # Пауза 0.5 секунды между сменами
        
        # Финальный вид и исчезновение
        self.move_camera(
            phi=70 * DEGREES,
            theta=45 * DEGREES,
            zoom=1,
            run_time=2
        )
        self.wait(1)
        
        # Исчезновение
        self.play(
            FadeOut(brick),
            FadeOut(length_line),
            FadeOut(width_line),
            FadeOut(height_line),
            FadeOut(length_label),
            FadeOut(width_label),
            FadeOut(height_label),
            FadeOut(title),
            FadeOut(dimensions_text),
            run_time=1.5
        )


class BrickBreak(ThreeDScene, SceneExtension):
    
    dimensions    = 3, 2, 1  # длина, ширина, высота кирпича
    n_parts = 4, 3, 2  # количество осколков по длине, ширине, высоте
    
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
        brick = self.make_brick().shift(IN)

        # Кирпичи сверху (n штук), сдвинутые случайным образом
        n = 6
        
        def stack(mobj, target):
            mobj.next_to(target, OUT, buff=0).shift(np.random.uniform(-1,1) * RIGHT)
        
        bricks_above = [
            brick.copy().set_color(BLUE).set_stroke(opacity=0.2)
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
        self.next_section('Sizing', skip_animations=SceneExtension.skip(False))
        
        self.play(brick.animate.shift(OUT))
        self.wait()
        
        dimL = Linear_Dimension(brick.get_critical_point(RIGHT),
                                brick.get_critical_point(LEFT),
                                text=Text('25 см').scale(0.7),
                                direction=UP,
                                offset=1.5,
                                outside_arrow=True,
                                ext_line_offset=0,
                                color=BLUE)
        dimL.set_opacity(0.5).next_to(brick,UP,buff=0).align_to(brick,IN)
        dimL['text'].set_opacity(1.0)
        
        dimH = Linear_Dimension(brick.get_critical_point(OUT),
                                brick.get_critical_point(IN),
                                text=Text('6.5 см').scale(0.7),
                                direction=RIGHT,
                                offset=1.5,
                                outside_arrow=True,
                                # ext_line_offset=0,
                                color=BLUE)
        dimH.set_opacity(0.5).next_to(brick,RIGHT,buff=0).align_to(brick,DOWN)
        dimH['text'].set_opacity(1.0).rotate(PI/2, Y_AXIS).rotate(-PI/2, axis=Z_AXIS, about_point=dimH['arrow1'].get_center())
        
        dimW = Linear_Dimension(brick.get_critical_point(UP),
                                brick.get_critical_point(DOWN),
                                text=Text('12 см').scale(0.7),
                                direction=LEFT,
                                offset=1.5,
                                outside_arrow=True,
                                ext_line_offset=0,
                                color=BLUE)
        dimW.set_opacity(0.5).next_to(brick,LEFT,buff=0).align_to(brick,IN)
        dimW['text'].set_opacity(1.0)
        
        
        self.play(
            FadeIn(dimL, shift=DOWN),
            FadeIn(dimW, shift=OUT),
            FadeIn(dimH, shift=LEFT),
            run_time=2
        )
        self.wait(20)





        
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


        
#%% Тестовый рендер
if __name__ == '__main__':
    
    from helpers.render import dev_render
    
    dev_render(__file__, BrickBreak)

        