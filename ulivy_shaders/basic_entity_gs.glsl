#version 320 es

#ifdef GL_ES
precision highp float;
#endif

layout(points)in;
layout(triangle_strip,max_vertices=4)out;

in VS_OUT{
    vec2 size;
    vec2 texPos;
    vec2 texSize;
    vec2 texFrame;
}gs_in[];

out vec2 fSize;
out vec2 fTexPos;
out vec2 fTexSize;
out vec2 fTexFrame;

uniform vec2 viewport;

void construct_entity(vec4 position)
{
    fSize=gs_in[0].size;
    fTexPos=gs_in[0].texPos;
    fTexSize=gs_in[0].texSize;
    fTexFrame=gs_in[0].texFrame;
    
    vec2 stepSize=2.*viewport;
    
    gl_Position=position+vec4(0.,-stepSize.y,0.,0.);// 1:bottom-left
    EmitVertex();
    gl_Position=position+vec4(stepSize.x,-stepSize.y,0.,0.);// 2:bottom-right
    EmitVertex();
    gl_Position=position+vec4(0.,0.,0.,0.);// 3:top-left
    EmitVertex();
    gl_Position=position+vec4(stepSize.x,0.,0.,0.);// 4:top-right
    EmitVertex();
    EndPrimitive();
}

void main(){
    construct_entity(gl_in[0].gl_Position);
}
