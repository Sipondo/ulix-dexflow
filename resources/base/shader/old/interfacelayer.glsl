#version 330

#if defined VERTEX_SHADER

in vec2 in_position;
in vec2 in_texcoord_0;

out vec2 uv0;

void main() {
    gl_Position = vec4(in_position, 0.0, 1.0);
    uv0 = vec2(in_texcoord_0[0], 1.0-in_texcoord_0[1]);
}

#elif defined FRAGMENT_SHADER

uniform sampler2D interface_layer;

in vec2 uv0;

out vec4 fragColor;

void main() {
    vec4 retrieveColor;
    // Lastly, render the overlay
    retrieveColor = texture(interface_layer, uv0);

    // If not transparent, render pixel
    if (retrieveColor.w > 0){
      fragColor = retrieveColor * retrieveColor.w + fragColor * (1-retrieveColor.w);
    }
}
#endif
