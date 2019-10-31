""" Some basic game objects """
from Base3DObjects import Point
class GameObject:
    """ The parental game object. Handles a few things,
    but expects children to overload most functions """
    def __init__(self, position: Point, scale: Point = Point(1, 1, 1),
                 rotation: Point = None, friction=0.0):
        self.position = position
        self.scale = scale
        self.rotation = rotation
        self.friction = friction

        self.update_bounding_box()

    def intersects(self, other):
        """ Very basic bounding box check """
        return (self.min_x <= other.max_x and self.max_x >= other.min_x) and \
               (self.min_y <= other.max_y and self.max_y >= other.min_y) and \
               (self.min_z <= other.max_z and self.max_z >= other.min_z)

    def update_bounding_box(self):
        """ Updates the bounding box. Mainly used by the player """
        self.max_x = self.position.x + self.scale.x / 2
        self.max_y = self.position.y + self.scale.y / 2
        self.max_z = self.position.z + self.scale.z / 2

        self.min_x = self.position.x - self.scale.x / 2
        self.min_y = self.position.y - self.scale.y / 2
        self.min_z = self.position.z - self.scale.z / 2

    def collision_check(self, other):
        """ Overload me if you want more precise results """
        return self.intersects(other)

class Player(GameObject):
    """ Player is a sphere! """
    def __init__(self, position, scale=Point(1, 1, 1),
                 rotation=None, friction=0.0, acceleration=1.0):
        super().__init__(position, scale, rotation, friction)
        self.direction = None
        self.acceleration = acceleration
        self.radius = self.scale.x / 2

    def collision_check(self, other):
        """ Slightly more elaborate collision check than the base class. """
        # Update player bounding box first
        self.update_bounding_box()

        if self.intersects(other):
            # Bounding boxes do collide. Time to eject the player properly.
            w = other.position.x - self.position.x
            h = other.position.z - self.position.z

            if w >= abs(h):
                self.position.x = other.min_x - self.scale.x / 2
                # return True
            elif -w >= abs(h):
                self.position.x = other.max_x + self.scale.x / 2
                # return True
            elif h >= abs(w):
                self.position.z = other.min_z - self.scale.z / 2
                # return True
            elif -h >= abs(w):
                self.position.z = other.max_z + self.scale.z / 2
            return True
        return False

    def sphere_intersects(self, other):
        """ Self is a sphere. Check for intersection using radius """
        x = max(other.position.x - other.scale.x / 2,
                min(self.position.x, (other.position.x + other.scale.x / 2)))
        y = max(other.position.y - other.scale.y / 2,
                min(self.position.y, (other.position.y + other.scale.y / 2)))
        z = max(other.position.z - other.scale.z / 2,
                min(self.position.z, (other.position.z + other.scale.z / 2)))

        distance_squared = (x - self.position.x) ** 2 + \
                           (y - self.position.y) ** 2 + \
                           (z - self.position.z) ** 2

        return distance_squared < (self.radius ** 2)

# Not used because time
class Enemy(GameObject):
    """ Enemy is a sphere """
    def __init__(self, position, scale=Point(1, 1, 1),
                 rotation=None, friction=0.0, acceleration=1.0,
                 hp=1.0):
        super().__init__(position, scale, rotation, friction)
        self.direction = None
        self.acceleration = acceleration
        self.hit_points = hp

class Wall(GameObject):
    """ A very basic wall object. """

class Trigger(GameObject):
    """ An invisible trigger object """
    def collision_check(self, other):
        return self.intersects(other)
