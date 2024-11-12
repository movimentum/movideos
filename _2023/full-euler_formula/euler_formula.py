# Комментарий об оптимизации рендеринга 
#
# В метках типа t=0.17, непрерывно обновляемых в процессе анимации,
# следовало бы использовать вместо MathTex обычный Text с правильным шрифтом.
# Это бы существенно ускорило рендеринг.
#

import random

from manim import *
from movi_ext import *


#%%
SceneExtension.video_orientation = 'landscape'


#%%
class Intro(MovingCameraScene, SceneExtension):
    def construct(self):
        header = Text('Комплексные числа', font_size=24).shift(UP*2)
        txt_i = MathTex(r'i^2=-1').next_to(header, DOWN)
        txt_eu = MathTex(r'e^{i\varphi}=\cos\varphi + i\sin\varphi')

        self.play(
            LaggedStart(
                Write(header),
                Write(txt_i),
                lag_ratio=0.5
            ),
            run_time=2
        )
        self.wait(5)

        self.play(Write(txt_eu), run_time=2)
        
        self.play(
            self.camera.frame.animate.set(width=txt_eu.width * 1.5),
            txt_i.animate.set_opacity(0.3),
            header.animate.set_opacity(0.3)
        )
        self.wait()
        
        n = 40
        positions = (np.random.rand(n, 3) - 0.5) * 7
        positions[:,2] = 0
        scales = np.random.rand(n) * 2
        q_marks = [MathTex(r'?').scale(sc).set_color(RED).set_opacity(0.5).move_to(pos) for sc,pos in zip(scales,positions)]
        self.play(LaggedStart(
            *[GrowFromCenter(q_mark) for q_mark in q_marks],
            lag_ratio=0.05
        ))
        self.wait()
        
        ani_g1 = AnimationGroup(
            *[FadeOut(txt) for txt in (txt_i, txt_eu, header)],
            lag_ratio=0.25,
            run_time=2
        )
        ani_g2 = AnimationGroup(
            self.camera.frame.animate.set(width=txt_eu.width * 1.0),
            run_time=5,
            rate_func=linear
        )
        ani_g3 = AnimationGroup(
            *[FadeOut(q_mark) for q_mark in q_marks],
            lag_ratio=0.05,
            run_time=5
        )
        self.play(ani_g1, ani_g2, ani_g3)
        self.wait()


