#
# 0. Завязка
#

import numpy as np

from manim import *

from movi_ext import *



#%%
SceneExtension.video_orientation = 'landscape'


#%%
class Introduction(MovingCameraScene, SceneExtension):
    def construct(self):
        
        wall = BrickWall(rows=8, cols=10)
        
        brace_L = Brace(wall, DOWN)
        label_L = Text('length').scale(0.5).next_to(brace_L, DOWN)
        grp_L = VGroup(brace_L, label_L)
        
        brace_H = Brace(wall, RIGHT)
        label_H = Text('height').scale(0.5).rotate(PI/2).next_to(brace_H, RIGHT)
        grp_H = VGroup(brace_H, label_H)
        
        self.play(Create(wall))
        
        self.play(
            FadeIn(grp_L, shift=UP),
            FadeIn(grp_H, shift=LEFT)
        )
        
        self.play(LaggedStart(
            *[FadeOut(wall.get_brick_at(col,row), shift=UR * (np.random.rand(3) - [0.5,0.5,0]))
              for row in range(8) for col in range(10)
              if col != 3
              ],
            lag_ratio=0.01),
        )
        
        # Заменяем стену на стопку
        brick = wall.get_brick_at(3,0)
        stack = BrickWall(rows=8, cols=1).align_to(brick, DL)
        
        self.remove(*wall.brick_objects)
        self.add(stack)
        
        
        self.play(FadeOut(grp_H, grp_L))
        
        brace = always_redraw(lambda:
            BraceBetweenPoints(
                stack.brick_objects[0].get_critical_point(RIGHT),
                stack.brick_objects[-1].get_critical_point(RIGHT),
                direction=DOWN
            )
        )
        label = always_redraw(lambda:
            Text('свес').scale(0.5).next_to(brace, DOWN)
        )
        dashed_line = always_redraw(lambda: DashedLine(
            stack.brick_objects[-1].get_corner(DR),
            brace.get_corner(UR),
            color=GRAY
        ))
        
        
        self.add(brace, label, dashed_line)
        
        
        for _ in range(4):
            stack.animate_bricks_random_shift_right(scene=self)
        
        
        
        # Удаляем убранные кирпичи
        #[wall.remove_brick_at(col,row) for row in range(8) for col in range(10) if col != 3]
        
        #remaining_bricks = [wall.get_brick_at(3,j)]
        # self.play(FadeOut(wall.get_column_objects(3)))
        #wall_new.animate_brick_shift(3, 0, RIGHT, scene=self)
        
        self.wait()


class BrickWall(VMobject):
    def __init__(
        self,
        rows=5,
        cols=8,
        brick_width=0.8,
        brick_height=0.4,
        brick_color=RED,
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
