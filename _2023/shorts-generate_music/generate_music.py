import os

from manim import *
from movi_ext import *


#%%
SceneExtension.CONFIG = dict(
    frame_width = 3/5 * 8,
    frame_height = 3/5 * 8 * 16/9
)


#is_melodic = False  # Youtube: Из технаря в композиторы: какофоничный порядок
is_melodic = True  # Youtube: Из технаря в композиторы: этюд в до мажоре


#%%
def get_sample(name):
    ''' name -- название ноты, напр. 'A#4' '''
    return os.path.join(repo_root, f'custom/sounds/notes_piano/{name}.mp3')


#%%
class MovingDot(Dot):
    def __init__(self, point,
                 radius=DEFAULT_DOT_RADIUS,
                 rot_freq=1,
                 note='C5',
                 text_pos=None,
                 **kwargs):
        super().__init__(point, radius, **kwargs)
        self.freq = rot_freq
        self.om = 2 * PI * rot_freq
        self.note = note
        self.gain = 0
        
        self.text = Text(note, font_size=24, color=self.get_color()).scale(0.6)
        self.text_orig_opacity = 0.2
        self.text.set_opacity(self.text_orig_opacity)
        self.text_opacity_max = 1
        self.fade_color = BLACK
        if text_pos:
            self.text.move_to(text_pos)

        self.tail = TracedPath(self.get_center,
                               dissipating_time=0.1,
                               stroke_opacity=[0.5, 0],
                               stroke_color=self.get_color()
                               )
        self.color_orig = self.get_color()
        
        self.update_duration = 0.5
        self.timer = 0
        
    
    # Добавляем / удаляем апдейтеры
    def activate_updater(self):
        if not self.check_updater():
            self.add_updater(self.update_with_timer)
    # def deactivate_updater(self):
        # if self.check_updater():
            # self.remove_updater(self.update_with_timer)
    def check_updater(self):
        return self.update_with_timer in self.updaters
    
    def set_gain(self, gain):
        self.gain = gain
        self.update_fade_color()
        self.update_max_text_opacity()
    
    def update_max_text_opacity(self):
        alpha = np.exp(self.gain)  # Если gain=0, то alpha=1
        self.text_opacity_max = 1 * alpha + self.text_orig_opacity * (1 - alpha)
    def update_fade_color(self):
        alpha = np.exp(self.gain)  # Если gain=0, то alpha=1
        self.fade_color = interpolate_color(BLACK, self.color_orig, alpha)

    def reset_timer(self):
        self.timer = self.update_duration
        #self.activate_updater()

    def update_with_timer(self, mob, dt):
        if self.timer == 0:
            return
        self.timer -= dt
        if self.timer < 0:
            self.timer = 0
            #self.deactivate_updater()
        alpha = 1 - self.timer / self.update_duration
        self.set(fill_color=interpolate_color(self.fade_color, self.color_orig, alpha))
        self.text.set_opacity(interpolate(self.text_opacity_max, self.text_orig_opacity, alpha))

    def get_sound(self):
        return get_sample(self.note)
    
    def set_sound(self, note):
        self.note = note


