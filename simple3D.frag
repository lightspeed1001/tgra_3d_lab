varying vec4 v_normal;
// varying vec4 v_s;
// varying vec4 v_h;

varying vec4 v_position;
uniform vec4 u_eye_position;

// idk random light that follows player
uniform vec4 u_light_position;
uniform vec4 u_light_color;
uniform float u_light_constant;
uniform float u_light_linear;
uniform float u_light_quadratic;

// Directional light
uniform vec4 u_global_light_direction;
uniform vec4 u_global_light_color;

// Flashlight
// Position is eye position, facing forward
uniform vec4 u_player_flashlight_position;
uniform vec4 u_player_flashlight_direction; // Should be view_matrix.n?
uniform vec4 u_player_flashlight_color;
uniform float u_player_flashlight_theta;
uniform float u_player_flashlight_constant;
uniform float u_player_flashlight_linear;
uniform float u_player_flashlight_quad;

uniform vec4 u_mat_diffuse;
uniform vec4 u_mat_specular;
uniform float u_mat_shiny;

vec4 calculate_directional_light()
{
	vec4 light_dir = normalize(-u_global_light_direction);
	vec4 v = normalize(u_eye_position - v_position);
	vec4 vh = normalize(light_dir + v);

	float lambert = max(dot(v_normal, light_dir), 0.0);
	float phong = max(dot(v_normal, vh), 0.0);

	return u_global_light_color * u_mat_diffuse * lambert
			+ u_global_light_color * u_mat_specular * pow(phong, u_mat_shiny)
			+ (u_global_light_color * 0.01);
}

vec4 calculate_player_light()
{
	vec4 v_s = normalize(u_light_position - v_position);

	vec4 v = normalize(u_eye_position - v_position);
	vec4 v_h = normalize(v_s + v);

	float lambert = max(dot(v_normal, v_s), 0.0);
	float phong = max(dot(v_normal, v_h), 0.0);

	float distance    = length(u_light_position - v_position);
	float attenuation = 1.0 / (u_light_constant + u_light_linear * distance + 
    		    			   u_light_quadratic * (distance * distance));  
	u_light_color *= attenuation;
	return u_light_color * u_mat_diffuse * lambert
			     + u_light_color * u_mat_specular * pow(phong, u_mat_shiny)
				 + u_light_color * 0.01;
}

vec4 calculate_player_flashlight()
{
	// https://learnopengl.com/Lighting/Light-casters
	// fragpos = v_position
	// lightdir = vector from fragpos to light pos
	vec4 light_dir = normalize(u_player_flashlight_position - v_position);
	float theta = dot(light_dir, normalize(u_player_flashlight_direction));
		
	if(theta > u_player_flashlight_theta) 
	{	
		vec4 v = normalize(u_eye_position - v_position);
		vec4 vh = normalize(light_dir + v);

		float lambert = max(dot(v_normal, light_dir), 0.0);
		float phong = max(dot(v_normal, vh), 0.0);

		return u_player_flashlight_color * u_mat_diffuse * lambert
			+ u_player_flashlight_color * u_mat_specular * pow(phong, u_mat_shiny)
			+ (u_player_flashlight_color * 0.01);
		// do lighting calculations
		// return u_player_flashlight_color * 0.6;
	}
	else  // else, use ambient light so scene isn't completely dark outside the spotlight.
		return u_player_flashlight_color * 0.01;
}

void main(void)
{   
	gl_FragColor = calculate_directional_light();
	// gl_FragColor += calculate_player_light();
	gl_FragColor += calculate_player_flashlight();
	// gl_FragColor = vec4(0.1, 0.0, 0.0, 1.0);
}
