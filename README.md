# Описание

Здесь выложены коды, сопроводительные материалы и инструменты, которые
использовались при создании видео для youtube-канала
[Movimentum](https://www.youtube.com/@movicave)
и теперь открыто распространяются под лицензией
[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed).

Математические анимации созданы с помощью движка
[manim-community](https://www.manim.community/)


# Требования
`manim 0.19.1`
`python 3.11, 3.13`

Имейте в виду, что со временем старые сцены могут прекратить рендериться из-за
изменения различных компонентов (например, в папке `custom`),
которые необходимы для них.


# Использование

Склонируйте репозиторий на локальный компьютер. Анимируемые сцены находятся
в папках `_{год}` и `_test_scenes`.

Для успешной сборки следует добавить путь до корневого каталога репозитория
к переменной окружения `PYTHONPATH`.

Автор использует дистрибутив-экосистему [Анаконда](https://www.anaconda.com/)
и работает в python-среде разработки **Spyder**, используя spyder-projects.
В этом случае Spyder сам выставит нужное значение в `PYTHONPATH`.

Для удобного рендеринга видео есть два способа. В обоих случаях результат
сохраняется в папке `media` корневого каталога.


### Создание видео в 4k 
Запустите скрипт `render_scene.py`, указав в нём относительный путь до файла
сцены и имя сцены

```python
fpath = '_test_scenes/creatures/creature_unity.py'
sname = 'CreatureUnityTest'
```

### Быстрый просмотр в низком качестве
Внизу каждого скрипта со сценой обычно будет бойлерплейт типа

```python
#%% Тестовый рендер
if __name__ == '__main__':
    
    dev_render(__file__, SceneName)
```

Требуется поменять `SceneName` на имя интересующей сцены и запустить скрипт.


# Дополнительные возможности

## Пропуск рендеринга
При создании сложных сцен удобно пропускать их части при рендеринге для
экономии времени. Для этого существует метод сцены
`self.next_section('section_name', skip_animations=True)`

В данном репозитории имеется вспомогательный класс `SceneExtension`, который
поможет не просто игнорировать рендеринг конкретного раздела, но и даст
возможность разом игнорировать все затребованные в коде пропуски рендеринга.

```python

from manim import *
from movi_ext import *


# Если требуется рендерить все разделы не зависимо от того, что указано в
# параметрах self.next_section, нужно выставить здесь True
SceneExtension.render_all_sections = False

class SceneWithSectionRendering(Scene, SceneExtension):  # наследуем класс-помощник
    
    def construct(self):

        self.next_section('first_part', skip_animations=SceneExtension.skip(False))
        # Эта часть не будет рендериться при использовании dev_render
        
        self.next_section('first_part', skip_animations=SceneExtension.skip(True))
        # А эта часть будет
```

## Кириллица в формулах

Для использования кириллических символов в формулах удобно воспользоваться
классом `TexCyr`

```python

from manim import Scene
from movi_ext import TexCyr

class TestScene(Scene):
    def construct(self):
        
        eq = TexCyr(r'$a = 25$ см')
        
        self.add(eq)
        self.wait()
```
