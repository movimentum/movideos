# Цель: создание конфигурации для рендеринга видео
# 
# Предполагается работа внутри Spyder Project, который добавляет в sys.path
# путь до корневого каталога данного проекта
# 

#%% Импорт
import os

from manim import config


#%% Константы
proj_dir = os.environ['PYTHONPATH'].split(os.pathsep)[-1]
media_root_dir = os.path.join(proj_dir, 'media')

video_settings = dict(
    prod = (3840, 2160, 60),
    dev = (854, 480, 15)
)


#%% Функции
def update_config_for_scene(
        quality='prod',
        orientation='landscape',
        media_subdir=None,
        save_sections=True,
        config_aux=None,
    ):
    
    # Сохранение секций
    config.save_sections = save_sections

    # Настройки директорий
    config.media_dir = (
        media_root_dir
        if not media_subdir else 
        os.path.join(media_root_dir, media_subdir)
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
    
    if config_aux:
        config.update(config_aux)


def get_media_dir_for_file(fpath):
    return os.path.dirname(os.path.relpath(fpath, proj_dir))


def update_config_for_dev(module_path, orientation, config_aux=None):
    media_subdir = get_media_dir_for_file(module_path)
    
    update_config_for_scene(
        quality='dev',
        orientation=orientation,
        media_subdir=media_subdir,
        save_sections=False,
        config_aux=config_aux
    )
