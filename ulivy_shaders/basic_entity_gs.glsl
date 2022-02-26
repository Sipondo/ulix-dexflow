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

out vec2 uv;
out vec2 fSize;
out vec2 fTexPos;
out vec2 fTexSize;
out vec2 fTexFrame;

uniform vec2 viewport;
uniform vec2 game_position;

void construct_entity(vec4 position)
{
    fSize=gs_in[0].size;
    fTexPos=gs_in[0].texPos;
    fTexSize=gs_in[0].texSize;
    fTexFrame=gs_in[0].texFrame;
    
    vec2 stepSize=2.*viewport*game_position;
    
    // position=vec4(position.xy*game_position,0,0);
    
    uv=vec2(0.,1.);
    gl_Position=position+vec4(0.,-stepSize.y,0.,0.);// 1:bottom-left
    EmitVertex();
    uv=vec2(1.,1.);
    gl_Position=position+vec4(stepSize.x,-stepSize.y,0.,0.);// 2:bottom-right
    EmitVertex();
    uv=vec2(0.,0.);
    gl_Position=position+vec4(0.,0.,0.,0.);// 3:top-left
    EmitVertex();
    uv=vec2(1.,0.);
    gl_Position=position+vec4(stepSize.x,0.,0.,0.);// 4:top-right
    EmitVertex();
    EndPrimitive();
}

void main(){
    construct_entity(vec4(gl_in[0].gl_Position.xy*game_position,0.,1.));
}
