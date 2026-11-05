#include "platform"

layout(location = 0) in vec2 aPos;
layout(location = 1) in vec2 aUv;
layout(location = 2) in vec2 aTexPos;
layout(location = 3) in vec2 aTexSize;
layout(location = 4) in vec2 aTexFrame;

out vec2 uv;
flat out vec2 fTexPos;
flat out vec2 fTexSize;
flat out vec2 fTexFrame;

uniform vec2 camera;
uniform vec2 view_size;
uniform vec2 map_offset;

void main()
{
    uv = aUv;
    fTexPos = aTexPos;
    fTexSize = aTexSize;
    fTexFrame = aTexFrame;

    vec2 world = aPos + map_offset;
    vec2 screen = (world - camera) / view_size;

    gl_Position = vec4(screen.x * 2.0 - 1.0, 1.0 - screen.y * 2.0, 0.0, 1.0);
}
