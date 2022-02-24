#version 320 es

#ifdef GL_ES
precision highp float;
#endif

layout(location=0)in vec2 aPos;
layout(location=1)in vec2 aSize;
layout(location=2)in vec2 aTexPos;
layout(location=3)in vec2 aTexSize;
layout(location=4)in vec2 aTexFrame;

out VS_OUT{
    vec2 size;
    vec2 texPos;
    vec2 texSize;
    vec2 texFrame;
}vs_out;

uniform vec2 offset;
uniform vec2 camera_position;

void main()
{
    vs_out.size=aSize;
    vs_out.texPos=aTexPos;
    vs_out.texSize=aTexSize;
    vs_out.texFrame=aTexFrame;
    gl_Position=vec4(aPos.x+offset.x-camera_position.x*2.,aPos.y+offset.y+camera_position.y*2.,0.,1.);
}
