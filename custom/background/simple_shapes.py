from manim import *


class BGSimpleShapes(VGroup):
    def __init__(
            self,
            n: int =100, 
            shapes: tuple[Mobject,Mobject,Mobject] = (Triangle, Square, Circle),
            span: [float, None] = None,
            seed: int = 0xDEAFBEAC,
        ):
        
        super().__init__()
        
        np.random.seed(seed)
        
        self.span = span if span else max(config.frame_height, config.frame_width)
        
        self.base_shapes = shapes
        self.n = n
        
        self._generate_random_shapes(n)
        self.mobs = self.submobjects
    
    
    def _generate_random_shapes(
            self,
            n: int,
            oplim: tuple[float, float] = (0.05,0.15),
            sclim: tuple[float, float] = (0.15,0.25)
        ):
        
        mobs = VGroup()

        for i in range(n):
            side_shift = (np.random.rand() - 0.5) * self.span
            vert_shift = (np.random.rand() - 0.5) * self.span
            total_shift = side_shift * RIGHT + vert_shift * UP
            shape = np.random.choice(self.base_shapes)
            opacity = interpolate(*oplim, np.random.rand())
            scale = interpolate(*sclim, np.random.rand())
            element = shape()              \
                .scale(scale)              \
                .set_opacity(opacity)      \
                .set_color(random_color()) \
                .shift(total_shift)
            element.init_center = element.get_center()
            element.t = 0.0
            self.add(element)
    
    
    def fadein(self, lag_ratio=0.01, scale=0.2):
        return LaggedStart(
            *[FadeIn(el, scale=scale) for el in self.mobs],
            lag_ratio=lag_ratio,
        )

    
    def fadeout_with_random_shift(self, lag_ratio=0.01, distance=1.0):
        anims = []
        for el in self.mobs:
            shift = shift=np.random.rand(3)-0.5
            shift *= distance
            anims.append(FadeOut(el, shift=shift))
        
        return AnimationGroup(*anims, lag_ratio=lag_ratio)


    def start_swinging(self, alims=[0.005,0.01], flims=[0.1,0.3]):
        def update_func(mob, dt, amp_vec, freq):
            mob.t += dt
            shift = amp_vec * np.sin(2*PI*freq * mob.t)
            mob.shift(shift)
            
        for mob in self.mobs:
            freq = interpolate(*flims, np.random.rand())
            ampl = interpolate(*alims, np.random.rand())
            direction  = np.random.rand(3) - 0.5
            direction /= np.linalg.norm(direction)
            amp_vec = ampl * direction
            mob.add_updater(
                # Named parameters to pass by assignment
                lambda mob, dt, a=amp_vec, f=freq: update_func(mob, dt, a, f)
            )


    def stop_swinging(self):
        anims = []
        for mob in self.mobs:
            mob.clear_updaters()
            mob.t = 0.0
            anims.append(mob.animate.move_to(mob.init_center))
        return AnimationGroup(*anims, lag_ratio=0.01)
    
    
    def shift_randomly(self, amount=1.0):
        anims = []
        for mob in self.mobs:
            side_shift = (np.random.rand() - 0.5) * self.span
            vert_shift = (np.random.rand() - 0.5) * self.span
            total_shift = side_shift * RIGHT + vert_shift * UP
            total_shift *= amount
            ani = mob.animate.shift(total_shift)
            anims.append(ani)
        return LaggedStart(*anims, lag_ratio=0.001)

    
    def revert_to_original_state(self):
        anims = [mob.animate.move_to(mob.init_center) for mob in self.mobs]
        return LaggedStart(*anims, lag_ratio=0.001)
        