#%%
class ComplexNumbers(MovingCameraScene, SceneExtension):
    def construct(self):
        
        # Общий вид комплексного числа z
        txt_z = MathTex('z', '=', 'x', '+', 'i', 'y')
        self.play(FadeIn(txt_z[:3], shift=LEFT), run_time=1.5)
        self.wait()
        self.play(FadeIn(txt_z[3:], shift=DOWN), lag_ratio=0.5)
        self.wait(1.5)

        # Готовим координатные оси
        ax_grp = self.prepare_axes()  # ax, plane, labels
        self.play(
            txt_z.animate.to_corner(UL),
            Create(ax_grp),
            run_time=2
        )
        self.wait()
        
        # Демонстрируем комплексное число как радиус-вектор
        trc = ValueTracker(0)
        color = YELLOW
        label_x = MathTex(r'x').scale(0.8).set_color(color)
        label_y = MathTex(r'y').scale(0.8).set_color(color)
        label_z = MathTex(r'z')
        z_grp = always_redraw(
            lambda: self.prepare_z(
                1, 1, trc, label=label_z,
                vec_stroke=5,
                vec_color=color,
                label_x=label_x,
                label_y=label_y,
                color=color
            )  # dot, dot_arrow, label, label_x, label_y, lines
        )
        
        # CC: комплексное число можно изобразить точкой на координатной плоскости
        self.play(FadeIn(z_grp))
        
        # CC: если вдоль действительной оси откладывать...
        self.play(Succession(*[Indicate(a, color=RED) for a in ax_grp[-1]], color=RED))
        self.wait()
        
        self.play(trc.animate.set_value(0.75), run_time=3)
        self.play(trc.animate.set_value(0.45), run_time=1)
        self.wait()
        
        # Выделяем радиус-вектор
        arr_cpy = z_grp[1].copy() # если анимировать не копию, то из-за always_redraw анимации не будет...
        self.play(Wiggle(arr_cpy, color=RED))
        self.remove(arr_cpy)
        self.wait()
        
        
        #
        # z = e^t
        #
        
        # Готовим текст
        txt_z_exp = MathTex(
            'z', '=', 'e', '^', 't'
        ).scale(1.5).set_color(WHITE).to_corner(UR)
        
        # Готовим новые оси
        ax_grp_2 = self.prepare_axes(x_length=14, origin_shift=3 * LEFT).move_to(ORIGIN)
        self.origin = self.ax.get_origin()  # после move_to ORIGIN

        # Готовим обновляемые объекты (вектор, метку времени)
        trc.set_value(0)
        dot_grp = always_redraw(
            lambda: self.prepare_real_z_exp(
                trc,
                idle_lable=False,
                color=YELLOW,
                vec_stroke=5,
                vec_color=YELLOW
            )  # dot, dot_arrow, label, label_x, label_y, lines
        )
        time_label = always_redraw(
            lambda: MathTex(
                r't', r'=', f'{trc.get_value():.2f}'
            ).next_to(txt_z_exp, DOWN).align_to(txt_z_exp, LEFT)
            #lambda: MathTex(r'DUMMY LABEL').next_to(txt_z_exp, DOWN)
        )
        
        # Обновляем периферию
        self.play(
            ReplacementTransform(ax_grp,ax_grp_2),
            FadeOut(z_grp, target_position=LEFT),
            TransformMatchingShapes(txt_z, txt_z_exp),
            run_time = 2
        )
        self.wait()
        
        # Указываем, что t в экспоненте есть время
        txt_t = Text('время', color=YELLOW).scale(0.7).next_to(txt_z_exp, DOWN)
        self.play(
            Indicate(txt_z_exp[-1], color=YELLOW, run_time=2),
            Succession(
                FadeIn(txt_t, scale=0.5),
                FadeOut(txt_t, scale=0.5),
                Create(time_label)
            )
        )
        self.wait()
        
        # Анимируем функцию
        self.play(Create(dot_grp))
        self.wait()
        self.play(
            trc.animate.set_value(np.log(6)),
            rate_func=linear,
            run_time=6
        )
        self.wait()
        
        # Демонстрируем скорость в разные моменты времени
        v1 = self.get_velocity_z_real(np.log(1), vec_stroke=5)
        v2 = self.get_velocity_z_real(np.log(3), vec_stroke=5)
        
        self.play(trc.animate.set_value(np.log(1)))
        self.wait()
        self.play(Create(v1))
        self.wait()
        
        # Добавляем подписи
        br1 = Brace(dot_grp[1]).shift(DOWN*0.2)
        txt1 = Text('координата', font_size=20).next_to(br1, DOWN)
        br1_grp = VGroup(br1, txt1)
        br2 = Brace(v1).shift(DOWN*0.2)
        txt2 = Text('скорость', font_size=20).next_to(br2, DOWN)
        br2_grp = VGroup(br2, txt2)
        self.play(FadeIn(br1_grp, scale=0.5), FadeIn(br2_grp, scale=0.5))
        self.wait()
        
        self.play(
            trc.animate.set_value(np.log(3)),
            ReplacementTransform(v1, v2),
            br1_grp.animate.set_opacity(0.2),
            br2_grp.animate.set_opacity(0.2)
        )
        self.wait()
        
        br3 = Brace(dot_grp[1]).shift(DOWN*0.2)
        txt3 = Text('координата', font_size=24).next_to(br3, DOWN)
        br3_grp = VGroup(br3, txt3)
        br4 = Brace(v2).shift(DOWN*0.2)
        txt4 = Text('скорость', font_size=24).next_to(br4, DOWN)
        br4_grp = VGroup(br4, txt4)
        self.play(ReplacementTransform(br1_grp, br3_grp),
                  ReplacementTransform(br2_grp, br4_grp))
        self.wait()
        
        
        #
        # Что если z = e^(it)?
        #
        
        # Готовим текст
        txt_z_i_exp = MathTex('z', '=', 'e', '^', '{i', 't}').scale(1.5).set_color(WHITE).to_corner(UR)
        #txt_z_i_exp.add_background_rectangle()
        
        # Готовим новые оси
        ax_grp_3 = self.prepare_axes(x_length=14, scale_factor=2.0).move_to(ORIGIN)
        self.origin = self.ax.get_origin()  # после move_to ORIGIN
        
        # Обновляем периферию
        # TODO: дёргается t_label справа вверху из-за того, что в конце анимации ax_grp_2 меняется на ax_grp_3, за которым следит t_label
        self.play(
            ReplacementTransform(ax_grp_2, ax_grp_3),
            FadeOut(br3_grp, scale=0.5, target_position=LEFT),
            FadeOut(br4_grp, scale=0.5, target_position=RIGHT),
            Uncreate(v2), Uncreate(dot_grp),
            TransformMatchingTex(txt_z_exp, txt_z_i_exp),
            FadeOut(time_label, scale=0.5)
        )
        self.play(Flash(txt_z_i_exp[-2]))
        self.wait()
        
        # Готовим обновляемые объекты (вектор, метку времени)
        trc.set_value(0)
        pos_grp = always_redraw(
            lambda: self.prepare_z(
                1, 0, trc,
                vec_stroke=5,
                vec_color=YELLOW,
                color=YELLOW
            )  # dot, dot_arrow, label, label_x, label_y, lines
        )
        
        self.play(FadeIn(pos_grp, scale=0.5))
        self.wait()
        
        # Выписываем производную
        z_der2_old = MathTex(
            r'\dfrac{dz(0)}{dt}', r'=', r'i', '\cdot e^{i\cdot 0}'
        ).to_corner(UL)
        z_der2 = MathTex(r'\dfrac{dz(0)}{dt}', r'=', r'i').set_color(RED)
        z_der2.scale(1.2).to_corner(UL)
        z_exp_cpy = txt_z_exp.copy()
        self.play(ReplacementTransform(z_exp_cpy, z_der2_old))
        self.wait()
        
        vel_grp = pos_grp[:2].copy()
        self.add(vel_grp)
        
        self.play(ReplacementTransform(z_der2_old, z_der2))
        self.play(vel_grp.animate
                  .set_color(RED)
                  .rotate(about_point=self.origin, angle=np.pi/2)
        )
        self.play(
            vel_grp.animate.shift(pos_grp[0].get_center() - self.origin)
        )
        self.wait()
        
        # Рисуем прямой угол между радиус-вектором и скоростью
        angle_right = RightAngle(
            Line(pos_grp[1].get_start(), pos_grp[1].get_end()),
            Line(vel_grp[1].get_start(), vel_grp[1].get_end()),
            length=0.5,
            quadrant=(-1,1)
        )
        self.play(Create(angle_right))
        self.wait()


        ##### Сделать пару z, vel, которая будет зависеть от параметра
        trc_r = ValueTracker(1.3)
        trc_fi = ValueTracker(np.pi / 2.5)
        lbl_z = MathTex('z = x + iy').scale(0.5)
        lbl_iz = MathTex('z = -y + ix').scale(0.5)
        grp_ziz = always_redraw(
            lambda: self.prepare_z_iz(
                trc_r,
                trc_fi,
                color_z=YELLOW,
                color_iz=RED,
                label_z=lbl_z,
                label_iz=lbl_iz
            )
        )
        
        z_der3_old = MathTex(
            r'\dfrac{dz(t)}{dt}', r'=', 'i', '\cdot', 'e^{it}'
        ).to_corner(UL)
        z_der3 = MathTex(
            r'\dfrac{dz(t)}{dt}', r'=', 'i', 'z'
        ).set_color(RED).scale(1.2).to_corner(UL)
        
        self.play(
            FadeOut(pos_grp, target_position=2*RIGHT),
            FadeOut(vel_grp, target_position=2*UR),
            FadeOut(angle_right, scale=0.5),
            Succession(
                GrowArrow(grp_ziz[0]),
                FadeIn(grp_ziz[1], scale=0.5),
                GrowArrow(grp_ziz[2])
            ),
            ReplacementTransform(z_der2, z_der3_old))
        self.wait()
        
        self.play(
            Indicate(z_der3_old[-1]),
            Indicate(txt_z_i_exp[2:])
        )
        
        z_cpy = txt_z_i_exp[0].copy()
        self.play(
            ReplacementTransform(z_cpy, z_der3[-1]),
            TransformMatchingShapes(z_der3_old, z_der3[:-1]),
            FadeIn(grp_ziz[3], scale=0.5)
        )
        self.wait()
        

        #
        # ДАЛЕЕ ИДЁТ ВРЕЗКА С ДЕМОНСТРАЦИЕЙ УМНОЖЕНИЯ НА i
        #
        
        self.add(grp_ziz)  # Группу требуется добавить, чтобы работала анимация!
        self.play(Create(grp_ziz[-1]))  # линии
        
        self.play(*[Indicate(grp_ziz[i]) for i in (1,3)])
        self.wait()
        
        
        pos_vel_right_angle = always_redraw(
            lambda: RightAngle(
                *[Line(grp_ziz[i].get_start(), grp_ziz[i].get_end()) for i in (0,2)],
                length=0.5,
                quadrant=(-1,1)
            )
        )
        
        # NB! Обязательно создать после введения группы grp_ziz,
        #     от которой зависит положение!
        self.play(Create(pos_vel_right_angle))  
        self.wait()
        
        self.play(
            trc_r.animate.set_value(1),
            trc_fi.animate.set_value(np.pi / 6)
        )
        self.wait()
        
        self.play(
            trc_r.animate.set_value(1.5),
            trc_fi.animate.set_value(5 * np.pi / 6)
        )
        
        self.wait()
        self.play(
            trc_r.animate.set_value(0.7),
            trc_fi.animate.set_value(2 * np.pi - np.pi / 5)
        )
        self.wait()
        
        self.play(
            trc_r.animate.set_value(1),
            trc_fi.animate.set_value(2 * np.pi)
        )
        self.wait()
        
        # Убираем линии и метки
        self.play(*[FadeOut(grp_ziz[i],scale=0.5) for i in (1,3,4)])
        self.wait()


        #
        # Вывод: e^it = cos(fi) + i sin(fi)
        #
        trc_fi.set_value(1e-8)  # чтобы арка угла выглядела сразу правильно
        grp_ziz_nolabel = always_redraw(
            lambda: self.prepare_z_iz(trc_r, trc_fi, color_z=YELLOW, color_iz=RED)
        )

        self.remove(grp_ziz[0], grp_ziz[2])
        self.add(grp_ziz_nolabel)
        
        ccl = Circle(
            radius=1*self.scale_factor,
            color=GRAY_C,
            stroke_width=3
        ).move_to(self.origin)
        
        ccl_flash = ccl.copy().set_color(BLUE).set_width(4)
        self.play(
            Create(ccl),
            FadeOut(pos_vel_right_angle, scale=3)
        )
        self.play(Succession(
            *[ShowPassingFlash(
                ccl_flash.copy(),
                time_width=0.2*i,
                run_time=1.5*i/3
              ) for i in range(1,3+1)]
            )
        )
        self.wait()
        
        
        # Рисуем угол \varphi между действительной осью и радиус-вектором
        self.play(trc_fi.animate.set_value(np.pi / 3))
        angle_phi = Angle(
            self.ax.get_x_axis(),
            Line(
                grp_ziz_nolabel[0].get_start(),
                grp_ziz_nolabel[0].get_end()
            ),
            radius=0.5
        )
        angle_phi_label = MathTex(r'\varphi')
        angle_phi_label.next_to(angle_phi, RIGHT).shift(0.1 * LEFT + 0.1 * UP)
        self.play(Succession(
            Create(angle_phi),
            Write(angle_phi_label)
        ))
        self.wait()
        
        # Подписи проекций
        txt_cos = MathTex(r'\cos\varphi')
        txt_cos.scale(0.5).next_to(self.origin, DR)
        txt_sin = MathTex(r'\sin\varphi')
        txt_sin.scale(0.5).rotate(angle=np.pi/2).next_to(self.origin, UL).shift(0.5 * UP)
        self.play(Write(txt_cos), Write(txt_sin))
        self.wait()
        
        
        #
        # Добавляем уравнение окружности
        #
        #                        0     1      2      3     4      5       6         7        8     9       10        11       12
        txt_zexp_ccl = MathTex(r'z', r'=', r'e^{', r'i', r't}', r'=', r'\cos', r'\varphi', r'+', r'i', r'\cdot', r'\sin', r'\varphi')
        txt_zexp_ccl.set_color(YELLOW).scale(1.1)
        txt_zexp_ccl.to_corner(UR)
        self.play(
            TransformMatchingShapes(txt_z_i_exp, txt_zexp_ccl),
            FadeOut(angle_phi_label, target_position=txt_zexp_ccl[7]),
            FadeOut(angle_phi_label.copy(), target_position=txt_zexp_ccl[12]),
            FadeOut(txt_cos, target_position=txt_zexp_ccl[6:8]),
            FadeOut(txt_sin, target_position=txt_zexp_ccl[11:])
        )
        self.play(
            trc_fi.animate.set_value(1e-8),
            FadeOut(angle_phi, scale=2)
        )
        self.wait()


        #
        # Пока что никто не гарантирует, что t = fi
        #
        time_tracker = ValueTracker(0)
        time_label = always_redraw(
            lambda: MathTex(
                r't', r'=', f'{time_tracker.get_value():.2f}'
            ).next_to(txt_zexp_ccl, DOWN).align_to(txt_zexp_ccl[8], LEFT)
        )
        fi_label = always_redraw(
            lambda: MathTex(
                r'\varphi', r'=', f'{trc_fi.get_value():.2f}'
            ).next_to(time_label, DOWN).align_to(txt_zexp_ccl[8], LEFT)
        )
        arc = always_redraw(
            lambda: Angle(
                Line(self.origin, self.ax.c2p(1,0)),
                Line(self.origin, grp_ziz_nolabel[0].get_end()),
                radius=0.5
                )
        )
        self.play(
            FadeIn(time_label, scale=0.5),
            FadeIn(fi_label, scale=0.5),
            FadeIn(arc)
        )

        # Намерено делаем расфазировку между t и fi
        self.play(
            trc_fi.animate(rate_func=rate_functions.ease_in_out_bounce).set_value(2*np.pi),
            time_tracker.animate(rate_func=linear).set_value(4),
            run_time=12
        )
        self.wait()
        
        # Другими словами, насколько реальное движение отличается от равномерного
        self.play(
            trc_fi.animate.set_value(1e-8),
            time_tracker.animate.set_value(0),
            run_time=2
        )
        self.wait()
        
        #
        # Закон Ньютона
        #
        txt_Newton = MathTex(
            r'\vec{F} = m \cdot \vec{a}').to_corner(DL).shift(UP)
        txt_accel = MathTex(r'\dfrac{\vec{F}}{m} = \vec{a}').to_corner(DL).shift(UP)
        txt_accel_2 = MathTex(r'\dfrac{\vec{F}}{m} = \dfrac{d\vec{V}}{dt}').to_corner(DL).shift(UP)
        txt_accel_3 = MathTex(r'\dfrac{\vec{F}}{m} = \dfrac{d (iz)}{dt}').to_corner(DL).shift(UP)
        txt_accel_4 = MathTex(r'\dfrac{\vec{F}}{m} = i \cdot (i z)').to_corner(DL).shift(UP)
        txt_accel_5 = MathTex(r'\dfrac{\vec{F}}{m} = -z').to_corner(DL).shift(UP).set_color(GOLD_A).scale(1.2)
        self.play(Write(txt_Newton))
        self.wait()
        self.play(
            TransformMatchingShapes(txt_Newton, txt_accel),
            run_time=2
        )
        self.wait()
        self.play(
            TransformMatchingShapes(txt_accel, txt_accel_2),
            run_time=2
        )
        self.wait()
        self.play(
            TransformMatchingShapes(txt_accel_2, txt_accel_3),
            run_time=2
        )
        self.wait()
        self.play(
            TransformMatchingShapes(txt_accel_3, txt_accel_4),
            run_time=2
        )
        self.wait()
        self.play(
            TransformMatchingShapes(txt_accel_4, txt_accel_5),
            run_time=2
        )
        self.wait()
        
        
        grp_zizmz = always_redraw(
            lambda: self.prepare_z_iz(
                trc_r,
                trc_fi,
                return_vecs=3,
                with_lines=False,
                color_z=YELLOW,
                color_iz=RED,
                color_mz=GOLD_A
            )
        )

        self.play(GrowArrow(grp_zizmz[-2]))
        self.wait()
        
        self.remove(grp_ziz_nolabel)
        self.add(grp_zizmz)
        
        arc_1 = always_redraw(
            lambda: RightAngle(
                Line(grp_zizmz[0].get_start(), grp_zizmz[0].get_end()),
                Line(grp_zizmz[2].get_start(), grp_zizmz[2].get_end()),
                quadrant=(-1, 1),
                other_angle=True,
                length=0.5,
            )
        )
        
        arc_2 = always_redraw(
            lambda: RightAngle(
                Line(grp_zizmz[2].get_start(), grp_zizmz[2].get_end()),
                Line(grp_zizmz[4].get_start(), grp_zizmz[4].get_end()),
                quadrant=(-1, 1),
                other_angle=True,
                length=0.5,
            )
        )
        
        self.play(Create(arc_1), Create(arc_2))
        self.wait()
        
        # Другими словами, насколько реальное движение отличается от равномерного
        self.play(
            trc_fi.animate(rate_func=linear).set_value(4 * np.pi),
            time_tracker.animate(rate_func=linear).set_value(4 * np.pi),
            run_time=12
        )
        self.wait()

        self.camera.frame.save_state()
        #self.remove(arc_1)
        #self.remove(arc_2)
        #self.remove(grp_zizmz)
        #grp_to_fade = VGroup(arc_1, arc_2, grp_zizmz)
        self.play(
            self.camera.frame.animate.set(width=ccl.width * 2.3),
            FadeOut(arc_1),
            FadeOut(arc_2),
            FadeOut(grp_zizmz)
        )
        self.wait()
        trc_fi.set_value(1e-8)
        time_tracker.set_value(0)
        
        rvec = always_redraw(
            lambda: Arrow(
                self.origin,
                self.ax.c2p(
                    np.cos(time_tracker.get_value()),
                    np.sin(time_tracker.get_value())
                ),
                stroke_width=5,
                color=YELLOW,
                buff=0
            )
        )
        self.play(GrowArrow(rvec))
        self.wait()
        
        arc = always_redraw(
            lambda: Arc(
                radius=1*self.scale_factor,
                angle=time_tracker.get_value(),
                arc_center=self.origin,
                color=RED,
                stroke_width=5
            )
        )
        
        arc_lbl = always_redraw(
            lambda: MathTex(
                r'\overset{\frown}{l} =', r'\varphi', r'=', f'{time_tracker.get_value():.2f}'
                ).scale(0.6).next_to(rvec.get_end(), UR, buff=SMALL_BUFF)
        )
        
        time_label2 = always_redraw(
            lambda: MathTex(
                r't', r'=', f'{time_tracker.get_value():.2f}', '=', f'{time_tracker.get_value()/np.pi:.1f}', r'\pi'
                ).scale(0.6).next_to(self.ax.c2p(-2,1), DR, buff=SMALL_BUFF)
        )
        
        
        self.add(arc)
        self.play(Write(arc_lbl), Write(time_label2))
        
        self.play(
            time_tracker.animate.set_value(1),
            rate_func=linear,
            run_time=1.5
        )
        self.wait()
        
        self.play(
            time_tracker.animate.set_value(3),
            rate_func=linear,
            run_time=3
        )
        self.wait()
        
        self.play(
            time_tracker.animate.set_value(6),
            rate_func=linear,
            run_time=6
        )
        self.wait()
        
        self.play(time_tracker.animate.set_value(2*np.pi))
        self.wait()
        
        self.play(
            Indicate(arc_lbl[1:]),
            Indicate(time_label2[0]),
            Indicate(time_label2[-2:]),
            run_time=2
        )
        self.wait()
        
        time_label2.updaters.pop()
        arc_lbl.updaters.pop()
        txt_t_fi = MathTex(
            r't', r'=', r'\varphi'
            ).move_to(self.origin).scale(1.5).shift(0.5 * UP)
        self.play(
            ReplacementTransform(time_label2[:2], txt_t_fi[:2]),
            ReplacementTransform(arc_lbl[1], txt_t_fi[2]),
            FadeOut(time_label2[2:], scale=2),
            FadeOut(arc_lbl[0], scale=2),
            FadeOut(arc_lbl[2:], scale=2),
        )
        self.wait()
        
        self.remove(arc)
        self.play(
            Restore(self.camera.frame),
            Uncreate(ax_grp_3),
            FadeOut(time_label, scale=0.5),
            FadeOut(fi_label, target_position=DOWN),
            FadeOut(rvec, scale=3),
            FadeOut(ccl, scale=5),
            Unwrite(z_der3),
            Unwrite(txt_accel_5),
            run_time = 3
        )
        self.wait()
        
        
        txt_final = MathTex(
            r'e^{', r'i', r'\varphi}', r'=', r'\cos', r'\varphi', r'+', r'i', r'\cdot', r'\sin', r'\varphi'
            ).scale(2).set_color(WHITE)
        self.play(
            #FadeOut(txt_zexp_ccl[4]),
            #FadeOut(txt_t_fi[:2], scale=0.5),
            TransformMatchingShapes(VGroup(txt_t_fi, txt_zexp_ccl), txt_final)
        )
        self.wait()
        
        txt_famous = MathTex(
            r'e^{', r'i', r'\pi}', r'=', '-1'
        ).scale(2).set_color(WHITE)
        self.play(TransformMatchingShapes(txt_final, txt_famous))
        self.wait()

        txt_comment = Text('Энергия...', font_size=32)
        txt_comment2 = Text(
            'сохраняется!',
            font_size=32
        ).next_to(txt_comment, RIGHT).align_to(txt_comment, DOWN)
        
        VGroup(
            txt_comment,
            txt_comment2
        ).next_to(txt_famous, DOWN, buff=MED_LARGE_BUFF).set_color(BLUE_B)
        self.play(Write(txt_comment))
        self.wait()
        self.play(Write(txt_comment2))
        self.wait()
        
        #
        # Для обложки
        #
        #self.play(self.camera.frame.animate.shift(0.5 * DOWN).set(width=VGroup(txt_famous, txt_comment, txt_comment2).width * 1.5))
        #return
        
        self.play(
            FadeOut(txt_comment, scale=0.5),
            FadeOut(txt_comment2, scale=0.5),
            FadeOut(txt_famous, scale=5),
            run_time = 2
        )
        self.wait()


    def prepare_axes(self, x_length=8, y_length=8, origin_shift=(0,0,0), scale_factor=1.7):
        x_origin_shift, y_origin_shift, _ = origin_shift
        self.x_length = x_length
        self.y_length = y_length
        self.scale_factor = scale_factor
        dx = x_length / 2 / scale_factor
        xmin = - dx - x_origin_shift
        xmax = + dx - x_origin_shift
        dy = y_length / 2 / scale_factor
        ymin = - dy - y_origin_shift
        ymax = + dy - y_origin_shift
        x_range = [xmin, xmax, 1]
        y_range = [ymin, ymax, 1]
        
        kwargs = dict(x_range=x_range, y_range=y_range, x_length=x_length, y_length=y_length)
        self.plane = NumberPlane(**kwargs).set_opacity(0.7)
        self.ax = Axes(**kwargs).add_coordinates()
        labels = self.ax.get_axis_labels(MathTex(r'\Re'), MathTex(r'\Im'))
        labels[0].next_to(self.ax.c2p(xmax*0.95,0,0), DOWN, buff=MED_SMALL_BUFF)
        labels[1].next_to(self.ax.c2p(0,ymax*0.92,0), LEFT, buff=MED_LARGE_BUFF)
        grp = VGroup(self.ax, self.plane, labels)
        grp.to_edge(RIGHT, buff=0)
        self.origin = self.ax.get_origin()  # после финального позиционирования!
        self.origin_local = self.ax.p2c(self.origin)
        return grp


    def prepare_z(self, x0, y0, tracker, shift_xy=(0,0), ampl_ratio=0.2, osc_freq=5, color=WHITE, vec_stroke=3, vec_color=WHITE,
                  label=VMobject(None), label_x=VMobject(None), label_y=VMobject(None)):
        """ x0,y0 -- координаты точки в self.ax при tracker = 0 """
        r0 = np.linalg.norm(np.array((x0,y0)) - self.origin_local)
        fi0 = np.angle(complex(x0, y0))
        ampl = ampl_ratio * r0  # амплитуда колебаний
        
        phase = 2 * np.pi * tracker.get_value() + fi0  # при tracker=0 имеем начальное положение, при tracker=2pi имеем полный оборот
        r = r0 + ampl * np.sin(osc_freq * (phase - fi0))
        x = r * np.cos(phase)
        y = r * np.sin(phase)

        # Точка
        point = self.ax.c2p(x,y)
        dot = Dot(point)
        dot.set_color(color)
        # Вектор
        dot_arrow = Arrow(self.origin, dot.get_center(), stroke_width=vec_stroke, color=vec_color, buff=0)
        # Координатные линии
        lines = self.ax.get_lines_to_point(point)
        lines.set_color(color).set_opacity(0.8)
        # Метка
        direction = self.ax.c2p(x,y) - self.ax.get_origin()
        direction /= np.linalg.norm(direction)
        label = label.move_to(point + 0.5 * direction)
        
        dir_y = RIGHT if x > 0 else LEFT
        dir_x = UP if y > 0 else DOWN
        label_x.next_to(lines[0], dir_x, buff=0.1)
        label_y.next_to(lines[1], dir_y, buff=0.1)
        
        grp = VGroup(dot, dot_arrow, label, label_x, label_y, lines)
        
        grp.shift(self.ax.c2p(*shift_xy) - self.origin)
        return grp


    def prepare_z_iz(self, trc_r, trc_fi, color_z=YELLOW, color_iz=RED, color_mz=BLUE_E, vec_stroke=5, label_z=VMobject(None), label_iz=VMobject(None), label_mz=VMobject(None), return_vecs=2, with_lines=True):
        """ trc_r, trc_fi -- трекеры радиуса и угла для точки z0 """
        r = trc_r.get_value()
        fi_z = trc_fi.get_value()
        fi_iz = fi_z + np.pi/2
        fi_mz = fi_z + np.pi
        
        def get_vector(r, fi, color, label):
            x = r * np.cos(fi)
            y = r * np.sin(fi)
            pnt = self.ax.c2p(x, y)
            dot = Dot(pnt).set_color(color)
            arrow = Arrow(self.origin, dot.get_center(), stroke_width=vec_stroke, color=color, buff=0)
            # Метка
            direction = self.ax.c2p(x,y) - self.ax.get_origin()
            direction /= np.linalg.norm(direction)
            label = label.move_to(pnt + 0.5 * direction)
            return x, y, pnt, dot, arrow, label
        
        x_z,  y_z,  pnt_z,  dot_z,  arr_z,  lbl_z  = get_vector(r, fi_z,  color_z,  label_z)
        x_iz, y_iz, pnt_iz, dot_iz, arr_iz, lbl_iz = get_vector(r, fi_iz, color_iz, label_iz)
        x_mz, y_mz, pnt_mz, dot_mz, arr_mz, lbl_mz = get_vector(r, fi_mz, color_mz, label_mz)
        
        # Переносим вектор скорости в конец вектора координаты
        VGroup(dot_iz, arr_iz, lbl_iz).shift(pnt_z - self.origin)
        
        # Переносим вектор ускорения в конец вектора скорости
        VGroup(dot_mz, arr_mz, lbl_mz).shift(dot_iz.get_center() - self.origin)

        # Координатные линии
        lines = self.ax.get_lines_to_point(pnt_z)
        lines.set_color(color_z).set_opacity(0.8)
        
        #return VGroup(dot_z, arr_z, lbl_z, dot_iz, arr_iz, lbl_iz, lines)
        if return_vecs == 1:
            grp = VGroup(arr_z, lbl_z)
        elif return_vecs == 2:
            grp = VGroup(arr_z, lbl_z, arr_iz, lbl_iz)
        elif return_vecs == 3:
            grp = VGroup(arr_z, lbl_z, arr_iz, lbl_iz, arr_mz, lbl_mz)
        if with_lines:
            grp.add(lines)

        return grp


    def prepare_real_z_exp(self, time_tracker, idle_lable=False, color=WHITE, vec_stroke=3, vec_color=WHITE, label=VMobject(None)):
        """ Горизонтальный вектор вдоль действительной оси """
        x = np.exp(time_tracker.get_value())
        y = 0
        # Точка
        point = self.ax.c2p(x,y)
        dot = Dot(point)
        dot.set_color(color)
        center = dot.get_center()
        # Вектор
        dot_arrow = Arrow(self.origin, center, stroke_width=vec_stroke, color=vec_color, buff=0)
        # Метка
        label = (
            MathTex('dummy')
            if idle_lable else
            MathTex(
                r'z', r'=', f'{x:.2f}', r'+', r'i', r'\cdot', r'0'
            ).scale(0.8).set_color(color)
        )
        label = label.next_to(point, UP)
        grp = VGroup(dot, dot_arrow, label)
        return grp


    def get_velocity_z_real(self, t, vec_stroke=3, color=RED):
        x = np.exp(t)
        vel_arrow = Arrow(
            self.ax.c2p(x,0),
            self.ax.c2p(2*x,0),
            stroke_width=vec_stroke,
            color=color,
            buff=0
        )
        return vel_arrow


