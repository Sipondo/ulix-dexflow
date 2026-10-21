#version 320 es

#ifdef GL_ES
precision highp float;
#endif

layout(location=0) in vec2 aPos;
layout(location=1) in vec2 aUv;
layout(location=2) in vec2 aTexPos;
layout(location=3) in vec2 aTexSize;
layout(location=4) in vec2 aTexFrame;

out vec2 uv;
out vec2 fTexPos;
out vec2 fTexSize;
out vec2 fTexFrame;

uniform vec2 offset;
uniform vec2 camera_position;
uniform vec2 viewport;
uniform vec2 game_position;

void main()
{
    uv = aUv;
    fTexPos = aTexPos;
    fTexSize = aTexSize;
    fTexFrame = aTexFrame;
    
    float x = 2.0 * aPos.x * viewport.x - 1.0;
    float y = 1.0 - 2.0 * aPos.y * viewport.y;
    
    x = x + offset.x - camera_position.x * 2.0;
    y = y + offset.y + camera_position.y * 2.0;
    
    gl_Position = vec4(x * game_position.x, y * game_position.y, 0.0, 1.0);
}
