#version 330

#define M_PI 3.1415926535897932384626433832795
uniform vec3 Position;
uniform vec3 Position_sway;
uniform bool Position_radial;

uniform vec3 Velocity;
uniform vec3 Velocity_sway;
uniform bool Velocity_radial;

uniform float Size;
uniform float Size_sway;

uniform vec3 Colour;
uniform vec3 Colour_sway;

uniform float Rotation;
uniform float Rotation_sway;

uniform float Rotation_velocity;
uniform float Rotation_velocity_sway;

uniform float Life;
uniform float Life_sway;

uniform float Stage;

uniform float time;

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
  return 1.-float((n*(n*n*15731+789221)+
1376312589)&0x7fffffff)/1073741824.;
}

void main(){
out_pos=vec4(Position,Stage);
if(Position_radial){
  out_pos.x+=Position_sway.x*sqrt(M_PI*rnd(vec2(gl_VertexID,time)));
  out_pos.y+=Position_sway.y*sqrt(M_PI*rnd(vec2(gl_VertexID+2,time*1.1)));
  out_pos.z+=Position_sway.z*sqrt(M_PI*rnd(vec2(gl_VertexID+73,time*1.7)));
}else{
  out_pos.x+=Position_sway.x*rnd(vec2(gl_VertexID,time));
  out_pos.y+=Position_sway.y*rnd(vec2(gl_VertexID+2,time*1.1));
  out_pos.z+=Position_sway.z*rnd(vec2(gl_VertexID+73,time*1.7));
}

out_vel=Velocity;
if(Velocity_radial){
  out_vel.x+=Velocity_sway.x*sqrt(M_PI*rnd(vec2(gl_VertexID+179,time*2.3)));
  out_vel.y+=Velocity_sway.y*sqrt(M_PI*rnd(vec2(gl_VertexID+283,time*3.7)));
  out_vel.z+=Velocity_sway.z*sqrt(M_PI*rnd(vec2(gl_VertexID+419,time*4.3)));
}else{
  out_vel.x+=Velocity_sway.x*rnd(vec2(gl_VertexID+179,time*2.3));
  out_vel.y+=Velocity_sway.y*rnd(vec2(gl_VertexID+283,time*3.7));
  out_vel.z+=Velocity_sway.z*rnd(vec2(gl_VertexID+419,time*4.3));
}

out_size=Size;
out_size+=Size_sway*rnd(vec2(gl_VertexID+547,time*5.9));

out_color=Colour;
out_color.x+=Colour_sway.x*rnd(vec2(gl_VertexID+661,time*6.7));
out_color.y+=Colour_sway.y*rnd(vec2(gl_VertexID+811,time*7.9));
out_color.z+=Colour_sway.z*rnd(vec2(gl_VertexID+947,time*9.7));

out_rot=Rotation;
out_rot+=Rotation_sway*rnd(vec2(gl_VertexID+1087,time*10.3));

out_rot_vel=Rotation_velocity;
out_rot_vel+=Rotation_velocity_sway*rnd(vec2(gl_VertexID+1409,time*13.1));

out_lifespan=Life;
out_lifespan+=Life_sway*rnd(vec2(gl_VertexID+1229,time*11.3));

out_noise=710*rnd(vec2(gl_VertexID+1381,time*12.7));

out_key=time;
}
