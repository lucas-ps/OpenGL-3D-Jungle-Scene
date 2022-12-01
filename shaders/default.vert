#version  330 core

// Set layout as a 3 component vector with 'in position' as input type, location number equal as 0,
layout (location = 0) in vec3 in_position;

// Variable of a 4x4 matrix for projection, model and view matrices
uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;

void main() {
    gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);
}