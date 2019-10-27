from math import *  # trigonometry
from OpenGL.GL import *
from OpenGL.GLU import *
from Base3DObjects import *


class Shader3D:
    """ Talks to the fragment/vertex shader programs """
    def __init__(self):
        vert_shader = glCreateShader(GL_VERTEX_SHADER)
        shader_file = open("simple3D.vert")
        glShaderSource(vert_shader, shader_file.read())
        shader_file.close()
        glCompileShader(vert_shader)
        result = glGetShaderiv(vert_shader, GL_COMPILE_STATUS)
        if result != 1:  # shader didn't compile
            print("Couldn't compile vertex shader\nShader compilation Log:\n" \
                  + str(glGetShaderInfoLog(vert_shader)))

        frag_shader = glCreateShader(GL_FRAGMENT_SHADER)
        shader_file = open("simple3D.frag")
        glShaderSource(frag_shader, shader_file.read())
        shader_file.close()
        glCompileShader(frag_shader)
        result = glGetShaderiv(frag_shader, GL_COMPILE_STATUS)
        if result != 1:  # shader didn't compile
            print("Couldn't compile fragment shader\nShader compilation Log:\n" \
                  + str(glGetShaderInfoLog(frag_shader)))

        self.renderingProgramID = glCreateProgram()
        glAttachShader(self.renderingProgramID, vert_shader)
        glAttachShader(self.renderingProgramID, frag_shader)
        glLinkProgram(self.renderingProgramID)

        # Item position?
        self.positionLoc = glGetAttribLocation(self.renderingProgramID, "a_position")
        glEnableVertexAttribArray(self.positionLoc)
        self.normalLoc = glGetAttribLocation(self.renderingProgramID, "a_normal")
        glEnableVertexAttribArray(self.normalLoc)
        self.textureLoc = glGetAttribLocation(self.renderingProgramID, "a_uv")
        glEnableVertexAttribArray(self.textureLoc)

        # Eye position
        self.eyePosLoc = glGetUniformLocation(self.renderingProgramID, "u_eye_position")

        # Player lantern light
        self.lightPosLoc       = glGetUniformLocation(self.renderingProgramID, "u_light_position")
        self.lightDiffuseLoc   = glGetUniformLocation(self.renderingProgramID, "u_light_color")
        self.lightAttConstant  = glGetUniformLocation(self.renderingProgramID, "u_light_constant")
        self.lightAttLinear    = glGetUniformLocation(self.renderingProgramID, "u_light_linear")
        self.lightAttQuadratic = glGetUniformLocation(self.renderingProgramID, "u_light_quadratic")

        # Global direction light
        self.globalLightDirection = glGetUniformLocation(self.renderingProgramID, "u_global_light_direction")
        self.globalLightColor     = glGetUniformLocation(self.renderingProgramID, "u_global_light_color")
        
        # Player flashlight
        self.flashlightPosition     = glGetUniformLocation(self.renderingProgramID, "u_player_flashlight_position")
        self.flashlightDirection    = glGetUniformLocation(self.renderingProgramID, "u_player_flashlight_direction")
        self.flashlightDiffuseLoc   = glGetUniformLocation(self.renderingProgramID, "u_player_flashlight_color")
        self.flashlightCutoff       = glGetUniformLocation(self.renderingProgramID, "u_player_flashlight_cutoff")
        self.flashlightAttConstant  = glGetUniformLocation(self.renderingProgramID, "u_player_flashlight_constant")
        self.flashlightAttLinear    = glGetUniformLocation(self.renderingProgramID, "u_player_flashlight_linear")
        self.flashlightAttQuadratic = glGetUniformLocation(self.renderingProgramID, "u_player_flashlight_quad")
        self.flashlightOuterCutoff  = glGetUniformLocation(self.renderingProgramID, "u_player_flashlight_outer_cutoff")

        # Material
        self.materialDiffuseLoc  = glGetUniformLocation(self.renderingProgramID, "u_mat_diffuse")
        self.materialSpecularLoc = glGetUniformLocation(self.renderingProgramID, "u_mat_specular")
        self.materialShinyLoc    = glGetUniformLocation(self.renderingProgramID, "u_mat_shiny")
        self.materialEmit        = glGetUniformLocation(self.renderingProgramID, "u_mat_emit")

        # Matrices
        self.modelMatrixLoc      = glGetUniformLocation(self.renderingProgramID, "u_model_matrix")
        self.viewMatrixLoc       = glGetUniformLocation(self.renderingProgramID, "u_view_matrix")
        self.projectionMatrixLoc = glGetUniformLocation(self.renderingProgramID, "u_projection_matrix")
        
        # "fog"
        self.fogDistance = glGetUniformLocation(self.renderingProgramID, "u_fog")
        self.fogColor    = glGetUniformLocation(self.renderingProgramID, "u_fog_color")

        # Texture
        self.useTexture = glGetUniformLocation(self.renderingProgramID, "u_use_texture")
        self.diffuse_texture = glGetUniformLocation(self.renderingProgramID, "u_tex_diffuse")
        self.specular_texture = glGetUniformLocation(self.renderingProgramID, "u_tex_specular")
        # glUniform

    def use(self):
        try:
            glUseProgram(self.renderingProgramID)
        except OpenGL.error.GLError:
            print(glGetProgramInfoLog(self.renderingProgramID))
            raise

    def set_diffuse_texture(self, i):
        glUniform1i(self.diffuse_texture, i)

    def set_specular_texture(self, i):
        glUniform1i(self.specular_texture, i)

    def set_model_matrix(self, matrix_array):
        glUniformMatrix4fv(self.modelMatrixLoc, 1, True, matrix_array)

    def set_projection_matrix(self, matrix_array):
        glUniformMatrix4fv(self.projectionMatrixLoc, 1, True, matrix_array)

    def set_view_matrix(self, matrix_array):
        glUniformMatrix4fv(self.viewMatrixLoc, 1, True, matrix_array)

    def set_position_attribute(self, vertex_array):
        glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 0, vertex_array)

    def set_normal_attribute(self, vertex_array):
        glVertexAttribPointer(self.normalLoc, 3, GL_FLOAT, False, 0, vertex_array)

    def set_texture_attribute(self, vertex_array):
        glVertexAttribPointer(self.textureLoc, 2, GL_FLOAT, False, 0, vertex_array)

    def set_eye_position(self, pos):
        glUniform4f(self.eyePosLoc, pos.x, pos.y, pos.z, 1.0)

    # Player lantern
    def set_light_position(self, pos):
        glUniform4f(self.lightPosLoc, pos.x, pos.y, pos.z, 1.0)

    def set_light_diffuse(self, rgb):
        glUniform4f(self.lightDiffuseLoc, rgb.r, rgb.g, rgb.b, 1.0)

    def set_light_attenuation_constant(self, f):
        glUniform1f(self.lightAttConstant, f)

    def set_light_attenuation_linear(self, f):
        glUniform1f(self.lightAttLinear, f)

    def set_light_attenuation_quad(self, f):
        glUniform1f(self.lightAttQuadratic, f)

    # Global Directional
    def set_global_light_direction(self, pos):
        glUniform4f(self.globalLightDirection, pos.x, pos.y, pos.z, 1.0)

    def set_global_light_color(self, rgb):
        glUniform4f(self.globalLightColor, rgb.r, rgb.g, rgb.b, 1.0)

    # Flashlight
    def set_flashlight_position(self, pos):
        glUniform4f(self.flashlightPosition, pos.x, pos.y, pos.z, 1.0)

    def set_flashlight_direction(self, pos):
        glUniform4f(self.flashlightDirection, pos.x, pos.y, pos.z, 1.0)

    def set_flashlight_color(self, rgb, a=1.0):
        glUniform4f(self.flashlightDiffuseLoc, rgb.r, rgb.g, rgb.b, a)

    def set_flashlight_cutoff(self, f):
        glUniform1f(self.flashlightCutoff, f)

    def set_flashlight_outer_cutoff(self, f):
        glUniform1f(self.flashlightOuterCutoff, f)

    def set_flashlight_attenuation_constant(self, f):
        glUniform1f(self.flashlightAttConstant, f)

    def set_flashlight_attenuation_linear(self, f):
        glUniform1f(self.flashlightAttLinear, f)

    def set_flashlight_attenuation_quad(self, f):
        glUniform1f(self.flashlightAttQuadratic, f)

    # Model
    # def set_material_diffuse(self, rgb, a=1.0):
    #     glUniform4f(self.materialDiffuseLoc, rgb[0], rgb[1], rgb[2], a)

    # def set_material_specular(self, rgb):
    #     glUniform4f(self.materialSpecularLoc, rgb[0], rgb[1], rgb[2], 1.0)

    def set_material_shiny(self, s):
        glUniform1f(self.materialShinyLoc, s)

    def set_material_emit(self, e):
        glUniform1f(self.materialEmit, e)

    def set_fog_distance(self, f):
        glUniform1f(self.fogDistance, f)

    def set_fog_color(self, rgb):
        glUniform4f(self.fogColor, rgb.r, rgb.g, rgb.b, 1.0)

    # Texture
    def set_use_texture(self, f):
        glUniform1f(self.useTexture, f)

    # Mesh lab
    def set_attribute_buffers(self, vertex_buffer_id, has_texture=0):
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_id)
        if(has_texture):
            glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 8 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(0))
            glVertexAttribPointer(self.normalLoc, 3, GL_FLOAT, False, 8 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(3 * sizeof(GLfloat)))
            glVertexAttribPointer(self.textureLoc, 2, GL_FLOAT, False, 8 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(6 * sizeof(GLfloat)))
        else:
            glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 6 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(0))
            glVertexAttribPointer(self.normalLoc, 3, GL_FLOAT, False, 6 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(3 * sizeof(GLfloat)))

        # glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 0, None)
        # glVertexAttribPointer(self.normalLoc, 3, GL_FLOAT, False, 0, None)

    def set_material_diffuse(self, color):
        glUniform4f(self.materialDiffuseLoc, color.r, color.g, color.b, 1.0)

    def set_material_specular(self, color):
        glUniform4f(self.materialSpecularLoc, color.r, color.g, color.b, 1.0)

    # def set_material_shiny(self, shininess):
    #     glUniform1f(self.materialShinyLoc, shininess)
