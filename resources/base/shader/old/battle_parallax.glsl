#version 330

#if defined VERTEX_SHADER

in vec2 in_position;
in vec2 in_texcoord_0;
uniform float Shake=-.0;

out vec2 uv0;

void main(){
  gl_Position=vec4(in_position.x,in_position.y+Shake,0,1.);
  uv0=in_texcoord_0;
}

#elif defined FRAGMENT_SHADER

uniform sampler2D Texture;
uniform float Offset;
uniform float Speed;
uniform float Brightness=1.;

in vec2 uv0;

out vec4 f_color;

void main(){
  vec4 col=texture(Texture,vec2((uv0.x+Offset)/Speed,uv0.y));
  f_color=vec4(col.x*Brightness,col.y*Brightness,col.z*Brightness,col.a);
}

#endif
