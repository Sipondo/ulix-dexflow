#version 320 es

#ifdef GL_ES
precision highp float;
#endif

layout(location=0)in vec2 aPos;
layout(location=1)in vec2 aSize;

out VS_OUT{
    vec2 size;
}vs_out;

uniform float poffset;

void main()
{
    vs_out.size=aSize;
    
    float x=aPos.x+poffset;
    float y=aPos.y;
    
    gl_Position=vec4(x-1.,y-1.,0.,1.);
}
