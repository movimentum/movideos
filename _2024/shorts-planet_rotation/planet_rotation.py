#
# Вращение планеты вокруг собственной оси при движении по орбите вокруг звезды
#

import random

from manim import *

from movi_ext import *


#%%
# Демонстрация ретроградного вращения в SolarSystem
is_retrograd_rotation_part = True

w_new = 3/4 * 8
h_new = 3/4 * 8 * 16/9
SceneExtension.CONFIG = dict(
    frame_width = w_new,
    frame_height = h_new
)

np.random.seed(0xDEADBEEF)


#%%
class StarDayDefinition(MovingCameraScene, SceneExtension):
    def construct(self):

        bg = BGSimpleShapes(100)
    
        cre = CreatureLambda(fill_opacity=0.7).scale(0.8).to_corner(UL, buff=LARGE_BUFF).shift(DOWN)
        cre2 =cre.copy().to_corner(UR, buff=LARGE_BUFF)
        cre3 =cre.copy().to_edge(DOWN, buff=LARGE_BUFF).shift(UR)
        cre_grp = VGroup(cre, cre2, cre3)
        
        self.play(
            LaggedStart(
                bg.fadein(lag_ratio=0.02, scale=0.2),
                Create(cre),
                Create(cre2),
                Create(cre3),
                lag_ratio=0.1
        ))
        self.wait()
        
        txt = Text(r"Звёздные сутки").scale(0.5).shift(UP)
        txt2 = MathTex(r'\approx', color=BLUE_A).next_to(txt, DOWN)
        txt3 = Text(r' 23 часа 56 минут', color=BLUE_A).scale(0.5).next_to(txt2, DOWN)
        grp = VGroup(txt, txt2, txt3)
        
        self.play(
            Write(grp),
            AnimationGroup(*[c.animate.look_at(txt) for c in cre_grp], lag_ratio=0.3)
        )
        
        self.play(
            self.camera.frame.animate(run_time=2).set(width=grp.get_width() * 1.3),
            LaggedStart(
                bg.fadeout_with_random_shift(lag_ratio=0.002),
                FadeOut(cre, scale=0.5),
                FadeOut(cre2, scale=0.8, shift=RIGHT),
                FadeOut(cre3, scale=1.3, shift=DOWN*0.5),
                FadeOut(grp, scale=2),
                lag_ratio=0.1
        ))
        self.wait()


