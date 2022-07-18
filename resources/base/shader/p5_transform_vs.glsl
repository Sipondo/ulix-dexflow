#version 320 es

#ifdef GL_ES
precision highp float;
#endif

in vec4 in_pos;
in vec3 in_vel;
in float in_size;
in vec3 in_color;
in float in_rot;
in float in_rot_vel;
in float in_lifespan;
in float in_noise;
in float in_key;

out vec3 vs_vel;
out float vs_size;
out vec3 vs_color;
out float vs_rot;
out float vs_rot_vel;
out float vs_lifespan;
out float vs_noise;
out float vs_key;

void main(){
	gl_Position=in_pos;
	vs_vel=in_vel;
	vs_size=in_size;
	vs_color=in_color;
	vs_rot=in_rot;
	vs_rot_vel=in_rot_vel;
	vs_lifespan=in_lifespan;
	vs_noise=in_noise;
	vs_key=in_key;
}
