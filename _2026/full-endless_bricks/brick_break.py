import numpy as np

from manim import *

from movi_ext import *

from manim_cad_drawing_utils import *


#%%
SceneExtension.render_all_sections = False

np.random.seed(0xDEADBEEF)


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
        
        
        ################################
        ## Основной кирпич и его ноша ##
        ################################
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

        #############
        ## Осколки ##
        #############
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

        
        #####################
        ## Разлёт осколков ##
        #####################
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
        

        ############################
        ## Восстановление кирпича ##
        ############################
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
        
        
        #####################
        ## Размеры кирпича ##
        #####################
        self.next_section('Sizing', skip_animations=SceneExtension.skip(True))
        
        self.play(brick.animate.shift(OUT*2))
        self.wait()
        
        # Рисуем размеры кирпича
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
        
        
        # Простой: меняем несколько раз позицию камеры
        self.change_camera_view(0, wait=5)
        self.change_camera_view(1, wait=5)
        self.change_camera_view(2, wait=5)
        self.change_camera_view(3, wait=5)
        self.change_camera_view(4, wait=5)
        
        
        #####################################################
        ## Добавляем стопку сверху и визуализируем размеры ##
        #####################################################
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
        
        
        #################################################
        ## Убираем старые размерности, добавляем новые ##
        #################################################
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
        
        
        ###############################################
        ## Визуализация локализованной зоны нагрузки ##
        ###############################################
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
