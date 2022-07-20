#version 320 es

#ifdef GL_ES
precision highp float;
#endif

uniform sampler2D texture0;

in vec2 uv;
in vec2 fSize;

out vec4 frag_color;

void main()
{
    frag_color=texture(texture0,uv);
}
