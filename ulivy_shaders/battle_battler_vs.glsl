#version 320 es

#ifdef GL_ES
precision highp float;
#endif

layout(location=0)in vec3 in_pos;

uniform float Shake;

void main(){
    gl_Position=vec4(in_pos.x,in_pos.y,in_pos.z+Shake,1.);
    // gl_Position=vec4(in_pos,1.);
}
