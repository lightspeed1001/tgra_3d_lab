from math import *  # trigonometry

from Base3DObjects import *


class ModelMatrix:
    def __init__(self):
        self.matrix = [1, 0, 0, 0,
                       0, 1, 0, 0,
                       0, 0, 1, 0,
                       0, 0, 0, 1]
        self.stack = []
        self.stack_count = 0
        self.stack_capacity = 0

    def load_identity(self):
        self.matrix = [1, 0, 0, 0,
                       0, 1, 0, 0,
                       0, 0, 1, 0,
                       0, 0, 0, 1]

    def copy_matrix(self):
        new_matrix = [0] * 16
        for i in range(16):
            new_matrix[i] = self.matrix[i]
        return new_matrix

    def add_transformation(self, matrix2):
        counter = 0
        new_matrix = [0] * 16
        for row in range(4):
            for col in range(4):
                for i in range(4):
                    new_matrix[counter] += self.matrix[row * 4 + i] * matrix2[col + 4 * i]
                counter += 1
        self.matrix = new_matrix

    def add_movement(self, position: Point):
        other_matrix = [1, 0, 0, position.x,
                        0, 1, 0, position.y,
                        0, 0, 1, position.z,
                        0, 0, 0, 1]
        self.add_transformation(other_matrix)

    def add_scale(self, scalar):
        other_matrix = [scalar, 0, 0, 0,
                        0, scalar, 0, 0,
                        0, 0, scalar, 0,
                        0, 0, 0, 1]
        self.add_transformation(other_matrix)

    def add_x_scale(self, scalar):
        other_matrix = [scalar, 0, 0, 0,
                        0, 1, 0, 0,
                        0, 0, 1, 0,
                        0, 0, 0, 1]
        self.add_transformation(other_matrix)

    def add_y_scale(self, scalar):
        other_matrix = [1, 0, 0, 0,
                        0, scalar, 0, 0,
                        0, 0, 1, 0,
                        0, 0, 0, 1]
        self.add_transformation(other_matrix)

    def add_z_scale(self, scalar):
        other_matrix = [1, 0, 0, 0,
                        0, 1, 0, 0,
                        0, 0, scalar, 0,
                        0, 0, 0, 1]
        self.add_transformation(other_matrix)

    def add_x_rotation(self, angle):
        other_matrix = [1, 0, 0, 0,
                     0, cos(angle), -sin(angle), 0,
                     0, sin(angle), cos(angle), 0,
                     0, 0, 0, 1]
        self.add_transformation(other_matrix)

    def add_y_rotation(self, angle):
        other_matrix = [cos(angle), 0, sin(angle), 0,
                     0, 1, 0, 0,
                     -sin(angle), 0, cos(angle), 0,
                     0, 0, 0, 1]
        self.add_transformation(other_matrix)

    def add_z_rotation(self, angle):
        other_matrix = [cos(angle), -sin(angle), 0, 0,
                        sin(angle), cos(angle), 0, 0,
                        0, 0, 1, 0,
                        0, 0, 0, 1]
        self.add_transformation(other_matrix)

    def add_nothing(self):
        other_matrix = [1, 0, 0, 0,
                        0, 1, 0, 0,
                        0, 0, 1, 0,
                        0, 0, 0, 1]
        self.add_transformation(other_matrix)

    # YOU CAN TRY TO MAKE PUSH AND POP (AND COPY) LESS DEPENDANT ON GARBAGE COLLECTION
    # THAT CAN FIX SMOOTHNESS ISSUES ON SOME COMPUTERS
    def push_matrix(self):
        self.stack.append(self.copy_matrix())

    def pop_matrix(self):
        self.matrix = self.stack.pop()

    # This operation mainly for debugging
    def __str__(self):
        ret_str = ""
        counter = 0
        for _ in range(4):
            ret_str += "["
            for _ in range(4):
                ret_str += " " + str(self.matrix[counter]) + " "
                counter += 1
            ret_str += "]\n"
        return ret_str


# The ViewMatrix class holds the camera's coordinate frame and
# set's up a transformation concerning the camera's position
# and orientation

