#version 320 es

#ifdef GL_ES
precision highp float;
#endif

// layout(location=0)in vec2 aPos;
// layout(location=1)in vec2 aSize;
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
    vec2 size;
}vs_out;

uniform float poffset;

void main()
{
    vs_out.size=in_size;
    
    float x=in_pos.x+poffset;
    float y=in_pos.y;
    
    gl_Position=vec4(x-1.,y-1.,0.,1.);
}
