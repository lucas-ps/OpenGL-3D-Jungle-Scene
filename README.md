
# PyGame/OpenGL 3D Jungle Scene

A basic jungle scene implemented in python using PyGame, modernGL and GLSL shaders. A video demo can be found here: https://youtu.be/qRt4sf1BtU8

# How to use

The requirements for this project are as follows:

- Python 3.8+
- numpy~=1.20.1
- PyWavefront~=1.3.3
- moderngl~=5.7.3
- pygame~=2.1.2

The program can be run by running the main.py file in the main folder.

# Explanation of the code

### Folders

- Main - Folder that holds all the python code.
- Models, textures - Folder that holds models and their textures.
- Shaders - Folder that holds GLSL shaders.

### Python files

- **Main**: This is the file that created the graphics engine instance by initiating pygame and setting necessary parameters using moderngl - the opengl library for this project. It also contains methods for rendering and timekeeping, which is used to update everything 60 times per second, or in other words, when you see an 'update' method it's called in time with this timekeeping.
	
- The main method creates an instance of the **Scene** class, which loads in all the objects. It does this by:
	- Loading in the texture for the object using the texture class.
	- Creating a vertex buffer object using the VBO class, specifically using the ObjVBO class for .obj files.
	- It then Inserts the created VBO into the vertex array object class.
	- And finally creates a model for the object, which stores all the information about it, including its position, rotation, scale, matrices, VAO, the shader program to use etc.
	
- **Renderer**: Class which renders objects in the scene and their shadows by going through the objects stored in the scene class. It then renders the skybox.
	
- **Shaders**: Class which loads in the GLSL files and stores them to be used in models.

- **Texture**: Class which loads in and stores texture files for objects and the skybox, as well as the depth texture used for shadows.

- **Link**: Class used to link the graphics engine instance to the VAO and texture instance, through these, anything which knows the app instance can access any of the other classes and their methods.

- **Light**: Class which holds attributes required for calculating Phong lighting and shadows. Now the bigger classes.

- **Model**: Class that passes parameters to the GLSL shaders, and calls all the relevant methods in the other required classes to generate models. The models included are the BaseModel, the ExtendedBaseModel, the SkyBox model and the ObjModel for .obj files.

- **Vertex Array Object (VAO)**: Class used to store a Vertex Buffer objects in Vertex Array Objects and the attributes required to render them such as the shader program and the VBO format.

- **Vertex Buffer Object (VBO)**: is a class for creating VBOs for models. It handles the generation of vertex data, with .obj files being read using the pywavefront library.
	
- **Camera**: Class that acts as a camera for the user's view. Performs translation and rotation. This class handles user input, either through the use of wasd to move forward, left, back and right; the use of left shift and space to go down and up, and mouse input to rotate. The pitch and yaw values are set to 0 and 90 to keep the scene looking normally oriented, however these can be adjusted. When this class is initiated, it also generates the projection matrix.

	- The update() method is called in the main program 60 times per second, meaning that every time this is called, the program firstly checks if the user is pressing any keys and if they are, it adjusts the camera's position attributes. It then checks if the mouse has moved, and adjusts the rotation parameter accordingly. Then, the camera vectors are calculated using the glm library and the view matrix is updated with these updated values.

### GLSL shaders

- To render the vertex buffer object and attributes for each pixel, from their model are processed in the default.vert GLSL class, which uses the rasterised texture co-ordinates and produces a calculated fragment position and Model View Projection matrix for shadows as well as other attributes needed to render the scene.

- To calculate the colour of each pixel, the default fragment shader is used. This fragment shader performs texture mapping pixels in a texture to rasterised texture coordinates. The texture pixels were previously calculated in the texture class by the moderngl library. The coordinates come from the VBO.

- Illumination is also calculated in this fragment file. In this program, I used phong shading which combines ambient, diffused, and specular light to modify the colour of a pixel to simulate lighting. Shadow mapping is also factored into this, with the previously mentioned depth texture being used to calculate which pixels have light blocked by an object. Rasterised shadow coordinates from the vertex file are used for these calculations. Shadows are  antialliased by using Percentage Closer Filtering by making multiple shadow map comparisons per pixel and averaging them together.

- The water vertex and fragment files are exactly the same except for that they account for an alpha value, which makes the water transparent. They were supposed to deal with environment mapping as the water would ideally be reflective, however I couldn't get this done on time as it kept giving me errors that I couldn’t figure out how to fix.
## License

[MIT](https://choosealicense.com/licenses/mit/)