class ViewMatrix:
    def __init__(self):
        self.eye = Point(0, 0, 0)
        self.u = Vector(1, 0, 0)
        self.v = Vector(0, 1, 0)
        self.n = Vector(0, 0, 1)

    def look(self, eye, center, up):
        self.eye = eye
        self.n = (eye - center)
        self.n.normalize()
        self.u = up.cross(self.n)
        self.u.normalize()
        self.v = self.n.cross(self.u)

    def get_matrix(self):
        minusEye = Vector(-self.eye.x, -self.eye.y, -self.eye.z)
        return [self.u.x, self.u.y, self.u.z, minusEye.dot(self.u),
                self.v.x, self.v.y, self.v.z, minusEye.dot(self.v),
                self.n.x, self.n.y, self.n.z, minusEye.dot(self.n),
                0, 0, 0, 1]

    def slide(self, del_u, del_v, del_n):
        self.eye += self.u * del_u + self.v * del_v + self.n * del_n
        # self.eye.x += del_u * self.u.x + del_v * self.v.x + del_n * self.n.x
        # self.eye.y += del_u * self.u.y + del_v * self.v.y + del_n * self.n.y
        # self.eye.z += del_u * self.u.z + del_v * self.v.z + del_n * self.n.z

    def roll(self, angle):
        # Rotate around n
        ang_cos = cos(angle * pi / 180.0)
        ang_sin = sin(angle * pi / 180.0)
        t = Vector(self.u.x, self.u.y, self.u.z)
        # self.n = ang_cos * t + ang_sin * self.v
        # self.v = -ang_sin * t + ang_cos * self.v
        self.u = Vector(ang_cos * t.x + ang_sin * self.v.x,
                        ang_cos * t.y + ang_sin * self.v.y,
                        ang_cos * t.z + ang_sin * self.v.z)

        self.v = Vector(-ang_sin * t.x + ang_cos * self.v.x,
                        -ang_sin * t.y + ang_cos * self.v.y,
                        -ang_sin * t.z + ang_cos * self.v.z)
    
    def yaw(self, angle):
        # Rotate around v
        ang_cos = cos(angle * pi / 180.0)
        ang_sin = sin(angle * pi / 180.0)
        t = Vector(self.u.x, self.u.y, self.u.z)
        self.u = Vector(ang_cos * t.x + ang_sin * self.n.x,
                        ang_cos * t.y + ang_sin * self.n.y,
                        ang_cos * t.z + ang_sin * self.n.z)

        self.n = Vector(-ang_sin * t.x + ang_cos * self.n.x,
                        -ang_sin * t.y + ang_cos * self.n.y,
                        -ang_sin * t.z + ang_cos * self.n.z)

    def pitch(self, angle):
        # Rotate around u
        ang_cos = cos(angle * pi / 180.0)
        ang_sin = sin(angle * pi / 180.0)
        t = Vector(self.n.x, self.n.y, self.n.z)
        self.n = Vector(ang_cos * t.x + ang_sin * self.v.x,
                        ang_cos * t.y + ang_sin * self.v.y,
                        ang_cos * t.z + ang_sin * self.v.z)

        self.v = Vector(-ang_sin * t.x + ang_cos * self.v.x,
                        -ang_sin * t.y + ang_cos * self.v.y,
                        -ang_sin * t.z + ang_cos * self.v.z)

class FPSViewMatrix(ViewMatrix):
    def slide(self, del_u, del_v, del_n):
        # self.eye += self.u * del_u + self.v * del_v + self.n * del_n
        self.eye.x += del_u * self.u.x + del_v * self.v.x + del_n * self.n.x
        # self.eye.y += del_u * self.u.y + del_v * self.v.y + del_n * self.n.y
        self.eye.z += del_u * self.u.z + del_v * self.v.z + del_n * self.n.z
    
    def roll(self, angle):
        pass
        # You generally can't roll the camera in an fps
        # Maybe implement a sort of lean mechanic?

        # # Rotate around n
        # ang_cos = cos(angle * pi / 180.0)
        # ang_sin = sin(angle * pi / 180.0)
        # t = Vector(self.u.x, self.u.y, self.u.z)
        # # self.n = ang_cos * t + ang_sin * self.v
        # # self.v = -ang_sin * t + ang_cos * self.v
        # self.u = Vector(ang_cos * t.x + ang_sin * self.v.x,
        #                 ang_cos * t.y + ang_sin * self.v.y,
        #                 ang_cos * t.z + ang_sin * self.v.z)

        # self.v = Vector(-ang_sin * t.x + ang_cos * self.v.x,
        #                 -ang_sin * t.y + ang_cos * self.v.y,
        #                 -ang_sin * t.z + ang_cos * self.v.z)
    
    def yaw(self, angle):
        # Rotate around v
        ang_cos = cos(angle * pi / 180.0)
        ang_sin = sin(angle * pi / 180.0)
        self.u = Vector( ang_cos * self.u.x + ang_sin * self.u.z,
                         self.u.y,
                        -ang_sin * self.u.x + ang_cos * self.u.z)
        self.v = Vector( ang_cos * self.v.x + ang_sin * self.v.z,
                         self.v.y,
                        -ang_sin * self.v.x + ang_cos * self.v.z)
        self.n = Vector( ang_cos * self.n.x + ang_sin * self.n.z,
                         self.n.y,
                        -ang_sin * self.n.x + ang_cos * self.n.z)

    def pitch(self, angle):
        # Rotate around u
        ang_cos = cos(angle * pi / 180.0)
        ang_sin = sin(angle * pi / 180.0)
        t = Vector(self.n.x, self.n.y, self.n.z)
        self.n = Vector(ang_cos * t.x + ang_sin * self.v.x,
                        ang_cos * t.y + ang_sin * self.v.y,
                        ang_cos * t.z + ang_sin * self.v.z)

        self.v = Vector(-ang_sin * t.x + ang_cos * self.v.x,
                        -ang_sin * t.y + ang_cos * self.v.y,
                        -ang_sin * t.z + ang_cos * self.v.z)

