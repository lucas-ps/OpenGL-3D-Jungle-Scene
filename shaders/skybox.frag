#version 330 core

// Outputs the fragment colour, takes texCubeCoords input from skybox.vert
out vec4 fragColour;
in vec3 texCubeCoords;

uniform samplerCube u_texture_skybox;

void main(){
    fragColour = texture(u_texture_skybox, texCubeCoords);
}