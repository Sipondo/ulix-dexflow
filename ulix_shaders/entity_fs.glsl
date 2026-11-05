#include "platform"

uniform sampler2D atlas;

in vec2 uv;
flat in vec2 fTexPos;
flat in vec2 fTexSize;
flat in vec2 fTexFrame;

layout(location = 0) out vec4 out_color;

const float ATLAS_SIZE = 4096.0;

void main()
{
    vec2 start = fTexPos / ATLAS_SIZE;
    vec2 size = fTexSize / ATLAS_SIZE / 4.0;

    start.x += size.x * fTexFrame.x;
    start.y += size.y * fTexFrame.y;

    vec4 color = texture(atlas, start + uv * size);
    if (color.a == 0.0) {
        discard;
    }

    out_color = color;
}
