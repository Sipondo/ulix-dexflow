#version 320 es

#ifdef GL_ES
precision highp float;
#endif

out vec4 frag_color;

out vec2 fSize;
out ivec2 fTexPos;
out ivec2 fTexSize;
out ivec2 fTexFrame;

void main()
{
    frag_color=vec4(fSize,1.,1.);
}
