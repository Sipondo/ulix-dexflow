#version 320 es

#ifdef GL_ES
precision highp float;
#endif

#define M_DEGPI.01745329251
#define PI 3.1415926538
layout(points)in;
layout(triangle_strip,max_vertices=4)out;

uniform mat4 projection;
uniform mat4 BillboardFace;
uniform float Size;
uniform vec3 CameraPosition;
uniform float Stage;
uniform int Rotvel;

// in vec3 vs_vel[1];
// in vec3 vs_color[1];
// in float vs_size[1];
// in float vs_rot[1];
// in float vs_noise[1];

in VS_OUT{
    vec3 vel;
    vec3 color;
    float size;
    float rot;
    float noise;
}gs_in[];

out vec3 out_color;
out float out_noise;
out vec2 uv;

float atan2(in float y,in float x)
{
    bool s=(abs(x)>abs(y));
    return mix(PI/2.-atan(x,y),atan(y,x),s);
}

void main(){
    if(gl_in[0].gl_Position.a!=Stage){return;}
    
    vec3 pos=gl_in[0].gl_Position.xyz*20.;
    float new_rot=gs_in[0].rot;
    
    if(Rotvel>0){
        vec2 pos_dir=(projection*vec4(pos,1.)).xy-(projection*vec4((gl_in[0].gl_Position.xyz+gs_in[0].vel)*20.,1.)).xy;
        new_rot=new_rot-(atan2(pos_dir.y,pos_dir.x)/M_DEGPI);
    }
    
    vec3 right=(BillboardFace*vec4(0.,sin((new_rot+90.)*M_DEGPI),cos((new_rot+90.)*M_DEGPI),1.)).xyz;
    vec3 up=(BillboardFace*vec4(0.,sin(new_rot*M_DEGPI),cos(new_rot*M_DEGPI),1.)).xyz;
    
    if(pos.z>-.1){
        vec4 proj_pos=projection*vec4(pos,1.);
        float size_modifier=Size*gs_in[0].size;
        pos=pos+CameraPosition;
        uv=vec2(1.,1.);
        out_color=gs_in[0].color;
        out_noise=gs_in[0].noise;
        gl_Position=projection*vec4(pos+(right+up)*size_modifier,1.);
        EmitVertex();
        
        uv=vec2(0.,1.);
        out_color=gs_in[0].color;
        out_noise=gs_in[0].noise;
        gl_Position=projection*vec4(pos+(-right+up)*size_modifier,1.);
        EmitVertex();
        
        uv=vec2(1.,0.);
        out_color=gs_in[0].color;
        out_noise=gs_in[0].noise;
        gl_Position=projection*vec4(pos+(right-up)*size_modifier,1.);
        EmitVertex();
        
        uv=vec2(0.,0.);
        out_color=gs_in[0].color;
        out_noise=gs_in[0].noise;
        gl_Position=projection*vec4(pos+(-right-up)*size_modifier,1.);
        EmitVertex();
        EndPrimitive();
    }
}
