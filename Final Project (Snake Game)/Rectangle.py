"""CS 108 Lab 12

This module is a model module for snake head and the body, creating rectangles.

@author: Serita Nelesen (smn4) - The Particle class from the particle module of Lab 12
@date: Fall, 2014
@author Seongrim Choi (sc83)
@date: Fall, 2021
"""
class Rectangle:
    def __init__(self, x=375, y=275, vel_x=0, vel_y=0, radius=10, color="white"):
        """Instantiate a particle object."""
        # Creating a rectangle based on the radius like a cirlce. 
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.radius = radius
        self.color = color
    
    def draw(self, drawing):
        """ Creating a rectangle object. """
        drawing.rectangle(self.x - self.radius,
             self.y - self.radius,
             self.x + self.radius,
             self.y + self.radius,
             color=self.color
             )
        
    def move(self, drawing):
        """ Moving rectangle object. """
        self.x += self.vel_x
        self.y += self.vel_y
        
        
        