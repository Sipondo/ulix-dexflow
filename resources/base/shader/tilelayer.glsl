#version 330

#if defined VERTEX_SHADER

in vec2 in_position;
in vec2 in_texcoord_0;

out vec2 uv0;

void main(){
  gl_Position=vec4(in_position,0.,1.);
  uv0=vec2(in_texcoord_0[0],1.-in_texcoord_0[1]);
}

#elif defined FRAGMENT_SHADER

uniform vec2 tileSize=vec2(16,16);
uniform vec2 modSize=vec2(1,1);
uniform vec2 displayBase=vec2(20,20);
uniform vec2 offset=vec2(0,0);

uniform vec2 displaySize;
uniform int layerHeight;
uniform vec2 worldSize;
uniform vec2 tilemapSize;

uniform sampler2D texture_tileset;
uniform usampler2DArray texturearray_masks;

uniform vec2 Zoom;
uniform vec2 Pan;
uniform float Alpha;

in vec2 uv0;

out vec4 fragColor;

void main(){
  vec2 pannedPosition=(((uv0+vec2(-.5,-.5))/Zoom+Pan)*displaySize/displayBase/tileSize+offset);
  vec2 tilePosition=mod(pannedPosition,modSize)/tilemapSize;
  vec2 worldPosition=floor(pannedPosition/modSize);
  vec4 retrieveColor;
  vec4 outputColor=vec4(0,0,0,0);
  
  if((worldPosition.x>=0)&&
  (worldPosition.x<worldSize.x)&&
  (worldPosition.y>=0)&&
  (worldPosition.y<worldSize.y)){
    
    // Check every layer
    for(int i=0;i<layerHeight;i++){
      
      // Retrieve information regarding which tile should be visualised
      vec4 mask=texture(texturearray_masks,vec3(worldPosition/worldSize,i));
      
      // Retrieve position of the pixel within the tileset image
      vec2 layerTilePosition=tilePosition+(vec2(mask.x,mask.y)/tilemapSize);
      
      // Retrieve the pixel that would be rendered
      retrieveColor=texture(texture_tileset,layerTilePosition);
      
      // If not transparent, render pixel
      if(retrieveColor.a>0){
        outputColor=retrieveColor*vec4(1,1,1,Alpha);// + outputColor * vec4(1, 1, 1, 1-Alpha);
      }
    }
    
    if(outputColor.a>0){
      fragColor=outputColor;
    }else{
      discard;
    }
  }
}
#endif
