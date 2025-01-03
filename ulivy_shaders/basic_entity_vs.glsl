#version 320 es

#ifdef GL_ES
precision highp float;
#endif

layout(location=0)in vec2 aPos;
layout(location=1)in vec2 aSize;
layout(location=2)in vec2 aUv;
layout(location=3)in vec2 aTexPos;
layout(location=4)in vec2 aTexSize;
layout(location=5)in vec2 aTexFrame;

// out VS_OUT{
    //     vec2 size;
    //     vec2 texPos;
    //     vec2 texSize;
    //     vec2 texFrame;
    //     vec4 position;
// }vs_out;

out vec2 uv;
out vec2 fSize;
out vec2 fTexPos;
out vec2 fTexSize;
out vec2 fTexFrame;

uniform vec2 offset;
uniform vec2 camera_position;
uniform vec2 viewport;
uniform vec2 game_position;

void main()
{
    
    uv=aUv;
    fSize=aSize;
    fTexPos=aTexPos;
    fTexSize=aTexSize;
    fTexFrame=aTexFrame;
    
    float x=2.*aPos.x*viewport.x-1.;
    float y=1.-2.*aPos.y*viewport.y;
    
    x=x+offset.x-camera_position.x*2.;
    y=y+offset.y+camera_position.y*2.;
    
    gl_Position=vec4(x,y,0.,1.)*game_position;
    vs_out.position=vec4(x,y,0.,1.);
    
}
