#version 320 es

#ifdef GL_ES
precision highp float;
#endif

layout(location=0)in vec4 in_pos;
layout(location=1)in vec3 in_vel;
layout(location=2)in float in_size;
layout(location=3)in vec3 in_color;
layout(location=4)in float in_rot;
layout(location=5)in float in_rot_vel;
layout(location=6)in float in_lifespan;
layout(location=7)in float in_noise;
layout(location=8)in float in_key;

// out vec3 vs_vel;
// out vec3 vs_color;
// out float vs_size;
// out float vs_rot;
// out float vs_noise;
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

uniform vec3 Basis;

void main(){
    vs_out.pos=vec4(in_pos.xyz*Basis,in_pos.a);
    vs_out.vel=in_vel*Basis;
    vs_out.size=in_size;
    vs_out.color=in_color;
    vs_out.rot=in_rot;
    vs_out.rot_vel=in_rot_vel;
    vs_out.lifespan=in_lifespan;
    vs_out.noise=in_noise;
    vs_out.key=in_key;
    gl_Position=vec4(in_pos.xyz*Basis,in_pos.a);
}
