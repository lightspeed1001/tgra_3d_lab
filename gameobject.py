from Matrices import Point, Vector

class GameObject:
    def __init__(self, position: Point, scale: Point = Point(1, 1, 1), rotation: Point = None, friction = 0.0):
        self.position = position
        self.scale = scale
        self.rotation = rotation
        self.friction = friction

        # print(self.scale_x, self.scale_y, self.scale_z)

    def collision_check(self, other):
        pass

    def distance_squared(self, other):
        pass

class Player(GameObject):
    """ Player is a sphere! """
    def __init__(self, position, scale = Point(1,1,1), rotation = None, friction = 0.0, acceleration = 1.0):
        super().__init__(position, scale, rotation, friction)
        self.direction = None
        self.acceleration = acceleration

    def collision_check(self, other, delta_time):
        
        pass
        


class Wall(GameObject):
    pass
