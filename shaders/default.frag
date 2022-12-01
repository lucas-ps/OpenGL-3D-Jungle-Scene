#version  330 core

// Fragment colour defines as fragColor variable, defined 0 as frame buffer.
layout (location = 0) out vec4 fragColor;

in vec2 uv_0;

uniform sampler2D u_texture_0;

// Reading fragments
void main() {
    vec3 color = texture(u_texture_0, uv_0).rgb;
    fragColor = vec4(color, 1.0);
}