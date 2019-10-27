"""
Lab excercises and more for Computer Graphics
at Rekjavik University, winter 2019

Author: Mikael Sigmundsson
Teacher: Kári Halldórsson
"""
# from OpenGL.GL import *
# from OpenGL.GLU import *
# from math import *

import pygame
from pygame.locals import *

from Shaders import *
from Matrices import *
from maze import Maze
from gameobject import *
from constants import *

class GraphicsProgram3D:
    """ The main game """
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
        self.cube = OptiCube()
        self.sphere = OptiSphere(24, 48)

        # Game settings
        self.fov = DEFAULT_FOV
        self.gravity = DEFAULT_GRAVITY
        self.clock = pygame.time.Clock()
        self.clock.tick()
        self.fps_print = 0.0

        # Texture
        # glActiveTexture(GL_TEXTURE0)
        self.shader.set_diffuse_texture(0)
        self.tex_id_01_diffuse = self.load_texture("container2.png")
        # self.tex_id_01_diffuse = self.load_texture("Brick_Wall_011_COLOR.jpg")
        self.shader.set_specular_texture(1)
        # glActiveTexture(GL_TEXTURE1)
        # self.tex_id_01_specular = self.load_texture("Brick_Wall_011_OCC.jpg")
        self.tex_id_01_specular = self.load_texture("container2_specular.png")
        # self.tex_id2 = self.load_texture("container2.png")
        print("Texture id diffuse: {}\nTexture id specular: {}"
              .format(self.tex_id_01_diffuse, self.tex_id_01_specular))

        # Things to make pylint happy
        self.project_matrix = None
        self.view_matrix = None
        self.floor = None
        self.ceiling = None
        self.maze = None
        self.chunks = None
        self.goal = None
        self.player = None

    def load_texture(self, image):
        """ Loads a texture into the buffer """
        texture_surface = pygame.image.load(image)
        texture_data = pygame.image.tostring(texture_surface, "RGBA", 1)
        width = texture_surface.get_width()
        height = texture_surface.get_height()

        # glEnable(GL_TEXTURE_2D)
        texid = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, texid)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height,
                     0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)

        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        return texid

    def update(self):
        """ Performs any per-frame updates """
        delta_time = self.clock.tick() / 1000.0
        self.fps_print += delta_time

        self.handle_input(pygame.key.get_pressed(), delta_time)
        # self.view_matrix.eye.y -= DEFAULT_GRAVITY * delta_time

        # if self.player.collision_check(self.floor):
        #     pass

        self.player.update_bounding_box()
        # Check for collisions
        for cube in self.chunks:
            if self.player.collision_check(cube):
                pass

        #if self.goal.collision_check(self.player):
        if self.player.collision_check(self.goal):
            print("You solved the maze!\nGenerating new maze!")
            self.new_game()
        if self.fps_print >= 1:
            print(self.clock.get_fps())
            # print(self.player.collision_poly)
            self.fps_print = 0.0

    def display(self):
        """ Draws the game world """
        # Draw boilerplate
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_FRAMEBUFFER_SRGB)
        glCullFace(GL_FRONT)
        # Enable AA
        glEnable(GL_MULTISAMPLE)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        # Refresh the view matrix (movement)
        self.shader.set_view_matrix(self.view_matrix.get_matrix())
        self.shader.set_eye_position(self.player.position)
        # Refresh the projection matrix (FOV changes)
        # self.project_matrix.set_perspective(self.fov, 800.0/600.0, 0.5, 10)
        # self.shader.set_projection_matrix(self.project_matrix.get_matrix())

        # Lights
        # Player lantern
        self.shader.set_light_position(self.view_matrix.eye)

        # Flashlight
        flashy_position = Point(self.view_matrix.eye.x,
                                self.view_matrix.eye.y * 0.7,
                                self.view_matrix.eye.z)
        self.shader.set_flashlight_position(flashy_position)
        self.shader.set_flashlight_direction(self.view_matrix.n)

        # Zero out model matrix, just in case
        self.model_matrix.load_identity()

        # Cube drawing mode
        self.cube.set_vertices(self.shader)

        # Draw the maze
        glEnable(GL_TEXTURE_2D)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_01_diffuse)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_01_specular)

        forward = Vector(self.view_matrix.n.x, self.view_matrix.n.y, self.view_matrix.n.z)
        # forward.normalize()
        self.shader.set_use_texture(1.0)
        self.shader.set_material_diffuse(COLOR_WALL)
        self.shader.set_material_specular(SPECULAR_WALL)
        self.shader.set_material_shiny(SHINY_WALL)
        self.shader.set_material_emit(EMIT_WALL)
        for cube in self.chunks:
            obj_dir = self.view_matrix.eye - cube.position
            # obj_dir.normalize()
            theta = obj_dir.dot(forward)
            dist_squared = obj_dir.length_squared()
            if theta - DRAW_ANGLE_CUTOFF <= 0 and \
                dist_squared > DRAW_ANGLE_MIN_DISTANCE \
                or dist_squared > DRAW_DISTANCE_CUTOFF_SQUARED:
                continue

            self.model_matrix.push_matrix()

            self.model_matrix.add_movement(position=cube.position)
            self.model_matrix.add_scale(cube.scale.x) # The walls are perfect cubes
            self.shader.set_model_matrix(self.model_matrix.matrix)
            self.cube.draw(self.shader)

            self.model_matrix.pop_matrix()
        self.shader.set_use_texture(0.0)
        glDisable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, -1)

        # Draw the floor
        # glEnable(GL_TEXTURE_2D)
        # glBindTexture(GL_TEXTURE_2D, self.tex_id2)
        # self.shader.set_use_texture(1.0)

        self.model_matrix.push_matrix()
        self.shader.set_material_diffuse(COLOR_FLOOR)
        self.shader.set_material_shiny(SHINY_FLOOR)
        self.shader.set_material_specular(SPECULAR_FLOOR)
        self.shader.set_material_emit(EMIT_WALL)
        self.model_matrix.add_movement(position=self.floor.position)
        self.model_matrix.add_x_scale(self.floor.scale.x)
        self.model_matrix.add_y_scale(self.floor.scale.y)
        self.model_matrix.add_z_scale(self.floor.scale.z)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw(self.shader)
        self.model_matrix.pop_matrix()

        # self.shader.set_use_texture(0.0)
        # glDisable(GL_TEXTURE_2D)
        # glBindTexture(GL_TEXTURE_2D, -1)

        # Draw the ceiling
        self.model_matrix.push_matrix()
        self.shader.set_material_diffuse(COLOR_CEILING)
        self.shader.set_material_shiny(SHINY_CEILING)
        self.shader.set_material_specular(SPECULAR_CEILING)
        self.shader.set_material_emit(EMIT_CEILING)
        self.model_matrix.add_movement(position=self.ceiling.position)
        self.model_matrix.add_x_scale(self.ceiling.scale.x)
        self.model_matrix.add_y_scale(self.ceiling.scale.y)
        self.model_matrix.add_z_scale(self.ceiling.scale.z)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw(self.shader)
        self.model_matrix.pop_matrix()

        # Draw the goal
        # Set the drawing mode to spheres first.
        # Alpha test for fun. Doesn't appear to work with spheres?
        # glEnable(GL_BLEND)
        # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.model_matrix.push_matrix()

        self.shader.set_material_diffuse(COLOR_GOAL)
        self.shader.set_material_specular(SPECULAR_GOAL)
        self.shader.set_material_shiny(SHINY_GOAL)
        self.shader.set_material_emit(EMIT_GOAL)

        self.model_matrix.add_movement(position=self.goal.position)
        self.model_matrix.add_scale(self.goal.scale.x)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.sphere.draw(self.shader)
        self.model_matrix.pop_matrix()
        # glDisable(GL_BLEND)

        pygame.display.flip()

    def handle_input(self, keys, delta_time):
        """ Handles any input from the keyboard """
        wasd_speed = PLAYER_MOVE_SPEED * delta_time
        other_speed = PLAYER_TURN_SPEED * delta_time
        # fov_delta = PLAYER_FOV_SPEED * delta_time

        if keys[K_d]:
            self.view_matrix.slide(wasd_speed, 0, 0)
        if keys[K_a]:
            self.view_matrix.slide(-wasd_speed, 0, 0)

        if keys[K_s]:
            self.view_matrix.slide(0, 0, wasd_speed)
        if keys[K_w]:
            self.view_matrix.slide(0, 0, -wasd_speed)

        if keys[K_LEFT]:
            self.view_matrix.yaw(other_speed)
        if keys[K_RIGHT]:
            self.view_matrix.yaw(-other_speed)

        # if keys[K_e]:
        #     self.view_matrix.roll(-other_speed)
        # if keys[K_q]:
        #     self.view_matrix.roll(other_speed)

        if keys[K_DOWN]:
            self.view_matrix.pitch(other_speed)
        if keys[K_UP]:
            self.view_matrix.pitch(-other_speed)

        # if keys[K_r]:
        #     self.view_matrix.slide(0, wasd_speed, 0)
        # if keys[K_f]:
        #     self.view_matrix.slide(0, -wasd_speed, 0)

        # if keys[K_g]:
        #     self.fov += fov_delta
        # if keys[K_t]:
        #     self.fov -= fov_delta

    def program_loop(self):
        """ Runs the game forever-ish """
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

    def setup_camera(self):
        """ Does any setup required for the camera """
        self.project_matrix = ProjectionMatrix()
        self.project_matrix.set_perspective(self.fov, WINDOW_WIDTH/WINDOW_HEIGHT,
                                            DEFAULT_NEAR, DEFAULT_FAR)
        self.view_matrix = FPSViewMatrix()
        eye_start = Point(PLAYER_STARTING_POS.x, PLAYER_STARTING_POS.y, PLAYER_STARTING_POS.z)
        eye_look = Point(PLAYER_STARTING_LOOK.x, PLAYER_STARTING_LOOK.y, PLAYER_STARTING_LOOK.z)
        self.view_matrix.look(eye_start, eye_look, VECTOR_UP)
        self.shader.set_projection_matrix(self.project_matrix.get_matrix())
        self.shader.set_view_matrix(self.view_matrix.get_matrix())


    def setup_lights(self):
        """ Sets up the lights """
        # Global directional light
        self.shader.set_global_light_direction(GLOBAL_LIGHT_DIRECTION)
        self.shader.set_global_light_color(GLOBAL_LIGHT_COLOR)
        # Player lantern
        self.shader.set_light_diffuse(PLAYER_LIGHT_COLOR)
        self.shader.set_light_attenuation_constant(PLAYER_LIGHT_ATT_CONSTANT)
        self.shader.set_light_attenuation_linear(PLAYER_LIGHT_ATT_LINEAR)
        self.shader.set_light_attenuation_quad(PLAYER_LIGHT_ATT_QUAD)
        # Flashlight
        self.shader.set_flashlight_color(PLAYER_FLASHLIGHT_COLOR)
        self.shader.set_flashlight_cutoff(PLAYER_FLASHLIGHT_CUTOFF)
        self.shader.set_flashlight_outer_cutoff(PLAYER_FLASHLIGHT_OUTER_CUTOFF)
        self.shader.set_flashlight_attenuation_constant(PLAYER_FLASHLIGHT_ATT_CONSTANT)
        self.shader.set_flashlight_attenuation_linear(PLAYER_FLASHLIGHT_ATT_LINEAR)
        self.shader.set_flashlight_attenuation_quad(PLAYER_FLASHLIGHT_ATT_QUAD)
        # Fog (technically an anti-light)
        self.shader.set_fog_distance(FOG_DISTANCE)
        self.shader.set_fog_color(FOG_COLOR)

    def setup_maze(self):
        """ Sets up the maze """
        w = MAZE_WIDTH
        h = MAZE_HEIGHT
        assert w & 1, "Width isn't odd!"
        assert h & 1, "Height isn't odd!"
        assert w >= 5 or h >= 5, "Maze too small!"
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

        # Ceiling setup
        ceiling_pos = floor_pos + Point(0, wall_scale + floor_size_y, 0)
        self.ceiling = Wall(ceiling_pos, floor_scale)

        # Maze setup
        self.maze = Maze(w=w, h=h, complexity=MAZE_COMPLEXITY, density=MAZE_DENSITY)
        self.maze.generate_maze()
        self.chunks = []
        wall_scale_p = Point(wall_scale*1.00, wall_scale*1.00, wall_scale*1.00)
        for row_num, row in enumerate(self.maze.maze):
            for col_num, col in enumerate(row):
                if col:
                    x = row_num * wall_scale
                    y = 0
                    z = col_num * wall_scale
                    self.chunks.append(Wall(Point(x, y, z), wall_scale_p))

        # Goal setup
        # It's theoretically possible for the goal to end up inside a wall,
        # but it's unlikely.
        goal_x = (w-2) * wall_scale
        goal_y = 0
        goal_z = (h-2) * wall_scale
        goal_scale = Point(MAZE_GOAL_SIZE, MAZE_GOAL_SIZE, MAZE_GOAL_SIZE)
        self.goal = Trigger(Point(goal_x, goal_y, goal_z), goal_scale)

    def setup_player(self):
        """ Sets up the player """
        self.player = Player(self.view_matrix.eye,
                             Point(PLAYER_RADIUS, PLAYER_RADIUS, PLAYER_RADIUS))

    def new_game(self):
        """ Wrapper for all the setup functions """
        self.setup_camera()
        self.setup_lights()
        self.setup_maze()
        self.setup_player()

    def start(self):
        """ Starts a brand new game. Don't call this twice. """
        self.new_game()
        glClearColor(COLOR_BG.r, COLOR_BG.b, COLOR_BG.g, 1.0)
        self.program_loop()


if __name__ == "__main__":
    GraphicsProgram3D().start()
