from Matrices import Point, Vector
from math import sqrt
class GameObject:
    def __init__(self, position: Point, scale: Point = Point(1, 1, 1), rotation: Point = None, friction = 0.0):
        self.position = position
        self.scale = scale
        self.rotation = rotation
        self.friction = friction
        
        self.max_x = self.position.x + self.scale.x / 2
        self.max_y = self.position.y + self.scale.y / 2
        self.max_z = self.position.z + self.scale.z / 2

        self.min_x = self.position.x - self.scale.x / 2
        self.min_y = self.position.y - self.scale.y / 2
        self.min_z = self.position.z - self.scale.z / 2

    def intersects(self, other):
        # (a.minX <= b.maxX && a.maxX >= b.minX) &&
        # (a.minY <= b.maxY && a.maxY >= b.minY) &&
        # (a.minZ <= b.maxZ && a.maxZ >= b.minZ);
        return (self.min_x <= other.max_x and self.max_x >= other.min_x) and \
               (self.min_y <= other.max_y and self.max_y >= other.min_y) and \
               (self.min_z <= other.max_z and self.max_z >= other.min_z)

    def collision_check(self, other):
        pass

class Player(GameObject):
    """ Player is a sphere! """
    def __init__(self, position, scale = Point(1,1,1), rotation = None, friction = 0.0, acceleration = 1.0):
        super().__init__(position, scale, rotation, friction)
        self.direction = None
        self.acceleration = acceleration
        self.radius = self.scale.x / 2

    def collision_check(self, other):
        # Just check if player is inside the object and eject him
        
        # Update player bounding box first
        self.max_x = self.position.x + self.scale.x / 2
        self.max_y = self.position.y + self.scale.y / 2
        self.max_z = self.position.z + self.scale.z / 2

        self.min_x = self.position.x - self.scale.x / 2
        self.min_y = self.position.y - self.scale.y / 2
        self.min_z = self.position.z - self.scale.z / 2

        if self.intersects(other):
            # Bounding boxes do collide. Time to eject the player properly.

            if(self.max_z > other.min_z):
                # print("this one?")
                self.position.z = other.max_z + self.scale.z / 2
                return True

            # This guy never gets called :(
            if(self.min_z > other.max_z):
                print("other one?")
                self.position.z = other.min_z - self.scale.z / 2
                return True
            # if( self.position.z > other.position.z and
            #     self.position.x > other.min_z and
            #     self.position.x < other.max_x):
            #         self.position.z = other.max_z + self.scale.z / 2
            #         return True
    
    def sphere_intersects(self, other):
        # other scale: 5 5 5
        # self scale: 0.75 0.75 0.75
        x = max(other.position.x - other.scale.x / 2, min(self.position.x, (other.position.x + other.scale.x / 2)))
        y = max(other.position.y - other.scale.y / 2, min(self.position.y, (other.position.y + other.scale.y / 2)))
        z = max(other.position.z - other.scale.z / 2, min(self.position.z, (other.position.z + other.scale.z / 2)))

        distance_squared = (x - self.position.x) ** 2 + \
                           (y - self.position.y) ** 2 + \
                           (z - self.position.z) ** 2

        return distance_squared < (self.radius ** 2)

class Enemy(GameObject):
    """ Enemy is a sphere """
    def __init__(self, position, scale = Point(1,1,1), rotation = None, friction = 0.0, acceleration = 1.0):
        super().__init__(position, scale, rotation, friction)
        self.direction = None
        self.acceleration = acceleration

class Wall(GameObject):
    def __init__(self, position: Point, scale: Point = Point(1, 1, 1), rotation: Point = None, friction = 0.0):
        super().__init__(position, scale, rotation, friction)
        
    pass

class Trigger(GameObject):
    pass
