#version 330

#if defined VERTEX_SHADER

in vec3 in_vert;
in vec4 in_anim;

out vec4 vert_anim;

void main(){
  gl_Position=vec4(in_vert.xyz,1.);
  vert_anim=in_anim;
}

#elif defined GEOMETRY_SHADER

layout(points)in;
layout(triangle_strip,max_vertices=4)out;

in vec4 vert_anim[1];
uniform float Zoom;
uniform vec2 WindowSize;
uniform vec2 WindowPosition;
uniform vec2 TextureSize;
uniform float LayerHeight;
out vec2 uv;
out vec4 geo_anim;

void main(){
  geo_anim=vert_anim[0];
  vec3 pos=gl_in[0].gl_Position.xyz;
  if(pos.z!=LayerHeight){
    return;
  }
  
  pos.x=round(pos.x-WindowPosition.x)/WindowSize.x*2-1;
  pos.y=round(WindowPosition.y-pos.y+WindowSize.y)/WindowSize.y*2-1;
  
  pos.x=pos.x*Zoom;
  pos.y=pos.y*Zoom;
  
  vec3 Size=vec3(geo_anim.a/WindowSize.x/8,geo_anim.z/WindowSize.y/8,1.)*Zoom;
  
  vec3 right=(vec4(1,0,0,1)).xyz;
  vec3 up=(vec4(0,1,0,1)).xyz;
  
  uv=vec2(1.,0.);
  gl_Position=vec4(pos+(right+up)*Size,1.);
  EmitVertex();
  
  uv=vec2(0.,0.);
  gl_Position=vec4(pos+(-right+up)*Size,1.);
  EmitVertex();
  
  uv=vec2(1.,1.);
  gl_Position=vec4(pos+(right-up)*Size,1.);
  EmitVertex();
  
  uv=vec2(0.,1.);
  gl_Position=vec4(pos+(-right-up)*Size,1.);
  EmitVertex();
  EndPrimitive();
}

#elif defined FRAGMENT_SHADER

uniform vec2 TextureSize;

in vec2 uv;
in vec4 geo_anim;
uniform sampler2DArray texturearray0;

out vec4 f_color;

void main(){
  vec2 coords=uv/4;
  coords.x+=mod(geo_anim.y,4)/4.;
  coords.y+=int(geo_anim.y/4.)/4.;
  coords.x*=geo_anim.a/TextureSize.y;
  coords.y*=geo_anim.z/TextureSize.x;
  vec4 col=texture(texturearray0,vec3(coords,geo_anim.x));//vec4(0.30, 0.50, 1.00, 1.0);
  f_color=col;
  /*
  if (col.a > 0.0){
    f_color = col;
  }else{
    discard;
  }*/
}

#endif
