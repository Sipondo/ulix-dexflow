#version 320 es

#ifdef GL_ES
precision highp float;
#endif

/* Outputs to the fragment shader */
out vec4 frag_color;
out vec2 tex_coord0;

/* vertex attributes */
in vec2 vPosition;
in vec2 vTexCoords0;

/* uniform variables */
uniform mat4 modelview_mat;
uniform mat4 projection_mat;
uniform vec4 color;
uniform float opacity;

void main(void){
    frag_color=color*vec4(1.,1.,1.,opacity);
    tex_coord0=vTexCoords0;
    gl_Position=projection_mat*modelview_mat*vec4(vPosition.xy,0.,1.);
}
