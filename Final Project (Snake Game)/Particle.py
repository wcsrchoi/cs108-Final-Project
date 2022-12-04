"""

This module simulates the snake game - You can its head to it the food and grow.

@author Seongrim Choi (sc83)
@date: Fall, 2021
"""
from random import randint

class Particle:
    def __init__(self, x=0, y=0, radius=10, color="yellow"):
        """Instantiate a particle object."""
        # Randomizes the location of the food appearing.
        if x == 0:
            x = randint(20, 730)
        if y == 0:
            y = randint(20, 530)
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self, drawing):
        """ Creating a particle object. """
        drawing.oval(self.x - self.radius,
             self.y - self.radius,
             self.x + self.radius,
             self.y + self.radius,
             color=self.color
             )