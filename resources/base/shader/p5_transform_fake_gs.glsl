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

// in vec3 vs_vel[1];
// in float vs_size[1];
// in vec3 vs_color[1];
// in float vs_rot[1];
// in float vs_rot_vel[1];
// in float vs_lifespan[1];
// in float vs_noise[1];
// in float vs_key[1];

in VS_OUT{
  vec4 pos;
  vec3 vel;
  float size;
  vec3 color;
  float rot;
  float rot_vel;
  float lifespan;
  float noise;
  float key;
}gs_in[];

out vec4 out_pos;
out vec3 out_vel;
out float out_size;
out vec3 out_color;
out float out_rot;
out float out_rot_vel;
out float out_lifespan;
out float out_noise;
out float out_key;

void main(){
  // if(gs_in[0].lifespan>=0.)
  // {
    //   if(gs_in[0].lifespan<100.)
    //   {
      float stp=StepSize;
      
      vec4 pos=gs_in[0].pos;
      vec3 vel=gs_in[0].vel;
      float size=gs_in[0].size;
      vec3 color=gs_in[0].color;
      float rot=gs_in[0].rot;
      float rot_vel=gs_in[0].rot_vel;
      float lifespan=gs_in[0].lifespan;
      float noise=gs_in[0].noise;
      float key=gs_in[0].key;
      
      // lifespan=lifespan-stp;
      
      // pos=pos+vec4(vel*stp,0.);
      // rot=rot+rot_vel*stp;
      
      out_pos=pos;
      out_vel=vel;
      // out_vel=vec3(1.,2.,3.);
      out_size=size;
      out_color=color;
      out_rot=rot;
      out_rot_vel=rot_vel;
      out_lifespan=lifespan;
      out_noise=noise;
      out_key=key;
      
      EmitVertex();
      EndPrimitive();
    //   }
  // }
}
