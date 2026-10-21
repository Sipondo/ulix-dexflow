#version 320 es

#ifdef GL_ES
precision highp float;
#endif

layout(location=0)in vec3 in_pos;

out VS_OUT{
    vec4 position;
}vs_out;

uniform float Shake;

void main(){
    gl_Position=vec4(in_pos.x,in_pos.y,in_pos.z+Shake,1.);
    vs_out.position=vec4(in_pos.x,in_pos.y,in_pos.z+Shake,1.);
    // gl_Position=vec4(in_pos,1.);
}
