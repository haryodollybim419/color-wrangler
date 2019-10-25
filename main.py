from __future__ import annotations
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.properties import( NumericProperty, ReferenceListProperty,
                             ObjectProperty, BooleanProperty,
                             StringProperty,ListProperty)
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivy.core.audio import SoundLoader
from kivy.vector import Vector
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.utils import platform
Window.clearcolor = (64/255.0, 64/255.0, 64/255.0, 0)

from typing import Optional, List
import random
from kivy.utils import platform
import sys

#for ads, uncomment the code with ("*")
#("*") from jnius import autoclass

#("*")
##if platform=="android":
##    PythonActivity=autoclass("org.renpy.android.PythonActivity")
##    AdBuddiz=autoclass("com.purplebrain.adbuddiz.sdk.AdBuddiz")



Window.size = (750, 600)


COLORS = [[0.85, 0, 0], [128/256, 128,256, 128/256], [255/256, 204/256, 204/256], [0.478754546, 0.256789, 1], [0.257890, 1, 0.6078127654], [0.5678, 0.455657, 0.233546], [153/255, 0, 76/255]]
        
        
class Color(Widget):
    pass

class ScorePopup(Popup):
    score = NumericProperty(0)
    high_score = NumericProperty(0)
    is_open = BooleanProperty(False)
    


class AnimateBallIntro(Widget):
    pass

class AnimateBarriersIntro(Image):
    def __init__(self, **kwargs):
        super(AnimateBarriersIntro, self).__init__(**kwargs)
        self.source = 'icons/barrier.png'

        

class WelcomeScreen(Screen):
    play_button = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)

    def exit_game(self):
        App.get_running_app().stop()

    def animate(self, instance): 
        Animation.cancel_all(instance) 
        anim = Animation(pos=(250, 400), t='in_bounce')
        anim += Animation(pos=(250, 400), t='in_elastic')
        count_anim_pos = 0
        for i in range(2):
            anim += Animation(pos=(250 + i*50, 400))
            count_anim_pos += (250 + i*50)
        for j in range(5):
            anim += Animation(pos=(count_anim_pos, 500+j*30), t='in_elastic')
        anim.start(instance)

    def animate_barriers(self, instance):
        Animation.cancel_all(instance)
        anim = Animation(pos=(125, 118))
        anim.start(instance)


class GameScreen(Screen):
    ball = ObjectProperty(None)
    score = NumericProperty(0)
    paddles = ListProperty([])
    end_point = ObjectProperty(None)
    first_barrier_loc = ListProperty([(50, 100)])
    max_per_screen = NumericProperty(15)
    on_pause = BooleanProperty(False)
    score_data = ListProperty([])
    end_score = NumericProperty(0)
    high_score = NumericProperty(0)
    score_obj = ObjectProperty(None)
    #ads_on_play = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.sound = SoundLoader.load('data/Cyberpunk Moonlight Sonata.wav')
        self.hit_paddle_sound = SoundLoader.load('data/hit_paddle.wav')
        self.hit_wrong_paddle_sound = SoundLoader.load('data/hit_red_paddle.wav')
        self.bind(size=self.size_callback)
        self.get_high_score()
        self.change_ball_once = 0
        self.game_clock = Clock
        #("*")
