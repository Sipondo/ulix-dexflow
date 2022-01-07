---vertex shader---
#version 320 es

// #ifdef GL_ES
// precision highp float;
// #endif

// /* Outputs to the fragment shader */
// out vec4 frag_color;
// out vec2 tex_coord0;

// /* vertex attributes */
// in vec2 vPosition;
// in vec2 vTexCoords0;

// /* uniform variables */
// uniform mat4 modelview_mat;
// uniform mat4 projection_mat;
// uniform vec4 color;
// uniform float opacity;

void main(void){
    // frag_color=color*vec4(1.,1.,1.,opacity);
    // tex_coord0=vTexCoords0;
    // gl_Position=projection_mat*modelview_mat*vec4(vPosition.xy,0.,1.);
}

---fragment shader---
#version 320 es

// #ifdef GL_ES
// precision highp float;
// #endif

// /* Outputs from the vertex shader */
// in vec4 frag_color;
// in vec2 tex_coord0;

// /* uniform texture samplers */
// uniform sampler2D texture0;

// uniform mat4 frag_modelview_mat;

// uniform vec2 resolution;
// uniform float time;
// uniform sampler2D texture1;
// uniform vec2 viewport;
// uniform vec2 texture_size;
// uniform vec2 map_size;

// uniform vec2 camera_position;

// out vec4 fragColor;

// texelFetch is not supported by android under OpenGLES 2.0
// until moving to 3.0+, use floating access texture2D instead

void main(void)
{
    // vec4 frag_coord=gl_FragCoord;
    
    // vec2 view_pos=tex_coord0.xy+camera_position;
    
    // fragColor=texelFetch(texture0,ivec2(30,30),0);
    
    // if((view_pos.x>=0.)&&(view_pos.y>=0.))
    // {
        //     // What location does this tile have in the world
        //     float world_locX=(float(int(view_pos.x/viewport.x)))/map_size.x;
        //     float world_locY=(float(int(view_pos.y/viewport.y)))/map_size.y;
        
        //     // What tile is at that location
        //     vec2 tile=texture(texture1,vec2(world_locX,world_locY)).xy*256.;
        
        //     tile.x-=1.;
        
        //     fragColor=texture(texture0,
            //         vec2(
                //             (
                    //                 mod(view_pos.x,viewport.x)
                    //                 /viewport.x+tile.x
                //             )/texture_size.x
                //             ,
                //             (
                    //                 mod(view_pos.y,viewport.y)
                    //                 /viewport.y+tile.y
                //             )/texture_size.y
            //         )
        //     );
    // }
}
