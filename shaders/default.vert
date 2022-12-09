#version  330 core

// Parsing Vertex Array Object
layout (location = 0) in vec2 in_texcoord_0;
layout (location = 1) in vec3 in_normal;
layout (location = 2) in vec3 in_position;

// Output for rasterised texture coords for the fragment shaders, normals, positions of fragments and shadows
out vec2 uv_0;
out vec3 normal;
out vec3 fragPos;
out vec4 shadowCoord;

// Initiates 4x4 matrices for projection for model and view matrices. Passed from model.py.
uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_view_light;
uniform mat4 m_model;

// Bias matrix for MVP calculations in texture space.
mat4 m_shadow_bias = mat4(
    0.5, 0.0, 0.0, 0.0,
    0.0, 0.5, 0.0, 0.0,
    0.0, 0.0, 0.5, 0.0,
    0.5, 0.5, 0.5, 1.0
);


void main() {
    // Rasterised texture coords.
    uv_0 = in_texcoord_0;

    // Calculating fragment position.
    fragPos = vec3(m_model * vec4(in_position, 1.0));

    // For making sure lighting is correct when model is not uniformly scaled.
    normal = mat3(transpose(inverse(m_model))) * normalize(in_normal);
    gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);

    // Generating shadow Model View Projection matrix for shadows.
    mat4 shadowMVP = m_proj * m_view_light * m_model;
    shadowCoord = m_shadow_bias * shadowMVP * vec4(in_position, 1.0);
    shadowCoord.z -= 0.005;

}