#version 120

attribute vec2 vPosition;
attribute vec2 vTexcoords;

varying vec2 fTexcoords;

void main()
{
    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
    fTexcoords = vTexcoords;
}