#version 320 es

#ifdef GL_ES
precision highp float;
precision highp sampler2DArray;
#endif

uniform sampler2D texture0;
uniform sampler2DArray texturearray1;
uniform float opacity;
uniform float noise_id;
uniform bool Usenoise;

in vec3 out_color;
in float out_noise;
in vec2 uv;

out vec4 frag_color;

void main(){
    vec4 col=texture(texture0,uv);
    if(Usenoise){
        if(col.a<=0.){
            discard;
        }
        col=col*col.a;
        col=col;//*texture(texturearray1,vec3(uv,int(mod(float(noise_id+out_noise),710.))));
        frag_color=col*vec4(out_color*opacity,col.a);
    }else{
        if(col.a<1.){
            discard;
        }
        frag_color=col*vec4(out_color*opacity,1.);
    }
}

