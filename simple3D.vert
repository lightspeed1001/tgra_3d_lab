attribute vec3 a_position;
attribute vec3 a_normal;
attribute vec2 a_uv;

uniform mat4 u_model_matrix;
uniform mat4 u_projection_view_matrix;
uniform mat4 u_projection_matrix;
uniform mat4 u_view_matrix;

varying vec4 v_normal;
varying vec4 v_s;
varying vec4 v_h;
varying vec4 v_position;
varying vec2 v_uv;

void main(void)
{
	// The only thing that the vertex shader does is convert from 
    // the meshes' local coordinates into global coordinates.
    // We need these two vectors to calculate the fragment shader properly.
	vec4 position = vec4(a_position.x, a_position.y, a_position.z, 1.0);
	position = u_model_matrix * position;
	vec4 normal = vec4(a_normal.x, a_normal.y, a_normal.z, 0.0);
    // Send the position and normal into the fragment shader.
	v_normal = normalize(u_model_matrix * normal);
	v_position = position;
	v_uv = a_uv;
    // Convert from local coordinates into global coordinates
	gl_Position = u_projection_matrix * u_view_matrix * position;
}
