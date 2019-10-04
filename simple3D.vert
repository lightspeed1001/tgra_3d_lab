attribute vec3 a_position;
attribute vec3 a_normal;

uniform mat4 u_model_matrix;
uniform mat4 u_projection_view_matrix;
uniform mat4 u_projection_matrix;
uniform mat4 u_view_matrix;

varying vec4 v_color;
// uniform vec4 u_color;

uniform vec4 u_light_position;
uniform vec4 u_light_diffuse;
uniform vec4 u_mat_diffuse;

void main(void)
{
	vec4 position = vec4(a_position.x, a_position.y, a_position.z, 1.0);
	position = u_model_matrix * position;

	vec4 normal = vec4(a_normal.x, a_normal.y, a_normal.z, 0.0);
	normal = u_model_matrix * normal;
	

	// float light_factor_1 = max(dot(normalize(normal), normalize(vec4(1, 2, 3, 0))), 0.0);
	// float light_factor_2 = max(dot(normalize(normal), normalize(vec4(-3, -2, -1, 0))), 0.0);
	// v_color = (light_factor_1 + light_factor_2) * u_color;

	vec4 s = normalize(u_light_position - position);
	normal = normalize(normal);
	float lambert = max(dot(normal, s), 0.0);
	v_color = u_light_diffuse * u_mat_diffuse * lambert;

	//position = u_projection_view_matrix * position;
	position = u_projection_matrix * u_view_matrix * position;
	//position = u_view_matrix * position;
	//position = u_projection_matrix * position;
	gl_Position = position;
}