// CONSTANTS
// -- Acceleration
vec3%ACC%=vec3(2.,0.,0.);
// -- Gravity
vec3%GRAV_POS%=vec3(1.,0.,0.);
float%GRAV_EXPONENT%=.5;
float%GRAV_FORCE%=2.;
// CONSTANTS_END
// DECLARATIONS
vec3 grav_diff;
float grav_length;
// DECLARATIONS_END

vel=vel+%ACC%*stp;
if((pos.z>-10.)&&(lifespan>0.)){
    if(%GRAV_FORCE%!=0.){
        grav_diff=%GRAV_POS%-pos.xyz;
        grav_length=pow(dot(grav_diff*grav_diff,vec3(1.,1.,1.)),%GRAV_EXPONENT%);
        vel=vel+grav_diff/grav_length*%GRAV_FORCE%*stp;
    }
    
    if((pos.z<0.)&&(vel.z<0.))
    {
        vel.z=-vel.z/1.4;
    }
}
