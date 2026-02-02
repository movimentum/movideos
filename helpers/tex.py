#
## Класс для latex-формул с русскими символами
#

from manim import Tex, TexTemplate


class TexCyr(Tex):
    
    _PREAMBLE = r"""\usepackage[english,russian]{babel}
\usepackage{amsmath}
\usepackage{amssymb}"""

    _template = TexTemplate(preamble=_PREAMBLE)

    
    def __init__(self, *args, **kwargs):
        
        kwargs['tex_template'] = self._template
        
        super().__init__(*args, **kwargs )
        
        
    