#%%
class ImaginaryUnityMultiplication(Scene, SceneExtension):
    def construct(self):
        plane_grp = ComplexNumbers.prepare_axes(self, scale_factor=3)
        plane_grp.move_to(ORIGIN)
        self.origin = self.ax.get_origin()
        self.add(plane_grp)
        
        xaxis = plane_grp[0].get_x_axis()
        yaxis = plane_grp[0].get_y_axis()
        ang_1_i  = RightAngle(xaxis, yaxis, length=0.25, quadrant=(1,1))
        ang_i_m1 = RightAngle(xaxis, yaxis, length=0.25, quadrant=(-1,1))
        ang_m1_mi = RightAngle(xaxis, yaxis, length=0.25, quadrant=(-1,-1))
        ang_mi_1 = RightAngle(xaxis, yaxis, length=0.25, quadrant=(1,-1))
        
        txt_1 = MathTex('z = 1')
        txt_i_old = MathTex('z = 1 \cdot i')
        txt_i = MathTex('z = i')
        txt_m1_old = MathTex('z = i \cdot i')
        txt_m1 = MathTex('z = -1')
        txt_mi_old = MathTex('z = -1 \cdot i')
        txt_mi = MathTex('z = -i')
        txt_1_2_old = MathTex('z = -i \cdot i')
        txt_1_2 = MathTex('z = 1')
        
        # z = 1
        pnt = self.ax.c2p(1,0)
        clr = YELLOW_E
        z_1 = Arrow(self.origin, pnt, stroke_width=10, color=clr, buff=0)
        txt_1.next_to(z_1, UP).align_to(z_1, RIGHT).set_color(clr)
        self.play(GrowArrow(z_1), FadeIn(txt_1, scale=0.5))
        self.wait()
        
        # z = i
        pnt = self.ax.c2p(0,1)
        clr = GREEN_E
        z_i = z_1.copy().set_color(clr)
        txt_i_old.move_to(pnt).align_to(pnt, UL).shift(MED_SMALL_BUFF * RIGHT).set_color(clr)
        txt_i.move_to(pnt).align_to(pnt, UL).shift(MED_SMALL_BUFF * RIGHT).set_color(clr)
        self.play(
            Rotate(z_i, about_point=self.origin, angle=np.pi/2),
            FadeIn(txt_i_old, scale=0.5),
            Create(ang_1_i)
        )
        self.play(TransformMatchingShapes(txt_i_old, txt_i))
        self.wait()
        
        # z = -1
        pnt = self.ax.c2p(-1,0)
        clr = TEAL_E
        z_m1 = z_i.copy().set_color(clr)
        txt_m1_old.move_to(pnt).align_to(pnt, DL).shift(MED_SMALL_BUFF * UP).set_color(clr)
        txt_m1.move_to(pnt).align_to(pnt, DL).shift(MED_SMALL_BUFF * UP).set_color(clr)
        self.play(
            Rotate(z_m1, about_point=self.origin, angle=np.pi/2),
            FadeIn(txt_m1_old, scale=0.5),
            Create(ang_i_m1)
        )
        self.play(TransformMatchingShapes(txt_m1_old, txt_m1))
        self.wait()
        
        # z = -i
        pnt = self.ax.c2p(0,-1)
        clr = BLUE_E
        z_mi = z_m1.copy().set_color(clr)
        txt_mi_old.move_to(pnt).align_to(pnt, DL).shift(MED_SMALL_BUFF * RIGHT).set_color(clr)
        txt_mi.move_to(pnt).align_to(pnt, DL).shift(MED_SMALL_BUFF * RIGHT).set_color(clr)
        self.play(
            Rotate(z_mi, about_point=self.origin, angle=np.pi/2),
            FadeIn(txt_mi_old, scale=0.5),
            Create(ang_m1_mi)
        )
        self.play(TransformMatchingShapes(txt_mi_old, txt_mi))
        self.wait()
        
        # Назад в z = 1
        pnt = self.ax.c2p(1,0)
        clr = YELLOW_E
        z_1_2 = z_mi.copy().set_color(clr)
        txt_1_2_old.move_to(pnt).align_to(pnt, UR).shift(MED_SMALL_BUFF * DL).set_color(clr)
        txt_1_2.move_to(pnt).align_to(pnt, UR).shift(MED_SMALL_BUFF * DL).set_color(clr)
        self.play(
            Rotate(z_1_2, about_point=self.origin, angle=np.pi/2),
            FadeIn(txt_1_2_old, scale=0.5),
            Create(ang_mi_1)
        )
        self.play(TransformMatchingShapes(txt_1_2_old, txt_1_2))
        self.play(FadeOut(txt_1_2, target_position=txt_1))
        self.wait()


