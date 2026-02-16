import sys

from helpers.render import prod_render


#%% Пути
root = '_2026/full-endless_bricks'
fn = '2-PhysicalLimitation.py'
sname = 'BrickBreak'


#%% Рендерим
sys.path.append(root)
fpath = f'{root}/{fn}'

prod_render(fpath, sname, preview=False, render_all_sections=True)
