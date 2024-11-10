from manim import *

from movi_ext import *


#%%
class EPiOrPiE(Scene, SceneExtension):
    
    video_orientation = 'portrait'
    
    CONFIG = dict(
        frame_height = 14 * 16/9,
        frame_width = 14
    )
    
    def construct(self):
        sign = r'\overset{?}{\gtrless}'
        sign_opacity = 0.5
        sign_color = RED
        
        # Исходный вопрос
        question = MathTex('{{e}}^{{\pi}}', sign, '{{\pi}}^{{e}}').scale(5)
        question[3].set_color(sign_color).set_opacity(sign_opacity)
        self.add(question)
        self.wait(1.0)
        
        
        # Убираем исходный вопрос наверх
        self.play(question.animate.move_to(UP*9.5))
        self.wait(0.5)
        
        # Перефразируем
        question_copy = question.copy()
        self.add(question_copy)
        text1 = MathTex('\ln{', '{{e}}^{{\pi}} }', sign, '\ln{', '{{\pi}}^{{e}} }').scale(3)
        text1[5].set_color(sign_color).set_opacity(sign_opacity)
        self.play(TransformMatchingTex(question_copy, text1))
        self.wait(0.5)
        
        # Преобразуем        
        text2 = MathTex('\pi', '\ln{', 'e', '}', sign, 'e', '\ln{', '\pi', '}').scale(3)
        text2[4].set_color(sign_color).set_opacity(sign_opacity)
        self.play(TransformMatchingTex(text1, text2))
        self.wait(0.5)
        
        
        # Делим на e*pi и сокращаем
        # TODO: Если изолировать подстроки, то появляется ошибка при рендеринге \frac{}{1}
        #text3 = MathTex('\frac{\  \pi \ln{e} }{1} \lessgtr e \ln{\pi}', substrings_to_isolate=to_isolate).scale(3)
        #text3 = MathTex('{ {{\pi}} \ln{e}} \over {\pi e}  \lessgtr {e \ln{ {{\pi}} } } \over {\pi e}').scale(3)
        text3 = MathTex('{', '\pi', '\ln{', 'e',   '}', '\over', '\pi', 'e', '}', sign,
                        '{', 'e',   '\ln{', '\pi', '}', '\over', '\pi', 'e', '}').scale(3)
        text3[9].set_color(sign_color).set_opacity(sign_opacity)
        self.play(TransformMatchingTex(text2, text3))
        self.wait(0.5)
        
        
        to_cancel = [1, 6, 11, 17]
        self.play(*[Indicate(text3[i]) for i in to_cancel])
        #self.play(*[FadeOut(text3[i]) for i in to_cancel])
        
        text4 = MathTex('{', '\ln{', 'e',   '}', '\over', 'e', '}', sign,
                        '{', '\ln{', '\pi', '}', '\over', '\pi', '}').scale(3)
        text4[7].set_color(sign_color).set_opacity(sign_opacity)

        anims = []
        replacement_list = [ i for i in range(len(text3)) if i not in to_cancel ]
        #replacement_list = list(range(len(text3)))
        #[ replacement_list.pop(i) for i in to_fade ]
        for i,i3 in enumerate(replacement_list):
            anims.append(ReplacementTransform(text3[i3],text4[i]))
        
        #self.play(TransformMatchingTex(text3, text4))  # порядок членов в анимации не гарантируется, так как есть повторяющиеся переменные
        self.play(*anims, *[FadeOut(text3[i]) for i in to_cancel])
        self.wait(0.5)
        
        
        # Расчищаем место для визуализации
        self.play(text4.animate.next_to(question, DOWN).scale(0.5))
        self.wait(0.5)
        
        
        # Строим график функции
        func = MathTex('y({{x}}) = { \ln {{x}} \over {{x}} }', color=BLUE).scale(3).shift(2*UP)
        #func.set_color_by_tex('x', WHITE)
        self.play(Write(func))
        self.wait(0.5)

        ax = Axes(x_range=[0,4], y_range=[-1,1], y_length=12,
                  x_axis_config={
                    "numbers_to_include": np.arange(0, 4.01, 1),
                    #"numbers_with_elongated_ticks": np.arange(-10, 10.01, 2),
                    }
            ).shift(3 * DOWN)
        ax_labels = ax.get_axis_labels()
        crv = ax.plot(lambda x: np.log(x) / x, x_range=[0.6,4])

        self.play(Create(ax), Create(ax_labels))
        self.play(Create(crv))
        self.wait(0.5)
            

        # Преобразуем производную, находим экстремум
        #
        # Красивое преобразование формул с латехом работает запутанно
        #
        #derv = MathTex(r'y^\prime({{x}}) = \left( { \ln {{x}} \over {{x}} } \right)^\prime = 0').scale(2).shift(1 * RIGHT + 6 * DOWN)
        # derv2 = MathTex('y^\prime({{x}}) = { 1 - \ln {{x}} \over {{x}}^2 } = 0').scale(2).shift(1 * RIGHT + 6 * DOWN)
        # derv3 = MathTex('1 - \ln {{x}} = 0').scale(2).shift(1 * RIGHT + 6 * DOWN)
        # derv4 = MathTex('x = e').scale(2).shift(1 * RIGHT + 6 * DOWN)
        derv = MathTex('y^\prime(x)', '=', r'\left( { {{\ln x}} \over {{x}} } \right)^\prime', '=', '0').scale(2).shift(1 * RIGHT + 6 * DOWN)
        derv2 = MathTex('y^\prime(x)', '=', '{', '1', '-', '{{\ln x}} \over {{x}}^2', '}', '=', '0').scale(2).shift(1 * RIGHT + 6 * DOWN)
        derv3 = MathTex('1', '-', '\ln x', '=', '0').scale(2).shift(1 * RIGHT + 6 * DOWN)
        derv4 = MathTex('x', '=', 'e').scale(2).shift(1 * RIGHT + 6 * DOWN)
        self.play(Write(derv))
        self.wait(0.5)
        self.play(TransformMatchingTex(derv, derv2))
        self.wait(0.5)
        self.play(TransformMatchingTex(derv2, derv3))
        self.wait(0.5)
        self.play(TransformMatchingTex(derv3, derv4))
        self.wait(0.5)
        
        
        # Рисуем положение экстремума
        vline = ax.get_vertical_line(ax.input_to_graph_point(np.e, crv), color=YELLOW)
        self.play(Create(vline), derv4.animate.scale(0.5*1.2).next_to(vline, LEFT))
        self.play(Circumscribe(derv4))
        self.wait(0.5)
        
        # Рисуем стрелки возрастания и убывания
        arrow_1 = Arrow(end=4 * RIGHT + 4 * UP).next_to(vline, DOWN).shift(3 * LEFT + DOWN)
        arrow_2 = Arrow(end=2 * RIGHT + 4 * DOWN).next_to(vline, DOWN).shift(2 * RIGHT + DOWN)
        sub_1 = MathTex(r'y(x) \uparrow').next_to(arrow_1, UP).shift(1.5 * DOWN)
        sub_2 = MathTex(r'y(x) \downarrow').next_to(arrow_2, UP).shift(1.5 * DOWN + 0.5 * RIGHT)
        
        arrow_1.set_opacity(0.5)
        arrow_2.set_opacity(0.5)
        sub_1.set_opacity(0.5)
        sub_2.set_opacity(0.5)
        self.play(Create(arrow_1), Write(sub_1))
        self.play(Create(arrow_2), Write(sub_2))
        self.wait(0.5)
        
        
        # Показываем точку с \pi на графике
        vline_pi = ax.get_vertical_line(ax.input_to_graph_point(np.pi, crv), color=GRAY)
        vline_pi_label = MathTex('x = \pi').scale(1.2).next_to(vline_pi, RIGHT)
        self.play(Create(vline_pi), Write(vline_pi_label))
        self.wait(0.5)
        
        
        # Расчищаем место под ответ
        grp = Group(ax, derv4, func, crv, vline, ax_labels, arrow_1, arrow_2,
                    sub_1, sub_2, vline_pi, vline_pi_label)
        self.play(grp.animate.scale(0.7).shift(3 * DOWN),
                  text4.animate.scale(2).move_to(ORIGIN + 4 * UP))
        self.wait(0.5)
        

        # Даём ответ
        self.play(Transform(text4[7], MathTex('>').scale(3).move_to(ORIGIN + 4*UP)))
        self.wait(0.5)
        
        question_answered = MathTex('{{e}}^{{\pi}}', '>', '{{\pi}}^{{e}}').scale(5).move_to(ORIGIN)
        question_answered.set_color(BLUE)
        anims = [ ReplacementTransform(question[i], question_answered[i]) for i in range(len(question)) ]
        
        self.play(FadeOut(text4), FadeOut(grp), *anims )

        #self.play(FadeOut(text4), FadeOut(grp), TransformMatchingTex(question, question_answered) )
        self.play(Circumscribe(question_answered))
        self.wait(0.5)
        
        e_pi = np.round(np.e**np.pi, 1)
        pi_e = np.round(np.pi**np.e, 1)
        text_e_pi = MathTex(f'\\approx {e_pi}').scale(2).next_to(question_answered, UP).shift(UP + 2.5 * LEFT)
        text_pi_e = MathTex(f'\\approx {pi_e}').scale(2).next_to(question_answered, DOWN + RIGHT).shift(DOWN + 2.5 * LEFT)
        self.play(Write(text_e_pi), Write(text_pi_e))
        self.wait(1.0)


#%% Тестовый рендер
if __name__ == '__main__':
    
    from helpers.render import dev_render
    
    dev_render(__file__, EPiOrPiE)
