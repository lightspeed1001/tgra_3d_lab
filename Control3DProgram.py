# from OpenGL.GL import *
# from OpenGL.GLU import *
from math import *

import pygame
from pygame.locals import *

import sys
import time

from Shaders import *
from Matrices import *
from maze import Maze
from gameobject import *

class GraphicsProgram3D:
    def __init__(self):

        pygame.init()
        pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)

        self.shader = Shader3D()
        self.shader.use()

        self.model_matrix = ModelMatrix()
        
        self.fov = pi / 2
        
        self.project_matrix = ProjectionMatrix()
        self.project_matrix.set_perspective(self.fov, 800.0/600.0, 0.5, 50)
        self.view_matrix = FPSViewMatrix()
        # Look dead ahead
        self.view_matrix.look(Point(5,1,5), Point(10,1,5), Vector(0,1,0))
        
        self.shader.set_projection_matrix(self.project_matrix.get_matrix())
        self.shader.set_view_matrix(self.view_matrix.get_matrix())
        
        self.cube = Cube()
        self.sphere = Sphere(24, 48)

        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.angle = 0

        self.gravity = 1

    def update(self):
        delta_time = self.clock.tick() / 1000.0

        self.angle += pi * delta_time
        self.handle_input(pygame.key.get_pressed(), delta_time)
        
        # Check for collisions
        for cube in self.chunks:
            if self.player.collision_check(cube, delta_time):
                print("boop")
        

        # if angle > 2 * pi:
        #     angle -= (2 * pi)

    def display(self):
        glEnable(GL_DEPTH_TEST)  ### --- NEED THIS FOR NORMAL 3D BUT MANY EFFECTS BETTER WITH glDisable(GL_DEPTH_TEST) ... try it! --- ###
        # glDisable(GL_DEPTH_TEST)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  ### --- YOU CAN ALSO CLEAR ONLY THE COLOR OR ONLY THE DEPTH --- ###

        glViewport(0, 0, 800, 600)
        
        self.shader.set_view_matrix(self.view_matrix.get_matrix())
        # self.project_matrix.set_perspective(self.fov, 800.0/600.0, 0.5, 10)
        # self.shader.set_projection_matrix(self.project_matrix.get_matrix())
        self.shader.set_eye_position(self.view_matrix.eye)

        # Light
        self.shader.set_light_position(self.view_matrix.eye)
        # self.shader.set_light_position(Point(cos(self.angle) * 10, 5, sin(self.angle) * 10))
        # self.shader.set_light_position(Point(0, 10, 0))
        # self.shader.set_light_diffuse(0.0, 0.0, 0.0)
        self.shader.set_light_diffuse(1.0, 1.0, 1.0)
        self.shader.set_light_specular(1.0, 1.0, 1.0)
        # self.shader.set_light_specular(0.0, 0.0, 0.0)
        
        self.shader.set_material_specular(1.0, 1.0, 1.0)
        self.shader.set_material_shiny(10)
        self.model_matrix.load_identity()
        
        # Cube drawing mode
        self.cube.set_vertices(self.shader)
        self.shader.set_material_diffuse(1.0, 0.0, 0.0)
        # Draw the maze
        for cube in self.chunks:
            self.model_matrix.push_matrix()
            
            self.model_matrix.add_movement(position = cube.position)
            self.model_matrix.add_scale(cube.scale.x) # The walls are perfect cubes
            self.shader.set_model_matrix(self.model_matrix.matrix)
            self.cube.draw(self.shader)
            
            self.model_matrix.pop_matrix()

        # Draw the floor
        self.model_matrix.push_matrix()
        self.shader.set_material_diffuse(0.0, 1.0, 0.0)
        # floor_x, floor_y, floor_z = self.floor[0]
        # floor_x_scale, floor_y_scale, floor_z_scale = self.floor[1]
        self.model_matrix.add_movement(position=self.floor.position)
        self.model_matrix.add_x_scale(self.floor.scale.x)
        self.model_matrix.add_y_scale(self.floor.scale.y)
        self.model_matrix.add_z_scale(self.floor.scale.z)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw(self.shader)
        self.model_matrix.pop_matrix()

        # Cube 1
        # self.model_matrix.push_matrix()
        # self.model_matrix.add_scale(1.5)
        # self.model_matrix.add_y_rotation(self.angle / 2)
        # self.shader.set_model_matrix(self.model_matrix.matrix)
        # self.shader.set_material_diffuse(1.0, 0.0, 0.0)
        # self.cube.draw(self.shader)
        # self.model_matrix.pop_matrix()

        # # Cube 2
        # self.model_matrix.push_matrix()
        # new_x = cos(self.angle) * 2
        # new_y = sin(self.angle) * 2
        # new_z = sin(self.angle) * 2

        # self.model_matrix.add_movement(new_x, new_y)
        # self.model_matrix.add_scale(0.5)
        # self.model_matrix.add_x_rotation(self.angle)
        # self.model_matrix.add_y_rotation(self.angle)
        # # self.model_matrix.add_z_rotation(self.angle)

        # self.shader.set_model_matrix(self.model_matrix.matrix)
        # self.shader.set_material_diffuse(0.0, 1.0, 0.0)

        # self.cube.draw(self.shader)
        # self.model_matrix.pop_matrix()

        # # Cube 3
        # self.model_matrix.push_matrix()
        # self.model_matrix.add_movement(9, 5, -2)
        # self.model_matrix.add_x_scale(2)
        # self.model_matrix.add_y_scale(2)
        # self.model_matrix.add_z_scale(2)
        # self.shader.set_model_matrix(self.model_matrix.matrix)
        # self.shader.set_material_diffuse(0.0, 0.0, 1.0)
        # self.cube.draw(self.shader)
        # self.model_matrix.pop_matrix()

        # # Cube 4
        # self.model_matrix.push_matrix()
        # self.model_matrix.add_movement(y=-2)
        # self.model_matrix.add_z_scale(10.0)
        # self.model_matrix.add_y_scale(0.1)
        # self.model_matrix.add_x_scale(10.0)
        # self.shader.set_model_matrix(self.model_matrix.matrix)
        # self.shader.set_material_diffuse(1.0, 1.0, 0.0)
        # self.cube.draw(self.shader)
        # self.model_matrix.pop_matrix()
        
        # # Sphere drawing mode
        # self.sphere.set_verties(self.shader)

        # # Sphere
        # self.model_matrix.push_matrix()
        # ball_x = self.view_matrix.eye.x# + self.view_matrix.n.x + 1
        # ball_y = self.view_matrix.eye.y# - 1.5
        # ball_z = self.view_matrix.eye.z# + self.view_matrix.n.z + 1 
        # self.model_matrix.add_movement(ball_x, ball_y, ball_z)
        # self.model_matrix.add_scale(0.5)
        # self.shader.set_material_diffuse(0.0, 0.66, 0.66)
        # self.shader.set_model_matrix(self.model_matrix.matrix)
        # self.sphere.draw(self.shader)
        # self.model_matrix.pop_matrix()

        pygame.display.flip()

    def handle_input(self, keys, delta_time):
        WASD_SPEED = 12.0 * delta_time
        OTHER_SPEED = 100.0 * delta_time
        FOV_DELTA = 0.25 * delta_time
        
        if keys[K_d]:
            self.view_matrix.slide(WASD_SPEED, 0, 0)
        if keys[K_a]:
            self.view_matrix.slide(-WASD_SPEED, 0, 0)

        if keys[K_s]:
            self.view_matrix.slide(0, 0, WASD_SPEED)
        if keys[K_w]:
            self.view_matrix.slide(0, 0, -WASD_SPEED)

        if keys[K_LEFT]:
            self.view_matrix.yaw(OTHER_SPEED)
        if keys[K_RIGHT]:
            self.view_matrix.yaw(-OTHER_SPEED)

        # if keys[K_e]:
        #     self.view_matrix.roll(-OTHER_SPEED)
        # if keys[K_q]:
        #     self.view_matrix.roll(OTHER_SPEED)

        if keys[K_DOWN]:
            self.view_matrix.pitch(OTHER_SPEED)
        if keys[K_UP]:
            self.view_matrix.pitch(-OTHER_SPEED)

        # if keys[K_r]:
        #     self.view_matrix.slide(0, WASD_SPEED, 0)
        # if keys[K_f]:
        #     self.view_matrix.slide(0, -WASD_SPEED, 0)

        if keys[K_g]:
            self.fov += FOV_DELTA
        if keys[K_t]:
            self.fov -= FOV_DELTA
    
    def program_loop(self):
        exiting = False
        while not exiting:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quitting!")
                    exiting = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        print("Escaping!")
                        exiting = True
            self.update()
            self.display()

        # OUT OF GAME LOOP
        pygame.quit()

    def start(self):
        print("Generating maze...")
        w = 27
        h = 35
        self.maze = Maze(w=w, h=h)
        self.maze.generate_maze()
        
        wall_scale = 5
        self.chunks = []
        floor_size_x = wall_scale * h
        floor_size_z = wall_scale * w
        floor_size_y = 0.5

        floor_pos = Point(floor_size_x / 2 - wall_scale / 2, 
                          -wall_scale/2, 
                          floor_size_z / 2 - wall_scale / 2)
        floor_scale = Point(floor_size_x, floor_size_y, floor_size_z)

        self.floor = Wall(floor_pos, floor_scale)
        # self.floor = ((floor_size_x / 2 - self.wall_scale / 2,-self.wall_scale/2, floor_size_z / 2 - self.wall_scale / 2), (floor_size_x, floor_size_y, floor_size_z))

        for row_num, row in enumerate(self.maze.maze):
            for col_num, col in enumerate(row):
                if col:
                    x = row_num * wall_scale
                    y = 0
                    z = col_num * wall_scale
                    self.chunks.append(Wall(Point(x, y, z), Point(wall_scale, wall_scale, wall_scale)))

        print("Maze generated!")

        player_radius = 1
        self.player = Player(self.view_matrix.eye, Point(player_radius, player_radius, player_radius))

        self.program_loop()


if __name__ == "__main__":
    GraphicsProgram3D().start()
