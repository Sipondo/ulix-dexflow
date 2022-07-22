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

out VS_OUT{
    float size;
}vs_out;

uniform float poffset;

void main()
{
    vs_out.size=in_size;
    
    gl_Position=vec4(0.,0.,0.,0.);
}
