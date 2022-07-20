#version 320 es

#ifdef GL_ES
precision highp float;
#endif

layout(points)in;
layout(points,max_vertices=10)out;

uniform float StepSize;
uniform float time;

uniform float UNI_user_x;
uniform float UNI_target_x;
uniform float UNI_user_y;
uniform float UNI_target_y;
uniform float UNI_user_z;
uniform float UNI_target_z;

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
  
  vec4 prev_pos;
float prev_stp;


vec3 prev_color;
vec3 prev_vel;
float prev_size;
float prev_key;
float prev_lifespan;
float prev_rot;
float prev_rot_vel;if(pos.a==8725064.)
{


if((pos.z<0.)&&(vel.z<0.))
{
    vel.z=-vel.z/(1.4);
    vel=vel/(1.);
    lifespan=lifespan/(3.);
}

}if(pos.a==8725064.)
{


vel=vel*vec3((.985), (.985), (.985));

}if(pos.a==8725064.)
{


pos=pos+vec4(vec3((0.), (0.), (0.)),0)*stp;
pos.x=(false?vec3((0.), (0.), (0.)).x:pos.x)+vec3((0.), (0.), (0.)).x*rnd(vec2(gl_PrimitiveIDIn,time))*stp;
pos.y=(false?vec3((0.), (0.), (0.)).y:pos.y)+vec3((0.), (0.), (0.)).y*rnd(vec2(gl_PrimitiveIDIn+2,time*1.1))*stp;
pos.z=(false?vec3((0.), (0.), (0.)).z:pos.z)+vec3((0.), (0.), (0.)).z*rnd(vec2(gl_PrimitiveIDIn+73,time*1.7))*stp;

vel=vel+vec3((0.), (0.), (1.5))*stp;
vel.x=(false?vec3((0.), (0.), (1.5)).x:vel.x)+vec3((0.), (0.), (0.)).x*rnd(vec2(gl_PrimitiveIDIn+179,time*2.3))*stp;
vel.y=(false?vec3((0.), (0.), (1.5)).y:vel.y)+vec3((0.), (0.), (0.)).y*rnd(vec2(gl_PrimitiveIDIn+283,time*3.7))*stp;
vel.z=(false?vec3((0.), (0.), (1.5)).z:vel.z)+vec3((0.), (0.), (0.)).z*rnd(vec2(gl_PrimitiveIDIn+419,time*4.3))*stp;

size=size+(0.)*stp;
size=(false?(0.):size)+(0.)*rnd(vec2(gl_PrimitiveIDIn+547,time*5.9))*stp;

color=color+vec3((0.), (0.), (0.));

color.x+=vec3((0.), (0.), (0.)).x*rnd(vec2(gl_PrimitiveIDIn+661,time*6.7));
color.y+=vec3((0.), (0.), (0.)).y*rnd(vec2(gl_PrimitiveIDIn+811,time*7.9));
color.z+=vec3((0.), (0.), (0.)).z*rnd(vec2(gl_PrimitiveIDIn+947,time*9.7));

rot=rot+(0.);
rot=(false?(0.):rot)+(0.)*rnd(vec2(gl_PrimitiveIDIn+1087,time*10.3));

rot_vel=rot_vel+(0.);
rot_vel=(false?(0.):rot_vel)+(0.)*rnd(vec2(gl_PrimitiveIDIn+1967,time*15.1));

lifespan=lifespan+(0.);
lifespan=(false?(0.):lifespan)+(0.)*rnd(vec2(gl_PrimitiveIDIn+1229,time*11.3));

}if(pos.a==8725064.)
{


prev_pos=pos;
prev_vel=vel;
prev_size=size;
prev_color=color;
prev_rot=rot;
prev_rot_vel=rot_vel;
prev_lifespan=lifespan;
prev_stp=stp;
prev_key=key;
stp=1.;


out_pos=pos;
out_pos.a=10159782.;
out_vel=vec3(0.,0.,0.);
out_size=size;
out_color=color;
out_rot=rot;
out_rot_vel=rot_vel;
out_lifespan=(0.1);
out_noise=noise+700.*rnd(vec2(gl_PrimitiveIDIn,time));
out_key=key;
EmitVertex();
EndPrimitive();

stp=prev_stp;
pos=prev_pos;
vel=prev_vel;
size=prev_size;
color=prev_color;
rot=prev_rot;
rot_vel=prev_rot_vel;
lifespan=prev_lifespan;
key=prev_key;

}
  
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
