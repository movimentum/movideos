#
# Сходимость к произвольному числу
#

from manim import *

from movi_ext import *

from auxfuncs import split2syms, shapes_to_background
from number_bag import NumberBag
from series import Series


#%%
SceneExtension.video_orientation = 'landscape'


#%% Демонстрация сходимости к любому числу путём "туда-сюда"
class ConvergeToAny(ZoomedScene, SceneExtension):
    def __init__(self, **kwargs):
        ZoomedScene.__init__(
            self,
            zoom_factor=0.2,
            zoomed_display_height=4,
            zoomed_display_width=8,
            image_frame_stroke_width=20,
            zoomed_camera_config={
                "default_frame_stroke_width": 3,
            },
            **kwargs
        )
        
        self.ax = None
        self.extra_label = None
        

    def construct(self):
        self.add_shapes_to_background()
        
        #
        ## Случай 1: alim = 1
        #
        alim = 1
        ax, lim_line, line_graph, labels, ser = self.prepare_case(42, alim)
        dots = line_graph.submobjects[1]
        grp = VGroup(ax, line_graph, lim_line, labels)
        self.play(Create(grp[:-1]))
        self.wait()
        

        # Close-up
        self.camera.frame.save_state()
        subgrp_labels = Group(*labels[:5])
        self.play(self.camera.frame.animate.move_to(subgrp_labels).set(width=2*subgrp_labels.width))
        self.wait()
        
        #   0	1	2	3	    4	5	6	7	8	9	   10	11	12	13	14	15	   16	17	18	19	20	21	   22	23	24	25	26	27	   28	29	30	31	32	33	   34	35	36	37	38	39	   40	41	42	43	44	45	   46	47	48	49	50	51	   52	53	54	55	56	57	   58	59	60	61	62	63	   64	65	66	67	    68	69	 70	71	
        #   1	-	{	1	\over	2	}	+	{	1	\over	3 	} 	- 	{ 	1 	\over	4 	} 	+ 	{ 	1 	\over	5 	} 	- 	{ 	1 	\over	6 	} 	+ 	{ 	1 	\over	7 	} 	- 	{ 	1 	\over	8 	} 	+ 	{ 	1 	\over	9 	} 	- 	{ 	1 	\over	10	} 	+ 	{ 	1 	\over	11	} 	- 	{ 	1 	\over	12	} 	+ 	\ldots	= 	\ln	2 	
        eq_raw = '1'
        for i in range(2, 2+11):
            operation = ' + ' if i % 2 else ' - '
            element = '{ 1 \over ' + f'{i}' + ' }'
            eq_raw += operation
            eq_raw += element
        eq_raw += ' + \ldots = \ln 2'
        eq_sym = split2syms(eq_raw)
        eq = MathTex(*eq_sym)
        eq.set(width=1.3*subgrp_labels.width)
        eq.move_to(self.camera.frame.get_corner(UR) + 0.15*DL, UR)
        self.play(Write(eq))
        self.wait()
        
        
        #
        # Добавляем 2 мешка с положительными и отрицательными элементами
        #
        bag_pos = NumberBag(GREEN, GREEN_A, GREEN_E, 5, 5, 'положительные слагаемые')
        bag_neg = NumberBag(RED, RED_A, RED_E, 5, 5, 'отрицательные слагаемые')
        bag_neg.next_to(bag_pos, RIGHT)
        bag_grp = VGroup(bag_pos, bag_neg)
        bag_grp.set(width = 0.25 * eq.width)
        bag_grp.next_to(eq, DOWN, buff=SMALL_BUFF).align_to(eq, RIGHT)
        self.play(FadeIn(bag_grp, scale=0),
                  rate_func=rate_functions.ease_out_back)
        self.wait()
        

        #
        # Объясняем формирование графика
        #        
        src_pos = ((0,),) + tuple([tuple(range(i,i+6)) for i in (7,19,31,43)])
        src_pos_flat = [x for xx in src_pos for x in xx]
        eq_pos = [[eq[i] for i in ii] for ii in src_pos]
        src_neg = tuple([tuple(range(i,i+6)) for i in (1, 13, 25)])
        src_neg_flat = [x for xx in src_neg for x in xx]
        eq_neg = [[eq[i] for i in ii] for ii in src_neg]
        eq_all = [eq_pos[:2], eq_neg[0:1], eq_pos[2:3], eq_neg[1:2], eq_pos[3:], eq_neg[2:3]]
        src_rem = set(range(len(eq))) - set(src_neg_flat) - set(src_pos_flat)


        for i, (dot, label, eq_sub) in enumerate(zip(dots[:6], labels[:6], eq_all)):
            is_pos = not i % 2
            n = len(eq_sub)
            if is_pos:
                c_to_remove = bag_pos.remove_circles(n)
                c = GREEN
            else:
                c_to_remove = bag_neg.remove_circles(n)
                c = RED
            self.add(*c_to_remove)  # чтобы удалённые окружности не пропадали из сцены
            
            eq_sub_flat = [x for xx in eq_sub for x in xx]
            self.play(Succession(
                Flash(dot, color=c, line_stroke_width=1, run_time=0.5),
                Group(*eq_sub_flat).animate.set_color(c).scale(1.2).shift(0.1*DOWN),
                VGroup(*c_to_remove).animate.shift(0.1 * UP).scale(1.1),
            ))
            self.play(
                *[FadeOut(*sub, target_position=label.get_center()) for sub in eq_sub],
                ReplacementTransform(VGroup(*c_to_remove), label),
            )

        #
        # Удаляем все остальные слагаемые и лишние элементы
        #
        bag_pos_circles = bag_pos.remove_remaining_circles()
        bag_neg_circles = bag_neg.remove_remaining_circles()
        self.play(
            LaggedStart(
                *[FadeOut(eq[i], target_position=dots[6], scale=0.5) for i in src_rem],
                lag_ratio=0.05
            ),
            LaggedStart(
                *[FadeOut(ccl, target_position=dots[6], scale=0.5) for ccl in bag_pos_circles],
                lag_ratio=0.05
            ),
            LaggedStart(
                *[FadeOut(ccl, target_position=dots[6], scale=0.5) for ccl in bag_neg_circles],
                lag_ratio=0.05
            ),
        )
        
        self.wait()
        self.play(FadeOut(*labels[:6]), FadeOut(bag_grp))

            
        #
        # Возвращаемся и смотрим на сходимость
        #
        c1 = grp.get_center()
        grp.move_to(ORIGIN)
        c2 = grp.get_center()
        dc = c2 - c1
        grp[:-1].shift(-dc)
        
        self.play(
            self.camera.frame.animate.move_to(ORIGIN).set(width=grp.width + LARGE_BUFF),
            grp[:-1].animate.move_to(ORIGIN)
        )
        self.wait()

        
        # Демонстрируем увеличивающую камеру
        self.zoomed_camera.frame.move_to(ax.c2p(0.5,alim), ORIGIN)
        self.zoomed_display.move_to(self.camera.frame.get_top(), UP).shift(MED_LARGE_BUFF * DOWN)
        self.activate_zooming(animate=True)
        self.wait()
        
        # Смотрим на последовательность вдоль предельной линии + в нескольких местах
        self.play(
            self.zoomed_camera.frame.animate.align_to(ax, RIGHT),
            LaggedStart(*[FadeIn(label, scale=2) for label in grp[-1]], lag_ratio=0.2),
            run_time=5,
            rate_func=linear
        )
        self.wait()
        self.play(self.zoomed_camera.frame.animate.move_to(ax.c2p(10,alim), ORIGIN))
        self.wait()
        self.play(self.zoomed_camera.frame.animate.move_to(ax.c2p(39,alim), ORIGIN))
        self.wait()
        self.play(self.zoomed_camera.frame.animate.move_to(ax.c2p(26,alim), ORIGIN))
        self.wait()
        
        
        #
        ## Случай 2: alim=ln2
        #
        alim = np.log(2)
        self.play(
            FadeOut(grp[1:]),
            self.zoomed_camera.frame.animate.move_to(ax.c2p(0,alim), ORIGIN),
        )

        ax, lim_line, line_graph, labels, ser = self.prepare_case(42, alim)  # ax те же
        ani_labels = self.change_extra_label_at_ax('\ln 2', alim)
        grp = VGroup(line_graph, lim_line, labels)
        self.play(Create(grp), *ani_labels)
        self.wait()
        self.play(self.zoomed_camera.frame.animate.move_to(ax.c2p(9,alim), ORIGIN))
        self.wait()
        self.play(self.zoomed_camera.frame.animate.move_to(ax.c2p(39,alim), ORIGIN))
        self.wait()
        self.play(self.zoomed_camera.frame.animate.move_to(ax.c2p(17,alim), ORIGIN))
        self.wait()
        self.play(self.zoomed_camera.frame.animate.move_to(ax.c2p(32,alim), ORIGIN))
        self.wait()
        
        
        #
        ## Случай 3: alim=1.5
        #
        alim = 1.5
        self.play(
            FadeOut(grp),
            self.zoomed_camera.frame.animate.move_to(ax.c2p(0,alim), ORIGIN),
        )

        ax, lim_line, line_graph, labels, ser = self.prepare_case(42, alim)  # ax те же
        ani_labels = self.change_extra_label_at_ax(str(alim), alim)
        grp = VGroup(line_graph, lim_line, labels)
        self.play(Create(grp), *ani_labels)
        self.wait()
        self.play(self.zoomed_camera.frame.animate.move_to(ax.c2p(12,alim), ORIGIN))
        self.wait()
        self.play(self.zoomed_camera.frame.animate.move_to(ax.c2p(25,alim), ORIGIN))
        self.wait()
        self.play(self.zoomed_camera.frame.animate.move_to(ax.c2p(20,alim), ORIGIN))
        self.wait()
        self.play(self.zoomed_camera.frame.animate.move_to(ax.c2p(40,alim), ORIGIN))
        self.wait()
    
    
    def add_shapes_to_background(self, n=100, opacity=0.07,
                                 expand=(-25,25), scale=0.4, seed=15):
        kwargs = dict(n=n, scale=scale, opacity=opacity, expand=expand,
                      seed=seed)
        self.bg_shapes = shapes_to_background(**kwargs)
        [self.add(x) for x in self.bg_shapes]
        
    
    def change_extra_label_at_ax(self, change_to_str, y):
        """ Изменяет дополнительную метку на осях """
        if not self.ax:
            return
        h = self.ax.axes[-1].numbers[0].height
        ani = []
        if self.extra_label:
            ani.append(FadeOut(self.extra_label, shift=LEFT))
        new_label = MathTex(change_to_str).set(height=h)
        new_label.next_to(self.ax.c2p(0,y), LEFT)
        ani.append(FadeIn(new_label, shift=RIGHT))
        self.extra_label = new_label
        return ani
    
    
    def prepare_case(self, xmax, alim):
        ax = self.ax
        if not ax:
            ax = Axes(
                x_range=[0, xmax, 5],
                y_range=[0, 2],
                x_length=20,
            )
            ax.add_coordinates()
            ax.to_edge(LEFT)
            self.ax = ax
        
        lim_line = ax.plot(lambda x: alim, stroke_width=2, color=BLUE)
        
        ser = Series(alim)
        ser.iterate(xmax // 2)
        xvals = list(range(1, 1+len(ser.AA_cur)))
        yvals = ser.AA_cur
        line_graph = ax.plot_line_graph(
            x_values=xvals,
            y_values=yvals,
            line_color=GOLD_E,
            vertex_dot_radius=0.05,
            vertex_dot_style=dict(stroke_width=1, fill_color=PURPLE),
            stroke_width=4,
        )
        
        # Готовим метки над точками
        labels = []
        for i, (x,y,dn) in enumerate(zip(xvals, yvals, ser.get_pos_neg_amount_array())):
            is_odd = i % 2
            pnt = ax.c2p(x,y)
            #sign = 1 if not is_odd else -1  # с минусами возникает путаница
            sign = 1
            label = Text(str(sign*dn), font_size=12)
            direction, color = (UP,GREEN) if not is_odd else (DOWN,RED)
            label.next_to(pnt, direction, buff=0.1).set_color(color)
            labels.append(label)
        
        return ax, lim_line, line_graph, VGroup(*labels), ser


#%% Тестовый рендер
if __name__ == '__main__':
    
    from helpers.render import dev_render
    
    dev_render(__file__, ConvergeToAny)
