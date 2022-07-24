#version 320 es

#ifdef GL_ES
precision highp float;
#endif

uniform sampler2D texture0;

in vec2 uv;

out vec4 frag_color;

void main(){
    vec4 col=texture(texture0,uv);
    // vec4 col=texture(texture0,vec2(uv.x,uv.y));
    frag_color=col;//vec4(1.,1.,1.,1.);
}

