# Цель: создание конфигурации для рендеринга видео
# 
# Предполагается работа внутри Spyder Project, который добавляет в sys.path
# путь до корневого каталога данного проекта
# 

#%% Импорт
from os.path import join, dirname, relpath
import sys

from manim import config


#%% Константы
media_root_dir = join(sys.path[-1], 'media')

video_settings = dict(
    prod = (3840, 2160, 60),
    dev = (854, 480, 15)
)


#%% Функции
def update_config_for_scene(
        quality='prod',
        orientation='landscape',
        media_subdir=None,
        save_sections=True
    ):
    
    # Сохранение секций
    config.save_sections = save_sections

    # Настройки директорий
    config.media_dir = (
        media_root_dir
        if not media_subdir else 
        join(media_root_dir, media_subdir)
    )
    
    # Настройки кадра
    pw, ph, fps = video_settings[quality]
    fw = 8 * 16 / 9
    fh = 8
    if orientation == 'portrait':
        pw, ph = ph, pw
        fw, fh = fh, fw
    elif orientation != 'landscape':
        msg = (
            'orientation should be landscape' +
            f'or portrait, but {orientation} was given'
        )
        raise ValueError(msg)
    
    config.pixel_width = pw
    config.pixel_height = ph
    config.frame_height = fh
    config.frame_width = fw
    config.frame_rate = fps


def get_media_dir_for_file(fpath):
    return dirname(relpath(fpath, sys.path[-1]))


def update_config_for_dev(module_path, orientation):
    media_subdir = get_media_dir_for_file(module_path)
    
    update_config_for_scene(
        quality='dev',
        orientation=orientation,
        media_subdir=media_subdir,
        save_sections=False
    )
