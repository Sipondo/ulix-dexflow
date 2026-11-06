GLSL_DESKTOP = '#version 330 core\n'
GLSL_ES = '#version 300 es\nprecision highp float;\nprecision highp int;\n'


def install_glsl_header(ctx):
    version = ctx.info['version']
    is_es = version.startswith('OpenGL ES') or version.startswith('WebGL')
    ctx.includes['platform'] = GLSL_ES if is_es else GLSL_DESKTOP