#%%
class ComplexUnityTest(Scene, SceneExtension):
    def construct(self):
        self.show_axes()
        
        alpha = ValueTracker(0)
        beta = ValueTracker(0)
        
        z1 = always_redraw(
            lambda: self.prepare_z(
                1.0, 1.0, alpha,
                osc_freq=11.327,
                label=MathTex(r'z_1'), color=RED
            )
        )
        z2 = always_redraw(
            lambda: self.prepare_z(
                1.0, 1.5, beta,
                osc_freq=2,
                label=MathTex(r'z_2'),
                color=GREEN
            )
        )

        self.play(*[FadeIn(z) for z in (z1,z2)])
        
        self.play(alpha.animate.set_value(-2), beta.animate.set_value(1), rate_func=linear, run_time=4)
        self.wait()
    
    
    def show_axes(self):
        self.x_length = x_length = 8
        self.y_length = y_length= 8
        self.scale_factor = scale_factor = 1.7
        xmax = x_length / 2 / scale_factor
        ymax = y_length / 2 / scale_factor
        x_range = [- xmax, xmax, 1]
        y_range = [- ymax, ymax, 1]
        
        kwargs = dict(
            x_range=x_range,
            y_range=y_range,
            x_length=x_length,
            y_length=y_length
        )
        self.plane = NumberPlane(**kwargs).set_opacity(0.7)
        self.ax = Axes(**kwargs).add_coordinates()
        labels = self.ax.get_axis_labels(MathTex(r'x'), MathTex(r'i y'))
        labels[0].next_to(self.ax.c2p(xmax*0.95,0,0), DOWN, buff=MED_SMALL_BUFF)
        labels[1].next_to(self.ax.c2p(0,ymax*0.92,0), LEFT, buff=MED_LARGE_BUFF)
        grp = VGroup(self.ax, self.plane, labels)
        grp.to_edge(RIGHT, buff=0)
        self.origin = self.ax.get_origin()  # после финального позиционирования!
        self.origin_local = self.ax.p2c(self.origin)
        self.add(grp)


    def prepare_z(
            self, x0, y0, tracker,
            ampl_ratio=0.2,
            osc_freq=5,
            label=VMobject(None),
            color=WHITE):
        """ x0,y0 -- координаты точки в self.ax при tracker = 0 """
        r0 = np.linalg.norm(np.array((x0,y0)) - self.origin_local)
        fi0 = np.angle(complex(x0, y0))
        ampl = ampl_ratio * r0  # амплитуда колебаний
        
        # tracker=0 --> начальное положение; tracker=2pi --> полный оборот
        phase = 2 * np.pi * tracker.get_value() + fi0
        r = r0 + ampl * np.sin(osc_freq * (phase - fi0))
        x = r * np.cos(phase)
        y = r * np.sin(phase)

        # Точка
        point = self.ax.c2p(x,y)
        dot = Dot(point)
        dot.set_color(color)
        # Вектор
        dot_arrow = Arrow(self.origin, dot.get_center(), stroke_width=3, buff=0)
        # Координатные линии
        lines = self.ax.get_lines_to_point(point)
        lines.set_color(color).set_opacity(0.5)
        # Метка
        direction = self.ax.c2p(x,y) - self.ax.get_origin()
        direction /= np.linalg.norm(direction)
        label = label.move_to(point + 0.5 * direction)
        grp = VGroup(dot, dot_arrow, label, lines)
        return grp


    def add_brace_to_z(self, z):
        (dot, arrow, lines, label), x, y = z
        br = BraceBetweenPoints(arrow.start, arrow.end)
        self.add(br)
        return br


#%% Тестовый рендер
if __name__ == '__main__':
    
    from helpers.render import dev_render
    
    # Intro, ComplexNumbers, ImaginaryUnityMultiplication, ComplexUnityTest
    dev_render(__file__, Intro)