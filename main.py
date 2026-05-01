from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
import random
import os

# Force black background
Window.clearcolor = (0.02, 0.02, 0.02, 1)

class Exit47Game(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.padding = [30, 30, 30, 30]
        self.spacing = 15
        
        # Game State
        self.unlocked_chapters = self.load_progress()
        self.text_speed = 0.08  
        self.is_typing = False
        self.type_event = None
        
        self.build_main_menu()

    # =====================================================================
    # 💾 PROGRESS SYSTEM
    # =====================================================================
    def load_progress(self):
        if os.path.exists("save_data.txt"):
            try:
                with open("save_data.txt", "r") as f:
                    return int(f.read().strip())
            except: return 1
        return 1

    def save_progress(self, chapter_num):
        # Only save if the new chapter is higher than what we already have
        current = self.load_progress()
        if chapter_num > current:
            with open("save_data.txt", "w") as f:
                f.write(str(chapter_num))
            self.unlocked_chapters = chapter_num

    # =====================================================================
    # 🏠 MENUS
    # =====================================================================
    def build_main_menu(self, *args):
        self.unlocked_chapters = self.load_progress() # Refresh progress
        self.clear_widgets()
        
        title_box = BoxLayout(orientation='vertical', size_hint_y=0.4)
        title_box.add_widget(Label(text="EXIT 47", font_size='65sp', bold=True))
        title_box.add_widget(Label(text="By hoyy", font_size='18sp', color=(0.5, 0.5, 0.5, 1)))
        self.add_widget(title_box)
        
        btn_layout = BoxLayout(orientation='vertical', spacing=15, size_hint_y=0.6, padding=[60, 20])
        
        # NEW GAME always starts Chapter 1
        new_game = Button(text="NEW GAME", background_color=(0.1, 0.1, 0.1, 1), font_size='20sp')
        new_game.bind(on_release=lambda x: self.start_chapter_1())
        btn_layout.add_widget(new_game)
        
        # CHAPTER SELECT
        chap_btn = Button(text="CHAPTER SELECT", background_color=(0.1, 0.1, 0.1, 1), font_size='20sp')
        chap_btn.bind(on_release=self.build_chapter_select)
        btn_layout.add_widget(chap_btn)
        
        # SETTINGS
        settings_btn = Button(text="SETTINGS", background_color=(0.1, 0.1, 0.1, 1), font_size='20sp')
        settings_btn.bind(on_release=self.build_settings_menu)
        btn_layout.add_widget(settings_btn)
        
        exit_btn = Button(text="EXIT", background_color=(0.1, 0.1, 0.1, 1), font_size='20sp')
        exit_btn.bind(on_release=lambda x: App.get_running_app().stop())
        btn_layout.add_widget(exit_btn)
        
        self.add_widget(btn_layout)

    def build_chapter_select(self, *args):
        self.clear_widgets()
        self.add_widget(Label(text="SELECT CHAPTER", font_size='40sp', bold=True, size_hint_y=0.2))
        
        chap_layout = BoxLayout(orientation='vertical', spacing=15, padding=[60, 20], size_hint_y=0.6)
        
        # List of chapters in the game
        chapters = [
            ("CHAPTER 1: A DAY AT OFFICE", 1, self.start_chapter_1),
            ("CHAPTER 2: THE DROP (LOCKED)", 2, None), # Placeholder for future
            ("CHAPTER 3: EXIT 47 (LOCKED)", 3, None)
        ]
        
        for name, num, cmd in chapters:
            if num <= self.unlocked_chapters:
                # UNLOCKED
                btn = Button(text=name.replace(" (LOCKED)", ""), background_color=(0.1, 0.4, 0.1, 1))
                if cmd: btn.bind(on_release=lambda x, c=cmd: c())
            else:
                # LOCKED
                btn = Button(text=name, background_color=(0.05, 0.05, 0.05, 1), color=(0.3, 0.3, 0.3, 1))
            
            chap_layout.add_widget(btn)
            
        self.add_widget(chap_layout)
        
        back = Button(text="BACK", size_hint_y=0.15, background_color=(0.3, 0, 0, 1))
        back.bind(on_release=self.build_main_menu)
        self.add_widget(back)

    def build_settings_menu(self, *args):
        self.clear_widgets()
        self.add_widget(Label(text="SETTINGS", font_size='40sp', bold=True, size_hint_y=0.2))
        setting_box = BoxLayout(orientation='vertical', spacing=20, padding=[60, 40], size_hint_y=0.6)
        setting_box.add_widget(Label(text="TEXT SPEED", font_size='20sp', color=(0.7,0.7,0.7,1)))
        
        speeds = [("SLOW", 0.15), ("STEADY", 0.08), ("FAST", 0.03), ("INSTANT", 0.001)]
        for name, val in speeds:
            btn = Button(text=name, background_color=(0.15, 0.15, 0.15, 1))
            if self.text_speed == val: btn.background_color = (0.3, 0.3, 0.3, 1)
            btn.bind(on_release=lambda x, v=val: self.set_speed(v))
            setting_box.add_widget(btn)
            
        self.add_widget(setting_box)
        back = Button(text="BACK TO MENU", size_hint_y=0.2, background_color=(0.3, 0, 0, 1))
        back.bind(on_release=self.build_main_menu)
        self.add_widget(back)

    def set_speed(self, value):
        self.text_speed = value
        self.build_settings_menu()

    def setup_game_screen(self):
        self.clear_widgets()
        header = BoxLayout(size_hint_y=None, height='70dp')
        header.add_widget(Label(text="EXIT 47", font_size='26sp', bold=True))
        menu_btn = Button(text="MENU", size_hint_x=None, width='100dp', background_color=(0.3, 0, 0, 1))
        menu_btn.bind(on_release=self.build_main_menu)
        header.add_widget(menu_btn)
        self.add_widget(header)
        
        self.story_label = Label(text="", font_size='20sp', text_size=(Window.width - 100, None), halign='left', valign='top', line_height=1.2)
        self.add_widget(self.story_label)
        
        self.timer_container = BoxLayout(size_hint_y=None, height='12dp')
        self.timer_widget = Label(text="") 
        self.timer_container.add_widget(self.timer_widget)
        self.timer_container.opacity = 0
        self.add_widget(self.timer_container)
        
        with self.timer_widget.canvas.before:
            Color(1, 0, 0, 1)
            self.timer_rect = Rectangle(pos=self.timer_widget.pos, size=(0, 12))
        
        self.button_area = BoxLayout(orientation='vertical', size_hint_y=None, height='220dp', spacing=15)
        self.add_widget(self.button_area)

    # =====================================================================
    # 🚨 ENGINE
    # =====================================================================
    def on_touch_down(self, touch):
        if self.is_typing:
            self.skip_text()
            return True
        return super().on_touch_down(touch)

    def skip_text(self):
        if self.type_event: Clock.unschedule(self.type_event)
        self.is_typing = False
        self.story_label.text = self.full_text
        self.display_controls()

    def write_text(self, text_list, callback=None, choice_data=None):
        self.setup_game_screen() 
        self.full_text = "\n\n".join(text_list)
        self.char_index = 0
        self.callback = callback
        self.choice_data = choice_data
        self.is_typing = True
        self.simulate_typewriter()

    def simulate_typewriter(self, *args):
        if self.char_index < len(self.full_text):
            self.story_label.text += self.full_text[self.char_index]
            self.char_index += 1
            delay = self.text_speed + random.uniform(-0.02, 0.02)
            self.type_event = Clock.schedule_once(self.simulate_typewriter, delay)
        else:
            self.is_typing = False
            self.display_controls()

    def display_controls(self):
        self.button_area.clear_widgets()
        if self.choice_data:
            self.timer_container.opacity = 1
            self.time_left = self.choice_data['time']
            self.total_t = self.time_left
            btn1 = Button(text=self.choice_data['a_text'], background_color=(0.15, 0.15, 0.15, 1), font_size='18sp')
            btn1.bind(on_release=lambda x: self.process_choice(self.choice_data['a_cmd']))
            btn2 = Button(text=self.choice_data['b_text'], background_color=(0.15, 0.15, 0.15, 1), font_size='18sp')
            btn2.bind(on_release=lambda x: self.process_choice(self.choice_data['b_cmd']))
            self.button_area.add_widget(btn1)
            self.button_area.add_widget(btn2)
            self.timer_clock = Clock.schedule_interval(self.run_timer, 0.05)
        else:
            cont = Button(text=">> TAP TO CONTINUE <<", background_color=(0,0,0,0), color=(0.5, 0.5, 0.5, 1))
            cont.bind(on_release=lambda x: self.callback())
            self.button_area.add_widget(cont)

    def run_timer(self, dt):
        self.time_left -= dt
        if self.time_left <= 0:
            Clock.unschedule(self.timer_clock)
            self.process_choice(self.choice_data['df'])
            return
        prog = self.time_left / self.total_t
        self.timer_rect.size = (self.timer_widget.width * prog, 12)
        self.timer_rect.pos = self.timer_widget.pos

    def process_choice(self, cmd):
        if hasattr(self, 'timer_clock'): Clock.unschedule(self.timer_clock)
        self.timer_container.opacity = 0
        cmd()

    # =====================================================================
    # 📖 CHAPTER 1: THE STORY
    # =====================================================================
    def start_chapter_1(self):
        self.write_text([
            "I wake up at 6:45 AM with my heart hammering against my ribs. I'm fifteen minutes late for work. My brain is foggy from whatever happened last night, and my bare feet hit the cold floor."
        ], choice_data={
            'a_text': "Rush out of bed", 'a_cmd': self.c1_rush,
            'b_text': "Pause for moment", 'b_cmd': self.c1_pause,
            'time': 7, 'df': self.c1_freeze
        })

    def c1_rush(self):
        self.write_text(["I shove the blankets off, ignore the alarm, and rush straight downstairs as fast as I can."], self.c1_kitchen)

    def c1_pause(self):
        self.write_text(["I sit on the bed for a few moments, reach over to switch off the alarm, and walk downstairs slowly."], self.c1_kitchen)

    def c1_freeze(self):
        self.write_text(["I just sit there on the edge of the bed staring at the wall until Anna calls out to me."], self.c1_kitchen)

    def c1_kitchen(self):
        self.write_text([
            "I hop downstairs. The first thing I see is Anna, my lady from heaven, in the kitchen preparing breakfast.",
            "\"Good morning!\" she says, her eyes widening.",
            "\"Morning... uhm, why didn't you wake me up?\" I ask.",
            "She looks back at the sizzling pan. \"I didn't wanna disturb your peaceful sleep, plus I wanted you to wake up on your own without me nagging you every morning,\" she responds.",
            "Marrying Anna was a dream. She looked like a princess pulled out of a Disney movie."
        ], self.c1_workshop)

    def c1_workshop(self):
        self.write_text([
            "After breakfast, we went to work. A year ago, 'SOUTH MOVERS' was created. Leo and Sarah joined the company.",
            "When we get to the workshop, Leo is already loading the items onto the back of the truck.",
            "\"Mark, can you get a move on and help me with this?\" Leo says.",
            "\"Fine, we'll take your scenic route, but only if you are driving,\" Anna responds."
        ], self.c1_drive)

    def c1_drive(self):
        self.write_text([
            "Our customer is moving far away from New Mexico, so this delivery is gonna be a long one. Anna looks out the window, looking magical.",
            "\"Hey, how long are you gonna keep drooling over your wife man, you look like you just met her,\" Leo whispers to me."
        ], choice_data={
            'a_text': "whisper back", 'a_cmd': self.c1_sincere,
            'b_text': "joke about it", 'b_cmd': self.c1_deflect,
            'time': 8, 'df': self.c1_silent
        })

    def c1_sincere(self):
        self.write_text(["I whisper back, \"I just can't get over the fact that I'm married to her.\"", "Leo smiles. \"Well get used to it man.\""], self.finish_c1)

    def c1_deflect(self):
        self.write_text(["I chuckle. \"Just making sure she doesn't fire us.\"", "Leo smirks and shakes his head."], self.finish_c1)

    def c1_silent(self):
        self.write_text(["I just smile softly and don't say anything.", "Leo mutters, \"Hopeless.\""], self.finish_c1)

    def finish_c1(self):
        self.save_progress(2) # Unlock Chapter 2
        self.write_text(["[END OF CHAPTER 1]", "Chapter 2 is now unlocked in Chapter Select.", "Returning to Menu..."], self.build_main_menu)

class Exit47App(App):
    def build(self):
        return Exit47Game()

if __name__ == '__main__':
    Exit47App().run()
