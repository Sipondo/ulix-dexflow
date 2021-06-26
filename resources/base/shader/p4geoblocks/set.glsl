// CONSTANTS
// -- Alter General
float%SIZE%=0;
float%SIZE_SWAY%=0;
bool%SIZE_ABS%=false;
float%ROT%=0;
float%ROT_SWAY%=0;
bool%ROT_ABS%=false;
float%ROT_VEL%=0;
float%ROT_VEL_SWAY%=0;
bool%ROT_VEL_ABS%=false;
float%LIFE%=0;
float%LIFE_SWAY%=0;
bool%LIFE_ABS%=false;
// -- Alter Position
vec3%POS%=vec3(0,0,0);
vec3%POS_SWAY%=vec3(0,0,0);
bool%POS_ABS_X%=false;
bool%POS_ABS_Y%=false;
bool%POS_ABS_Z%=false;
// -- Alter Velocity
vec3%VEL%=vec3(0,0,0);
vec3%VEL_SWAY%=vec3(0,0,0);
bool%VEL_ABS_X%=false;
bool%VEL_ABS_Y%=false;
bool%VEL_ABS_Z%=false;
// -- Alter Colour
vec3%COL%=vec3(0,0,0);
vec3%COL_SWAY%=vec3(0,0,0);
bool%COL_ABS_X%=false;
bool%COL_ABS_Y%=false;
bool%COL_ABS_Z%=false;
// CONSTANTS_END
// DECLARATIONS
// DECLARATIONS_END

pos.x=(%POS_ABS_X%?0:pos.x)+%POS_SWAY%.x*rnd(vec2(gl_PrimitiveIDIn,time))*stp;
pos.y=(%POS_ABS_Y%?0:pos.y)+%POS_SWAY%.y*rnd(vec2(gl_PrimitiveIDIn+2,time*1.1))*stp;
pos.z=(%POS_ABS_Z%?0:pos.z)+%POS_SWAY%.z*rnd(vec2(gl_PrimitiveIDIn+73,time*1.7))*stp;
pos=pos+vec4(%POS%,0)*stp;

vel.x=(%VEL_ABS_X%?0:vel.x)+%VEL_SWAY%.x*rnd(vec2(gl_PrimitiveIDIn+179,time*2.3))*stp;
vel.y=(%VEL_ABS_Y%?0:vel.y)+%VEL_SWAY%.y*rnd(vec2(gl_PrimitiveIDIn+283,time*3.7))*stp;
vel.z=(%VEL_ABS_Z%?0:vel.z)+%VEL_SWAY%.z*rnd(vec2(gl_PrimitiveIDIn+419,time*4.3))*stp;
vel=vel+%VEL%*stp;

size=(%SIZE_ABS%?0:size)+%SIZE_SWAY%*rnd(vec2(gl_PrimitiveIDIn+547,time*5.9))*stp;
size=size+%SIZE%*stp;

color=color+%COL%;

color.x+=%COL_SWAY%.x*rnd(vec2(gl_PrimitiveIDIn+661,time*6.7));
color.y+=%COL_SWAY%.y*rnd(vec2(gl_PrimitiveIDIn+811,time*7.9));
color.z+=%COL_SWAY%.z*rnd(vec2(gl_PrimitiveIDIn+947,time*9.7));

rot=rot+%ROT%;
rot=(%ROT_ABS%?0:rot)+%ROT_SWAY%*rnd(vec2(gl_PrimitiveIDIn+1087,time*10.3));

rot_vel=rot_vel+%ROT_VEL%;
rot_vel=(%ROT_VEL_ABS%?0:rot_vel)+%ROT_VEL_SWAY%*rnd(vec2(gl_PrimitiveIDIn+1967,time*15.1));

lifespan=lifespan+%LIFE%;
lifespan=(%LIFE_ABS%?0:lifespan)+%LIFE_SWAY%*rnd(vec2(gl_PrimitiveIDIn+1229,time*11.3));
