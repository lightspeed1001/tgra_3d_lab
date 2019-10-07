varying vec4 v_normal;
varying vec4 v_s;
varying vec4 v_h;

varying vec4 v_position;
uniform vec4 u_eye_position;
uniform vec4 u_light_position;

uniform vec4 u_light_diffuse;
uniform vec4 u_light_specular;

uniform vec4 u_mat_diffuse;
uniform vec4 u_mat_specular;
uniform float u_mat_shiny;

void main(void)
{   
    v_s = normalize(u_light_position - v_position);

	vec4 v = normalize(u_eye_position - v_position);
	v_h = normalize(v_s + v);

	float lambert = max(dot(v_normal, v_s), 0.0);
	float phong = max(dot(v_normal, v_h), 0);

	gl_FragColor = u_light_diffuse * u_mat_diffuse * lambert
			     + u_light_specular * u_mat_specular * pow(phong, u_mat_shiny);
}