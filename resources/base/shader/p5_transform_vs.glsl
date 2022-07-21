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

// out vec3 vs_vel;
// out float vs_size;
// out vec3 vs_color;
// out float vs_rot;
// out float vs_rot_vel;
// out float vs_lifespan;
// out float vs_noise;
// out float vs_key;
out VS_OUT{
	vec4 pos;
	vec3 vel;
	float size;
	vec3 color;
	float rot;
	float rot_vel;
	float lifespan;
	float noise;
	float key;
}vs_out;

void main(){
	// gl_Position=in_pos;
	vs_out.pos=in_pos;
	vs_out.vel=in_vel;
	vs_out.size=in_size;
	vs_out.color=in_color;
	vs_out.rot=in_rot;
	vs_out.rot_vel=in_rot_vel;
	vs_out.lifespan=in_lifespan;
	vs_out.noise=in_noise;
	vs_out.key=in_key;
}
