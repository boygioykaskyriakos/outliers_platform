"""Implement a class Airplane that keeps track of the following features of an airplane:

• consumption: an integer representing number of litres consumed per km of dis- tance
• position: a tuple (pair) of integers representing a position of the plane on a map (assume that the airplane can only
be in one of the positions of the 1 km x 1 km grid)
• fuel_level: a float number representing the current fuel level in litres.

Implement the following methods:
• constructor __init__: takes four integer parameters (in the specified sequence) initX, initY, cons and init_fuel,
 where (initX, initY) represents initial location of the plane, cons represents the consumption (litre/km) and init_fuel
 represents the initial fuel level
• goto: takes two integer parameters X and Y representing the location where the plane needs to go to. If the airplane
has enough fuel to travel there from its current location, the method moves it there, updates remaining fuel level, and
 returns True. Otherwise, the plain does not move and False is returned.
• refuel: takes one integer parameter indicating how many litres of fuel are added. No value returned.

Assume that the airplane travels in a direct line between two positions (X1,Y1) and (X2, Y 2). The distance between two
locations is computed as 􏰓(X2 − X1)2 + (Y 2 − Y 1)2

Indicative test cases:
   ap789 = Airplane(0, 0, 10, 3000)
   assert ap789.goto(95,70) == True
   assert ap789.position[0] == 95 and ap789.position[1]==70
   assert abs(ap789.fuel_level - 1819.96) < 0.01
   assert ap789.goto(300,300) == False
   assert abs(ap789.fuel_level - 1819.96) < 0.01"""

import math


class Airplane:
    def __init__(self, initX, initY, cons, init_fuel):
        # cartesian
        self.initX = initX
        self.initY = initY
        self.position = (initX, initY)
        # fuel consumptions
        self.cons = cons
        self.total_cons = 0
        self.init_fuel = init_fuel
        self.fuel_level = init_fuel

    def goto(self, X, Y):
        # calculate distance between old and new position
        dist = math.sqrt(((self.initX - X) ** 2) + ((Y - self.initY) ** 2))
        # if applicable
        if self.cons * dist < self.init_fuel:
            # update new position
            self.initX = X
            self.initY = Y
            self.position = (X, Y)
            # calculate fuel level
            self.fuel_level -= self.cons * dist

            return True
        else:
            return False

    def refuel(self, fill):
        self.fuel_level += fill


if __name__ == "__main__":
    ap789 = Airplane(0, 0, 10, 3000)
    assert ap789.goto(95, 70) is True
    assert ap789.position[0] == 95 and ap789.position[1] == 70
    assert abs(ap789.fuel_level - 1819.96) < 0.01
    assert ap789.goto(300, 300) is False
    assert abs(ap789.fuel_level - 1819.96) < 0.01