#%%
class SolarSystem(ThreeDScene, SceneExtension):

    rotate_similar = True
    phi = PI / 2.5
    theta = PI / 3
    earth_axis_to_ecliptics_angle = PI / 6
    
    def construct(self):
    
        # Фон
        self.generate_bg()
    
        # Источник света -- в центр солнца
        self.camera.light_source.set_points(np.array([0,0,0]).reshape(-1,3))

        # Оси
        dX = w_new / 2
        axes = ThreeDAxes(x_range=(-dX, dX, 1), y_range=(-dX, dX, 1), z_range=(-dX, dX, 1), x_length=w_new, y_length=w_new, z_length=w_new)
        axes.set_opacity(0.2).set_color(YELLOW_A)
        self.set_camera_orientation(phi=self.phi, theta=self.theta)

        # Солнце
        sun = Sphere(
            center=(0,0,0),
            radius=0.5,
            resolution=(20,20),
            u_range=[0, TAU],
            v_range=[0, PI],
            checkerboard_colors=(YELLOW_A,YELLOW_E),
        )
        
        # Планета
        t_tracker = ValueTracker(0)
        earth_grp = always_redraw(
                    lambda: self.construct_earth(t_tracker)
        )
        
        # Плоскость эклиптики
        trajectory = Circle(radius=2, stroke_opacity=0.2, fill_opacity=0.2, color=BLUE)
        
        self.add(axes, sun, earth_grp, trajectory)
        #self.add(sun, earth_grp, trajectory)

        #
        ## Анимации
        #
        
        # Вращение камеры
        self.begin_ambient_camera_rotation()

        
        # Просто вращение
        self.play(
            t_tracker.animate(rate_func=linear).set_value(5),
            run_time=5,
        )
        t_tracker.set_value(0)
        

        self.play(
            self.camera.zoom_tracker.animate.set_value(1.4),
            self.camera._frame_center.animate.move_to(LEFT * 2),
            t_tracker.animate(rate_func=linear).set_value(2),
            run_time=2,
        )
        
        if is_retrograd_rotation_part:
            self.rotate_similar = False
        
        self.play(
            t_tracker.animate(rate_func=linear).set_value(3),
            run_time=2,
        )
        
        self.play(
            self.camera.zoom_tracker.animate.set_value(1.1),
            self.camera._frame_center.animate.move_to(RIGHT * 0.5),
            t_tracker.animate(rate_func=linear).set_value(5),
            run_time=2,
        )
        
        self.wait(0.05)  # чтобы не потерять последний кадр

    
    def construct_earth(self, t_trk, t_sun_round=5, t_self_round=1, r=0.2, res=(10,10), ckbrd_colors=(BLUE_D,BLUE_E), scale_text=True):
        t = t_trk.get_value()
        phi = t / t_sun_round * TAU
        dist_from_sun = 2
        center = np.array((np.cos(phi), np.sin(phi), 0))
        center *= dist_from_sun
        
        earth = Sphere(
            center=center,
            radius=r,
            resolution=res,
            u_range=[0, TAU],
            v_range=[0, PI],
            checkerboard_colors=ckbrd_colors,
        )

        axis = DashedLine(center + 2*r*OUT, center + 2*r*IN, stroke_width=2, stroke_opacity=0.4, color=RED, dash_length=0.03)
        earth.add(axis)
        
        # Наклон оси вращения Земпли
        psi = - self.earth_axis_to_ecliptics_angle
        earth.rotate(psi, axis=(0,1,0))
        
        # Собственное вращение Земли
        n_rots = t / t_self_round 
        alpha = n_rots * TAU
        if not self.rotate_similar:
            alpha *= -1
        earth.rotate(alpha, axis=(np.sin(psi),0,np.cos(psi)))
        
        txt = Text(f'{n_rots / t_sun_round * 365:.0f} дней').scale(0.2).next_to(earth, UR)
        phi = self.camera.get_phi()
        theta = self.camera.get_theta()
        txt.rotate(angle=self.camera.get_phi(), axis=(1,0,0))
        txt.rotate(angle=PI/2+self.camera.get_theta(), axis=(0,0,1))
        if scale_text:
            txt.scale(1 + 0.05 * int(n_rots + 1) )
        
        return VGroup(earth,txt)
        

    def generate_bg(self, n=100):
        # mobs = []
        # shapes = (Triangle, Square, Circle)
        # for i in range(n):
        #     side_shift = (np.random.rand() - 0.5) * h_new
        #     vert_shift = (np.random.rand() - 0.5) * h_new
        #     total_shift = side_shift * RIGHT + vert_shift * UP
        #     shape = np.random.choice(shapes)
        #     element = shape().scale(0.15).shift(total_shift).set_opacity(0.08).set_color(random_color())
        #     mobs.append(element)
        
        bg = BGSimpleShapes(100)
        
        grp = VGroup(*bg.mobs)
        grp.rotate(angle=self.phi, axis=(1,0,0))
        grp.rotate(angle=PI/2+self.theta, axis=(0,0,1))
        
        self.add(grp)
        
        
