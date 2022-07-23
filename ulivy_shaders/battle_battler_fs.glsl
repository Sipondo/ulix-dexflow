#version 320 es

#ifdef GL_ES
precision highp float;
#endif

uniform float Brightness;
uniform bool Cutout;
uniform sampler2D Texture;
uniform float AnimationFrame;
uniform float AnimationLength;
uniform float Mirror;
uniform bool IsShadow;

in vec2 uv;
out vec4 frag_color;

void main(){
    vec2 subframe=vec2((Mirror*uv.x+AnimationFrame)/AnimationLength,uv.y);
    // vec4 col=texture(Texture,subframe);
    // frag_color=texture(Texture,uv);
    frag_color=texture(Texture,subframe);
    // frag_color=vec4(.5294,.0745,.1216,1.);
    // if(col.a<.9){
        //     discard;
    // }else{
        //     if(IsShadow){
            //         col=col*vec4(0,0,0,.5);
        //     }
        //     if(Cutout){
            //         f_color=vec4(0,0,0,.001);
        //     }else{
            //         col.r*=Brightness;//*Brightness;
            //         col.g*=Brightness;//*Brightness;
            //         col.b*=Brightness;//*Brightness;
            //         f_color=col;
        //     }
    // }
}
