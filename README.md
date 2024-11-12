# Описание

Здесь выложены коды, сопроводительные материалы и инструменты, которые
использовались при создании видео для youtube-канала
[Movimentum](https://www.youtube.com/@movicave)
и теперь открыто распространяются под лицензией
[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed).

Математические анимации созданы с помощью движка
[manim-community](https://www.manim.community/)


# Требования
`manim 0.18.1`
`python 3.11`

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
