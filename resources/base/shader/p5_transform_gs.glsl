#version 320 es

#ifdef GL_ES
precision highp float;
#endif

layout(points)in;
layout(points,max_vertices=10)out;

uniform float StepSize;
uniform float time;

%UNIFORMS%

in vec3 vs_vel[1];
in float vs_size[1];
in vec3 vs_color[1];
in float vs_rot[1];
in float vs_rot_vel[1];
in float vs_lifespan[1];
in float vs_noise[1];
in float vs_key[1];

out vec4 out_pos;
out vec3 out_vel;
out float out_size;
out vec3 out_color;
out float out_rot;
out float out_rot_vel;
out float out_lifespan;
out float out_noise;
out float out_key;

float rnd(vec2 x)
{
  int n=int(x.x*40.+x.y*6400.);
  n=(n<<13)^n;
  return 1.-float((n*(n*n*15731+789221)+\
1376312589)&0x7fffffff)/1073741824.;
}

void main(){
if(vs_lifespan[0]>=0.)
{
  float stp=StepSize;
  
  vec4 pos=gl_in[0].gl_Position;
  vec3 vel=vs_vel[0];
  float size=vs_size[0];
  vec3 color=vs_color[0];
  float rot=vs_rot[0];
  float rot_vel=vs_rot_vel[0];
  float lifespan=vs_lifespan[0];
  float noise=vs_noise[0];
  float key=vs_key[0];
  
  bool keep_alive=true;
  
  lifespan=lifespan-stp;
  
  %GEOBLOCKS%
  
  pos=pos+vec4(vel*stp,0.);
  rot=rot+rot_vel*stp;
  if(!keep_alive){return;}
  if(time<0.){return;}
  out_pos=pos;
  out_vel=vel;
  out_size=size;
  out_color=color;
  out_rot=rot;
  out_rot_vel=rot_vel;
  out_lifespan=lifespan;
  out_noise=noise;
  out_key=key;
  
  EmitVertex();
  EndPrimitive();
}
}
