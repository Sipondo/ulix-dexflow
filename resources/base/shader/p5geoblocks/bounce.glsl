// CONSTANTS
// -- Bounce
float%VERTICAL_DAMPEN%=1.4;
float%DAMPEN%=1.;
float%LIFE_DAMPEN%=1.;
// CONSTANTS_END
// DECLARATIONS
// DECLARATIONS_END

if((pos.z<0.)&&(vel.z<0.))
{
    vel.z=-vel.z/%VERTICAL_DAMPEN%;
    vel=vel/%DAMPEN%;
    lifespan=lifespan/%LIFE_DAMPEN%;
}
