# -*- coding: utf-8 -*-

class Asteroid:

    def __init__(self, *args, **kwargs):
        self.quantity = 0
        self.volume = 0
        self.distance = 0
        self.ore_type = None
        self.group_coordinates = None
        self.coordinates = None
        for key, value in kwargs.items():
            if key == 'dis_units' and value == 'km':
                self.distance *= 1000
            elif key in 'quantity, volume, distance':
                setattr(self, key, float(value))
            else:
                setattr(self, key, value)
        
    def __str__(self):
        return str(self.ore_type) + ', ' + str(self.volume) + ' m3, ' + str(self.distance) + ' m.'





