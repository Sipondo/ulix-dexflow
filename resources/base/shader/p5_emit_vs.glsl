#version 320 es

#ifdef GL_ES
precision highp float;
#endif

in float in_index;
// in vec4 inVec;

out VS_OUT{
  float index;
}vs_out;

void main(){
  // if(inVec.a>-9999.){
    if(in_index>-999.){
      vs_out.index=float(gl_VertexID);
    }
  }
  