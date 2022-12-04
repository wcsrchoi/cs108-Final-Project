"""CS 108 Lab 12

This module simulates the snake game - You can move the snake to eat food and make it to grow.
                                       Game is over when the snkae hits the wall or its own body.

@author: Serita Nelesen (smn4) - distance function from the helper module of Lab 12
@date: Fall, 2014
@author Seongrim Choi (sc83)
@date: Fall, 2021
"""

from guizero import App, Drawing, PushButton, Box, Text, TextBox
from Rectangle import Rectangle
from Particle import Particle
from copy import copy


class SnakeGame:
    """ Runs as simulation of the snake game. """
    def __init__(self, app):
        
        # list of recntangles for the body
        self.r_list = []
        
        # length of snake
        self.snake_len = 1
        
        # stop_game
        self.stop_game = False
        
        # ignore_keyboard
        self.ignore_keyboard = False
        
        # score
        self.score = 0
        
        # app view
        app.title = 'Snake Game'
        app.when_key_pressed = self.process_key_event
        app.width = 750
        app.height = 600
        
        # game view
        box = Box(app, layout='grid', width=750, height=600)
        self.drawing = Drawing(box, width=750, height=550, grid=[0,0,20,1])
        self.drawing.bg = "black"
        
        # Buttons
        add_button = PushButton(box, command=self.reset, text='New Game', grid=[0, 2])
        add_button = PushButton(box, command=self.leaderboard, text='Leader Board', grid=[1, 2])
        self.score_text =Text(box, text="Score: 0", grid=[15, 2], align='right')
        self.status = Text(box, text="", grid=[13, 2], align='right')
        
        # Rectangle
        self.rectangle = Rectangle()
        
        # Particle
        self.particle = Particle()   
              
        # Draw with frame
        app.repeat(10, self.draw_frame)
        
#----------------------------------------------------------------------------------------------------       
        
    def draw_frame(self):
        """ Star to Draw! """
        
        # When game_over method is executed, stop rendering
        if self.stop_game == True:
            return 
        
        self.drawing.clear()
        self.rectangle.draw(self.drawing)
        self.particle.draw(self.drawing)
        
        # Creating a copy of the snake head.
        # As the snake moves the front rectangle is created and the tail is keep getting erased.
        r1 = copy(self.rectangle)
        self.r_list.append(r1)
        if len(self.r_list) > self.snake_len:
            self.r_list.pop(0)
            
        for rectangle in self.r_list:
            rectangle.draw(self.drawing)
            
        self.rectangle.move(self.drawing)
        
        # If the snake eats food, then grow and increase the score.
        if self.in_range(self.particle.x, self.particle.y, self.rectangle.x, self.rectangle.y):
            self.particle = Particle()
            self.snake_len += 5
            self.score += 1
            self.score_text.value = 'Score: {}'.format(self.score)
            
        # If the snake hits the wall or its own body, execute the game_over method, which freezes everthing.
        if self.rectangle.x - self.rectangle.radius < 0 or self.rectangle.x + self.rectangle.radius > 750:
            self.status.value = 'Game Over!'
            self.game_over()
        elif self.rectangle.y - self.rectangle.radius < 0 or self.rectangle.y + self.rectangle.radius > 550:
            self.status.value = 'Game Over!'
            self.game_over()
        elif self.hit() == True:
            self.status.value = 'Game Over!'
            self.game_over()
        
#----------------------------------------------------------------------------------------------------

    def leaderboard(self):
        """ Opening Leaderboard just for reading for the Leaderboard button command. """
        app = App(title="Leaderboard")
        lbr = open('leaderboard.txt', 'r')
        lbr = lbr.readline()
        Text(app, text="The Highest Score:")
        Text(app, text=lbr)
        
            
