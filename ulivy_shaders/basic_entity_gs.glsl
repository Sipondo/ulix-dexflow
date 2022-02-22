#version 320 es

#ifdef GL_ES
precision highp float;
#endif

layout(points)in;
layout(triangle_strip,max_vertices=4)out;

in VS_OUT{
    vec2 size;
    ivec2 texPos;
    ivec2 texSize;
    ivec2 texFrame;
}gs_in[];

out vec2 fSize;
out ivec2 fTexPos;
out ivec2 fTexSize;
out ivec2 fTexFrame;

void construct_entity(vec4 position)
{
    fSize=gs_in[0].size;
    fTexPos=gs_in[0].texPos;
    fTexSize=gs_in[0].texSize;
    fTexFrame=gs_in[0].texFrame;
    
    gl_Position=position+vec4(-.2,-.2,0.,0.);// 1:bottom-left
    EmitVertex();
    gl_Position=position+vec4(.2,-.2,0.,0.);// 2:bottom-right
    EmitVertex();
    gl_Position=position+vec4(-.2,.2,0.,0.);// 3:top-left
    EmitVertex();
    gl_Position=position+vec4(.2,.2,0.,0.);// 4:top-right
    EmitVertex();
    EndPrimitive();
}

void main(){
    construct_entity(gl_in[0].gl_Position);
}
