from pythonforandroid.recipe import PyProjectRecipe


class ZenGLRecipe(PyProjectRecipe):
    version = '2.7.3'
    url = 'https://files.pythonhosted.org/packages/source/z/zengl/zengl-{version}.tar.gz'
    site_packages_name = 'zengl'


recipe = ZenGLRecipe()
