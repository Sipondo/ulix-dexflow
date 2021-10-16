"""
Plasma Shader
=============

This shader example have been taken from
http://www.iquilezles.org/apps/shadertoy/ with some adaptation.

This might become a Kivy widget when experimentation will be done.
"""


from kivy.clock import Clock
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.graphics import RenderContext, BindTexture, Rectangle
from kivy.graphics.texture import Texture
from kivy.core.image import Image, ImageData
from kivy.properties import StringProperty, ObjectProperty
from kivy.core.window import Window
from kivy.resources import resource_find

import numpy as np
import lark
import termcolor

# Plasma shader
plasma_shader = """
$HEADER$

uniform vec2 resolution;
uniform float time;
uniform sampler2D texture1;
uniform vec2 size;

void main(void)
{
   vec4 frag_coord = gl_FragCoord;
   gl_FragColor = texture2D(texture0,vec2(tex_coord0.x/size.x, tex_coord0.y/size.y));
   /*
   float x = frag_coord.x;
   float y = frag_coord.y;
   float mov0 = x+y+cos(sin(time)*2.)*100.+sin(x/100.)*1000.;
   float mov1 = y / resolution.y / 0.2 + time;
   float mov2 = x / resolution.x / 0.2 - time;
   float c1 = abs(sin(mov1+time)/2.+mov2/2.-mov1-mov2+time);
   float c2 = abs(sin(c1+sin(mov0/1000.+time)
              +sin(y/40.+time)+sin((x+y)/100.)*3.));
   float c3 = abs(sin(c2+cos(mov1+mov2+c2)+cos(mov2)+sin(x/1000.)));
   gl_FragColor = vec4( c1,c2,c3,1.0)*texture2D(texture0,tex_coord0);
   */
   //gl_FragColor = vec4( gl_FragColor.x+frag_coord.x/900,gl_FragColor.y+frag_coord.y/900,gl_FragColor.z+(frag_coord.x+frag_coord.y)/4000,1.0)*texture2D(texture0,tex_coord0);
}
"""

VIEW_WIDTH = 8


class ShaderWidget(FloatLayout):

    # property to set the source code for fragment shader
    fs = StringProperty(None)

    def __init__(self, **kwargs):
        # Instead of using Canvas, we will use a RenderContext,
        # and change the default shader used.
        self.canvas = RenderContext()

        self.tex1 = Image.load(
            resource_find("resources/essentials/graphics/tilesets/outside_tiny.png")
        ).texture
        self.tex2 = Image.load(resource_find("tex3.jpg")).texture

        self.tex1.mag_filter = "nearest"

        # call the constructor of parent
        # if they are any graphics object, they will be added on our new canvas
        super(ShaderWidget, self).__init__(**kwargs)

        # with self.canvas:
        # self.canvas.add(Rectangle(size=self.size))
        self.canvas["texture0"] = 0
        self.canvas["texture1"] = 1
        self.canvas.add(BindTexture(texture=self.tex2, index=1))
        print(self.size)
        self.rec1 = Rectangle(size=Window.size, texture=self.tex1)
        self.canvas.add(self.rec1)
        # self.rec1.texture = self.tex2
        # self.canvas.add(BindTexture(texture=self.tex2, index=0))

        print(dir(self.canvas))
        # BindTexture(source="tex4.jpg", index=0)

        # We'll update our glsl variables in a clock
        Clock.schedule_interval(self.update_glsl, 1 / 60.0)

    def on_fs(self, instance, value):
        # set the fragment shader to our source code
        shader = self.canvas.shader
        old_value = shader.fs
        shader.fs = value
        if not shader.success:
            shader.fs = old_value
            raise Exception("failed")

    def update_glsl(self, *largs):
        self.rec1.size = Window.size
        print(np.zeros(3))
        # self.canvas["size"] = list(
        #     map(
        #         float,
        #         (
        #             2
        #             * self.tex1.size[0]
        #             / self.tex1.size[1]
        #             * Window.size[1]
        #             / Window.size[1],
        #             2
        #             * self.tex1.size[1]
        #             / self.tex1.size[1]
        #             * Window.size[0]
        #             / Window.size[1],
        #         ),
        #     )
        # )  # list(map(lambda x: float(x / 128), Window.size))
        self.canvas["size"] = list(
            map(
                float,
                (
                    2 * self.tex1.size[0] / self.tex1.size[1] * 800 / Window.size[0],
                    2 * self.tex1.size[1] / self.tex1.size[1] * 800 / Window.size[1],
                ),
            )
        )  # list(map(lambda x: float(x / 128), Window.size))
        # self.canvas["size"] = list(
        #     map(float, (1, 1))
        # )  # list(map(lambda x: float(x / 128), Window.size))
        self.canvas["time"] = Clock.get_boottime()
        self.canvas["resolution"] = list(map(float, self.size))
        # This is needed for the default vertex shader.
        win_rc = Window.render_context
        self.canvas["projection_mat"] = win_rc["projection_mat"]
        self.canvas["modelview_mat"] = win_rc["modelview_mat"]
        self.canvas["frag_modelview_mat"] = win_rc["frag_modelview_mat"]


class UlivyApp(App):
    def build(self):
        return ShaderWidget(fs=plasma_shader)


if __name__ == "__main__":
    UlivyApp().run()
