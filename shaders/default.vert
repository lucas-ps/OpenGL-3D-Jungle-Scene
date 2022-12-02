#version  330 core

// Parsing Vertex Array Object
layout (location = 0) in vec2 in_texcoord_0;
layout (location = 1) in vec3 in_normal;
layout (location = 2) in vec3 in_position;

// Output variable for rasterised texture coords for the fragment program
out vec2 uv_0;
out vec3 normal;
out vec3 fragPos;

// Initiates 4x4 matrices for projection for model and view matrices. Passed from model.py.
uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;

void main() {
    uv_0 = in_texcoord_0;
    fragPos = vec3(m_model * vec4(in_position, 1.0));
    // For making sure lighting is correct when model is not uniformly scaled
    normal = mat3(transpose(inverse(m_model))) * normalize(in_normal);
    gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);
}