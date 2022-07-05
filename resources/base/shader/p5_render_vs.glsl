#version 330

in vec4 in_pos;
in vec3 in_vel;
in float in_size;
in vec3 in_color;
in float in_rot;
in float in_noise;
in float in_key;

out vec3 vs_vel;
out vec3 vs_color;
out float vs_size;
out float vs_rot;
out float vs_noise;

uniform vec3 Basis;

void main(){
    gl_Position=vec4(in_pos.xyz*Basis,in_pos.a);
    vs_vel=in_vel*Basis;
    vs_size=in_size;
    vs_color=in_color;
    vs_rot=in_rot;
    vs_noise=in_noise;
}
