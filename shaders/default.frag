#version  330 core

// Fragment colour defines as fragColor variable, defined 0 as frame buffer.
layout (location = 0) out vec4 fragColor;

// Rasterised texture coords output from .vert file.
in vec2 uv_0;
// Normal data output from .vert file.
in vec3 normal;
in vec3 fragPos;

// Structure containing light intensity values.
struct Light {
    vec3 position;
    vec3 Ia;
    vec3 Id;
    vec3 Is;
};

uniform Light light;
uniform sampler2D u_texture_0;
uniform vec3 camPos;

// Function to calculate lighting using Phong lighting.
vec3 getLight(vec3 colour) {
    vec3 Normal = normalize(normal);

    // Ambient light intensity
    vec3 ambient = light.Ia;

    // Diffusion light intensity using Lambert's law
    vec3 lightDir = normalize(light.position - fragPos);
    vec3 diffuse = max(0.0, dot(lightDir, Normal)) * light.Id;

    // Specular light intensity
    vec3 viewDir = normalize(camPos - fragPos);
    vec3 reflectDir = reflect(-lightDir, normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32.0);
    vec3 specular = spec * light.Is;

    return colour * (ambient + diffuse + specular);
}

// Reading and rendering fragments.
void main() {
    vec3 colour = texture(u_texture_0, uv_0).rgb;
    colour = getLight(colour);
    fragColor = vec4(colour, 1.0);
}