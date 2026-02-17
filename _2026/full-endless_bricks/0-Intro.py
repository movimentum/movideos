#
# 0. Завязка
#

import numpy as np

from manim import *

from movi_ext import *


#%%
SceneExtension.video_orientation = 'landscape'

np.random.seed(0xDEADBEEF)


#%%
class Introduction(MovingCameraScene, SceneExtension):
    def construct(self):
        
        # Запускаем фон
        shapes = BGSimpleShapes()
        self.play(shapes.fadein())
        shapes.start_swinging()
        
        self.camera.frame.save_state()

        
        # Строим стену
        wall = BrickWall(rows=8, cols=10)
        
        brace_H = Brace(wall, RIGHT)
        label_H = MathTex('h \\rightarrow max ?', color=BLUE).rotate(PI/2).next_to(brace_H, RIGHT)
        grp_H = VGroup(brace_H, label_H).set_color(BLUE)
        
        self.play(Create(wall))
        self.play(FadeIn(grp_H, shift=LEFT, scale=0.5))
        self.wait()
        
        # Наклонить голову на бок?
        grp = VGroup(wall, grp_H)
        self.play(
            Rotate(grp, -PI/2),
            self.camera.frame.animate.set(height=1.1*grp.get_width())
        )
        self.wait()
        
        brace_L = Brace(wall, LEFT)
        label_L = MathTex('l \\rightarrow max ?').rotate(-PI/2).next_to(brace_L, LEFT)
        grp_L = VGroup(brace_L, label_L).set_color(BLUE)
        
        self.play(FadeIn(grp_L, shift=UP, scale=0.5))
        self.wait()
        
        grp.add(grp_L)
        
        self.play(
            Rotate(grp, PI/2),
            Restore(self.camera.frame)
        )
        self.wait()

        # Разбираем стену, оставляем один столбец
        self.play(LaggedStart(
            *[FadeOut(wall.get_brick_at(col,row), shift=UR * (np.random.rand(3) - [0.5,0.5,0]))
              for row in range(8) for col in range(10)
              if col != 3
              ],
            lag_ratio=0.01),
            Unwrite(grp_H),
            Unwrite(grp_L),
        )
        self.wait()

        # Заменяем стену на новую стопку кирпичей, смещённых вправо
        brick = wall.get_brick_at(3,0)
        stack = BrickWall(rows=8, cols=1).align_to(brick, DL)
        self.remove(*wall.brick_objects)
        self.add(stack)

        self.play(LaggedStart(*[FadeOut(
            brick,
            shift=2.0*RIGHT*(np.random.rand(3)-[0.5,0.5,0])) for brick in stack],
            lag_ratio=0.01
        ))
        self.wait()

        self.play(LaggedStart(
            *[FadeIn(brick, shift=DOWN) for brick in stack],
            lag_ratio=0.5
        ))
        self.wait()
        
        stack.animate_bricks_random_shift_right(scene=self)
        
        
        # Смещаем стопку и вместе с ней двигаем размер свеса
        brace_frozen = BraceBetweenPoints(
            stack.brick_objects[0].get_critical_point(RIGHT),
            stack.brick_objects[-1].get_critical_point(RIGHT),
            direction=DOWN
        )

        label_frozen = MathTex('L').next_to(brace_frozen, DOWN)

        dashed_line_frozen = DashedLine(
            stack.brick_objects[-1].get_corner(DR),
            brace_frozen.get_corner(UR),
            color=GRAY
        )

        self.play(
            Write(brace_frozen),
            Write(label_frozen),
            Create(dashed_line_frozen)
        )
        self.wait()
        
        brace = always_redraw(lambda: BraceBetweenPoints(
            stack.brick_objects[0].get_critical_point(RIGHT),
            stack.brick_objects[-1].get_critical_point(RIGHT),
            direction=DOWN
        ))

        label = always_redraw(lambda: MathTex('L').next_to(brace, DOWN))
        
        dashed_line = always_redraw(lambda: DashedLine(
            stack.brick_objects[-1].get_corner(DR),
            brace.get_corner(UR),
            color=GRAY
        ))
        
        self.remove(brace_frozen, label_frozen, dashed_line_frozen)        
        self.add(brace, label, dashed_line)
        
        # То самое место, где стопка двигается
        for _ in range(4):
            stack.animate_bricks_random_shift_right(scene=self)
        
        
        # Готовим вопрос о наибольшем свесе
        frozen_label = label.copy()
        self.remove(label)
        self.add(frozen_label)
        
        new_label = MathTex('L', '\\rightarrow max').next_to(brace, DOWN)
        self.play(LaggedStart(
            *[ReplacementTransform(frozen_label, new_label[0]),Write(new_label[1])],
            lag_ratio=0.4
        ))
        self.wait()
        
        
        # Вопросики сыпятся
        n = 40
        positions  = np.random.rand(n, 3) - 0.5
        positions *= [12,6,0] 
        scales = np.random.rand(n) * 2.5
        q_marks = [
            MathTex(r'?').scale(sc).set_color(BLUE).set_opacity(0.5).move_to(pos)
            for sc,pos in zip(scales,positions)
        ]
        self.play(LaggedStart(
            *[GrowFromCenter(q_mark) for q_mark in q_marks],
            lag_ratio=0.05
        ))
        self.wait()
        
        
        # Завершаем введение
        shapes.stop_swinging()

        ani_g0 = AnimationGroup(
            FadeOut(new_label, shift=DOWN),
            FadeOut(brace, shift=DOWN, scale=0.5),
            Uncreate(dashed_line),
            lag_ratio=0.25,
            run_time=2
        )
        ani_g1 = AnimationGroup(
            *[FadeOut(brick, shift=UR*(np.random.rand(3) - 0.5)) for brick in stack],
            lag_ratio=0.25,
            run_time=2
        )
        ani_g2 = AnimationGroup(
            self.camera.frame.animate.set(width=wall.get_height() * 1.0),
            run_time=4,
            rate_func=linear
        )
        ani_g3 = AnimationGroup(
            *[FadeOut(q_mark, scale=0.5) for q_mark in q_marks],
            lag_ratio=0.05,
            run_time=3.5
        )
        
        self.play(ani_g0, ani_g1, ani_g2, ani_g3, shapes.fadeout_with_random_shift())
        self.wait()


