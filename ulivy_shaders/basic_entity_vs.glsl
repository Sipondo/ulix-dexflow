#version 320 es

#ifdef GL_ES
precision highp float;
#endif

layout(location=0)in vec2 aPos;
layout(location=1)in vec2 aSize;
layout(location=2)in ivec2 aTexPos;
layout(location=3)in ivec2 aTexSize;
layout(location=4)in ivec2 aTexFrame;

out VS_OUT{
    vec2 size;
    ivec2 texPos;
    ivec2 texSize;
    ivec2 texFrame;
}vs_out;

void main()
{
    vs_out.pos=aPosr;
    vs_out.texPos=aTexPos;
    vs_out.texSize=aTexSize;
    vs_out.texFrame=aTexFrame;
    gl_Position=vec4(aPos.x,aPos.y,0.,1.);
}