#----------------------------------------------------------------------------------------------------
            
    def game_over(self):
        """ This function freezes and open another window to enter your name if you have the highest score. """
        
        # Draw the text 'Game Over' when you are dead.
        self.drawing.text(250, 275, text='Game Over :(', color="red", font='arial', size=30, max_width=None)
        
        # Keyboard is ignored
        self.ignore_keyboard = True
        
        # Game is stopped
        self.stop_game = True
        
        # Open a window to enter your name and can check the person who has the highest score from the leaderboard text file.
        app = App(title="")
        your_name = Text(app, text="Enter Your Name:")
        box = Box(app, layout='grid')
        self.name = TextBox(box, width=20, grid=[0, 0])
        ok = PushButton(box, command=self.name_leaderboard, text="Ok", grid=[0, 1])
        your_name = Text(box, text="Your score is: {}".format(self.score), grid=[0, 2])
        number1 = Text(box, text="The Highest Score:", grid=[0, 4])
        
        lbr = open('leaderboard.txt', 'r')
        lbr = lbr.readline()
        lbrs = lbr.split(': ')
        if self.score >= int(lbrs[2]):
            Text(box, text='{}: {}'.format(self.name, self.score), grid=[0, 5])
        else:
            Text(box, text=lbr, grid=[0, 5])
       
        
        
        app.display()
        
#----------------------------------------------------------------------------------------------------        
        
    def name_leaderboard(self):
        """ Saving your score if your score is highest in the game. """
        lbr = open('leaderboard.txt', 'r')
        lbr = lbr.readline()
        lbrs = lbr.split(': ')
        if self.score >= int(lbrs[2]):
            lbw = open('leaderboard.txt', 'w')
            lbw.write('{}: '.format(self.name.value) + self.score_text.value)
            lbw.close()
        else:
            pass
        
            
#----------------------------------------------------------------------------------------------------
        
    def hit(self):
        """ Check if the snake head hit its body. """
        for i in range(len(self.r_list) - 1):
            if self.rectangle.x == self.r_list[i].x and self.rectangle.y == self.r_list[i].y:
                return True
        return False
        
#----------------------------------------------------------------------------------------------------  
            
    def reset(self):
        """ Change the values to initial values as it was before, for new game. """
        self.status.value = ''
        self.score = 0
        self.score_text.value = 'Score: 0'
        self.snake_len = 1
        self.rectangle = Rectangle()
        self.r_list= []
        app.when_key_pressed = self.process_key_event
        self.stop_game = False
        self.ignore_keyboard = False
        
#----------------------------------------------------------------------------------------------------               
        
    def in_range(self, px, py, rx, ry):
        """ In Bulean, Compute the distance between two points, between the snake head and the food. """
        if self.distance(px, py, rx, ry) <= 20:
            return True
        else:
            return False
        
#----------------------------------------------------------------------------------------------------         
        
    def distance(self, x1, y1, x2, y2):
        """ Compute the distance between two points. """
        # This method is from the Lab 12
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        
#----------------------------------------------------------------------------------------------------          
        
    def process_key_event(self, event):
        """ Implementing the arrow keys to the game. """
        
        # when the game is over, the keyboard is ignored.
        if self.ignore_keyboard == True:
            return
        
        # Get the key symbol. event.key doesn't work for all keys.
        key = event.tk_event.keysym
        
        # When right arrow key is pressed, snake moves to right and left arrow key is ignored while going right.
        if key == 'Right':
            if self.rectangle.vel_x == -5 and self.rectangle.vel_y == 0:
                pass
            else:  
                self.rectangle.vel_x = 5
                self.rectangle.vel_y = 0
                
        # When left arrow key is pressed, snake moves to left and right arrow key is ignored while going left.        
        elif key == 'Left':
            if self.rectangle.vel_x == 5 and self.rectangle.vel_y == 0:
                pass
            else:
                self.rectangle.vel_x = -5
                self.rectangle.vel_y = 0
        
        # When rup arrow key is pressed, snake moves to up and down arrow key is ignored while going up.
        elif key == 'Up':
            if self.rectangle.vel_x == 0 and self.rectangle.vel_y == 5:
                pass
            else:
                self.rectangle.vel_x = 0
                self.rectangle.vel_y = -5
                
        # # When down arrow key is pressed, snake moves to down and up arrow key is ignored while going down.        
        elif key == 'Down':
            if self.rectangle.vel_x == 0 and self.rectangle.vel_y == -5:
                pass
            else:
                self.rectangle.vel_x = 0
                self.rectangle.vel_y = 5

#----------------------------------------------------------------------------------------------------

app = App()
SnakeGame(app)
app.display()
