#version 320 es

#ifdef GL_ES
precision highp float;
#endif

/* Outputs from the vertex shader */
in vec4 frag_color;
in vec2 tex_coord0;

/* uniform texture samplers */
uniform sampler2D texture0;
uniform sampler2D texture1;

uniform mat4 frag_modelview_mat;

uniform vec2 map_size;
uniform vec2 resolution;
uniform vec2 texture_size;
uniform vec2 viewport;

uniform float time;

uniform vec2 camera_position;

out vec4 fragColor;

// texelFetch is not supported by android under OpenGLES 2.0
// until moving to 3.0+, use floating access texture2D instead

void main(void)
{
    vec4 frag_coord=gl_FragCoord;
    
    vec2 view_pos=tex_coord0.xy+camera_position;
    
    if((view_pos.x>=0.)&&(view_pos.y>=0.))
    {
        // What location does this tile have in the world
        int world_locX=int(view_pos.x/viewport.x);
        int world_locY=int(view_pos.y/viewport.y);
        
        // What tile is at that location
        vec2 tile=texelFetch(texture1,ivec2(world_locX,world_locY),0).xy*256.;
        
        tile.x-=1.;
        
        fragColor=texelFetch(texture0,
            ivec2(
                int(
                    mod(view_pos.x,viewport.x)
                    /viewport.x*16.
                )+int(tile.x)*16
                ,
                int(
                    mod(view_pos.y,viewport.y)
                    /viewport.y*16.
                )+int(tile.y)*16
            ),0
        );
    }
}