#%%
class UnravelCircleToLine(MovingCameraScene, SceneExtension):
    def construct(self):
        trk = ValueTracker(0)
        mobs = always_redraw(
                lambda: self.get_mobs(trk, r=0.3, base_shift=DOWN, color=RED)
        )
        mobs2 = always_redraw(
                lambda: self.get_mobs(trk, r=0.6, base_shift=UP, color=YELLOW)
        )

        txt_R = MathTex(r'R').move_to(mobs2)
        txt_r = MathTex(r'r').move_to(mobs)
        txt_radii = MathTex('R', '=', '2', r'\cdot', 'r')
        txt_radii.shift(3 * UP)

        self.play(
            Create(mobs),
            Create(mobs2),
            Write(txt_R),
            Write(txt_r),
        )
        self.wait()
        
        self.play(
            LaggedStart(
                ReplacementTransform(txt_R, txt_radii[0]),
                ReplacementTransform(txt_r, txt_radii[-1]),
                *[FadeIn(el, shift=np.random.rand(3) - 0.5) for el in txt_radii[1:-1]],
                lag_ratio=0.2,
            )
        )
        self.wait()

        self.play(trk.animate.set_value(PI*2))
        self.wait()

        line2 = mobs2[0].copy().set(cap_style=CapStyleType.ROUND)
        line11 = mobs[0].copy().set(cap_style=CapStyleType.ROUND)
        self.remove(mobs, mobs2)
        self.add(line2, line11)  # порядок важен!
        line11.save_state()
        
        self.play(line2.animate.set(stroke_width=8))
        self.wait()

        line11.generate_target()
        line11.target.move_to(line2).align_to(line2, LEFT)
        
        
        br = Brace(line2, UP)
        txt = MathTex(r'2\pi \cdot R').scale(0.5).next_to(br, UP)
        self.play(Write(br), Write(txt))
        self.wait()
        
        self.play(MoveToTarget(line11))
        
        line12 = DashedLine(
            line11.get_end(),
            line11.get_start(),
            color=line11.get_color(),
            cap_style=CapStyleType.ROUND
        )
        line12.move_to(line2).align_to(line2, RIGHT)  # покажем её позже
        
        br11 = Brace(line11, DOWN)
        br12 = Brace(line12, DOWN)
        txt11 = MathTex(r'2\pi \cdot r').scale(0.5).next_to(br11, DOWN)
        txt12 = MathTex(r'2\pi \cdot r').scale(0.5).next_to(br12, DOWN)
        
        self.play(LaggedStart(
            Write(txt11),
            FadeIn(br11, shift=UP*0.5),
        ))
        self.wait()
        
        self.play(
            Write(txt12),
            TransformFromCopy(line11, line12, path_arc=90*DEGREES),
            FadeIn(br12, scale=0.5),
        )
        self.wait()
        
        # Откатываемся назад
        elements_to_hide = (br, txt, br11, br12, txt11, txt12, line12)
        directions = [np.random.rand(3)-0.5 for el in elements_to_hide]
        self.play(LaggedStart(
            *[FadeOut(el, shift=d) for el,d in zip(elements_to_hide, directions)],
            lag_ratio=0.2
        ))
        self.wait()
        
        self.play(Restore(line11))
        self.wait()
        
        #
        ## Снова скручиваем окружности и фокусируемся на них
        #
        mobs = always_redraw(
                lambda: self.get_mobs(trk, r=0.3, base_shift=DOWN, color=RED)
        )
        mobs2 = always_redraw(
                lambda: self.get_mobs(trk, r=0.6, base_shift=UP, color=YELLOW)
        )
        
        self.remove(line11, line2)
        self.add(mobs, mobs2)
        
        self.play(trk.animate.set_value(0))
        self.wait()
        
        grp = VGroup(mobs, mobs2).copy()
        self.add(grp)
        self.remove(mobs, mobs2)
        
        self.play(
            self.camera.frame.animate.move_to(grp).set(width=grp.get_width()*4),
            txt_radii.animate.next_to(grp, UP, buff=LARGE_BUFF),
        )
        self.wait()


    def get_mobs(self, angle_tracker, r=0.5, base_shift=ORIGIN, color=WHITE):
        a = angle_tracker.get_value()
        line_length = r * a
        shift = RIGHT * line_length
        line_start = LEFT * 2 + base_shift
        line_end = line_start + shift
        
        line = Line(line_start, line_end, color=color)

        arc = Arc(
            radius=r,
            start_angle=-PI/2,
            angle=2*PI-a,
            color=color
        )
        arc.shift(line_end-arc.get_start())
        
        return VGroup(line, arc)
        