# The ProjectionMatrix class builds transformations concerning
# the camera's "lens"
class ProjectionMatrix:
    def __init__(self, left=-1, right=1, bottom=-1, top=1, near=-1, far=1, ortho=True):
        self.left = left
        self.right = right
        self.bottom = bottom
        self.top = top
        self.near = near
        self.far = far

        self.is_orthographic = ortho

    def set_perspective(self, fov_y, aspect_ratio, near, far):
        self.near = near
        self.far = far
        self.top = near * tan(fov_y / 2)
        self.bottom = -self.top
        self.right = self.top * aspect_ratio
        self.left = -self.right
        self.is_orthographic = False

    def set_orthographic(self, left, right, bottom, top, near, far):
        self.left = left
        self.right = right
        self.bottom = bottom
        self.top = top
        self.near = near
        self.far = far
        self.is_orthographic = True

    def get_matrix(self):
        if self.is_orthographic:
            A = 2 / (self.right - self.left)
            B = -(self.right + self.left) / (self.right - self.left)
            C = 2 / (self.top - self.bottom)
            D = -(self.top + self.bottom) / (self.top - self.bottom)
            E = 2 / (self.near - self.far)
            F = (self.near + self.far) / (self.near - self.far)

            return [A, 0, 0, B,
                    0, C, 0, D,
                    0, 0, E, F,
                    0, 0, 0, 1]

        else:
            A = (2 * self.near) / (self.right - self.left)
            B = (self.right + self.left) / (self.right - self.left)
            C = (2 * self.near) / (self.top - self.bottom)
            D = (self.top + self.bottom) / (self.top - self.bottom)
            E = -(self.far + self.near) / (self.far - self.near)
            F = -(2 * self.far * self.near) / (self.far - self.near)
            
            return [A, 0, B, 0,
                    0, C, D, 0,
                    0, 0, E, F,
                    0, 0, -1, 0]

# IDEAS FOR OPERATIONS AND TESTING:
# if __name__ == "__main__":
#     matrix = ModelMatrix()
#     matrix.push_matrix()
#     print(matrix)
#     matrix.add_translation(3, 1, 2)
#     matrix.push_matrix()
#     print(matrix)
#     matrix.add_scale(2, 3, 4)
#     print(matrix)
#     matrix.pop_matrix()
#     print(matrix)

#     matrix.add_translation(5, 5, 5)
#     matrix.push_matrix()
#     print(matrix)
#     matrix.add_scale(3, 2, 3)
#     print(matrix)
#     matrix.pop_matrix()
#     print(matrix)

#     matrix.pop_matrix()
#     print(matrix)

#     matrix.push_matrix()
#     matrix.add_scale(2, 2, 2)
#     print(matrix)
#     matrix.push_matrix()
#     matrix.add_translation(3, 3, 3)
#     print(matrix)
#     matrix.push_matrix()
#     matrix.add_rotation_y(pi / 3)
#     print(matrix)
#     matrix.push_matrix()
#     matrix.add_translation(1, 1, 1)
#     print(matrix)
#     matrix.pop_matrix()
#     print(matrix)
#     matrix.pop_matrix()
#     print(matrix)
#     matrix.pop_matrix()
#     print(matrix)
#     matrix.pop_matrix()
#     print(matrix)
