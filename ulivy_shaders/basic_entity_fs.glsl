#version 320 es

#ifdef GL_ES
precision highp float;
#endif

uniform sampler2D texture0;

in vec2 uv;
in vec2 fSize;
in vec2 fTexPos;
in vec2 fTexSize;
in vec2 fTexFrame;

out vec4 frag_color;

void main()
{
    vec2 start=fTexPos/4096.;
    vec2 size=fTexSize/4096./4.;
    
    start.x+=size.x*fTexFrame.x;
    start.y+=size.y*fTexFrame.y;
    
    frag_color=texture(texture0,start+uv*size);
    // frag_color=texture(texture0,uv);
}
