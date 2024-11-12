#
# Искатель путей в проекте
#

import os

from .config import repo_root


#%%
class PathFinder:
    
    def __init__(self):
        self.root = repo_root
    
    def get_svg_path(self, name: str, group: str = '') -> str:
        fn = name if not name.endswith('.svg') else name[:-4]
        fpath = os.path.join(self.root, 'custom', 'svg', group, fn)
        return fpath
    
    def get_svgpath_person(self, name: str) -> str:
        return self.get_svg_path(name, group='persons')
    
    def get_svgpath_object(self, name: str) -> str:
        return self.get_svg_path(name, group='objects')

    def get_svgpath_simple(self, name: str) -> str:
        return self.get_svg_path(name, group='simple')


#%%
pather = PathFinder()