#%%
class DotsGenerateMusic(MovingCameraScene, SceneExtension):
    def construct(self):
        #
        # Струны
        #
        string  = Line(ORIGIN + MED_SMALL_BUFF * UP,   2 * UP,   color=GOLD, stroke_opacity=0.8, stroke_width=2)
        string2 = Line(ORIGIN + MED_SMALL_BUFF * DOWN, 2 * DOWN, color=GOLD, stroke_opacity=0.8, stroke_width=2)
        string3  = Line(ORIGIN + MED_SMALL_BUFF * LEFT,   2 * LEFT,   color=GOLD, stroke_opacity=0.8, stroke_width=2)
        string4  = Line(ORIGIN + MED_SMALL_BUFF * RIGHT,   2 * RIGHT,   color=GOLD, stroke_opacity=0.8, stroke_width=2)
        strings = VGroup(string, string2, string3, string4)
        
        notes  = self.get_note_list('C','C#','D','D#','E','F','F#','G','G#','A','A#','B')
        N = len(notes) - 1
        freq_min = 0.5
        #freq_max = freq_min + N / 56  # Df = (N_шариков - 1) / желаемое_время_ролика
        freq_max = freq_min + 1/2 * N / 56  # Df = (N_шариков - 1) / желаемое_время_ролика --> половина полного суммарного периода
        freqs = [ (1-i/N)*freq_min + i/N*freq_max for i in range(len(notes))]

        mdots = VGroup()
        tails = VGroup()
        texts = VGroup()
        self.mdots = mdots
        colors = color_gradient((WHITE,BLUE_E,RED_A), N+1)
        shift_min = 0.7
        shift_max = 1.9
        def get_shift(freq):
            shift  = shift_min * (freq_max - freq) + shift_max * (freq - freq_min)
            shift /= (freq_max - freq_min)
            return shift
        for note, freq, color in zip(notes, freqs, colors):
            pos = get_shift(freq) * LEFT
            mdot = MovingDot(
                pos,
                radius=0.065,
                rot_freq=freq,
                note=note,
                color=color,
                stroke_width=2,
            )
            mdots.add(mdot)
            tails.add(mdot.tail)
            texts.add(mdot.text)
        texts.arrange_in_grid(rows=6, cols=6, buff=0.13).next_to(string2, DOWN)

        
        #
        # Фон
        #
        anims = []
        shapes = (Triangle, Square, Circle)
        for i in range(100):
            side_shift = (np.random.rand() - 0.5) * self.CONFIG['frame_height']
            vert_shift = (np.random.rand() - 0.5) * self.CONFIG['frame_height']
            total_shift = side_shift * RIGHT + vert_shift * UP
            shape = np.random.choice(shapes)
            element = shape(stroke_width=2).scale(0.2).shift(total_shift).set_opacity(0.05).set_color(random_color())
            anims.append(Create(element))


        self.play(
            LaggedStart(*anims, lag_ratio=0.01),
            LaggedStart(*[FadeIn(mdot) for mdot in mdots], lag_ratio=0.02),
            FadeIn(tails),
            FadeIn(texts),
            Create(strings),
        )
        
        
        [mdot.add_updater(self.func_updater) for mdot in mdots]
        [mdot.activate_updater() for mdot in mdots]
        
        # Bug: https://github.com/ManimCommunity/manim/issues/3950
        # LaggedStart does not resume updating, manim 0.18.1
        # This is a hot-fix
        mdots.resume_updating()
        
 
        def create_connecting_lines():
            lines = VGroup()
            for i in range(len(mdots) - 1):
                cur = mdots[i+1]
                pre = mdots[i]
                line = Line(pre.get_center(), cur.get_center(),
                            stroke_width=1)
                line.set_opacity(0.5)
                lines.add(line)
            return lines
        
        lines = always_redraw(create_connecting_lines)
        self.add(lines)
        
        #
        # Заголовок
        #
        #cap1 = Text('шарики выбивают', font="PT Sans Caption")
        #cap2 = Text('ноты из струны', font="PT Sans Caption")
        #cap_grp = VGroup(cap1, cap2).arrange(DOWN).set_color((BLUE,GRAY_A)).scale(0.42).next_to(string, UP)

        #self.play(Create(string), Create(string2), Write(cap_grp))


        if not is_melodic:
            self.play_all()
        else:
            chords = ('C', 'F', 'G', 'Am', 'F', 'G', 'C', 'G')
            chords *= 2
            durations = (56 / len(chords),) * len(chords)
            chords += ('C',)
            durations += (1,)
            self.play_melodically(chords, durations)


    def get_note_list(self, *notes, octaves=(3,4,5)):
        return [note + str(oc) for oc in octaves for note in notes]


    def play_all(self):
        """ Звуки от всех шариков воспроизводятся """
        self.wait(58)


    def play_melodically(self, chords, durations):
        """ Возпроизводятся только мелодичные звуки в заданной последовательности """
        harmonies = dict(
            C = self.get_note_list('C', 'E', 'G'),
            F = self.get_note_list('F', 'A', 'C'),
            G = self.get_note_list('G', 'B', 'D'),
            Am = self.get_note_list('A', 'C', 'E'),
            all_notes = self.get_note_list('C','C#','D','D#','E','F','F#','G','G#','A','A#','B')
        )
        # Устанавливаем громкость нот в соответствии с аккордом
        def set_sound_gain_for_chord(chord):
            notes_to_play = harmonies[chord]
            for mdot in self.mdots:
                if mdot.note in notes_to_play:
                    mdot.set_gain(0)
                else:
                    mdot.set_gain(-1000)
        # Проигрываем
        for chord, duration in zip(chords, durations):
            set_sound_gain_for_chord(chord)
            corr = 1 / 60  # missed frame correction
            self.wait(duration + corr)

    
    def func_updater(self, mob, dt):
        dfi = mob.om * dt
        x_old, y_old, _ = mob.get_center()
        mob.rotate(dfi, about_point=ORIGIN)
        x_new, y_new, _ = mob.get_center()
        #if x_old >= 0 and x_new <= 0:
        if x_old * x_new < 0 or y_old * y_new < 0:
            self.add_sound(mob.get_sound(), gain=mob.gain)
            mob.reset_timer()


#%% Тестовый рендер
if __name__ == '__main__':
    
    from helpers.render import dev_render
    
    dev_render(__file__, DotsGenerateMusic)