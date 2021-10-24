from kivy.clock import Clock
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.core.window import Window
from kivy.graphics import RenderContext, BindTexture, Rectangle, Color, Line
from kivy.graphics.texture import Texture
from kivy.core.image import Image, ImageData
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivy.core.window import Window
from kivy.resources import resource_find, resource_add_path, resource_remove_path
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label

import os
import numpy as np
import lark
import termcolor

# Plasma shader
plasma_shader = """
$HEADER$

uniform vec2 resolution;
uniform float time;
uniform sampler2D texture1;
uniform vec2 viewport;

void main(void)
{
   vec4 frag_coord = gl_FragCoord;
   gl_FragColor = texture2D(texture0,vec2(mod(tex_coord0.x,viewport.x)/viewport.x/8.0, mod(tex_coord0.y,viewport.y)/viewport.y/16.0));
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


class FPSCounter(AnchorLayout):

    # property to set the source code for fragment shader
    counter = NumericProperty()
    age = NumericProperty()

    def __init__(self, **kwargs):
        super(FPSCounter, self).__init__(anchor_x="left", anchor_y="top")
        Clock.schedule_interval(self.update_counter, 0)
        Clock.schedule_interval(self.update_label, 1 / 4)

    def update_counter(self, dt):
        self.counter += 1
        self.age += dt

    def update_label(self, dt):
        if self.age > 0.6:
            self.age = self.age / 2
            self.counter = self.counter / 2
        self.clear_widgets()
        self.add_widget(
            Label(
                text=f"[color=33dd33]{(self.counter+self.age) // self.age:.0f}[/color]",
                size=(50, 15),
                size_hint=(None, None),
                markup=True,
            )
        )


class ShaderWidget(FloatLayout):

    # property to set the source code for fragment shader
    fs = StringProperty(None)

    def __init__(self, **kwargs):
        # Instead of using Canvas, we will use a RenderContext,
        # and change the default shader used.
        self.canvas = RenderContext()

        pth = os.path.join("resources", "essentials", "graphics", "tilesets")
        resource_add_path(pth)
        self.tex1 = Image.load(resource_find("outside_tiny.png")).texture
        resource_remove_path(pth)
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
        Clock.schedule_interval(self.update_glsl, 0)  # 1 / 60.0)

    def on_fs(self, instance, value):
        # set the fragment shader to our source code
        shader = self.canvas.shader
        old_value = shader.fs
        shader.fs = value
        if not shader.success:
            shader.fs = old_value
            raise Exception("failed")

    def update_glsl(self, dt):
        self.rec1.size = Window.size
        # print(np.zeros(3))
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
        # csize = list(
        #     map(
        #         float,
        #         (
        #             2 * self.tex1.size[0] / self.tex1.size[1] * 800 / Window.size[0],
        #             2 * self.tex1.size[1] / self.tex1.size[1] * 800 / Window.size[1],
        #         ),
        #     )
        # )

        texture_size = (self.tex1.size[0] / 16, self.tex1.size[1] / 16)

        viewport = (Window.size[0] / 32, Window.size[1] / 32)  # (float(16), float(3))
        # viewport = (float(16), float(3))

        viewport = (float(1 / viewport[0]), float(1 / viewport[1]))
        self.canvas["viewport"] = viewport
        # print(csize)
        # list(map(lambda x: float(x / 128), Window.size))
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


class Overlay2Layouts(Screen):
    def __init__(self, **kwargs):
        super(Overlay2Layouts, self).__init__(**kwargs)
        self.size = Window.size

        layout1 = FloatLayout(opacity=0.5)
        with layout1.canvas:
            Color(1, 0, 0, 1)  # red colour
            Line(
                points=[
                    self.center_x,
                    self.height / 4,
                    self.center_x,
                    self.height * 3 / 4,
                ],
                width=dp(2),
            )
            Line(
                points=[
                    self.width * 3 / 4,
                    self.center_y,
                    self.width / 4,
                    self.center_y,
                ],
                width=dp(2),
            )

        layout2 = FloatLayout()
        with layout2.canvas:
            Color(0, 0, 0, 1)  # black colour
            Line(circle=[self.center_x, self.center_y, 190], width=dp(2))

        self.add_widget(ShaderWidget(fs=plasma_shader))
        # self.add_widget(layout1)
        self.add_widget(layout2)
        self.add_widget(FPSCounter())


class UlivyApp(App):
    def build(self):
        return Overlay2Layouts()
        # return ShaderWidget(fs=plasma_shader)


if __name__ == "__main__":
    UlivyApp().run()
