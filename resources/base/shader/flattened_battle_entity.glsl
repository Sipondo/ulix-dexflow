#version 330

#if defined VERTEX_SHADER

in vec3 in_pos;
uniform float Shake=-.0;

void main(){
  gl_Position=vec4(in_pos.x,in_pos.y,in_pos.z+Shake,1.);
  // gl_Position=vec4(in_pos,1.);
}

#elif defined GEOMETRY_SHADER
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
    pos=pos-((BillboardFace*vec4(0,0,2*(1-HeightShare),1)).xyz*Size);
  }
  
  pos=pos+CameraPosition;
  
  if(!IsShadow){
    uv=vec2(1.,1.);
    gl_Position=Mvp*vec4(pos+(right+up+up),1.);
    EmitVertex();
    
    uv=vec2(0.,1.);
    gl_Position=Mvp*vec4(pos+(-right+up+up),1.);
    EmitVertex();
    
    uv=vec2(1.,0.);
    gl_Position=Mvp*vec4(pos+(right),1.);
    EmitVertex();
    
    uv=vec2(0.,0.);
    gl_Position=Mvp*vec4(pos+(-right),1.);
    EmitVertex();
    EndPrimitive();
  }else{
    uv=vec2(1.,1.);
    gl_Position=Mvp*vec4(pos+(right+up+up),1.);
    EmitVertex();
    
    uv=vec2(0.,1.);
    gl_Position=Mvp*vec4(pos+(-right+up+up),1.);
    EmitVertex();
    
    uv=vec2(1.,1-HeightShare);
    gl_Position=Mvp*vec4(pos+(right),1.);
    EmitVertex();
    
    uv=vec2(0.,1-HeightShare);
    gl_Position=Mvp*vec4(pos+(-right),1.);
    EmitVertex();
    EndPrimitive();
    
    uv=vec2(0.,1.);
    gl_Position=Mvp*vec4(pos+(-right+up+up),1.);
    EmitVertex();
    
    uv=vec2(1.,1.);
    gl_Position=Mvp*vec4(pos+(right+up+up),1.);
    EmitVertex();
    
    uv=vec2(0.,1-HeightShare);
    gl_Position=Mvp*vec4(pos+(-right),1.);
    EmitVertex();
    
    uv=vec2(1.,1-HeightShare);
    gl_Position=Mvp*vec4(pos+(right),1.);
    EmitVertex();
    
    EndPrimitive();
  }
}

#elif defined FRAGMENT_SHADER

uniform float Brightness;
uniform bool Cutout;
uniform sampler2D Texture;
uniform int AnimationFrame;
uniform int AnimationLength;
uniform int Mirror;
uniform bool IsShadow;

in vec2 uv;
out vec4 f_color;

void main(){
  vec2 subframe=vec2((Mirror*uv.x+AnimationFrame)/AnimationLength,uv.y);
  vec4 col=texture(Texture,subframe);
  if(col.a<.9){
    discard;
  }else{
    if(IsShadow){
      col=col*vec4(0,0,0,.5);
    }
    if(Cutout){
      f_color=vec4(0,0,0,.001);
    }else{
      col.r*=Brightness;//*Brightness;
      col.g*=Brightness;//*Brightness;
      col.b*=Brightness;//*Brightness;
      f_color=col;
    }
  }
}

#endif