##        if platform=="android":
##            AdBuddiz.setPublisherKey("publish key"); #publisher ker
##            Adbuddiz.setTestModeActive();  #for testing purposes
##            Adbuddiz.cacheAds(PythonActivity.mActivity); #this will cache ads

    def show_ads(self):
        if platform=="android":
            Adbuddiz.showAd(PythonActivity.mActivity) #show a popup

    

    def check_sound(self, dt = None):
        self.sound.loop = True
        self.sound.play()

    def open_score_popup(self):
        self.score_obj.open()
        #("*")self.show_ads()
        #print("catching ads...") #for testing uncomment

    

    def play_game_sound(self):
        #Clock.schedule_interval(self.check_sound, 1.0)
        self.check_sound()
       

    def get_high_score(self):
        with open("data/score.txt", "r") as file:
            data = file.read()
            self.high_score = int(data)
            self.score_obj = ScorePopup()
        file.close()

    def write_high_score(self, score):
        open("data/score.txt", 'w').close()
        with open("data/score.txt", "w") as file:
            data = file.write(str(score))
        file.close()
    
    def add_new_paddles(self, remove=True):
        if remove:
            self.remove_paddles()
        new_paddles = Paddle()
        new_paddles.update_position()
        new_paddles.velocity = [-(random.randrange(5, 20)), 0]
        new_paddles.change_paddle_color()
        self.add_widget(new_paddles)
        self.paddles = self.paddles + [new_paddles]

        
    def size_callback(self, instance, value):
        for paddle in self.paddles:
            paddle.height = value[1]
            paddle.update_position()

    def on_touch_down(self, touch):
        #pos_hit 
        #bottom 35
        #right 715
        #left 45
        #top 505
        
        #self.My_Clock.unschedule(self.Update)
        if 567 <= touch.pos[0] <= 593  and 545 <= touch.pos[1] <= 588:
            self.on_pause = False
            self.switch_screen_to_end()
        if 365 <= touch.pos[0] <= 395  and 545 <= touch.pos[1] <= 588:
            self.on_pause = False
            self.switch_screen_to_welcome()
        if touch.pos[1] < 540:
            if self.on_pause == False:
                self.game_clock.schedule_interval(self.update, 1.0/60.0)
            self.ball.ball_pos.append(self.pos[:])
            if self.ball.pos[0] <= self.ball.ball_pos[0][0] + 650:
                if self.ball.pos[1] <= self.ball.ball_pos[0][1] + 10:
                    self.ball.velocity = [5, 11]
                else:
                    self.ball.velocity = [5, -11]
            else:
                self.ball.move_back_state = True
                self.ball.velocity = [-4, 0]
            self.ball.ball_pos[1:] = []

    
    def update(self, dt):
        self.on_pause = True
        self.ball.move()
        if len(self.paddles) < self.max_per_screen:
            self.add_new_paddles(remove=False)
        for paddle in self.paddles:
            if paddle.x < -20:
                self.remove_widget(paddle)
                self.paddles.remove(paddle)
            if paddle.x >= -20:
                paddle.move()

        for paddle in self.paddles:
            if self.ball.collide_widget(paddle):
                if self.score <= -500:
                    if self.score_obj.is_open == False:
                        self.open_score_popup()
                        self.score_obj.is_open = True
                if paddle.paddle_color == COLORS[0] and not(self.score < -500):
                    self.score -= 15
                    self.hit_wrong_paddle_sound.play()
                else:
                    if self.ball.hit_color == paddle.paddle_color and not(self.score < -500):
                        self.hit_paddle_sound.play()
                        self.remove_widget(paddle)
                        self.paddles.remove(paddle)
                        self.score += 50
                        if self.score > 0:
                            self.score_data.append(self.score)
                            if max(self.score_data) > 1:
                                self.score_data = [max(self.score_data)]
                        if len(self.score_data) > 0:
                           self.end_score =  max(self.end_score, self.score_data[-1])
                           self.score_obj.score = self.end_score
                           if  self.change_ball_once == 0:
                               self.change_ball_once += 1
                               #self.ball.change_ball_color()
                               
                        
        if self.high_score < self.end_score:
            self.write_high_score(self.end_score)
            self.score_obj.high_score = self.end_score
        else:
            self.score_obj.high_score = self.high_score
            
                
                
        if 710 <= self.ball.pos[0] <= 720:
            #right
            self.ball.velocity = [-8, 0]
            
        elif 40 <= self.ball.pos[0] <= 50:
            
            #left
            self.ball.velocity = [8, 0]
            
        elif 500<= self.ball.pos[1] <= 510:
            #up
            self.ball.velocity = [0, -7]
            
        elif 30<= self.ball.pos[1] <= 40:
            #down
            self.ball.velocity = [0, 7]

    def switch_screen_to_welcome(self, *args):
        app = App.get_running_app()
        app.root.current_screen.game_clock.unschedule(app.root.current_screen.update)
        app.root.current = "welcome"

    def switch_screen_to_end(self, *args):
        app = App.get_running_app()
        app.root.current_screen.game_clock.unschedule(app.root.current_screen.update)
        app.root.current = "endscreen"
        
