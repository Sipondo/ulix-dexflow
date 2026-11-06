#include "platform"

// draws one compiled tile block (world.ldtkc) out of the shared tile atlas
uniform highp usampler2D tiles;
uniform sampler2D atlas;

uniform vec2 camera;
uniform vec2 view_size;
uniform vec2 map_offset;

in vec2 v_screen;

layout (location = 0) out vec4 out_color;

const int TILE = 16;

void main() {
    vec2 world = camera + v_screen * view_size + map_offset;
    ivec2 cell = ivec2(floor(world));
    if (any(lessThan(cell, ivec2(0))) || any(greaterThanEqual(cell, textureSize(tiles, 0)))) {
        discard;
    }

    uvec2 tile = texelFetch(tiles, cell, 0).xy;
    if (tile == uvec2(0u)) {
        discard;
    }

    ivec2 pixel = min(ivec2(fract(world) * float(TILE)), ivec2(TILE - 1));
    vec4 color = texelFetch(atlas, (ivec2(tile) - ivec2(1, 0)) * TILE + pixel, 0);
    if (color.a == 0.0) {
        discard;
    }
    out_color = color;
}
