#version 320 es

#ifdef GL_ES
precision highp float;
#endif

layout(points)in;
layout(triangle_strip,max_vertices=4)out;

in VS_OUT{
    vec2 size;
}gs_in[];

out vec2 uv;
out vec2 fSize;

void construct_entity(vec4 position)
{
    fSize=gs_in[0].size;
    
    vec2 stepSize=vec2(.1,.1);
    
    position=position+vec4(stepSize.x,-2.*stepSize.y,0.,0.);
    
    stepSize.x=stepSize.x*fSize.x;
    stepSize.y=stepSize.y*fSize.y;
    
    uv=vec2(0.,1.);
    gl_Position=position+vec4(-stepSize.x,0.,0.,0.);// 1:bottom-left
    EmitVertex();
    uv=vec2(1.,1.);
    gl_Position=position+vec4(stepSize.x,0.,0.,0.);// 2:bottom-right
    EmitVertex();
    uv=vec2(0.,0.);
    gl_Position=position+vec4(-stepSize.x,2.*stepSize.y,0.,0.);// 3:top-left
    EmitVertex();
    uv=vec2(1.,0.);
    gl_Position=position+vec4(stepSize.x,2.*stepSize.y,0.,0.);// 4:top-right
    EmitVertex();
    EndPrimitive();
}

void main(){
    construct_entity(vec4(gl_in[0].gl_Position.xy,0.,1.));
}
