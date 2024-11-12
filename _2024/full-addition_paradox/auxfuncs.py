#
# Дополнительные функции для использования при создании анимаций
#

#%%
from manim import *
import re


#%%
def split2syms(s):
    """ Из строки-формулы делает массив
        a = b + ( c * d - e ) ^ 2
    """
    # Удаляем двойные пробелы
    s_no_mult_spaces = re.sub(' +', ' ', s)
    return s_no_mult_spaces.split(' ')


def get_tex_split(s):
    """ Формируем вспомогательную строку для использования при поэлементной анимации """
    end = '\t'
    spl = split2syms(s)
    num = list(range(len(spl)))
    
    print('#   ', end='')
    for i,v in zip(num, spl):
        n_symbols = max(len(str(i)), len(v))
        print(f'{i:{n_symbols}}', end=end)
        
    print()
    print('#   ', end='')
    for i,v in zip(num, spl):
        n_symbols = max(len(str(i)), len(v))
        print(f'{v:{n_symbols}}', end=end)


def shapes_to_background(n=100, scale=0.25, opacity=0.1,
                         expand=(15,15), center=(0,0), seed=0):
    """ Создаёт различные фигуры для заполнения пустого фона """
    np.random.seed(seed)
    shapes = (Triangle, Square, Circle)
    bg_shapes = []
    for i in range(n):
        side_shift = (np.random.rand() - 0.5) * expand[0]
        vert_shift = (np.random.rand() - 0.5) * expand[1]
        total_shift  = (center[0] + side_shift) * RIGHT
        total_shift += (center[1] + vert_shift) * UP
        shape = np.random.choice(shapes)
        _color = np.random.choice(color.manim_colors._all_manim_colors)
        element = shape().scale(scale).shift(total_shift).set_opacity(opacity).set_color(_color)
        bg_shapes.append(element)
    return bg_shapes


def questions_to_background(n, camera_frame, scale=2, color=RED, opacity=0.5, seed=0):
    np.random.seed(seed)
    positions = (np.random.rand(n, 3) - 0.5) * camera_frame.get_width()
    positions += camera_frame.get_center()
    positions[:,2] = 0
    scales = np.random.rand(n) * scale
    q_marks = [MathTex(r'?').scale(sc).set_color(color).set_opacity(opacity).move_to(pos) for sc,pos in zip(scales,positions)]
    return q_marks


#%% Распечатаем нумерацию элементов формулы для отладки
if __name__ == '__main__':
    raw = '1 - {1 \\over 2} + {1 \\over 3} - {1 \\over 4} + {1 \\over 5} + {1 \\over 6} + \ldots = \\ln 2'
    get_tex_split(raw)
