// CONSTANTS
// -- General
vec3%POINT%=vec3(1.,0.,0.);
float%DISTANCE%=1;
// CONSTANTS_END
// DECLARATIONS
float prev_stp;
// DECLARATIONS_END

if(length(pos.xyz-%POINT%)<%DISTANCE%)
{
    prev_stp=stp;
    stp=1.;
    pos.a=%TARGET_STAGE%;
    %GEOBLOCKS%
    stp=prev_stp;
}
