#version 120

varying vec2 fTexcoords;
uniform sampler2D textureObj;

// uniform vec2 noiseOffset;
// uniform sampler2D noiseTex;
// uniform float noiseStrength;

void main()
{
    // vec2 new_fTexcoords = fTexcoords + texture2D(noiseTex, noiseOffset) * noiseStrength;
    vec2 new_fTexcoords = fTexcoords;
    gl_FragColor = texture2D(textureObj, new_fTexcoords);
}