class EndPoint(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos
    

class Paddle(Widget):
    paddle_color = ListProperty([1,random.uniform(0, 1),
                              random.uniform(0, 1)])
    gap_pos = NumericProperty(50)
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    marked = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(Paddle, self).__init__(**kwargs)
        self.size = [random.randrange(50, 100), 30]
        self.pos = [200,
        random.randrange(35, 435)]

    def update_position(self):
        #least (45, 35)
        #highest (645, 435)
        #650 self.pos.x
        self.size_hint = (None, None)
        self.size = [random.randrange(50, 100), 30]
        self.pos = [650,
        random.randrange(35, 435)]
        

    def change_paddle_color(self):
        self.paddle_color = random.choice(COLORS)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class Ball(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    hit_color = ListProperty(random.choice(COLORS[1:]))
    ball_pos = ListProperty([])
    
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

    def change_ball_color(self):
        self.hit_color = random.choice(COLORS[1:])
       
        
class FowardButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(FowardButton, self).__init__(**kwargs)
        self.source = 'icons/forward-icon.png'

class BackwardButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(BackwardButton, self).__init__(**kwargs)
        self.source = 'icons/back-icon.png'

    def switch_screen_to_welcome(self, *args):
        app = App.get_running_app()
        if app.root.current == "game":
            app.root.current_screen.game_clock.unschedule(app.root.current_screen.update)
        app.root.current = "welcome"

    def switch_screen_to_game(self, *args):
        app = App.get_running_app()
        app.root.current = "game"


class PlayButtonIntro(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(PlayButtonIntro, self).__init__(**kwargs)
        self.source = 'icons/play_icon3.png'

    def on_release(self):
        self.source = 'icons/play_icon4.png'

    def clocked_switch(self):
        Clock.schedule_once(self.switch_screen_to_game, 3)

    def switch_screen_to_game(self, *args):
        app = App.get_running_app()
        app.root.current = "game"
        app.root.current_screen.play_game_sound()
        app.root.current_screen.score_obj.is_open = False
        app.root.current_screen.score_data = []
        app.root.current_screen.score_obj.score = 0
        app.root.current_screen.end_score = 0
        app.root.current_screen.ball.change_ball_color()
        app.root.current_screen.score = 0
        app.root.current_screen.on_pause = False

class EndScreen(Screen):
    def __init__(self, **kwargs):
        super(EndScreen, self).__init__(**kwargs)

    def switch_screen_to_game(self, *args):
        app = App.get_running_app()
        app.root.current = "game"
        app.root.current_screen.play_game_sound()
        app.root.current_screen.score_obj.is_open = False
        app.root.current_screen.score_data = []
        app.root.current_screen.score_obj.score = 0
        app.root.current_screen.end_score = 0
        app.root.current_screen.ball.change_ball_color()
        app.root.current_screen.score = 0
        
    
class ColorWranglerApp(App):
    def build(self):
        self.icon = 'icons/paintball.png'
        game = GameScreen(name="game")
        sm.add_widget(WelcomeScreen(name="welcome"))
        sm.add_widget(EndScreen(name="endscreen"))
        sm.add_widget(game)
        return sm

if __name__ == "__main__":
    sm = ScreenManager()
    ColorWranglerApp().run()
