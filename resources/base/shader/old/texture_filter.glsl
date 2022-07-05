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
uniform float Contrast=1.;
uniform vec3 Filter=vec3(1.,1.,1.);

void main(){
  vec4 col=texture(texture0,uv);
  col.rgb=col.rgb*Filter;
  if(Contrast!=1.){
    col.rgb=((col.rgb-.5f)*max(Contrast,0))+.5f;
  }
  if(col.a>0.){
    out_color=col;
  }else{
    discard;
  }
}
#endif
