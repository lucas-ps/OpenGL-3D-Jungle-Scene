class Renderer:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.link = app.link
        self.scene = app.scene

        # Depth buffer for shadows
        self.depth_texture = self.link.texture.textures['depth_texture']
        self.depth_framebuffer = self.ctx.framebuffer(depth_attachment=self.depth_texture)

    def render_shadow(self):
        """
        Renders the scene's shadows
        """
        self.depth_framebuffer.clear()
        self.depth_framebuffer.use()
        for obj in self.scene.objects:
            obj.render_shadow()

    def render(self):
        """
        Renders each object in the object list, then the skybox.
        """
        self.app.ctx.screen.use()
        self.render_shadow()
        self.app.ctx.screen.use()
        for obj in self.scene.objects:
            obj.render()
        self.scene.skybox.render()

    def destroy(self):
        self.depth_framebuffer.release()
