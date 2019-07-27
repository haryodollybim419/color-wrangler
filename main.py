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
Window.clearcolor = (64/255.0, 64/255.0, 64/255.0, 0)
import math

from typing import Optional, List
import random

import sys


COLORS = [[0.85, 0, 0], [0.478754546, 0.256789, 1], [0.257890, 1, 0.6078127654], [0.5678, 0.455657, 0.233546], [153/255, 0, 76/255]]

class Color(Widget):
    pass

class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)
        #self.sound = SoundLoader.load('data/drum_roll.flac')

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
        #self.sound.play()

    def animate_barriers(self, instance):
        Animation.cancel_all(instance)
        anim = Animation(pos=(125, 170))
        anim.start(instance)



class GameScreen(Screen):
    ball = ObjectProperty(None)
    score = NumericProperty(0)
    paddles = ListProperty([])
    end_point = ObjectProperty(None)
    first_barrier_loc = ListProperty([(50, 200)])
    max_per_screen = NumericProperty(25)

    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.bind(size=self.size_callback)
    
    def add_new_paddles(self, remove=True):
        if remove:
            self.remove_paddles()
        new_paddles = Paddle()
        new_paddles.update_position()
        new_paddles.velocity = [-(random.randrange(5, 25)), 0]
        new_paddles.change_paddle_color()
        self.add_widget(new_paddles)
        self.paddles = self.paddles + [new_paddles]

        
    def size_callback(self, instance, value):
        for paddle in self.paddles:
            paddle.height = value[1]
            paddle.update_position()

    
    def update(self, dt):
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
                if paddle.paddle_color == COLORS[0]:
                    self.score -= 1
                else:
                    if self.ball.hit_color == paddle.paddle_color:
                        self.remove_widget(paddle)
                        self.paddles.remove(paddle)
                        self.score += 10
            

        if 710 <= self.ball.pos[0] <= 720:
            #right
            self.ball.velocity = [-5.0, 0]
            
        elif 40 <= self.ball.pos[0] <= 50:
            
            #left
            self.ball.velocity = [5.0, 0]
            
        elif 500<= self.ball.pos[1] <= 510:
            #up
            self.ball.velocity = [0, -4]
            
        elif 30<= self.ball.pos[1] <= 40:
            #down
            self.ball.velocity = [0, 4]
        
        
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


    def on_touch_down(self, touch):
        #pos_hit 
        #bottom 35
        #right 715
        #left 45
        #top 505
        
        self.ball_pos.append(self.pos[:])
        if self.pos[0] <= self.ball_pos[0][0] + 650:
            if self.pos[1] <= self.ball_pos[0][1] + 10:
                self.velocity = [2, 8]
            else:
                self.velocity = [2, -8]
        else:
            self.move_back_state = True
            self.velocity = [-4, 0]
        self.ball_pos[1:] = []

       
        
##class FowardButton(ButtonBehavior, Image):
##    def __init__(self, **kwargs):
##        super(FowardButton, self).__init__(**kwargs)
##        self.source = 'icons/forward-icon.png'

class BackwardButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(BackwardButton, self).__init__(**kwargs)
        self.source = 'icons/back-icon.png'

    def switch_screen_to_game(self, *args):
        app = App.get_running_app()
        app.root.current = "welcome"

class PlayButtonIntro(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(PlayButtonIntro, self).__init__(**kwargs)
        self.source = 'icons/play_icon3.png'

    def on_release(self):
        self.source = 'icons/play_icon4.png'

    def clocked_switch(self):
        Clock.schedule_once(self.switch_screen_to_game, 9.5)

    def switch_screen_to_game(self, *args):
        app = App.get_running_app()
        app.root.current = "game"

class AnimateBallIntro(Widget):
    pass

class AnimateBarriersIntro(Image):
    def __init__(self, **kwargs):
        super(AnimateBarriersIntro, self).__init__(**kwargs)
        self.source = 'icons/barrier.png'

class BallWranglerApp(App):
    def build(self):
        self.icon = 'icons/barrier.png'
        game = GameScreen(name="game")
        sm.add_widget(WelcomeScreen(name="welcome"))
        sm.add_widget(game)
        Clock.schedule_interval(game.update, 1.0/60.0)
        return sm

if __name__ == "__main__":
    sm = ScreenManager()
    BallWranglerApp().run()