#%%
class CoinRotation(ThreeDScene, SceneExtension):
    def construct(self):
        dX = w_new / 2
        axes = ThreeDAxes(
            x_range=(-dX, dX, 1),
            y_range=(-dX, dX, 1),
            z_range=(-dX, dX, 1),
            x_length=w_new,
            y_length=w_new,
            z_length=w_new
        )
        
        # Фон
        bg = BGSimpleShapes(150)
        anims = [Create(el) for el in bg.mobs]
        
        # Основные объекты
        self.ccl_main = Circle().set_color(YELLOW)
        arr_main = Arrow(
            start=self.ccl_main.get_center(),
            end=self.ccl_main.get_top(),
            buff=0
        )
        arr_main.set_color(self.ccl_main.get_color())
        dashes_main = self.make_dashes_in_circle(
            self.ccl_main,
            n_dashes=16,
            dash_length_ratio=1/8
        )  # TODO: длина между штрихами должна быть одинакова для обеих окружностей --> n_dashes ~ R
        
        angle_tracker = ValueTracker(0)
        grp_rot = always_redraw(
                lambda: self.construct_circle_with_arrow(
                    angle_tracker,
                    radius_ratio=0.5,
                    with_creature=True
                )
        )
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.add(axes)
        
        anims.extend([
            Create(self.ccl_main),
            GrowArrow(arr_main),
            Create(grp_rot),
            Create(dashes_main)
        ])
        self.move_camera(
            phi=0,
            theta=-90*DEGREES,
            run_time=0.5,
            added_anims=anims,
            lag_ratio=0.1
        )
        self.wait(0.5)
        
        # Качение без вращения камеры
        self.play(
            angle_tracker.animate.set_value(-360*DEGREES),
            run_time=2,
            rate_func=linear
        )
        self.wait(0.5)

        self.play(
            angle_tracker.animate.set_value(0*DEGREES),
            run_time=0.5
        )
        self.play(
            angle_tracker.animate.set_value(-360*DEGREES),
            run_time=4,
            rate_func=linear
        )
        self.wait()

        anims = [angle_tracker.animate.set_value(-2 * 360 * DEGREES)]
        self.move_camera(theta=(-90-360)* DEGREES, added_anims=anims, run_time=4, rate_func=linear)
        
        self.wait()
        
    
    def make_dashes_in_circle(self, ccl, n_dashes = 8, dash_length_ratio=1/4):
        dashes = []
        dash_end = ccl.get_bottom()
        dash_start = ccl.get_bottom() + (ccl.get_center() - ccl.get_bottom()) * dash_length_ratio
        for i in range(1, n_dashes):
            line = Line(dash_start, dash_end).set_opacity(0.5)
            line.rotate(360 * DEGREES * i / n_dashes, about_point=ccl.get_center())
            dashes.append(line)
        return VGroup(*dashes).set_color(ccl.get_color())
    
    
    def construct_circle_with_arrow(self, angle_tracker, color=RED, radius_ratio=1, n_dashes = 8, dash_length_ratio = 1/4, with_creature=False):
        fi = angle_tracker.get_value()
        ccl = Circle(radius=radius_ratio)
        ccl.shift((self.ccl_main.get_top() - ORIGIN) * (1 + radius_ratio))
        ccl.set_color(color)
        arr = Arrow(
            start=ccl.get_center(),
            end=ccl.get_bottom(),
            buff=0
        ).set_color(color)
        dashes = self.make_dashes_in_circle(ccl, n_dashes, dash_length_ratio)
        
        if with_creature:
            cre = CreatureLambda().scale(0.3)
            cre.next_to(ccl.get_bottom(), DOWN)
            cre.look_at(ccl.get_center())
            cre.rotate(fi, about_point=self.ccl_main.get_center())
        else:
            cre = VMobject(None)
        
        grp = VGroup(ccl, arr, dashes)
        
        # Вращение вокруг собственной оси
        grp.rotate(fi / radius_ratio, about_point=ccl.get_center())
        
        # Вращение вокруг центра главной окружности
        grp.rotate(fi, about_point=self.ccl_main.get_center())
        
        return VGroup(grp, cre)


#%% Тестовый рендер
if __name__ == '__main__':
    
    from helpers.render import dev_render
    
    dev_render(__file__, CoinRotation)
