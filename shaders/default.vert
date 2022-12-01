#version  330 core

// Parsing Vertex Array Object
layout (location = 0) in vec2 in_texcoord_0;
layout (location = 1) in vec3 in_position;

// Output variable for rasterised texture coords for the fragment shader
out vec2 uv_0;

// Initiates 4x4 matrices for projection for model and view matrices. Passed from model.py.
uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;

void main() {
    uv_0 = in_texcoord_0;
    gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);
}