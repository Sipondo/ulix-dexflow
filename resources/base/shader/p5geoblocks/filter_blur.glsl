// CONSTANTS
// -- General
float%LIFE%=1.;
// CONSTANTS_END
// DECLARATIONS
vec4 prev_pos;
vec3 prev_vel;
float prev_size;
vec3 prev_color;
float prev_rot;
float prev_rot_vel;
float prev_lifespan;
float prev_stp;
float prev_key;
// DECLARATIONS_END

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

%GEOBLOCKS%
out_pos=pos;
out_pos.a=%TARGET_STAGE%;
out_vel=vec3(0.,0.,0.);
out_size=size;
out_color=color;
out_rot=rot;
out_rot_vel=rot_vel;
out_lifespan=%LIFE%;
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
