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
// out vec3 vs_color;
// out float vs_size;
// out float vs_rot;
// out float vs_noise;
out VS_OUT{
    vec3 vel;
    vec3 color;
    float size;
    float rot;
    float noise;
}vs_out;

uniform vec3 Basis;

void main(){
    gl_Position=vec4(in_pos.xyz*Basis,in_pos.a);
    vs_out.vel=in_vel*Basis;
    vs_out.size=in_size;
    vs_out.color=in_color;
    vs_out.rot=in_rot;
    vs_out.noise=in_noise;
}
