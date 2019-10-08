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
from constants import *

class GraphicsProgram3D:
    def __init__(self):
        """ Things that don't change between restarts """
        # Pygame
        pygame.init()
        pygame.display.gl_set_attribute(GL_MULTISAMPLEBUFFERS, 1)
        pygame.display.gl_set_attribute(GL_MULTISAMPLESAMPLES, 2)
        pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)

        # Shader
        self.shader = Shader3D()
        self.shader.use()

        # Objects
        self.model_matrix = ModelMatrix()
        self.cube = Cube()
        self.sphere = Sphere(24, 48)

        # Game settings
        self.fov = DEFAULT_FOV
        self.gravity = DEFAULT_GRAVITY
        self.clock = pygame.time.Clock()
        self.clock.tick()

    def update(self):
        delta_time = self.clock.tick() / 1000.0

        self.handle_input(pygame.key.get_pressed(), delta_time)
        self.view_matrix.eye.y -= DEFAULT_GRAVITY * delta_time

        if self.player.collision_check(self.floor):
            pass
            #print("boop")
        # Check for collisions
        for cube in self.chunks:
            if self.player.collision_check(cube):
                pass
                # print("boop")


    def display(self):
        # Draw boilerplate
        glEnable(GL_DEPTH_TEST)  ### --- NEED THIS FOR NORMAL 3D BUT MANY EFFECTS BETTER WITH glDisable(GL_DEPTH_TEST) ... try it! --- ###
        glEnable(GL_FRAMEBUFFER_SRGB)
        glEnable(GL_MULTISAMPLE)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  ### --- YOU CAN ALSO CLEAR ONLY THE COLOR OR ONLY THE DEPTH --- ###
        glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # Refresh the view matrix (movement)
        self.shader.set_view_matrix(self.view_matrix.get_matrix())
        self.shader.set_eye_position(self.player.position)
        # Refresh the projection matrix (FOV changes)
        # self.project_matrix.set_perspective(self.fov, 800.0/600.0, 0.5, 10)
        # self.shader.set_projection_matrix(self.project_matrix.get_matrix())
        

        # Lights
        # Attached to player
        self.shader.set_light_position(self.view_matrix.eye)
        # self.shader.set_light_diffuse(0.0, 0.0, 0.0)
        self.shader.set_light_diffuse(CAMERA_LIGHT_DIFFUSE)
        self.shader.set_light_specular(CAMERA_LIGHT_SPECULAR)
        self.shader.set_light_ambience(CAMERA_LIGHT_AMBIENT)
        # self.shader.set_light_specular(0.0, 0.0, 0.0)
        
        # Some other light
        # TODO

        # Flashlight
        # TODO

        # Zero out model matrix, just in case
        self.model_matrix.load_identity()
        
        # Cube drawing mode
        self.cube.set_vertices(self.shader)
        
        # Draw the maze
        self.shader.set_material_diffuse(COLOR_WALL)
        self.shader.set_material_specular(SPECULAR_WALL)
        self.shader.set_material_shiny(SHINY_WALL)

        for cube in self.chunks:
            self.model_matrix.push_matrix()
            
            self.model_matrix.add_movement(position = cube.position)
            self.model_matrix.add_scale(cube.scale.x) # The walls are perfect cubes
            self.shader.set_model_matrix(self.model_matrix.matrix)
            self.cube.draw(self.shader)
            
            self.model_matrix.pop_matrix()

        # Draw the floor
        self.model_matrix.push_matrix()
        self.shader.set_material_diffuse(COLOR_FLOOR)
        self.shader.set_material_shiny(SHINY_FLOOR)
        self.shader.set_material_specular(SPECULAR_FLOOR)
        self.model_matrix.add_movement(position=self.floor.position)
        self.model_matrix.add_x_scale(self.floor.scale.x)
        self.model_matrix.add_y_scale(self.floor.scale.y)
        self.model_matrix.add_z_scale(self.floor.scale.z)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw(self.shader)
        self.model_matrix.pop_matrix()
        
        # Sphere drawing mode
        # self.sphere.set_verties(self.shader)

        # Sphere
        # self.model_matrix.push_matrix()
        # ball_x = self.view_matrix.eye.x # + self.view_matrix.n.x + 1
        # ball_y = self.view_matrix.eye.y - 4
        # ball_z = self.view_matrix.eye.z # + self.view_matrix.n.z + 1 
        # self.model_matrix.add_movement(Point(ball_x, ball_y, ball_z))
        # # self.model_matrix.add_movement(Point(5,1,5))
        # self.model_matrix.add_scale(PLAYER_RADIUS)
        # self.shader.set_material_diffuse(COLOR_ENEMY)
        # self.shader.set_model_matrix(self.model_matrix.matrix)
        # self.sphere.draw(self.shader)
        # self.model_matrix.pop_matrix()

        pygame.display.flip()

    def handle_input(self, keys, delta_time):
        WASD_SPEED = PLAYER_MOVE_SPEED * delta_time
        OTHER_SPEED = PLAYER_TURN_SPEED * delta_time
        FOV_DELTA = PLAYER_FOV_SPEED * delta_time
        
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
        """ Things that could change between games """
        # Camera
        self.project_matrix = ProjectionMatrix()
        self.project_matrix.set_perspective(self.fov, WINDOW_WIDTH/WINDOW_HEIGHT, DEFAULT_NEAR, DEFAULT_FAR)
        self.view_matrix = FPSViewMatrix()
        self.view_matrix.look(PLAYER_STARTING_POS, PLAYER_STARTING_LOOK, VECTOR_UP)
        self.shader.set_projection_matrix(self.project_matrix.get_matrix())
        self.shader.set_view_matrix(self.view_matrix.get_matrix())

        print("Generating maze...")
        w = MAZE_WIDTH
        h = MAZE_HEIGHT
        
        # Floor setup
        wall_scale = MAZE_WALL_SIZE
        floor_size_x = wall_scale * h
        floor_size_z = wall_scale * w
        floor_size_y = MAZE_FLOOR_THICK

        floor_pos = Point(floor_size_x / 2 - wall_scale / 2, 
                          -wall_scale / 2 - floor_size_y / 2, 
                          floor_size_z / 2 - wall_scale / 2)
        floor_scale = Point(floor_size_x, floor_size_y, floor_size_z)
        self.floor = Wall(floor_pos, floor_scale)
        
        # Maze setup
        self.maze = Maze(w=w, h=h, complexity=MAZE_COMPLEXITY, density=MAZE_DENSITY)
        self.maze.generate_maze()
        self.chunks = []
        for row_num, row in enumerate(self.maze.maze):
            for col_num, col in enumerate(row):
                if col:
                    x = row_num * wall_scale
                    y = 0
                    z = col_num * wall_scale
                    self.chunks.append(Wall(Point(x, y, z), Point(wall_scale, wall_scale, wall_scale)))

        print("Maze generated!")

        # Player setup
        self.player = Player(self.view_matrix.eye, Point(PLAYER_RADIUS, PLAYER_RADIUS, PLAYER_RADIUS))

        glClearColor(COLOR_BG[0], COLOR_BG[1], COLOR_BG[2], COLOR_BG[3])
        self.program_loop()


if __name__ == "__main__":
    GraphicsProgram3D().start()
