#version  330 core

// Fragment colour defines as fregColor variable, defined 0 as frame buffer.
layout (location = 0) out vec4 fragColor;

// Reading fragments
void main() {
    vec3 color = vec3(1, 0, 0);
    fragColor = vec4(color, 1.0);
}