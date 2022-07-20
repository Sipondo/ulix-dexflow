// CONSTANTS
// -- General
float%LIFE_MIN%=0;
float%LIFE_MAX%=100.;
// -- Position
vec3%MIN_POS%=vec3(-100.,-100.,-100.);
vec3%MAX_POS%=vec3(100.,100.,100.);
// -- Velocity
vec3%MIN_VEL%=vec3(-100.,-100.,-100.);
vec3%MAX_VEL%=vec3(100.,100.,100.);
// CONSTANTS_END
// DECLARATIONS
float prev_stp;
// DECLARATIONS_END

if((pos.x>%MIN_POS%.x)&&(pos.x<%MAX_POS%.x)
&&(pos.y>%MIN_POS%.y)&&(pos.y<%MAX_POS%.y)
&&(pos.z>%MIN_POS%.z)&&(pos.z<%MAX_POS%.z)
&&(vel.x>%MIN_VEL%.x)&&(vel.x<%MAX_VEL%.x)
&&(vel.y>%MIN_VEL%.y)&&(vel.y<%MAX_VEL%.y)
&&(vel.z>%MIN_VEL%.z)&&(vel.z<%MAX_VEL%.z)
&&(lifespan>%LIFE_MIN%)&&(lifespan<%LIFE_MAX%))
{
    prev_stp=stp;
    stp=1.;
    pos.a=%TARGET_STAGE%;
    %GEOBLOCKS%
    stp=prev_stp;
}