#%% Стена из кирпичей
class BrickWall(VMobject):
    def __init__(
        self,
        rows=5,
        cols=8,
        brick_width=0.8,
        brick_height=0.4,
        brick_color=RED_E,
        mortar_color=WHITE,
        mortar_width=0.02,
        offset_even_rows=True,
        show_labels=False,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        # Сохраняем параметры
        self.rows = rows
        self.cols = cols
        self.brick_width = brick_width
        self.brick_height = brick_height
        self.brick_color = brick_color
        self.mortar_color = mortar_color
        self.mortar_width = mortar_width
        self.offset_even_rows = offset_even_rows
        self.show_labels = show_labels
        
        # Создаем двумерный массив для хранения кирпичей
        self.bricks = [[None for _ in range(cols)] for _ in range(rows)]
        self.brick_objects = []  # Все объекты кирпичей
        
        # Создаем стену
        self.create_wall()
        
        # Добавляем все кирпичи в группу VMobject
        self.add(*self.brick_objects)
    
    def create_wall(self):
        """Создает стену из кирпичей"""
        for j in range(self.rows):
            for i in range(self.cols):
                # Создаем прямоугольник-кирпич
                brick = Rectangle(
                    width=self.brick_width - self.mortar_width,
                    height=self.brick_height - self.mortar_width,
                    fill_color=self.get_brick_color(i, j),
                    fill_opacity=1.0,
                    stroke_color=self.mortar_color,
                    stroke_width=self.mortar_width * 10,
                    stroke_opacity=1.0
                )
                
                # Позиционируем кирпич
                pos = self.get_brick_position(i, j)
                brick.move_to(pos)
                
                # Сохраняем кирпич
                self.bricks[j][i] = brick
                self.brick_objects.append(brick)
                
                # Добавляем подпись если нужно
                if self.show_labels:
                    label = Text(f"({i},{j})", font_size=14, color=WHITE)
                    label.move_to(pos)
                    self.brick_objects.append(label)
    
    def get_brick_position(self, i, j):
        """Возвращает позицию кирпича с учетом смещения"""
        # Базовые координаты
        x = i * self.brick_width - (self.cols * self.brick_width) / 2 + self.brick_width/2
        y = j * self.brick_height - (self.rows * self.brick_height) / 2 + self.brick_height/2
        
        # Смещение для шахматного порядка
        if self.offset_even_rows and j % 2 == 1:
            x += self.brick_width / 2
        
        return np.array([x, y, 0])
    
    def get_brick_color(self, i, j):
        """Возвращает цвет кирпича"""
        if isinstance(self.brick_color, (list, tuple)):
            # Если передан список цветов
            color_idx = (i + j) % len(self.brick_color)
            return self.brick_color[color_idx]
        elif callable(self.brick_color):
            # Если передана функция
            return self.brick_color(i, j, self.rows, self.cols)
        else:
            # Если передан один цвет
            return self.brick_color
    
    def get_brick_at(self, i, j):
        """Возвращает кирпич по индексам (i, j)"""
        if 0 <= j < self.rows and 0 <= i < self.cols:
            return self.bricks[j][i]
        return None
    
    def highlight_brick(self, i, j, color=YELLOW, animate=True, scene=None):
        """Подсвечивает кирпич по индексам"""
        brick = self.get_brick_at(i, j)
        if brick:
            if animate and scene:
                scene.play(brick.animate.set_fill(color, opacity=1.0))
            else:
                brick.set_fill(color, opacity=1.0)
            return brick
        return None
    
    def reset_brick_color(self, i, j, animate=True, scene=None):
        """Восстанавливает исходный цвет кирпича"""
        brick = self.get_brick_at(i, j)
        if brick:
            original_color = self.get_brick_color(i, j)
            if animate and scene:
                scene.play(brick.animate.set_fill(original_color, opacity=1.0))
            else:
                brick.set_fill(original_color, opacity=1.0)
    
    def get_brick_center(self, i, j):
        """Возвращает центр кирпича по индексам"""
        brick = self.get_brick_at(i, j)
        if brick:
            return brick.get_center()
        return None
    
    def animate_brick_shift(self, i, j, direction, distance=0.2, scene=None):
        """Анимирует смещение кирпича"""
        brick = self.get_brick_at(i, j)
        if brick and scene:
            scene.play(brick.animate.shift(direction * distance))
            scene.play(brick.animate.shift(-direction * distance))
    
    def get_grid_coordinates(self, point):
        """Возвращает координаты кирпича, в котором находится точка"""
        # Преобразуем точку в локальные координаты стены
        local_point = point - self.get_center()
        
        # Вычисляем индексы
        i = int((local_point[0] + (self.cols * self.brick_width) / 2) / self.brick_width)
        j = int((local_point[1] + (self.rows * self.brick_height) / 2) / self.brick_height)
        
        # Проверяем границы
        if 0 <= i < self.cols and 0 <= j < self.rows:
            # Учитываем смещение строк
            if self.offset_even_rows and j % 2 == 1:
                local_x = local_point[0] - self.brick_width / 2
                i = int((local_x + (self.cols * self.brick_width) / 2) / self.brick_width)
            
            if 0 <= i < self.cols:
                return (i, j)
        
        return None

    
    def animate_bricks_random_shift_right(self, max_displacement=0.8, scene=None):
        """ Возвращает столбец из кирпичей """
        if scene == None:
            return
        
        animations = []
        
        displacements = np.cumsum(np.random.rand(self.rows) * max_displacement)
        displacements -= displacements[0]
        
        base_brick = self.brick_objects[0]
        
        for shift, brick in zip(displacements, self.brick_objects):
            ani = brick.animate.align_to(base_brick, LEFT).shift(shift * RIGHT)
            animations.append(ani)
        
        scene.play(*animations)
            
            
#%% Тестовый рендер
if __name__ == '__main__':
    
    from helpers.render import dev_render
    
    dev_render(__file__, Introduction)
