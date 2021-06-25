#version 330

#if defined VERTEX_SHADER

in vec4 in_pos;
in float in_size;
in vec3 in_color;
in float in_rot;
in float in_noise;
in float in_key;

out vec3 vs_color;
out float vs_size;
out float vs_rot;
out float vs_noise;

uniform vec3 Basis;

void main(){
	gl_Position=vec4(in_pos.xyz*Basis,in_pos.a);
	vs_size=in_size;
	vs_color=in_color;
	vs_rot=in_rot;
	vs_noise=in_noise;
}

#elif defined GEOMETRY_SHADER

#define M_DEGPI.01745329251
layout(points)in;
layout(triangle_strip,max_vertices=4)out;

uniform mat4 projection;
uniform mat4 BillboardFace;
uniform float Size;
uniform vec3 CameraPosition;
uniform float Stage;

in vec3 vs_color[1];
in float vs_size[1];
in float vs_rot[1];
in float vs_noise[1];

out vec3 out_color;
out float out_noise;
out vec2 uv;

void main(){
	vec3 pos=gl_in[0].gl_Position.xyz*20;
	
	if(gl_in[0].gl_Position.a!=Stage){return;}
	
	vec3 right=(BillboardFace*vec4(0,sin((vs_rot[0]+90)*M_DEGPI),cos((vs_rot[0]+90)*M_DEGPI),1)).xyz;
	vec3 up=(BillboardFace*vec4(0,sin(vs_rot[0]*M_DEGPI),cos(vs_rot[0]*M_DEGPI),1)).xyz;
	
	if(pos.z>-.1){
		vec4 proj_pos=projection*vec4(pos,1.);
		if(vs_rot[0]>-1000)
		{
			float size_modifier=Size*vs_size[0];
			pos=pos+CameraPosition;
			uv=vec2(1.,1.);
			out_color=vs_color[0];
			out_noise=vs_noise[0];
			gl_Position=projection*vec4(pos+(right+up)*size_modifier,1.);
			EmitVertex();
			
			uv=vec2(0.,1.);
			out_color=vs_color[0];
			out_noise=vs_noise[0];
			gl_Position=projection*vec4(pos+(-right+up)*size_modifier,1.);
			EmitVertex();
			
			uv=vec2(1.,0.);
			out_color=vs_color[0];
			out_noise=vs_noise[0];
			gl_Position=projection*vec4(pos+(right-up)*size_modifier,1.);
			EmitVertex();
			
			uv=vec2(0.,0.);
			out_color=vs_color[0];
			out_noise=vs_noise[0];
			gl_Position=projection*vec4(pos+(-right-up)*size_modifier,1.);
			EmitVertex();
			EndPrimitive();
		}
	}
}

#elif defined FRAGMENT_SHADER

uniform sampler2D texture0;
uniform sampler2DArray texturearray1;
uniform float opacity;
uniform int noise_id;
uniform bool Usenoise;

in vec3 out_color;
in float out_noise;
in vec2 uv;

out vec4 f_color;

void main(){
	vec4 col=texture(texture0,uv);
	if(Usenoise){
		if(col.a<=0.){
			discard;
		}
		col=col*col.a;
		col=col*texture(texturearray1,vec3(uv,mod(noise_id+int(out_noise),710)));
		f_color=col*vec4(out_color,col.a)*opacity;
	}else{
		if(col.a<1.){
			discard;
		}
		f_color=col*vec4(out_color,1.);
	}
}

#endif
