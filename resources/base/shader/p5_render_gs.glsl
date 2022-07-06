#version 330

#define M_DEGPI.01745329251
#define PI 3.1415926538
layout(points)in;
layout(triangle_strip,max_vertices=4)out;

uniform mat4 projection;
uniform mat4 BillboardFace;
uniform float Size;
uniform vec3 CameraPosition;
uniform float Stage;
uniform bool Rotvel=true;

in vec3 vs_vel[1];
in vec3 vs_color[1];
in float vs_size[1];
in float vs_rot[1];
in float vs_noise[1];

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
    
    vec3 pos=gl_in[0].gl_Position.xyz*20;
    float new_rot=vs_rot[0];
    
    if(Rotvel){
        vec2 pos_dir=(projection*vec4(pos,1.)).xy-(projection*vec4((gl_in[0].gl_Position.xyz+vs_vel[0])*20,1.)).xy;
        new_rot=new_rot-(atan2(pos_dir.y,pos_dir.x)/M_DEGPI);
    }
    
    vec3 right=(BillboardFace*vec4(0,sin((new_rot+90)*M_DEGPI),cos((new_rot+90)*M_DEGPI),1)).xyz;
    vec3 up=(BillboardFace*vec4(0,sin(new_rot*M_DEGPI),cos(new_rot*M_DEGPI),1)).xyz;
    
    if(pos.z>-.1){
        vec4 proj_pos=projection*vec4(pos,1.);
        float size_modifier=Size*vs_size[0];
        pos=pos+CameraPosition;
        uv=vec2(1.,1.);
        out_color=vs_color[0];
        out_noise=vs_noise[0];
        gl_Position=projection*vec4(pos+(right+up)*size_modifier,1.);
        EmitVertex();
        
        uv=vec2(0.,1.);
        out_color=vs_color[0];
        out_noise=vs_noise[0];
        gl_Position=projection*vec4(pos+(-right+up)*size_modifier,1.);
        EmitVertex();
        
        uv=vec2(1.,0.);
        out_color=vs_color[0];
        out_noise=vs_noise[0];
        gl_Position=projection*vec4(pos+(right-up)*size_modifier,1.);
        EmitVertex();
        
        uv=vec2(0.,0.);
        out_color=vs_color[0];
        out_noise=vs_noise[0];
        gl_Position=projection*vec4(pos+(-right-up)*size_modifier,1.);
        EmitVertex();
        EndPrimitive();
    }
}
