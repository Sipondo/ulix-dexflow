#version 320 es

#ifdef GL_ES
precision highp float;
#endif

uniform sampler2D texture0;
uniform float offset;
uniform float speed;
uniform float brightness;

in vec2 uv;

out vec4 frag_color;

void main(){
    vec4 col=texture(texture0,vec2((uv.x+offset)/speed,uv.y));
    // vec4 col=texture(texture0,vec2(uv.x,uv.y));
    frag_color=vec4(col.x*brightness,col.y*brightness,col.z*brightness,col.a);
}

