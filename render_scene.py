from helpers.render import prod_render


fpath = '_test_scenes/creatures/creature_unity.py'
sname = 'CreatureUnityTest'

prod_render(fpath, sname, preview=False, render_all_sections=True)
