#version 330

#if defined VERTEX_SHADER

in vec3 in_position;
in vec2 in_texcoord_0;
uniform float Shake=-.0;

out vec2 uv;

void main(){
  gl_Position=vec4(in_position.x,in_position.y+Shake,in_position.z,1.);
  uv=in_texcoord_0;
}

#elif defined FRAGMENT_SHADER

out vec4 out_color;
in vec2 uv;

uniform sampler2D texture0;
uniform sampler2D texture1;
uniform float Contrast=1.;

void main(){
  vec4 c_b=texture(texture0,uv);
  vec4 c_n=texture(texture1,uv);
  if(Contrast!=1.){
    c_n.rgb=((c_n.rgb-.5f)*max(Contrast,0))+.5f;
  }
  out_color=vec4(c_b.x-c_n.x*c_n.a,c_b.y-c_n.y*c_n.a,c_b.z-c_n.z*c_n.a,c_b.a);
}
#endif
