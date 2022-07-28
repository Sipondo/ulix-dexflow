#version 320 es

#ifdef GL_ES
precision highp float;
#endif

layout(points)in;
layout(triangle_strip,max_vertices=8)out;

uniform mat4 Mvp;
uniform mat4 BillboardFace;
uniform vec3 CameraPosition;
uniform float Size;
uniform bool IsShadow;
uniform float HeightShare;

out vec2 uv;

void main(){
    vec3 pos=gl_in[0].gl_Position.xyz;
    vec3 right=(BillboardFace*vec4(0,1,0,1)).xyz*Size;
    vec3 up;
    if(IsShadow){
        up=((vec4(1,0,0,1)*Size)).xyz;//*Size;
    }else{
        up=(BillboardFace*vec4(0,0,1,1)).xyz*Size;
        pos=pos-((BillboardFace*vec4(0,0,2.*(1.-HeightShare),1)).xyz*Size);
    }
    
    // vec3 right=vec3(-1.,0.,0.);
    // vec3 up=vec3(0.,-1.,0.);
    
    pos=pos+CameraPosition;
    
    // vec2 stepSize=vec2(0.,0.);
    // stepSize.x=.1;
    // stepSize.y=.1;
    
    // vec4 position=vec4(pos,1.);
    
    // uv=vec2(0.,1.);
    // gl_Position=Mvp*(position+vec4(-stepSize.x,0.,0.,0.));// 1:bottom-left
    // // gl_Position.x=0.;
    // // gl_Position.a=0.;
    // // gl_Position.z=0.;
    // // gl_Position.y=0.;
    // EmitVertex();
    // uv=vec2(1.,1.);
    // gl_Position=position+vec4(stepSize.x,0.,0.,0.);// 2:bottom-right
    // EmitVertex();
    // uv=vec2(0.,0.);
    // gl_Position=position+vec4(-stepSize.x,2.*stepSize.y,0.,0.);// 3:top-left
    // EmitVertex();
    // uv=vec2(1.,0.);
    // gl_Position=position+vec4(stepSize.x,2.*stepSize.y,0.,0.);// 4:top-right
    // EmitVertex();
    // EndPrimitive();
    if(!IsShadow){
        uv=vec2(1.,0.);
        gl_Position=Mvp*vec4(pos+(right+up+up),1.);
        EmitVertex();
        
        uv=vec2(0.,0.);
        gl_Position=Mvp*vec4(pos+(-right+up+up),1.);
        EmitVertex();
        
        uv=vec2(1.,1.);
        gl_Position=Mvp*vec4(pos+(right),1.);
        EmitVertex();
        
        uv=vec2(0.,1.);
        gl_Position=Mvp*vec4(pos+(-right),1.);
        EmitVertex();
        EndPrimitive();
    }else{
        uv=vec2(1.,1.-HeightShare);
        gl_Position=Mvp*vec4(pos+(right+up+up),1.);
        EmitVertex();
        
        uv=vec2(0.,1.-HeightShare);
        gl_Position=Mvp*vec4(pos+(-right+up+up),1.);
        EmitVertex();
        
        uv=vec2(1.,1.);
        gl_Position=Mvp*vec4(pos+(right),1.);
        EmitVertex();
        
        uv=vec2(0.,1.);
        gl_Position=Mvp*vec4(pos+(-right),1.);
        EmitVertex();
        EndPrimitive();
        
        uv=vec2(0.,1.-HeightShare);
        gl_Position=Mvp*vec4(pos+(-right+up+up),1.);
        EmitVertex();
        
        uv=vec2(1.,1.-HeightShare);
        gl_Position=Mvp*vec4(pos+(right+up+up),1.);
        EmitVertex();
        
        uv=vec2(0.,1.);
        gl_Position=Mvp*vec4(pos+(-right),1.);
        EmitVertex();
        
        uv=vec2(1.,1.);
        gl_Position=Mvp*vec4(pos+(right),1.);
        EmitVertex();
        
        EndPrimitive();
    }
}
