varying vec4 v_normal;
varying vec4 v_position;
uniform vec4 u_eye_position;

// Lanter light around the player
uniform vec4 u_light_position;
uniform vec4 u_light_color;
uniform float u_light_constant;
uniform float u_light_linear;
uniform float u_light_quadratic;

// Directional light
uniform vec4 u_global_light_direction;
uniform vec4 u_global_light_color;

// Flashlight
uniform vec4 u_player_flashlight_position;
uniform vec4 u_player_flashlight_direction;
uniform vec4 u_player_flashlight_color;
uniform float u_player_flashlight_cutoff;
uniform float u_player_flashlight_outer_cutoff;
uniform float u_player_flashlight_constant;
uniform float u_player_flashlight_linear;
uniform float u_player_flashlight_quad;

// Material
uniform vec4 u_mat_diffuse;
uniform vec4 u_mat_specular;
uniform float u_mat_shiny;
uniform float u_mat_emit;

// "fog"
uniform float u_fog;
uniform vec4 u_fog_color;

vec4 calculate_directional_light()
{
	// Start by checking in what direction the light is facing.
    // For some weird reason, the "standard" thing to do is
    // to face the light away from the scene, 
    // and then reverse it in the shader.
	vec4 light_dir = normalize(-u_global_light_direction);
    // Get the vector from the camera to the fragment
	vec4 v = normalize(u_eye_position - v_position);
    // Get the vector from the light to the other one
    // It's used to calculate the specularity
	vec4 vh = normalize(light_dir + v);

    // Calculate the true color of the material
	float lambert = max(dot(v_normal, light_dir), 0.0);
    // Calculate the specularity/shininess
	float phong = max(dot(v_normal, vh), 0.0);

    // Combine the values, along with a little bit of ambience
	return u_global_light_color * u_mat_diffuse * lambert
			+ u_global_light_color * u_mat_specular * pow(phong, u_mat_shiny)
			+ (u_global_light_color * 0.01);
}

vec4 calculate_player_light()
{
	// https://learnopengl.com/Lighting/Light-casters
	// This function is identical to the other one, with one added thing.
	vec4 light_dir = normalize(u_light_position - v_position);

	vec4 v = normalize(u_eye_position - v_position);
	vec4 v_h = normalize(light_dir + v);

	float lambert = max(dot(v_normal, light_dir), 0.0);
	float phong = max(dot(v_normal, v_h), 0.0);
	// We want to limit the range of the light, so we need to reduce
	// the strenght of the light as the fragments get further away.
	float distance    = length(u_light_position - v_position);
	float attenuation = 1.0 / (u_light_constant + u_light_linear * distance + 
    		    			   u_light_quadratic * (distance * distance));  
	// Once we calculate the attenuation scale, we simply modify the color
	// of the light accordingly.
	u_light_color *= attenuation;
	return u_light_color * u_mat_diffuse * lambert
			     + u_light_color * u_mat_specular * pow(phong, u_mat_shiny)
				 + u_light_color * 0.01;
}

vec4 calculate_player_flashlight()
{
	// Direction of the light as always.
	vec4 light_dir = normalize(u_player_flashlight_position - v_position);
	// Now we want to calculate the angle of the light between the light and the target
	float theta = dot(light_dir, normalize(u_player_flashlight_direction));
	// If we just check the angle, we'd end up with an unnatural ring of light,
	// so we need to calculate some fudge values.
	float epsilon = u_player_flashlight_cutoff - u_player_flashlight_outer_cutoff;
	// As it gets further away from the cutoff point, 
	// it gets darker, until it's completely black.
	float intensity = clamp((theta - u_player_flashlight_outer_cutoff) / epsilon, 0.0, 1.0);
	
	// Then we simply calculate the colors, same as always.
	vec4 v = normalize(u_eye_position - v_position);
	vec4 vh = normalize(light_dir + v);

	float lambert = max(dot(v_normal, light_dir), 0.0);
	float phong = max(dot(v_normal, vh), 0.0);

	// Flashlights don't go infinitely far, so we limit that as well
	float distance    = length(u_player_flashlight_position - v_position);
	float attenuation = 1.0 / (u_player_flashlight_constant + u_player_flashlight_linear * distance + 
    		    			   u_player_flashlight_quad * (distance * distance));  

	// Remember to modify the color according to our intensity and attenuation!
	u_player_flashlight_color *= intensity;
	u_player_flashlight_color *= attenuation;
	return u_player_flashlight_color * u_mat_diffuse * lambert
		+ u_player_flashlight_color * u_mat_specular * pow(phong, u_mat_shiny)
		+ (u_player_flashlight_color * 0.01);
}

void main(void)
{   
	// I decided to break the main function into multiple
    // sub functions, since it makes for much more readable code.
	gl_FragColor = calculate_directional_light();
	gl_FragColor += calculate_player_light();
	// None of my materials have any emissions, but just in case
	gl_FragColor += u_mat_diffuse * u_mat_emit;
	if(u_fog > 0)
	{
		// The fog effect simply fades all the colors to the fog color,
		// as objects get further away.
		float len = max(min(1 - length(v_position - u_eye_position) / u_fog, 1.0), 0.0);
		gl_FragColor = vec4(gl_FragColor.rgb * min(1 - length(v_position - u_eye_position) / u_fog, 1.0), 1);
	}
	// I wanted the flashlight to cut through the fog, just to see if I could.
	// It works great.
	gl_FragColor += calculate_player_flashlight();
}
