#
# 3. Заключение
#
import numpy as np

from manim import *

from movi_ext import *

from brick_break import BrickBreak


#%%
SceneExtension.render_all_sections = False

np.random.seed(0xDEADBEEF)


#%%
class Conclusion(BrickBreak):
    
    def construct(self):
        
        l, w, h    = self.dimensions  # длина, ширина, высота кирпича
        
        # Запускаем вращение камеры
        self.set_camera_orientation(phi=60*DEGREES, theta=230*DEGREES, zoom=0.9)
        self.begin_ambient_camera_rotation(rate=0.015)
        
        
        # Исходный кирпич
        brick = self.make_brick().shift(IN*2)
        
        # Кирпичи сверху (n штук), сдвинутые случайным образом
        n = 5
        stack = [
            brick.copy()
            .set_color(BLUE)
            .set_opacity(0.4)
            .set_stroke(opacity=0.4) for _ in range(n)
        ]
        
        def align(mobj, base, idx):
            mobj.next_to(base, OUT, buff=0).shift(l/2 * 1/idx * RIGHT)
        
        align(stack[0], brick, n)
        [align(stack[i], stack[i-1], n-i) for i in range(1,n)]
        
        self.play(Succession(
            Create(brick),
            LaggedStart(*[FadeIn(s, shift=2*IN) for s in stack], lag_ratio=0.5)
        ))
        self.wait()
        
        # Убираем нижний кирпич из стопки, и стопка падает, но отскакивает
        def remove_bottom_and_back(n, wait_before_recreate=1, success=False):
            [s.save_state() for s in stack]

            dn = 1 if success else 0
            
            shift = h * IN * (n + dn)
            rf_forward = rate_functions.ease_out_bounce
            ft_backward = smooth
            
            # Вперёд
            self.play(LaggedStart(
                *[FadeOut(s, scale=0.5) for s in stack[:n]],
                *[s.animate(rate_func=rf_forward).shift(shift) for s in stack[n:]],
                lag_ratio=0.2
            ), run_time=2)
            
            self.wait(wait_before_recreate)
            
            winners = [s.copy().set_color(GOLD) for s in stack[n:]] if success else []
            
            if success:
                [s.saved_state.set_opacity(0.1).set_stroke(opacity=0.1) for s in stack]
                for s in stack[:n]:
                    s.set_opacity(0.2).set_stroke(opacity=0.2)
                for s in stack[n:]:
                    s = s.saved_state
            
            # Назад
            self.play(LaggedStart(
                # *[w.animate.set_color(GOLD) for w in winners],
                *[Restore(s) for s in stack[n:][::-1]],
                *[FadeIn(s, scale=0.5) for s in stack[:n][::-1]],
                lag_ratio=0.2
            ), run_time=2)
            self.wait()
            
            return winners

        
        # Вот здесь анимируем исключение кирпичей
        remove_bottom_and_back(1)
        remove_bottom_and_back(3)
        winners = remove_bottom_and_back(4, success=True)
        
        # Выделяем пятый кирпич как первый выступивший за край нижнего кирпича
        winner_top_face = winners[0][1]
        upper_bot_face = stack[-1][0]
        
        lines = VGroup()
        [lines.add(DashedLine(
            upper_bot_face.get_corner(d),
            winner_top_face.get_corner(d),
            color=GOLD_A,
            stroke_opacity=0.4
         )) for d in (DL,DR,UL,UR)]
        
        self.play(
            Create(lines),
            *[FadeIn(w, shift=IN) for w in winners]
        )
        self.wait()
        
        
        # Завершаем сцену
        self.play(LaggedStart(
            Uncreate(lines),
            *[FadeOut(s, shift=np.random.choice((-1,1))*RIGHT) for s in stack],
            lag_ratio=0.2            
        ))
        self.wait()
        
        grp = VGroup(brick, *[winners])
        
        self.play(grp.animate.scale(1.2).move_to(ORIGIN))
        self.wait()
        self.play(grp.animate(run_time=2).scale(0.9))
        self.wait()
        self.play(grp.animate(rate_func=rate_functions.ease_out_bounce, run_time=2).scale(0.7))
        self.wait()
        self.play(FadeOut(grp, scale=0.2))
        self.wait()
        
        self.stop_ambient_camera_rotation()


#%% Тестовый рендер
if __name__ == '__main__':
    
    from helpers.render import dev_render
    
    dev_render(__file__, Conclusion)
