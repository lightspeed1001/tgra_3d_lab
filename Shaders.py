from OpenGL.GL import *
from math import *  # trigonometry

from Base3DObjects import *


class Shader3D:
    def __init__(self):
        vert_shader = glCreateShader(GL_VERTEX_SHADER)
        shader_file = open("simple3D.vert")
        glShaderSource(vert_shader, shader_file.read())
        shader_file.close()
        glCompileShader(vert_shader)
        result = glGetShaderiv(vert_shader, GL_COMPILE_STATUS)
        if result != 1:  # shader didn't compile
            print("Couldn't compile vertex shader\nShader compilation Log:\n" + str(glGetShaderInfoLog(vert_shader)))

        frag_shader = glCreateShader(GL_FRAGMENT_SHADER)
        shader_file = open("simple3D.frag")
        glShaderSource(frag_shader, shader_file.read())
        shader_file.close()
        glCompileShader(frag_shader)
        result = glGetShaderiv(frag_shader, GL_COMPILE_STATUS)
        if result != 1:  # shader didn't compile
            print("Couldn't compile fragment shader\nShader compilation Log:\n" + str(glGetShaderInfoLog(frag_shader)))

        self.renderingProgramID = glCreateProgram()
        glAttachShader(self.renderingProgramID, vert_shader)
        glAttachShader(self.renderingProgramID, frag_shader)
        glLinkProgram(self.renderingProgramID)

        self.positionLoc = glGetAttribLocation(self.renderingProgramID, "a_position")
        glEnableVertexAttribArray(self.positionLoc)

        self.normalLoc = glGetAttribLocation(self.renderingProgramID, "a_normal")
        glEnableVertexAttribArray(self.normalLoc)

        self.eyePosLoc = glGetUniformLocation(self.renderingProgramID, "u_eye_position")
        # self.colorLoc = glGetUniformLocation(self.renderingProgramID, "u_color")
        self.lightPosLoc         = glGetUniformLocation(self.renderingProgramID, "u_light_position")
        self.lightDiffuseLoc     = glGetUniformLocation(self.renderingProgramID, "u_light_diffuse")
        self.lightSpecularLoc    = glGetUniformLocation(self.renderingProgramID, "u_light_specular")

        self.materialDiffuseLoc  = glGetUniformLocation(self.renderingProgramID, "u_mat_diffuse")
        self.materialSpecularLoc = glGetUniformLocation(self.renderingProgramID, "u_mat_specular")
        self.materialShinyLoc = glGetUniformLocation(self.renderingProgramID, "u_mat_shiny")

        self.modelMatrixLoc = glGetUniformLocation(self.renderingProgramID, "u_model_matrix")
        # self.projectionViewMatrixLoc = glGetUniformLocation(self.renderingProgramID, "u_projection_view_matrix")
        self.viewMatrixLoc = glGetUniformLocation(self.renderingProgramID, "u_view_matrix")
        self.projectionMatrixLoc = glGetUniformLocation(self.renderingProgramID, "u_projection_matrix")

    def use(self):
        try:
            glUseProgram(self.renderingProgramID)
        except OpenGL.error.GLError:
            print(glGetProgramInfoLog(self.renderingProgramID))
            raise

    def set_model_matrix(self, matrix_array):
        glUniformMatrix4fv(self.modelMatrixLoc, 1, True, matrix_array)

    # def set_projection_view_matrix(self, matrix_array):
    #     glUniformMatrix4fv(self.projectionViewMatrixLoc, 1, True, matrix_array)

    def set_projection_matrix(self, matrix_array):
        glUniformMatrix4fv(self.projectionMatrixLoc, 1, True, matrix_array)

    def set_view_matrix(self, matrix_array):
        glUniformMatrix4fv(self.viewMatrixLoc, 1, True, matrix_array)

    def set_position_attribute(self, vertex_array):
        glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 0, vertex_array)

    def set_normal_attribute(self, vertex_array):
        glVertexAttribPointer(self.normalLoc, 3, GL_FLOAT, False, 0, vertex_array)

    # def set_solid_color(self, r, g, b):
    #     glUniform4f(self.colorLoc, r, g, b, 1.0)

    def set_eye_position(self, pos):
        glUniform4f(self.eyePosLoc, pos.x, pos.y, pos.z, 1.0)

    def set_light_position(self, pos):
        glUniform4f(self.lightPosLoc, pos.x, pos.y, pos.z, 1.0)

    def set_light_diffuse(self, r, g, b):
        glUniform4f(self.lightDiffuseLoc, r, g, b, 1.0)

    def set_light_specular(self, r, g, b):
        glUniform4f(self.lightSpecularLoc, r, g, b, 1.0)

    def set_material_diffuse(self, r, g, b):
        glUniform4f(self.materialDiffuseLoc, r, g, b, 1.0)

    def set_material_specular(self, r, g, b):
        glUniform4f(self.materialSpecularLoc, r, g, b, 1.0)

    def set_material_shiny(self, s):
        glUniform1f(self.materialShinyLoc, s)