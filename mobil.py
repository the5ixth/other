from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.button import Button
import time
import random


class PongPaddle(Widget):
    score = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity_x = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    trickey_direction = 0
    trickey_degree = 0

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            self.trickey_direction = random.choice([-1,1])
            self.trickey_degree = random.randint(0,20)
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2) * 7
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset

    def move(self, ball, speed=.7):
        if ball.center_y > self.center_y:
            self.velocity = (0, speed)
        elif ball.center_y < self.center_y:
            self.velocity = ( 0, -speed)
        else:
            self.velocity = (0, 0)
        self.pos = Vector ( *self.velocity ) + self.pos
   

   
    def predict_AI(self, ball, height, width, speed=2, player_one=False, trickey=True, oponent=None):
        # get variables
        b_cntr_x, b_cntr_y = ball.center
        b_pos_x, b_pos_y = ball.pos
        b_vx, b_vy = ball.velocity
        
        #each player calculates the width different because the b_vx is negative
        if player_one:
            width_remain = b_pos_x - 50
        else:
            width_remain = width - b_pos_x -50

        frames_remain = width_remain / b_vx

        # make sure the frames remaning is pos due to b_vx negative
        if frames_remain < 0:
            frames_remain *= -1

        # calculate the y address where the ball will colide
        y_addr = b_cntr_y
        for i in range(int(frames_remain)):
            y_addr += b_vy 
   
        tgt_y = y_addr

        # calculate bounces
        while tgt_y > height *2:
            tgt_y -= height
        while tgt_y < 0 - height:
            tgt_y += height
        if tgt_y >= height:
            tgt_y = height - (tgt_y - height)
        elif tgt_y < 0:
            tgt_y = height - ( tgt_y + height)

        
        # use the enemys position against them
        if oponent and trickey:
            enmy_y = oponent.pos[1]
            if enmy_y > (height / 2 ):
                tgt_y = tgt_y +  ((( height - self.pos[1] ) / ( height / 2 ))  * 75 )
            elif enmy_y < (height / 2 ):
                tgt_y = tgt_y  - (( self.pos[1]  / ( height / 2 ))  * 75 )

            

        # try to make the ball bounce at weird angles
        elif trickey:
            tgt_y = tgt_y + ( self.trickey_direction * 5 * self.trickey_degree)

        #if tgt_y < 100:
        #    tgt_y = 100
        #if tgt_y > height - 100:
        #    tgt_y = height-100

        # if the target y is closer than the speed will allow
        if tgt_y > self.center_y:
            diff = tgt_y - self.center_y
            if diff < speed:
                self.velocity = (0, diff)
            else:
                self.velocity= (0,speed)
        elif tgt_y < self.center_y:
            diff =  self.center_y - tgt_y
            if diff < speed:
                self.velocity = (0, -diff)
            else:
                self.velocity = (0, -speed)
        elif tgt_y == self.center_y:
            self.velocity = (0, 0)


        # set the new paddles position
        self.pos = Vector( *self.velocity) + self.pos

        

class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        if 0 <= self.velocity_x < 4:
            self.velocity_x = 4
        elif 0 > self.velocity_x > -4:
            self.velocity_x = -4
        self.pos = Vector( *self.velocity ) + self.pos


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)


    def serve_ball(self, vel=(-4, 0)):
        #vel = Vector(vel).rotate(random.randint(0,360))
        self.ball.center = self.center
        self.player1.center_y = self.center[1]
        self.player2.center_y = self.center[1]
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()
    
        # bounce of paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # player ai movement
        #self.player2.center_y = self.ball.center_y
        #self.player1.center_y = self.ball.center_y
        self.player2.predict_AI(self.ball, self.top, self.width)
        self.player1.predict_AI(self.ball, self.top, self.width, player_one=True, oponent=self.player2)

        # bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        # went of to a side to score point?
        if self.ball.x < self.x:
            pts = 1
            if pts < 0:
                pts *= -1
            self.player2.score += int(pts)
            self.serve_ball(vel=(4, 0))
        if self.ball.x > self.width:
            pts = 1
            if pts < 0:
                pts *= -1
            self.player1.score += int(pts)
            self.serve_ball(vel=(-4, 0))


    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        #if touch.x > self.width - self.width / 3:
            #self.player2.center_y = touch.y


class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    PongApp().run()
