// CONSTANTS
// -- General
float%STATEMENT%=true;
// CONSTANTS_END
// DECLARATIONS
float prev_stp;
// DECLARATIONS_END

if(%STATEMENT%)
{
    prev_stp=stp;
    stp=1;
    pos.a=%TARGET_STAGE%;
    %GEOBLOCKS%
    stp=prev_stp;
}
