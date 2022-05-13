#version 320 es

#ifdef GL_ES
precision highp float;
#endif

in vec2 vPosition;
in vec2 vTexCoords0;

uniform mat4 modelview_mat;
uniform mat4 projection_mat;
uniform float shake;

out vec2 uv;

void main(){
    gl_Position=projection_mat*modelview_mat*vec4(vPosition.x,vPosition.y+shake,0,1.);
    uv=vTexCoords0;
}
