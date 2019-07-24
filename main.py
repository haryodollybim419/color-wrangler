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

class Color(Widget):
    pass

class GameScreen(Screen):
    ball = ObjectProperty(None)
    paddles = ListProperty([])
    first_barrier_loc = ListProperty([(50, 200)])
    max_x = NumericProperty(0)
   
    
    def remove_paddles(self):
        self.remove_widget(self.paddles[0])
        self.paddles = self.paddles[1:]
        
    def add_new_paddles(self, remove=True):
        if remove:
            self.remove_paddles()
        new_paddles = Paddle()
        new_paddles.update_position()
        new_paddles.move()
        new_paddles.velocity = [-3, 0]
        #new_paddles.change_paddle_color()
        self.add_widget(new_paddles)
        print(self.paddles)
        self.paddles = self.paddles + [new_paddles]
        
        
        
    def animate(self):
        anim = Animation(pos=self.first_barrier_loc[0])    
        anim.start(self.ball)

    def update(self, dt):
        self.ball.move()
        if self.max_x <= 2:
            self.add_new_paddles(remove=False)                
            self.max_x += 1
            #self.new
        if 710 <= self.ball.pos[0] <= 720:
            #right
            self.ball.velocity = [-5.0, 0]
            
        elif 40 <= self.ball.pos[0] <= 50:
            
            #left
            self.ball.velocity = [5.0, 0]
            self.paddles[-1].velocity = [-3, 0]
            
        elif 500<= self.ball.pos[1] <= 510:
            #up
            self.ball.velocity = [0, -4]
            
        elif 30<= self.ball.pos[1] <= 40:
            #down
            self.ball.velocity = [0, 4]
        
        
            
        

class Paddle(Widget):
    length = NumericProperty(random.randint(70, 150))
    paddle_color = ListProperty([1,random.uniform(0, 1),
                              random.uniform(0, 1)])
    gap_size = NumericProperty(50)
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    marked = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(Paddle, self).__init__(**kwargs)

    def update_position(self):
        #least (45, 35)
        #highest (645, 435)
        self.size_hint = (None, None)
        self.size = (random.randrange(50, 100), 30)
        self.pos = (random.randrange(45, 645), random.randrange(35, 435))

    def change_paddle_color(self):
        self.paddle_color = random.choice([(1, 0, 1), (1,0, 0), (0.25, 1, 0)])

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos
        
    

class Ball(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    hit_color = ListProperty([1,random.uniform(0, 1),
                              random.uniform(0, 1)])
    x_bound = NumericProperty(700)
    y_bound = NumericProperty(500)
    ball_pos = ListProperty(None)
    move_back_state = BooleanProperty(None)

    
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos
    
    def bounce_ball(self,angle):
        self.velocity = Vector(2, 0).rotate(45)


    def on_touch_down(self, touch):
        #pos_hit 
        #bottom 35
        #right 715
        #left 45
        #top 505
        
        self.ball_pos.append(self.pos[:])
##        if self.pos[0] == 715:
##            #right
##            self.velocity = [-4, 0]
##            
##        elif self.pos[0] == 45:
##            print('pos', self.pos[0])
##            #left
##            self.velocity = [4, 0]
##            
##        elif self.pos[1] == 505:
##            #up
##            self.velocity = [0, -4]
##            
##        elif self.pos[1] == 35:
##            #down
##            self.velocity = [0, 4]
        
            
        if self.pos[0] <= self.ball_pos[0][0] + 650:
            if self.pos[1] <= self.ball_pos[0][1] + 10:
                self.velocity = [1.25, 4]
            else:
                self.velocity = [1.25, -4]
        else:
            self.move_back_state = True
            self.velocity = [-4, 0]
        self.ball_pos[1:] = []
        
            
            
        
class FowardButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(FowardButton, self).__init__(**kwargs)
        self.source = 'icons/forward-icon.png'

class BackwardButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(BackwardButton, self).__init__(**kwargs)
        self.source = 'icons/back-icon.png'

class BallWranglerApp(App):
    from kivy.config import Config
    Config.set('graphics', 'width', '800')
    Config.set('graphics', 'height', '400')
    
    def build(self):
        game = GameScreen()
        game.animate()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game

if __name__ == "__main__":
    BallWranglerApp().run()
